# ui/components/graph_handlers.py - DATA RESET FIX
"""
FIXED graph callback handlers with proper data reset between uploads
"""

import json
import traceback
import hashlib
import pandas as pd
import io
import base64

from dash import Input, Output, State, html, no_update
from dash.dependencies import ALL

# Import UI components
from ui.components.graph import create_graph_component
from ui.components.stats import create_enhanced_stats_component, create_enhanced_stats_data_processor
from ui.components.classification import create_classification_component

# Import processing modules
from services.onion_model import run_onion_model_processing
from services.cytoscape_prep import prepare_cytoscape_elements
from services.graph_config import GRAPH_PROCESSING_CONFIG, UI_STYLES
from utils.constants import REQUIRED_INTERNAL_COLUMNS
from services.file_utils import decode_uploaded_csv
from services.csv_loader import load_csv_event_log


class DataResetFixedGraphHandlers:
    """FIXED handlers with proper data reset between uploads"""
    
    def __init__(self, app):
        self.app = app
        self.graph_component = create_graph_component()
        self.stats_component = create_enhanced_stats_component()
        self.stats_processor = create_enhanced_stats_data_processor()
        self.classification_component = create_classification_component()
        
        # Define display names for consistency
        self.DOORID_COL_DISPLAY = REQUIRED_INTERNAL_COLUMNS['DoorID']
        self.USERID_COL_DISPLAY = REQUIRED_INTERNAL_COLUMNS['UserID']
        self.EVENTTYPE_COL_DISPLAY = REQUIRED_INTERNAL_COLUMNS['EventType']
        self.TIMESTAMP_COL_DISPLAY = REQUIRED_INTERNAL_COLUMNS['Timestamp']
        
        # Instance variables to track current processing session
        self.current_session_data = None
        self.processing_session_id = None
        
    def register_callbacks(self):
        """Register all graph-related callbacks"""
        self._register_data_reset_generation_handler()
        self._register_node_interaction_handlers()
        
    def _register_data_reset_generation_handler(self):
        """FIXED main callback with proper data reset between uploads"""
        @self.app.callback(
            [
                Output('onion-graph', 'elements', allow_duplicate=True),
                Output('processing-status', 'children', allow_duplicate=True),
                Output('graph-output-container', 'style', allow_duplicate=True),
                Output('stats-panels-container', 'style', allow_duplicate=True),
                Output('yosai-custom-header', 'style', allow_duplicate=True),
                
                # EXISTING STATISTICS OUTPUTS
                Output('total-access-events-H1', 'children'),
                Output('event-date-range-P', 'children'),
                Output('stats-date-range-P', 'children'),
                Output('stats-days-with-data-P', 'children'),
                Output('stats-num-devices-P', 'children'),
                Output('stats-unique-tokens-P', 'children'),
                Output('most-active-devices-table-body', 'children'),
                
                # NEW ENHANCED STATISTICS OUTPUTS
                Output('stats-non-access-events-P', 'children'),
                Output('stats-duplicate-events-P', 'children'),
                Output('stats-uncommon-events-P', 'children'),
                
                # STORES
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
        def generate_with_data_reset(
            n_clicks,
            file_contents_b64,
            stored_column_mapping_json,
            all_door_ids_from_store,
            floor_values,
            floor_ids,
            is_ee_values,
            is_ee_ids,
            is_stair_values,
            is_stair_ids,
            security_slider_values,
            security_slider_ids,
            num_floors_from_input,
            manual_map_choice,
            csv_headers,
            existing_saved_classifications_json
        ):
            return self._process_with_data_reset(
                n_clicks,
                file_contents_b64,
                stored_column_mapping_json,
                all_door_ids_from_store,
                floor_values,
                floor_ids,
                is_ee_values,
                is_ee_ids,
                is_stair_values,
                is_stair_ids,
                security_slider_values,
                security_slider_ids,
                num_floors_from_input,
                manual_map_choice,
                csv_headers,
                existing_saved_classifications_json
            )
    
    def _register_node_interaction_handlers(self):
        """Register node tap and interaction handlers"""
        @self.app.callback(
            Output('tap-node-data-output', 'children'),
            Input('onion-graph', 'tapNodeData')
        )
        def display_tap_node_data_final(data):
            return self.graph_component.format_node_details(data)
    
    def _process_with_data_reset(
        self,
        n_clicks,
        file_contents_b64,
        stored_column_mapping_json,
        all_door_ids_from_store,
        floor_values,
        floor_ids,
        is_ee_values,
        is_ee_ids,
        is_stair_values,
        is_stair_ids,
        security_slider_values,
        security_slider_ids,
        num_floors_from_input,
        manual_map_choice,
        csv_headers,
        existing_saved_classifications_json
    ):
        """FIXED graph generation with proper data reset"""
        
        print("=" * 80)
        print("🔄 STARTING NEW PROCESSING SESSION - CLEARING ALL PREVIOUS DATA")
        print("=" * 80)
        
        # CRITICAL: Clear any previous session data
        self._clear_session_data()
        
        # Create new session ID based on file contents
        session_id = (
            hashlib.md5(str(file_contents_b64).encode()).hexdigest()[:8]
            if file_contents_b64 else
            "no_file"
        )
        self.processing_session_id = session_id
        
        print(f"🆔 New processing session ID: {session_id}")
        
        # Initialize default values
        hide_style = UI_STYLES['hide']
        show_style = UI_STYLES['show_block']
        show_stats_style = UI_STYLES['show_flex_stats']
        
        default_stats = self.stats_component.get_default_stats_values()
        graph_elements = []
        status_msg = "Processing..."
        
        if not n_clicks or not file_contents_b64:
            print("❌ No button click or file data - returning defaults")
            return self._create_reset_default_response(
                hide_style, default_stats, stored_column_mapping_json
            )
        
        try:
            print(f"✅ Starting processing for session {session_id}")
            
            # Process classifications
            result = self._process_classifications(
                manual_map_choice,
                all_door_ids_from_store,
                floor_values,
                floor_ids,
                is_ee_values,
                is_ee_ids,
                is_stair_values,
                is_stair_ids,
                security_slider_values,
                security_slider_ids,
                csv_headers,
                existing_saved_classifications_json
            )
            
            current_door_classifications = result['classifications']
            confirmed_entrances = result['entrances']
            all_manual_classifications = result['all_classifications']
            
            # Process CSV data with COMPLETE RESET
            processed_data = self._process_csv_data_with_reset(
                file_contents_b64,
                stored_column_mapping_json,
                csv_headers,
                session_id
            )
            
            if not processed_data['success']:
                print(f"❌ CSV processing failed: {processed_data['error']}")
                return self._create_reset_error_response(
                    processed_data['error'],
                    hide_style,
                    default_stats,
                    stored_column_mapping_json
                )
            
            df_final = processed_data['dataframe']
            df_original = processed_data['original_dataframe']
            
            print(
                f"📊 DATA LOADED - Original: {len(df_original)} rows, "
                f"Final: {len(df_final)} rows"
            )
            print(
                f"📊 Session {session_id} - Data difference: "
                f"{len(df_original) - len(df_final)} rows filtered"
            )
            
            # Store session data for tracking
            self.current_session_data = {
                'session_id': session_id,
                'original_count': len(df_original),
                'final_count': len(df_final),
                'df_original': df_original,
                'df_final': df_final
            }
            
            # Run onion model processing
            model_result = self._run_reset_onion_model(
                df_final,
                num_floors_from_input,
                confirmed_entrances,
                current_door_classifications,
                session_id
            )
            
            if model_result['success']:
                # Generate graph elements and RESET stats
                graph_elements = model_result['graph_elements']
                
                # FIXED statistics extraction with session tracking
                reset_stats_data = self._extract_reset_statistics(
                    model_result['enriched_df'],
                    model_result['device_attrs'],
                    session_id
                )
                
                current_yosai_style = show_style if graph_elements else hide_style
                status_msg = (
                    f"Graph generated for session {session_id}!"
                    if graph_elements else
                    f"Processed session {session_id}, but no graph elements to display."
                )
                
                print(f"✅ SUCCESS for session {session_id}")
                
                return self._create_reset_success_response(
                    graph_elements,
                    reset_stats_data,
                    current_yosai_style,
                    show_style,
                    show_stats_style,
                    status_msg,
                    all_manual_classifications,
                    stored_column_mapping_json
                )
            else:
                print(
                    f"❌ Onion model failed for session {session_id}: "
                    f"{model_result['error']}"
                )
                return self._create_reset_error_response(
                    model_result['error'],
                    hide_style,
                    default_stats,
                    stored_column_mapping_json
                )
                
        except Exception as e:
            print(f"💥 EXCEPTION in session {session_id}: {e}")
            traceback.print_exc()
            return self._create_reset_error_response(
                str(e),
                hide_style,
                default_stats,
                stored_column_mapping_json
            )
    
    def _clear_session_data(self):
        """Clear all previous session data"""
        print("🧹 Clearing previous session data...")
        self.current_session_data = None
        self.processing_session_id = None
        # Clear any class-level caches or state here if needed
    
    def _process_csv_data_with_reset(
        self,
        file_contents_b64,
        stored_column_mapping_json,
        csv_headers,
        session_id
    ):
        """RESET-SAFE CSV processing that ensures clean data"""
        try:
            print(f"📁 Processing CSV data for session {session_id}...")
            
            # Decode CSV and load original data - FRESH LOAD
            csv_io_for_loader = decode_uploaded_csv(file_contents_b64)
            
            # Load original data for statistics comparison - FRESH LOAD
            content_type, content_string = file_contents_b64.split(',')
            decoded = base64.b64decode(content_string)
            df_original = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
            
            print(
                f"📊 Session {session_id}: Original data FRESH loaded: "
                f"{len(df_original)} rows, columns: {list(df_original.columns)}"
            )
            
            # Get column mapping
            if isinstance(stored_column_mapping_json, str):
                all_column_mappings = json.loads(stored_column_mapping_json)
            else:
                all_column_mappings = stored_column_mapping_json or {}
            
            header_key = (
                json.dumps(sorted(csv_headers)) if csv_headers else None
            )
            stored_map = (
                all_column_mappings.get(header_key) if header_key else None
            )
            
            # Ensure we cover all required internal columns
            required_keys = set(REQUIRED_INTERNAL_COLUMNS.keys())
            mapped_keys = set(stored_map.values()) if stored_map else set()
            if not stored_map or not required_keys.issubset(mapped_keys):
                raise ValueError(
                    "No valid column mapping found. "
                    "Please ensure all required columns are mapped."
                )
            
            print(f"🗂️ Session {session_id}: Column mapping: {stored_map}")
            
            # Prepare mapping for loader
            mapping_for_loader_csv_to_display = {}
            for csv_col_name, internal_key in stored_map.items():
                if internal_key in REQUIRED_INTERNAL_COLUMNS:
                    display_name = REQUIRED_INTERNAL_COLUMNS[internal_key]
                    mapping_for_loader_csv_to_display[csv_col_name] = display_name
                else:
                    mapping_for_loader_csv_to_display[csv_col_name] = internal_key
            
            print(
                f"🔗 Session {session_id}: Mapping for loader: "
                f"{mapping_for_loader_csv_to_display}"
            )
            
            # Load DataFrame - FRESH LOAD
            df_final = load_csv_event_log(
                csv_io_for_loader,
                mapping_for_loader_csv_to_display
            )
            
            if df_final is None:
                raise ValueError("Failed to load CSV for processing.")
            
            print(
                f"📊 Session {session_id}: Final data FRESH loaded: "
                f"{len(df_final)} rows, columns: {list(df_final.columns)}"
            )
            
            # Validate required display columns
            missing_display_columns = [
                display_name
                for internal_key, display_name in REQUIRED_INTERNAL_COLUMNS.items()
                if display_name not in df_final.columns
            ]
            
            if missing_display_columns:
                raise ValueError(
                    f"Missing required columns: {', '.join(missing_display_columns)}"
                )
            
            return {
                'success': True,
                'dataframe': df_final,
                'original_dataframe': df_original  # Include original for comparison
            }
            
        except Exception as e:
            print(f"💥 ERROR in CSV processing for session {session_id}: {e}")
            return {'success': False, 'error': str(e)}
    
    def _run_reset_onion_model(
        self,
        df_final,
        num_floors_from_input,
        confirmed_entrances,
        current_door_classifications,
        session_id
    ):
        """RESET-SAFE onion model processing"""
        try:
            print(f"🧠 Running onion model for session {session_id}...")
            
            config = GRAPH_PROCESSING_CONFIG.copy()
            config['num_floors'] = (
                num_floors_from_input
                if num_floors_from_input
                else GRAPH_PROCESSING_CONFIG['num_floors']
            )

            enriched_df, device_attrs, path_viz, all_paths = run_onion_model_processing(
                df_final.copy(),  # Use copy to avoid modifying original
                config,
                confirmed_official_entrances=confirmed_entrances,
                detailed_door_classifications=current_door_classifications
            )
            
            if enriched_df is not None:
                print(
                    f"✅ Session {session_id}: Onion model completed - "
                    f"enriched: {len(enriched_df)} rows"
                )
                
                # Generate graph elements
                nodes, edges = prepare_cytoscape_elements(
                    device_attrs,
                    path_viz,
                    all_paths
                )
                graph_elements = nodes + edges
                
                return {
                    'success': True,
                    'graph_elements': graph_elements,
                    'enriched_df': enriched_df,
                    'device_attrs': device_attrs,
                    'path_viz': path_viz,
                    'all_paths': all_paths
                }
            else:
                return {
                    'success': False,
                    'error': f"Error in processing for session {session_id}: incomplete result."
                }
                
        except Exception as e:
            print(f"💥 ERROR in onion model for session {session_id}: {e}")
            return {'success': False, 'error': str(e)}
    
    def _extract_reset_statistics(self, enriched_df, device_attrs, session_id):
        """RESET-SAFE statistics extraction using current session data"""
        
        print(f"📈 Extracting statistics for session {session_id}...")
        
        if (
            not self.current_session_data
            or self.current_session_data['session_id'] != session_id
        ):
            print(f"⚠️ WARNING: Session data mismatch for {session_id}")
            # Fallback to basic stats
            return self.stats_component.get_default_stats_values()
        
        # Use session data to ensure we're using the CORRECT original and final counts
        original_count = self.current_session_data['original_count']
        final_count = self.current_session_data['final_count']
        df_original = self.current_session_data['df_original']
        
        print(f"📊 Session {session_id} statistics:")
        print(f"   - Original CSV rows: {original_count}")
        print(f"   - Final processed rows: {final_count}")
        print(f"   - Enriched rows: {len(enriched_df)}")
        
        # Use FIXED stats processor with session data
        enhanced_stats_raw = self.stats_processor.extract_enhanced_stats(
            enriched_df,
            df_original,  # Use original from session
            processing_info={'session_id': session_id, 'final_count': final_count}
        )
        
        print(f"🔢 Session {session_id} raw stats: {enhanced_stats_raw}")
        
        # Format for display
        formatted_stats = self.stats_component.format_enhanced_statistics_data(
            enhanced_stats_raw
        )
        
        print(f"📋 Session {session_id} formatted stats: {formatted_stats}")
        
        # Convert to format expected by callback outputs
        stats = self.stats_component.get_default_stats_values()
        
        # Update with actual data
        if enhanced_stats_raw:
            # Basic stats
            stats['total_access_events'] = f"{enhanced_stats_raw['total_events']:,}"
            stats['event_date_range'] = enhanced_stats_raw['date_range']
            stats['stats_date_range'] = formatted_stats['date_range']
            stats['stats_days_with_data'] = formatted_stats['days_with_data']
            stats['stats_num_devices'] = formatted_stats['num_devices']
            stats['stats_unique_tokens'] = formatted_stats['unique_tokens']
            
            # Device table
            if enhanced_stats_raw['device_counts']:
                stats['most_active_devices_table'] = [
                    html.Tr([
                        html.Td(device),
                        html.Td(f"{count:,}", style={'textAlign': 'right'})
                    ])
                    for device, count in enhanced_stats_raw['device_counts'].items()
                ]
            
            # NEW ENHANCED STATS
            stats['stats_non_access_events'] = formatted_stats['non_access_events']
            stats['stats_duplicate_events'] = formatted_stats['duplicate_events']
            stats['stats_uncommon_events'] = formatted_stats['uncommon_events']
        
        print(f"✅ Session {session_id} final display stats ready")
        return stats
    
    def _create_reset_default_response(
        self,
        hide_style,
        default_stats,
        stored_column_mapping_json
    ):
        """Reset-safe default response"""
        # Use .get(...) calls in case default_stats is missing enhanced keys
        return (
            [],
            "Missing data or button not clicked.",
            hide_style,
            hide_style,
            hide_style,
            # Basic stats
            default_stats.get('total_access_events', ""),
            default_stats.get('event_date_range', ""),
            default_stats.get('stats_date_range', ""),
            default_stats.get('stats_days_with_data', ""),
            default_stats.get('stats_num_devices', ""),
            default_stats.get('stats_unique_tokens', ""),
            default_stats.get('most_active_devices_table', []),
            # NEW enhanced stats
            default_stats.get('stats_non_access_events', ""),
            default_stats.get('stats_duplicate_events', ""),
            default_stats.get('stats_uncommon_events', ""),
            # Stores
            no_update,
            stored_column_mapping_json
        )
    
    def _create_reset_success_response(
        self,
        graph_elements,
        stats_data,
        yosai_style,
        graph_style,
        stats_style,
        status_msg,
        all_manual_classifications,
        stored_column_mapping_json
    ):
        """Reset-safe success response"""
        return (
            graph_elements,
            status_msg,
            graph_style,
            stats_style,
            yosai_style,
            # Basic stats
            stats_data['total_access_events'],
            stats_data['event_date_range'],
            stats_data['stats_date_range'],
            stats_data['stats_days_with_data'],
            stats_data['stats_num_devices'],
            stats_data['stats_unique_tokens'],
            stats_data['most_active_devices_table'],
            # NEW enhanced stats
            stats_data['stats_non_access_events'],
            stats_data['stats_duplicate_events'],
            stats_data['stats_uncommon_events'],
            # Stores
            json.dumps(all_manual_classifications) if all_manual_classifications else no_update,
            stored_column_mapping_json
        )
    
    def _create_reset_error_response(
        self,
        error_msg,
        hide_style,
        default_stats,
        stored_column_mapping_json
    ):
        """Reset-safe error response"""
        return (
            [],
            f"Error: {error_msg}",
            hide_style,
            hide_style,
            hide_style,
            # Basic stats
            default_stats.get('total_access_events', ""),
            default_stats.get('event_date_range', ""),
            default_stats.get('stats_date_range', ""),
            default_stats.get('stats_days_with_data', ""),
            default_stats.get('stats_num_devices', ""),
            default_stats.get('stats_unique_tokens', ""),
            default_stats.get('most_active_devices_table', []),
            # NEW enhanced stats
            default_stats.get('stats_non_access_events', ""),
            default_stats.get('stats_duplicate_events', ""),
            default_stats.get('stats_uncommon_events', ""),
            # Stores
            no_update,
            stored_column_mapping_json
        )
    
    def _process_classifications(
        self,
        manual_map_choice,
        all_door_ids_from_store,
        floor_values,
        floor_ids,
        is_ee_values,
        is_ee_ids,
        is_stair_values,
        is_stair_ids,
        security_slider_values,
        security_slider_ids,
        csv_headers,
        existing_saved_classifications_json
    ):
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
            floor_map = {
                f_id['index']: f_val for f_id, f_val in zip(floor_ids, floor_values)
            }
            # Assume ee_val is a list (from a Checklist) containing 'is_ee' if checked.
            is_ee_map = {}
            for ee_id, ee_val in zip(is_ee_ids, is_ee_values):
                index = ee_id['index']
                if isinstance(ee_val, (list, tuple)):
                    is_ee_map[index] = ('is_ee' in ee_val)
                else:
                    is_ee_map[index] = bool(ee_val)
            # Similarly for stair
            is_stair_map = {}
            for st_id, st_val in zip(is_stair_ids, is_stair_values):
                index = st_id['index']
                if isinstance(st_val, (list, tuple)):
                    is_stair_map[index] = ('is_stair' in st_val)
                else:
                    is_stair_map[index] = bool(st_val)
            
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


# Factory function for easy handler creation
def create_enhanced_graph_handlers(app):
    """Factory function to create DATA RESET FIXED enhanced graph handlers"""
    return DataResetFixedGraphHandlers(app)

# Backward compatibility
def create_graph_handlers(app):
    """Factory function to create graph handlers (DATA RESET FIXED version)"""
    return DataResetFixedGraphHandlers(app)
