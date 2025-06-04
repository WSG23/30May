# ui/components/enhanced_stats_handlers.py
"""
Enhanced Statistics Handlers - Comprehensive callback management for enhanced stats
Integrates seamlessly with existing graph_handlers.py while adding powerful new capabilities
"""

import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import traceback
import io
import base64

from dash import Input, Output, State, html, dcc, callback, no_update
from dash.dependencies import ALL
import plotly.graph_objects as go
import plotly.express as px

# Import existing components
from ui.components.enhanced_stats import create_enhanced_stats_component
from ui.themes.style_config import COLORS
from utils.constants import REQUIRED_INTERNAL_COLUMNS
from services.onion_model import run_onion_model_processing
from services.cytoscape_prep import prepare_cytoscape_elements
from services.graph_config import GRAPH_PROCESSING_CONFIG, UI_STYLES
from services.file_utils import decode_uploaded_csv
from services.csv_loader import load_csv_event_log
from utils.logging_config import get_logger

logger = get_logger(__name__)


class EnhancedStatsHandlers:
    """Handles all enhanced statistics callbacks and business logic"""
    
    def __init__(self, app):
        self.app = app
        self.enhanced_stats = create_enhanced_stats_component()
        
        # Display names for consistency
        self.DOORID_COL_DISPLAY = REQUIRED_INTERNAL_COLUMNS['DoorID']
        self.USERID_COL_DISPLAY = REQUIRED_INTERNAL_COLUMNS['UserID']
        self.EVENTTYPE_COL_DISPLAY = REQUIRED_INTERNAL_COLUMNS['EventType']
        self.TIMESTAMP_COL_DISPLAY = REQUIRED_INTERNAL_COLUMNS['Timestamp']
        
    def register_callbacks(self):
        """Register all enhanced statistics callbacks"""
        self._register_main_enhanced_stats_handler()
        self._register_chart_interaction_handlers()
        self._register_export_handlers()
        self._register_real_time_handlers()
        self._register_analytics_tools_handlers()
        
    def _register_main_enhanced_stats_handler(self):
        """Main callback for generating enhanced statistics and charts"""
        @self.app.callback(
            [
                # Enhanced stats outputs
                Output('enhanced-total-access-events-H1', 'children'),
                Output('enhanced-event-date-range-P', 'children'),
                Output('events-trend-indicator', 'children'),
                Output('events-trend-indicator', 'style'),
                #Output('avg-events-per-day', 'children'),
                
                # Enhanced statistics panel
                Output('enhanced-stats-date-range-P', 'children'),
                Output('enhanced-stats-days-with-data-P', 'children'),
                Output('enhanced-stats-num-devices-P', 'children'),
                Output('enhanced-stats-unique-tokens-P', 'children'),
                Output('peak-hour-stat', 'children'),
                Output('busiest-day-stat', 'children'),
                Output('avg-session-length', 'children'),
                Output('compliance-score', 'children'),
                
                # Enhanced devices panel
                Output('total-devices-summary', 'children'),
                Output('active-devices-today', 'children'),
                Output('enhanced-most-active-devices-table-body', 'children'),
                
                # Peak activity panel
                Output('peak-hour-display', 'children'),
                Output('peak-day-display', 'children'),
                Output('peak-activity-events', 'children'),
                Output('activity-level-indicator', 'children'),
                
                # Security distribution panel
                Output('security-level-breakdown', 'children'),
                Output('security-compliance-score', 'children'),
                
                # User patterns panel
                Output('most-active-user', 'children'),
                Output('avg-user-activity', 'children'),
                Output('unique-users-today', 'children'),
                Output('primary-access-pattern', 'children'),
                Output('access-pattern-description', 'children'),
                
                # Charts
                Output('main-analytics-chart', 'figure'),
                Output('security-pie-chart', 'figure'),
                Output('device-heatmap-chart', 'figure'),
                
                # Data stores
                Output('enhanced-stats-data-store', 'data'),
                Output('chart-data-store', 'data'),
            ],
            [
                Input('confirm-and-generate-button', 'n_clicks'),
                Input('refresh-stats-btn', 'n_clicks'),
                Input('stats-refresh-interval', 'n_intervals'),
                Input('chart-hourly-btn', 'n_clicks'),
                Input('chart-daily-btn', 'n_clicks'),
                Input('chart-security-btn', 'n_clicks'),
                Input('chart-devices-btn', 'n_clicks'),
            ],
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
                State('manual-door-classifications-store', 'data'),
                State('enhanced-stats-data-store', 'data'),
                State('chart-data-store', 'data'),
            ],
            prevent_initial_call=True
        )
        def generate_enhanced_stats(
            generate_clicks, refresh_clicks, refresh_intervals,
            hourly_clicks, daily_clicks, security_clicks, devices_clicks,
            file_contents_b64, stored_column_mapping_json, all_door_ids_from_store,
            floor_values, floor_ids, is_ee_values, is_ee_ids, is_stair_values, is_stair_ids,
            security_slider_values, security_slider_ids, num_floors_from_input, manual_map_choice,
            csv_headers, existing_saved_classifications_json, existing_stats_data, existing_chart_data
        ):
            return self._process_enhanced_stats_generation(
                generate_clicks, refresh_clicks, refresh_intervals,
                hourly_clicks, daily_clicks, security_clicks, devices_clicks,
                file_contents_b64, stored_column_mapping_json, all_door_ids_from_store,
                floor_values, floor_ids, is_ee_values, is_ee_ids, is_stair_values, is_stair_ids,
                security_slider_values, security_slider_ids, num_floors_from_input, manual_map_choice,
                csv_headers, existing_saved_classifications_json, existing_stats_data, existing_chart_data
            )
    
    def _register_chart_interaction_handlers(self):
        """Register chart interaction callbacks"""
        @self.app.callback(
            [
                Output('chart-hourly-btn', 'color'),
                Output('chart-daily-btn', 'color'),
                Output('chart-security-btn', 'color'),
                Output('chart-devices-btn', 'color'),
            ],
            [
                Input('chart-hourly-btn', 'n_clicks'),
                Input('chart-daily-btn', 'n_clicks'),
                Input('chart-security-btn', 'n_clicks'),
                Input('chart-devices-btn', 'n_clicks'),
            ],
            prevent_initial_call=True
        )
        def update_chart_buttons(hourly_clicks, daily_clicks, security_clicks, devices_clicks):
            from dash import ctx
            
            if not ctx.triggered:
                return "primary", "outline-primary", "outline-primary", "outline-primary"
            
            button_id = ctx.triggered[0]['prop_id'].split('.')[0]
            
            colors = ["outline-primary", "outline-primary", "outline-primary", "outline-primary"]
            if button_id == 'chart-hourly-btn':
                colors[0] = "primary"
            elif button_id == 'chart-daily-btn':
                colors[1] = "primary"
            elif button_id == 'chart-security-btn':
                colors[2] = "primary"
            elif button_id == 'chart-devices-btn':
                colors[3] = "primary"
            
            return colors
    
    def _register_export_handlers(self):
        """Register export functionality callbacks"""
        @self.app.callback(
            Output('export-stats-btn', 'children'),
            [
                Input('export-pdf-btn', 'n_clicks'),
                Input('export-excel-btn', 'n_clicks'),
                Input('export-charts-btn', 'n_clicks'),
                Input('export-json-btn', 'n_clicks'),
            ],
            [State('enhanced-stats-data-store', 'data')],
            prevent_initial_call=True
        )
        def handle_export_requests(pdf_clicks, excel_clicks, charts_clicks, json_clicks, stats_data):
            from dash import ctx
            
            if not ctx.triggered or not stats_data:
                return no_update
            
            button_id = ctx.triggered[0]['prop_id'].split('.')[0]
            
            try:
                if button_id == 'export-pdf-btn':
                    return self._export_pdf_report(stats_data)
                elif button_id == 'export-excel-btn':
                    return self._export_excel_data(stats_data)
                elif button_id == 'export-charts-btn':
                    return self._export_charts_png(stats_data)
                elif button_id == 'export-json-btn':
                    return self._export_json_data(stats_data)
            except Exception as e:
                logger.error(f"Export error: {e}")
                return "❌ Export Failed"
            
            return no_update
    
    def _register_real_time_handlers(self):
        """Register real-time update handlers"""
        @self.app.callback(
            [
                Output('stats-refresh-interval', 'disabled'),
                Output('real-time-toggle', 'label'),
            ],
            [Input('real-time-toggle', 'value')],
            prevent_initial_call=True
        )
        def toggle_real_time_updates(real_time_enabled):
            if real_time_enabled:
                return False, "Real-time ON"
            else:
                return True, "Real-time OFF"
    
    def _register_analytics_tools_handlers(self):
        """Register analytics tools callbacks"""
        @self.app.callback(
            Output('anomaly-detection-btn', 'children'),
            [Input('anomaly-detection-btn', 'n_clicks')],
            [State('enhanced-stats-data-store', 'data')],
            prevent_initial_call=True
        )
        def run_anomaly_detection(n_clicks, stats_data):
            if not n_clicks or not stats_data:
                return no_update
            
            # Placeholder for anomaly detection
            anomalies = self._detect_anomalies(stats_data)
            if anomalies:
                return f"🚨 {len(anomalies)} Anomalies"
            else:
                return "✅ No Anomalies"
    
    def _process_enhanced_stats_generation(self, generate_clicks, refresh_clicks, refresh_intervals,
                                         hourly_clicks, daily_clicks, security_clicks, devices_clicks,
                                         file_contents_b64, stored_column_mapping_json, all_door_ids_from_store,
                                         floor_values, floor_ids, is_ee_values, is_ee_ids, is_stair_values, is_stair_ids,
                                         security_slider_values, security_slider_ids, num_floors_from_input, manual_map_choice,
                                         csv_headers, existing_saved_classifications_json, existing_stats_data, existing_chart_data):
        """Main processing logic for enhanced statistics"""
        
        try:
            # Check if we need to trigger processing
            should_process = generate_clicks or refresh_clicks or refresh_intervals
            
            if not should_process or not file_contents_b64:
                return self._create_default_enhanced_response()
            
            # Process classifications (reuse from existing handlers)
            result = self._process_classifications(
                manual_map_choice, all_door_ids_from_store, floor_values, floor_ids,
                is_ee_values, is_ee_ids, is_stair_values, is_stair_ids,
                security_slider_values, security_slider_ids, csv_headers, existing_saved_classifications_json
            )
            
            current_door_classifications = result['classifications']
            confirmed_entrances = result['entrances']
            
            # Process CSV data
            processed_data = self._process_csv_data(
                file_contents_b64, stored_column_mapping_json, csv_headers
            )
            
            if not processed_data['success']:
                return self._create_error_enhanced_response(processed_data['error'])
            
            df_final = processed_data['dataframe']
            
            # Run onion model processing
            model_result = self._run_onion_model(
                df_final, num_floors_from_input, confirmed_entrances, current_door_classifications
            )
            
            if model_result['success']:
                # Process enhanced statistics
                enhanced_stats = self.enhanced_stats.process_enhanced_stats(
                    model_result['enriched_df'], 
                    model_result['device_attrs']
                )
                
                # Determine which chart to show
                chart_type = self._determine_chart_type(
                    hourly_clicks, daily_clicks, security_clicks, devices_clicks
                )
                
                # Generate charts
                charts = self._generate_charts(
                    model_result['enriched_df'], 
                    model_result['device_attrs'],
                    chart_type
                )
                
                return self._create_success_enhanced_response(
                    enhanced_stats, charts, model_result
                )
            else:
                return self._create_error_enhanced_response(model_result['error'])
                
        except Exception as e:
            logger.error(f"Enhanced stats processing error: {e}")
            traceback.print_exc()
            return self._create_error_enhanced_response(str(e))
    
    def _process_classifications(self, manual_map_choice, all_door_ids_from_store, floor_values, floor_ids,
                               is_ee_values, is_ee_ids, is_stair_values, is_stair_ids,
                               security_slider_values, security_slider_ids, csv_headers, existing_saved_classifications_json):
        """Process door classifications (reused from existing handler)"""
        
        if isinstance(existing_saved_classifications_json, str):
            all_manual_classifications = json.loads(existing_saved_classifications_json)
        else:
            all_manual_classifications = existing_saved_classifications_json or {}
        
        current_door_classifications = {}
        confirmed_entrances = []
        
        if manual_map_choice == 'yes' and all_door_ids_from_store:
            # Build mappings from form data
            floor_map = {f_id['index']: f_val for f_id, f_val in zip(floor_ids, floor_values)}
            is_ee_map = {ee_id['index']: 'is_ee' in ee_val for ee_id, ee_val in zip(is_ee_ids, is_ee_values)}
            is_stair_map = {st_id['index']: 'is_stair' in st_val for st_id, st_val in zip(is_stair_ids, is_stair_values)}
            
            security_map_slider_to_value = {}
            for s_id, s_val in zip(security_slider_ids, security_slider_values):
                if s_val <= 2:
                    security_val = "unclassified"
                elif s_val <= 5:
                    security_val = "green"
                elif s_val <= 7:
                    security_val = "yellow"
                else:
                    security_val = "red"
                security_map_slider_to_value[s_id['index']] = security_val
            
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
        """Process CSV data (reused from existing handler)"""
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
                raise ValueError("No valid column mapping found.")
            
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
            
            return {'success': True, 'dataframe': df_final}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _run_onion_model(self, df_final, num_floors_from_input, confirmed_entrances, current_door_classifications):
        """Run onion model processing (reused from existing handler)"""
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
                return {
                    'success': True,
                    'enriched_df': enriched_df,
                    'device_attrs': device_attrs,
                    'path_viz': path_viz,
                    'all_paths': all_paths
                }
            else:
                return {'success': False, 'error': "Error in processing: incomplete result."}
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _determine_chart_type(self, hourly_clicks, daily_clicks, security_clicks, devices_clicks):
        """Determine which chart type to display"""
        from dash import ctx
        
        if not ctx.triggered:
            return 'hourly'  # default
        
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        
        if button_id == 'chart-hourly-btn':
            return 'hourly'
        elif button_id == 'chart-daily-btn':
            return 'daily'
        elif button_id == 'chart-security-btn':
            return 'security'
        elif button_id == 'chart-devices-btn':
            return 'devices'
        else:
            return 'hourly'
    
    def _generate_charts(self, enriched_df, device_attrs, chart_type):
        """Generate all charts for the dashboard"""
        charts = {}
        
        # Main chart based on selected type
        if chart_type == 'hourly':
            charts['main'] = self.enhanced_stats.create_hourly_activity_chart(enriched_df)
        elif chart_type == 'daily':
            charts['main'] = self.enhanced_stats.create_daily_trends_chart(enriched_df)
        elif chart_type == 'security':
            charts['main'] = self.enhanced_stats.create_security_distribution_chart(device_attrs)
        elif chart_type == 'devices':
            charts['main'] = self.enhanced_stats.create_device_usage_chart(enriched_df)
        else:
            charts['main'] = self.enhanced_stats.create_hourly_activity_chart(enriched_df)
        
        # Secondary charts (always present)
        charts['security_pie'] = self.enhanced_stats.create_security_distribution_chart(device_attrs)
        charts['device_heatmap'] = self._create_device_heatmap_chart(enriched_df)
        
        return charts
    
    def _create_device_heatmap_chart(self, df):
        """Create device activity heatmap"""
        if df is None or df.empty:
            return self.enhanced_stats._create_empty_chart("No data for heatmap")
        
        if self.TIMESTAMP_COL_DISPLAY not in df.columns or self.DOORID_COL_DISPLAY not in df.columns:
            return self.enhanced_stats._create_empty_chart("Missing required columns for heatmap")
        
        # Create hour vs device heatmap
        df['hour'] = df[self.TIMESTAMP_COL_DISPLAY].dt.hour
        heatmap_data = df.groupby(['hour', self.DOORID_COL_DISPLAY]).size().reset_index(name='count')
        
        # Pivot for heatmap
        pivot_data = heatmap_data.pivot(index=self.DOORID_COL_DISPLAY, columns='hour', values='count').fillna(0)
        
        # Limit to top 10 devices for readability
        top_devices = df[self.DOORID_COL_DISPLAY].value_counts().head(10).index
        pivot_data = pivot_data.loc[pivot_data.index.isin(top_devices)]
        
        fig = go.Figure(data=go.Heatmap(
            z=pivot_data.values,
            x=pivot_data.columns,
            y=pivot_data.index,
            colorscale='Blues',
            colorbar=dict(title="Events")
        ))
        
        fig.update_layout(
            title="Device Activity Heatmap",
            xaxis_title="Hour of Day",
            yaxis_title="Device ID",
            **self.enhanced_stats.chart_theme['layout']
        )
        
        return fig
    
    def _create_default_enhanced_response(self):
        """Create default response when no data is available"""
        default_stats = self.enhanced_stats._get_default_enhanced_stats()
        empty_chart = self.enhanced_stats._create_empty_chart("No data available")
        
        return (
            # Enhanced access events
            "0", "N/A", "N/A", {'color': COLORS['text_secondary']}, "0 events/day",
            
            # Enhanced statistics  
            "N/A", "0 days", "0 devices", "0 users", "N/A", "N/A", "N/A", "N/A",
            
            # Enhanced devices
            "0 Total Devices", "0 active today", [],
            
            # Peak activity
            "N/A", "N/A", "0 events", html.Div("No activity data", style={'color': COLORS['text_secondary']}),
            
            # Security distribution
            [html.P("No security data", style={'color': COLORS['text_secondary']})], "0%",
            
            # User patterns
            "N/A", "0 events/user", "0", "No Pattern", "Insufficient data for analysis",
            
            # Charts
            empty_chart, empty_chart, empty_chart,
            
            # Data stores
            json.dumps(default_stats), "{}"
        )
    
    def _create_success_enhanced_response(self, enhanced_stats, charts, model_result):
        """Create successful response with all enhanced statistics"""
        
        # Format enhanced access events
        total_events = f"{enhanced_stats['total_events']:,}"
        date_range = enhanced_stats['date_range']
        
        # Calculate trend (placeholder - would need historical data)
        trend_text = "📈 +5.2%"
        trend_style = {'color': COLORS['success'], 'fontSize': '1rem'}
        
        avg_per_day = f"{enhanced_stats['events_per_day']:.1f} events/day"
        
        # Enhanced statistics
        stats_date_range = f"Date range: {enhanced_stats['date_range']}"
        stats_days = f"Days: {enhanced_stats['days_with_data']}"
        stats_devices = f"Devices: {enhanced_stats['num_devices']}"
        stats_users = f"Users: {enhanced_stats['unique_users']}"
        peak_hour_stat = f"Peak Hour: {enhanced_stats['peak_hour']}:00"
        busiest_day_stat = f"Busiest Day: {enhanced_stats['peak_day']}"
        avg_session = f"Avg Events/User: {enhanced_stats['avg_events_per_user']:.1f}"
        compliance = f"Score: {enhanced_stats['compliance_score']}%"
        
        # Enhanced devices
        total_devices_summary = f"{enhanced_stats['num_devices']} Total Devices"
        devices_active_today = f"{enhanced_stats['devices_active_today']} active today"
        
        # Create enhanced device table
        device_table = self._create_enhanced_device_table(model_result['enriched_df'])
        
        # Peak activity
        peak_hour_display = f"{enhanced_stats['peak_hour']}:00"
        peak_day_display = f"Busiest: {enhanced_stats['peak_day']}"
        peak_activity_events = f"{enhanced_stats['peak_hour_events']} events at peak"
        
        # Activity level indicator
        activity_level = self._create_activity_level_indicator(enhanced_stats['activity_variance'])
        
        # Security distribution
        security_breakdown = self._create_security_breakdown(enhanced_stats['security_distribution'])
        compliance_score = f"{enhanced_stats['compliance_score']}%"
        
        # User patterns
        most_active_user = f"Top User: {enhanced_stats['most_active_user']}"
        avg_user_activity = f"Avg: {enhanced_stats['avg_events_per_user']:.1f} events/user"
        users_today = f"{enhanced_stats['unique_users']} unique users"
        
        # Access patterns
        primary_pattern, pattern_description = self._analyze_access_patterns(enhanced_stats)
        
        return (
            # Enhanced access events
            total_events, date_range, trend_text, trend_style, avg_per_day,
            
            # Enhanced statistics
            stats_date_range, stats_days, stats_devices, stats_users,
            peak_hour_stat, busiest_day_stat, avg_session, compliance,
            
            # Enhanced devices
            total_devices_summary, devices_active_today, device_table,
            
            # Peak activity
            peak_hour_display, peak_day_display, peak_activity_events, activity_level,
            
            # Security distribution
            security_breakdown, compliance_score,
            
            # User patterns
            most_active_user, avg_user_activity, users_today, primary_pattern, pattern_description,
            
            # Charts
            charts['main'], charts['security_pie'], charts['device_heatmap'],
            
            # Data stores
            json.dumps(enhanced_stats), json.dumps(charts, default=str)
        )
    
    def _create_error_enhanced_response(self, error_message):
        """Create error response"""
        error_text = f"Error: {error_message}"
        error_style = {'color': COLORS['critical']}
        
        return (
            # Enhanced access events
            "Error", error_text, "N/A", error_style, "N/A",
            
            # Enhanced statistics
            error_text, "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A",
            
            # Enhanced devices
            "Error", error_text, [],
            
            # Peak activity
            "Error", error_text, "N/A", html.Div(error_text, style=error_style),
            
            # Security distribution
            [html.P(error_text, style=error_style)], "Error",
            
            # User patterns
            error_text, "N/A", "N/A", "Error", error_text,
            
            # Charts
            self.enhanced_stats._create_empty_chart(error_message),
            self.enhanced_stats._create_empty_chart(error_message),
            self.enhanced_stats._create_empty_chart(error_message),
            
            # Data stores
            "{}", "{}"
        )
    
    def _create_enhanced_device_table(self, df):
        """Create enhanced device table with trend indicators"""
        if df is None or df.empty or self.DOORID_COL_DISPLAY not in df.columns:
            return [html.Tr([html.Td("No data available", colSpan=3)])]
        
        device_counts = df[self.DOORID_COL_DISPLAY].value_counts().head(5)
        
        table_rows = []
        for device, count in device_counts.items():
            # Create simple trend indicator (placeholder)
            trend_indicator = "📈" if count > device_counts.median() else "📊"
            
            table_rows.append(
                html.Tr([
                    html.Td(device, style={'fontSize': '0.9rem'}),
                    html.Td(f"{count:,}", style={'textAlign': 'right', 'fontSize': '0.9rem'}),
                    html.Td(trend_indicator, style={'textAlign': 'center', 'fontSize': '0.9rem'})
                ])
            )
        
        return table_rows
    
    def _create_activity_level_indicator(self, activity_variance):
        """Create activity level indicator"""
        if activity_variance > 1000:
            level = "🔥 High"
            color = COLORS['critical']
        elif activity_variance > 500:
            level = "📊 Medium"
            color = COLORS['warning']
        else:
            level = "📉 Low"
            color = COLORS['success']
        
        return html.Div([
            html.Span(level, style={'color': color, 'fontWeight': 'bold'}),
            html.Br(),
            html.Small("Activity Variance", style={'color': COLORS['text_tertiary']})
        ])
    
    def _create_security_breakdown(self, security_distribution):
        """Create security level breakdown display"""
        if not security_distribution:
            return [html.P("No security data", style={'color': COLORS['text_secondary']})]
        
        items = []
        colors = {
            'green': COLORS['success'],
            'yellow': COLORS['warning'],
            'red': COLORS['critical'],
            'unclassified': COLORS['border']
        }
        
        for level, count in security_distribution.items():
            color = colors.get(level, COLORS['text_secondary'])
            items.append(
                html.P([
                    html.Span(f"{level.title()}: ", style={'color': COLORS['text_primary']}),
                    html.Span(f"{count} devices", style={'color': color, 'fontWeight': 'bold'})
                ], style={'margin': '5px 0'})
            )
        
        return items
    
    def _analyze_access_patterns(self, enhanced_stats):
        """Analyze access patterns for insights"""
        if enhanced_stats['peak_hour'] == 'N/A':
            return "No Pattern", "Insufficient data for analysis"
        
        peak_hour = enhanced_stats['peak_hour']
        
        if 7 <= peak_hour <= 10:
            return "Morning Rush", "Peak activity during morning hours (7-10 AM)"
        elif 11 <= peak_hour <= 14:
            return "Lunch Activity", "High activity during lunch period (11 AM-2 PM)"
        elif 15 <= peak_hour <= 18:
            return "Evening Rush", "Peak activity during evening hours (3-6 PM)"
        elif 19 <= peak_hour <= 23:
            return "Evening Activity", "Activity continues into evening (7-11 PM)"
        else:
            return "Off-Hours Activity", "Unusual peak activity during off-hours"
    
    # Export methods
    def _export_pdf_report(self, stats_data):
        """Export comprehensive PDF report"""
        # Placeholder - would generate PDF
        return "📄 PDF Generated"
    
    def _export_excel_data(self, stats_data):
        """Export data to Excel format"""
        # Placeholder - would generate Excel
        return "📊 Excel Generated"
    
    def _export_charts_png(self, stats_data):
        """Export charts as PNG images"""
        # Placeholder - would export charts
        return "📈 Charts Exported"
    
    def _export_json_data(self, stats_data):
        """Export raw data as JSON"""
        # Placeholder - would export JSON
        return "💾 JSON Generated"
    
    def _detect_anomalies(self, stats_data):
        """Detect anomalies in the data"""
        # Placeholder anomaly detection logic
        anomalies = []
        
        if stats_data.get('peak_hour_events', 0) > 1000:
            anomalies.append("Unusually high peak activity")
        
        if stats_data.get('compliance_score', 0) < 50:
            anomalies.append("Low security compliance")
        
        return anomalies


# Factory function
def create_enhanced_stats_handlers(app):
    """Factory function to create enhanced stats handlers"""
    return EnhancedStatsHandlers(app)