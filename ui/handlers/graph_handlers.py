# ui/handlers/graph_handlers.py
"""
Graph callback handlers - extracted from graph_callbacks.py
Separated business logic from UI definitions
"""

import json
import traceback
from dash import Input, Output, State, html, no_update
from dash.dependencies import ALL

# Import UI components - type: ignore to suppress Pylance warnings
from ui.components.graph import create_graph_component  # type: ignore
from ui.components.stats import create_stats_component, create_stats_data_processor  # type: ignore
from ui.components.classification import create_classification_component  # type: ignore

# Import processing modules
from processing.onion_model import run_onion_model_processing
from processing.cytoscape_prep import prepare_cytoscape_elements
from processing.graph_config import GRAPH_PROCESSING_CONFIG, UI_STYLES
from constants.constants import REQUIRED_INTERNAL_COLUMNS
from data_io.file_utils import decode_uploaded_csv
from data_io.csv_loader import load_csv_event_log


class GraphHandlers:
    """Handles all graph-related callbacks and business logic"""
    
    def __init__(self, app):
        self.app = app
        self.graph_component = create_graph_component()
        self.stats_component = create_stats_component()
        self.stats_processor = create_stats_data_processor()
        self.classification_component = create_classification_component()
        
        # Define display names for consistency
        self.DOORID_COL_DISPLAY = REQUIRED_INTERNAL_COLUMNS['DoorID']
        self.USERID_COL_DISPLAY = REQUIRED_INTERNAL_COLUMNS['UserID']
        self.EVENTTYPE_COL_DISPLAY = REQUIRED_INTERNAL_COLUMNS['EventType']
        self.TIMESTAMP_COL_DISPLAY = REQUIRED_INTERNAL_COLUMNS['Timestamp']
        
    def register_callbacks(self):
        """Register all graph-related callbacks"""
        self._register_main_generation_handler()
        self._register_node_interaction_handlers()
        
    def _register_main_generation_handler(self):
        """Main callback for generating the complete graph and stats"""
        @self.app.callback(
            [
                Output('onion-graph', 'elements', allow_duplicate=True),
                Output('processing-status', 'children', allow_duplicate=True),
                Output('graph-output-container', 'style', allow_duplicate=True),
                Output('stats-panels-container', 'style', allow_duplicate=True),
                Output('yosai-custom-header', 'style', allow_duplicate=True),
                Output('total-access-events-H1', 'children'),
                Output('event-date-range-P', 'children'),
                Output('stats-date-range-P', 'children'),
                Output('stats-days-with-data-P', 'children'),
                Output('stats-num-devices-P', 'children'),
                Output('stats-unique-tokens-P', 'children'),
                Output('most-active-devices-table-body', 'children'),
                Output('manual-door-classifications-store', 'data', allow_duplicate=True),
                Output('column-mapping-store', 'data', allow_duplicate=True)
            ],
            Input('confirm-and-generate-button', 'n_clicks'),
            [
                State('uploaded-file-store', 'data'),
                State('column-mapping-store', 'data'),
                State('all-doors-from-csv-store', 'data'),
                State({'type': 'floor-select', 'index': ALL}, 'value'),
                State({'type': 'floor-select', 'index': ALL}, 'id'),
                State({'type': 'is-ee-check', 'index': ALL}, 'value'),
                State({'type': 'is-ee-check', 'index': ALL}, 'id'),
                State({'type': 'is-stair-check', 'index': ALL}, 'value'),
                State({'type': 'is-stair-check', 'index': ALL}, 'id'),
                State({'type': 'security-level-slider', 'index': ALL}, 'value'),
                State({'type': 'security-level-slider', 'index': ALL}, 'id'),
                State('num-floors-input', 'value'),
                State('manual-map-toggle', 'value'),
                State('csv-headers-store', 'data'),
                State('manual-door-classifications-store', 'data')
            ],
            prevent_initial_call=True
        )
        def generate_model_final(n_clicks, file_contents_b64, stored_column_mapping_json, all_door_ids_from_store,
                                 floor_values, floor_ids, is_ee_values, is_ee_ids, is_stair_values, is_stair_ids,
                                 security_slider_values, security_slider_ids, num_floors_from_input, manual_map_choice,
                                 csv_headers, existing_saved_classifications_json):

            return self._process_graph_generation(
                n_clicks, file_contents_b64, stored_column_mapping_json, all_door_ids_from_store,
                floor_values, floor_ids, is_ee_values, is_ee_ids, is_stair_values, is_stair_ids,
                security_slider_values, security_slider_ids, num_floors_from_input, manual_map_choice,
                csv_headers, existing_saved_classifications_json
            )
    
    def _register_node_interaction_handlers(self):
        """Register node tap and interaction handlers"""
        @self.app.callback(
            Output('tap-node-data-output', 'children'),
            Input('onion-graph', 'tapNodeData')
        )
        def display_tap_node_data_final(data):
            return self.graph_component.format_node_details(data)
    
    def _process_graph_generation(self, n_clicks, file_contents_b64, stored_column_mapping_json, all_door_ids_from_store,
                                 floor_values, floor_ids, is_ee_values, is_ee_ids, is_stair_values, is_stair_ids,
                                 security_slider_values, security_slider_ids, num_floors_from_input, manual_map_choice,
                                 csv_headers, existing_saved_classifications_json):
        """Process the main graph generation logic"""
        
        # Initialize default values
        hide_style = UI_STYLES['hide']
        show_style = UI_STYLES['show_block']
        show_stats_style = UI_STYLES['show_flex_stats']
        
        default_stats = self.stats_component.get_default_stats_values()
        graph_elements = []
        status_msg = "Processing..."
        
        if not n_clicks or not file_contents_b64:
            return self._create_default_response(hide_style, default_stats, stored_column_mapping_json)
        
        try:
            # Process classifications
            result = self._process_classifications(
                manual_map_choice, all_door_ids_from_store, floor_values, floor_ids,
                is_ee_values, is_ee_ids, is_stair_values, is_stair_ids,
                security_slider_values, security_slider_ids, csv_headers, existing_saved_classifications_json
            )
            
            current_door_classifications = result['classifications']
            confirmed_entrances = result['entrances']
            all_manual_classifications = result['all_classifications']
            
            # Process CSV data
            processed_data = self._process_csv_data(
                file_contents_b64, stored_column_mapping_json, csv_headers
            )
            
            if not processed_data['success']:
                return self._create_error_response(
                    processed_data['error'], hide_style, default_stats, stored_column_mapping_json
                )
            
            df_final = processed_data['dataframe']
            
            # Run onion model processing
            model_result = self._run_onion_model(
                df_final, num_floors_from_input, confirmed_entrances, current_door_classifications
            )
            
            if model_result['success']:
                # Generate graph elements and stats
                graph_elements = model_result['graph_elements']
                stats_data = model_result['stats_data']
                
                current_yosai_style = show_style if graph_elements else hide_style
                status_msg = "Graph generated!" if graph_elements else "Processed, but no graph elements to display."
                
                return self._create_success_response(
                    graph_elements, stats_data, current_yosai_style, show_style, show_stats_style,
                    status_msg, all_manual_classifications, stored_column_mapping_json
                )
            else:
                return self._create_error_response(
                    model_result['error'], hide_style, default_stats, stored_column_mapping_json
                )
                
        except Exception as e:
            traceback.print_exc()
            return self._create_error_response(
                str(e), hide_style, default_stats, stored_column_mapping_json
            )
    
    def _process_classifications(self, manual_map_choice, all_door_ids_from_store, floor_values, floor_ids,
                                is_ee_values, is_ee_ids, is_stair_values, is_stair_ids,
                                security_slider_values, security_slider_ids, csv_headers, existing_saved_classifications_json):
        """Process door classifications from form inputs"""
        
        if isinstance(existing_saved_classifications_json, str):
            all_manual_classifications = json.loads(existing_saved_classifications_json)
        else:
            all_manual_classifications = existing_saved_classifications_json or {}
        
        current_door_classifications = {}
        confirmed_entrances = []
        
        if manual_map_choice == 'yes' and all_door_ids_from_store:
            # Get security levels mapping
            security_levels_map = self.classification_component.get_security_levels_map()
            
            # Build mappings from form data
            floor_map = {f_id['index']: f_val for f_id, f_val in zip(floor_ids, floor_values)}
            is_ee_map = {ee_id['index']: 'is_ee' in ee_val for ee_id, ee_val in zip(is_ee_ids, is_ee_values)}
            is_stair_map = {st_id['index']: 'is_stair' in st_val for st_id, st_val in zip(is_stair_ids, is_stair_values)}
            
            security_map_slider_to_value = {
                s_id['index']: security_levels_map.get(s_val, {}).get("value", "unclassified")
                for s_id, s_val in zip(security_slider_ids, security_slider_values)
            }
            
            # Build classifications for each door
            for door_id in all_door_ids_from_store:
                floor = floor_map.get(door_id, '1')
                is_ee = is_ee_map.get(door_id, False)
                is_stair = is_stair_map.get(door_id, False)
                security = security_map_slider_to_value.get(door_id, 'green')
                
                current_door_classifications[door_id] = {
                    'floor': str(floor),
                    'is_ee': is_ee,
                    'is_stair': is_stair,
                    'security': security
                }
                
                if is_ee:
                    confirmed_entrances.append(door_id)
            
            # Save classifications
            if csv_headers:
                key = json.dumps(sorted(csv_headers))
                all_manual_classifications[key] = current_door_classifications
        
        return {
            'classifications': current_door_classifications,
            'entrances': confirmed_entrances,
            'all_classifications': all_manual_classifications
        }
    
    def _process_csv_data(self, file_contents_b64, stored_column_mapping_json, csv_headers):
        """Process CSV data for onion model"""
        try:
            # Decode CSV
            csv_io_for_loader = decode_uploaded_csv(file_contents_b64)
            
            # Get column mapping
            if isinstance(stored_column_mapping_json, str):
                all_column_mappings = json.loads(stored_column_mapping_json)
            else:
                all_column_mappings = stored_column_mapping_json or {}
            
            header_key = json.dumps(sorted(csv_headers)) if csv_headers else None
            stored_map = all_column_mappings.get(header_key) if header_key else None
            
            if not stored_map or set(stored_map.values()) < set(REQUIRED_INTERNAL_COLUMNS.keys()):
                raise ValueError("No valid column mapping found. Please ensure all required columns are mapped.")
            
            # Prepare mapping for loader
            mapping_for_loader_csv_to_display = {}
            for csv_col_name, internal_key in stored_map.items():
                if internal_key in REQUIRED_INTERNAL_COLUMNS:
                    display_name = REQUIRED_INTERNAL_COLUMNS[internal_key]
                    mapping_for_loader_csv_to_display[csv_col_name] = display_name
                else:
                    mapping_for_loader_csv_to_display[csv_col_name] = internal_key
            
            # Load DataFrame
            df_final = load_csv_event_log(csv_io_for_loader, mapping_for_loader_csv_to_display)
            
            if df_final is None:
                raise ValueError("Failed to load CSV for processing.")
            
            # Validate required columns
            missing_display_columns = [
                display_name for internal_key, display_name in REQUIRED_INTERNAL_COLUMNS.items()
                if display_name not in df_final.columns
            ]
            
            if missing_display_columns:
                raise ValueError(f"Missing required columns: {', '.join(missing_display_columns)}")
            
            return {'success': True, 'dataframe': df_final}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _run_onion_model(self, df_final, num_floors_from_input, confirmed_entrances, current_door_classifications):
        """Run the onion model processing"""
        try:
            config = GRAPH_PROCESSING_CONFIG.copy()
            config['num_floors'] = num_floors_from_input or GRAPH_PROCESSING_CONFIG['num_floors']

            enriched_df, device_attrs, path_viz, all_paths = run_onion_model_processing(
                df_final.copy(),
                config,
                confirmed_official_entrances=confirmed_entrances,
                detailed_door_classifications=current_door_classifications
            )
            
            if enriched_df is not None:
                # Generate graph elements
                nodes, edges = prepare_cytoscape_elements(device_attrs, path_viz, all_paths)
                graph_elements = nodes + edges
                
                # Extract statistics
                stats_data = self._extract_statistics(enriched_df, device_attrs)
                
                return {
                    'success': True,
                    'graph_elements': graph_elements,
                    'stats_data': stats_data
                }
            else:
                return {'success': False, 'error': "Error in processing: incomplete result."}
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _extract_statistics(self, enriched_df, device_attrs):
        """Extract statistics from processed data"""
        stats = self.stats_component.get_default_stats_values()
        
        if enriched_df is not None and not enriched_df.empty:
            # Total events
            stats['total_access_events'] = f"{len(enriched_df):,}"
            
            # Date range
            if self.TIMESTAMP_COL_DISPLAY in enriched_df.columns:
                min_d = enriched_df[self.TIMESTAMP_COL_DISPLAY].min()
                max_d = enriched_df[self.TIMESTAMP_COL_DISPLAY].max()
                if min_d and max_d:
                    stats['event_date_range'] = f"{min_d.strftime('%d.%m.%Y')} - {max_d.strftime('%d.%m.%Y')}"
                    stats['stats_date_range'] = f"Date range: {stats['event_date_range']}"
                    stats['stats_days_with_data'] = f"Days: {enriched_df[self.TIMESTAMP_COL_DISPLAY].dt.date.nunique()}"
            
            # Device and user counts
            if self.DOORID_COL_DISPLAY in enriched_df.columns:
                stats['stats_num_devices'] = f"Devices: {enriched_df[self.DOORID_COL_DISPLAY].nunique()}"
                
                # Most active devices
                device_counts = enriched_df[self.DOORID_COL_DISPLAY].value_counts().nlargest(5)
                stats['most_active_devices_table'] = [
                    html.Tr([html.Td(device), html.Td(f"{count:,}", style={'textAlign': 'right'})])
                    for device, count in device_counts.items()
                ]
            
            if self.USERID_COL_DISPLAY in enriched_df.columns:
                stats['stats_unique_tokens'] = f"Tokens: {enriched_df[self.USERID_COL_DISPLAY].nunique()}"
        
        return stats
    
    def _create_default_response(self, hide_style, default_stats, stored_column_mapping_json):
        """Create default response when no processing occurs"""
        return (
            [], "Missing data or button not clicked.", hide_style, hide_style, hide_style,
            default_stats['total_access_events'], default_stats['event_date_range'],
            default_stats['stats_date_range'], default_stats['stats_days_with_data'],
            default_stats['stats_num_devices'], default_stats['stats_unique_tokens'],
            default_stats['most_active_devices_table'], no_update, stored_column_mapping_json
        )
    
    def _create_success_response(self, graph_elements, stats_data, yosai_style, graph_style, stats_style,
                                status_msg, all_manual_classifications, stored_column_mapping_json):
        """Create success response with graph and stats"""
        return (
            graph_elements, status_msg, graph_style, stats_style, yosai_style,
            stats_data['total_access_events'], stats_data['event_date_range'],
            stats_data['stats_date_range'], stats_data['stats_days_with_data'],
            stats_data['stats_num_devices'], stats_data['stats_unique_tokens'],
            stats_data['most_active_devices_table'],
            json.dumps(all_manual_classifications) if all_manual_classifications else no_update,
            stored_column_mapping_json
        )
    
    def _create_error_response(self, error_msg, hide_style, default_stats, stored_column_mapping_json):
        """Create error response"""
        return (
            [], f"Error: {error_msg}", hide_style, hide_style, hide_style,
            default_stats['total_access_events'], default_stats['event_date_range'],
            default_stats['stats_date_range'], default_stats['stats_days_with_data'],
            default_stats['stats_num_devices'], default_stats['stats_unique_tokens'],
            default_stats['most_active_devices_table'], no_update, stored_column_mapping_json
        )


# Factory function for easy handler creation
def create_graph_handlers(app):
    """Factory function to create graph handlers"""
    return GraphHandlers(app)