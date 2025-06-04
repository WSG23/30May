# ui/components/graph_handlers.py - ENHANCED VERSION (FIXED PLOTLY & TYPE ISSUES)
"""
Enhanced graph callback handlers with advanced analytics and chart generation - FIXED
"""

import json
import traceback
import pandas as pd
import base64
import io
from datetime import datetime
from typing import Dict, List, Tuple, Any, Optional, Union  # FIXED: Added proper type imports
from dash import Input, Output, State, html, no_update, callback
from dash.dependencies import ALL
import plotly.express as px
import plotly.graph_objects as go
from plotly.graph_objs import Figure  # FIXED: Proper plotly import

# Import UI components
from ui.components.graph import create_graph_component
from ui.components.stats import create_enhanced_stats_component
from ui.components.classification import create_classification_component

# Import processing modules
from services.onion_model import run_onion_model_processing
from services.cytoscape_prep import prepare_cytoscape_elements
from services.graph_config import GRAPH_PROCESSING_CONFIG, UI_STYLES
from utils.constants import REQUIRED_INTERNAL_COLUMNS
from services.file_utils import decode_uploaded_csv
from services.csv_loader import load_csv_event_log


class EnhancedGraphHandlers:
    """Enhanced handlers with advanced analytics, charts, and export capabilities - FIXED"""
    
    def __init__(self, app):
        self.app = app
        self.graph_component = create_graph_component()
        self.stats_component = create_enhanced_stats_component()  # Enhanced version
        self.classification_component = create_classification_component()
        
        # Cache for processed data - FIXED: Proper type annotations
        self.data_cache: Dict[str, Any] = {
            'enriched_df': None,
            'device_attrs': None,
            'metrics_data': None,
            'last_processed': None
        }
        
        # Define display names for consistency
        self.DOORID_COL_DISPLAY = REQUIRED_INTERNAL_COLUMNS['DoorID']
        self.USERID_COL_DISPLAY = REQUIRED_INTERNAL_COLUMNS['UserID']
        self.EVENTTYPE_COL_DISPLAY = REQUIRED_INTERNAL_COLUMNS['EventType']
        self.TIMESTAMP_COL_DISPLAY = REQUIRED_INTERNAL_COLUMNS['Timestamp']
        
    def register_callbacks(self):
        """Register all enhanced graph-related callbacks"""
        self._register_main_generation_handler()
        self._register_node_interaction_handlers()
        self._register_chart_callbacks()
        self._register_export_callbacks()
        self._register_analytics_callbacks()
        
    def _register_main_generation_handler(self):
        """Enhanced main callback for generating complete analytics"""
        @self.app.callback(
            [
                # Original outputs
                Output('onion-graph', 'elements', allow_duplicate=True),
                Output('processing-status', 'children', allow_duplicate=True),
                Output('graph-output-container', 'style', allow_duplicate=True),
                Output('stats-panels-container', 'style', allow_duplicate=True),
                Output('yosai-custom-header', 'style', allow_duplicate=True),
                
                # Enhanced statistics outputs
                Output('total-access-events-H1', 'children'),
                Output('event-date-range-P', 'children'),
                #Output('avg-events-per-day', 'children'),
                Output('peak-activity-day', 'children'),
                
                # User analytics outputs
                Output('stats-unique-users', 'children'),
                Output('stats-avg-events-per-user', 'children'),
                Output('stats-most-active-user', 'children'),
                Output('stats-devices-per-user', 'children'),
                Output('stats-peak-hour', 'children'),
                
                # Device analytics outputs
                Output('total-devices-count', 'children'),
                Output('entrance-devices-count', 'children'),
                Output('high-security-devices', 'children'),
                Output('most-active-devices-table-body', 'children'),
                
                # Peak activity outputs
                Output('peak-hour-display', 'children'),
                Output('peak-day-display', 'children'),
                Output('busiest-floor', 'children'),
                Output('entry-exit-ratio', 'children'),
                Output('weekend-vs-weekday', 'children'),
                
                # Security overview outputs
                Output('security-level-breakdown', 'children'),
                Output('compliance-score', 'children'),
                Output('anomaly-alerts', 'children'),
                
                # Analytics insights outputs
                Output('traffic-pattern-insight', 'children'),
                Output('security-score-insight', 'children'),
                Output('efficiency-insight', 'children'),
                Output('anomaly-insight', 'children'),
                
                # Chart outputs
                Output('main-analytics-chart', 'figure'),
                Output('security-pie-chart', 'figure'),
                Output('heatmap-chart', 'figure'),
                
                # Storage outputs
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
        def generate_enhanced_model(n_clicks, file_contents_b64, stored_column_mapping_json, all_door_ids_from_store,
                                   floor_values, floor_ids, is_ee_values, is_ee_ids, is_stair_values, is_stair_ids,
                                   security_slider_values, security_slider_ids, num_floors_from_input, manual_map_choice,
                                   csv_headers, existing_saved_classifications_json):

            return self._process_enhanced_graph_generation(
                n_clicks, file_contents_b64, stored_column_mapping_json, all_door_ids_from_store,
                floor_values, floor_ids, is_ee_values, is_ee_ids, is_stair_values, is_stair_ids,
                security_slider_values, security_slider_ids, num_floors_from_input, manual_map_choice,
                csv_headers, existing_saved_classifications_json
            )
    
    def _register_chart_callbacks(self):
        """Register chart interaction callbacks"""
        @self.app.callback(
            [
                Output('main-analytics-chart', 'figure', allow_duplicate=True),
                Output('security-pie-chart', 'figure', allow_duplicate=True),
                Output('heatmap-chart', 'figure', allow_duplicate=True)
            ],
            [
                Input('chart-type-selector', 'value'),
                Input('refresh-analytics', 'n_clicks')
            ],
            prevent_initial_call=True
        )
        def update_charts(chart_type, refresh_clicks):
            """Update charts based on selection"""
            if self.data_cache['enriched_df'] is None:
                empty_fig = self._create_empty_figure("No data available")
                return empty_fig, empty_fig, empty_fig
            
            df = self.data_cache['enriched_df']
            device_attrs = self.data_cache['device_attrs']
            
            # Generate main chart based on selection
            main_chart = self._generate_chart_by_type(chart_type, df, device_attrs)
            
            # Always update secondary charts
            security_chart = self.stats_component.create_security_pie_chart(device_attrs)
            heatmap_chart = self.stats_component.create_activity_heatmap(df)
            
            return main_chart, security_chart, heatmap_chart
    
    def _register_export_callbacks(self):
        """Register export and download callbacks"""
        @self.app.callback(
            Output("download-stats-csv", "data"),
            Input("export-stats-csv", "n_clicks"),
            prevent_initial_call=True
        )
        def export_stats_csv(n_clicks):
            """Export statistics as CSV"""
            if n_clicks and self.data_cache['metrics_data']:
                csv_data = self.stats_component.export_stats_to_csv(self.data_cache['metrics_data'])
                if csv_data:
                    return dict(content=csv_data, filename="analytics_stats.csv", base64=True)
            return no_update
        
        @self.app.callback(
            [
                Output("download-report", "data"),
                Output("export-status", "children")
            ],
            Input("generate-pdf-report", "n_clicks"),
            prevent_initial_call=True
        )
        def generate_report(n_clicks):
            """Generate comprehensive report"""
            if n_clicks and self.data_cache['metrics_data']:
                report_text = self.stats_component.generate_summary_report(self.data_cache['metrics_data'])
                
                # Convert to downloadable format
                report_bytes = report_text.encode('utf-8')
                report_b64 = base64.b64encode(report_bytes).decode()
                
                status = html.Div([
                    html.Span("✅ Report generated successfully!", 
                             style={'color': '#2DBE6C', 'fontWeight': 'bold'})
                ], style={'marginTop': '10px'})
                
                return (
                    dict(content=report_b64, filename=f"analytics_report_{datetime.now().strftime('%Y%m%d_%H%M')}.txt", base64=True),
                    status
                )
            
            return no_update, no_update
        
        @self.app.callback(
            Output("export-status", "children", allow_duplicate=True),
            Input("export-charts-png", "n_clicks"),
            prevent_initial_call=True
        )
        def export_charts_status(n_clicks):
            """Show export status for charts"""
            if n_clicks:
                return html.Div([
                    html.Span("📈 Use the camera icon in chart toolbar to download individual charts",
                             style={'color': '#2196F3', 'fontSize': '0.9rem'})
                ], style={'marginTop': '10px'})
            return no_update
    
    def _register_analytics_callbacks(self):
        """Register advanced analytics callbacks"""
        @self.app.callback(
            Output('analytics-detailed-breakdown', 'children'),
            Input('toggle-advanced-analytics', 'n_clicks'),
            prevent_initial_call=True
        )
        def toggle_detailed_analytics(n_clicks):
            """Toggle detailed analytics view"""
            if n_clicks and self.data_cache['metrics_data']:
                return self._create_detailed_breakdown(self.data_cache['metrics_data'])
            return html.Div("Click 'Advanced View' to see detailed breakdown")
    
    def _register_node_interaction_handlers(self):
        """Register node tap and interaction handlers"""
        @self.app.callback(
            Output('tap-node-data-output', 'children'),
            Input('onion-graph', 'tapNodeData')
        )
        def display_tap_node_data_enhanced(data):
            """Enhanced node data display with additional metrics"""
            if not data or data.get('is_layer_parent'):
                return "Upload CSV, map headers, (optionally classify doors), then Confirm & Generate. Tap a node for its details."
            
            details = [f"🎯 {data.get('label', data.get('id'))}"]
            
            # Enhanced node information
            if 'layer' in data:
                details.append(f"Layer: {data['layer']}")
            if 'floor' in data:
                details.append(f"Floor: {data['floor']}")
            if data.get('is_entrance'):
                details.append("🚪 Entry/Exit Point")
            if data.get('is_stair'):
                details.append("🏢 Stairway")
            if 'security_level' in data:
                security_emoji = {'green': '🟢', 'yellow': '🟡', 'red': '🔴', 'unclassified': '⚪'}.get(data['security_level'], '⚪')
                details.append(f"{security_emoji} Security: {data['security_level'].title()}")
            if data.get('is_critical'):
                details.append("⭐ Critical Device")
            if 'most_common_next' in data:
                details.append(f"→ Next: {data['most_common_next']}")
            
            # Add activity metrics if available
            if self.data_cache['enriched_df'] is not None:
                device_events = self.data_cache['enriched_df'][
                    self.data_cache['enriched_df'][self.DOORID_COL_DISPLAY] == data.get('id')
                ]
                if not device_events.empty:
                    details.append(f"📊 Events: {len(device_events)}")
                    unique_users = device_events[self.USERID_COL_DISPLAY].nunique()
                    details.append(f"👥 Users: {unique_users}")
            
            return " | ".join(details)
    
    def _process_enhanced_graph_generation(self, n_clicks, file_contents_b64, stored_column_mapping_json, all_door_ids_from_store,
                                         floor_values, floor_ids, is_ee_values, is_ee_ids, is_stair_values, is_stair_ids,
                                         security_slider_values, security_slider_ids, num_floors_from_input, manual_map_choice,
                                         csv_headers, existing_saved_classifications_json):
        """Enhanced processing with comprehensive analytics"""
        
        # Initialize default values
        hide_style = UI_STYLES['hide']
        show_style = UI_STYLES['show_block']
        show_stats_style = UI_STYLES['show_flex_stats']
        
        # Default return values
        default_values = self._get_default_enhanced_outputs(hide_style)
        
        if not n_clicks or not file_contents_b64:
            return default_values
        
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
                error_values = self._create_error_response(
                    processed_data['error'], hide_style, stored_column_mapping_json
                )
                return error_values
            
            df_final = processed_data['dataframe']
            
            # Run onion model processing
            model_result = self._run_onion_model(
                df_final, num_floors_from_input, confirmed_entrances, current_door_classifications
            )
            
            if model_result['success']:
                # Cache processed data - FIXED: Proper assignment
                self.data_cache['enriched_df'] = model_result['enriched_df']
                self.data_cache['device_attrs'] = model_result['device_attrs']
                self.data_cache['last_processed'] = datetime.now()  # FIXED: Direct assignment
                
                # Calculate enhanced metrics
                enhanced_metrics = self.stats_component.calculate_enhanced_metrics(
                    model_result['enriched_df'], 
                    model_result['device_attrs']
                )
                self.data_cache['metrics_data'] = enhanced_metrics  # FIXED: Direct assignment
                
                # Generate charts
                main_chart = self.stats_component.create_hourly_activity_chart(model_result['enriched_df'])
                security_chart = self.stats_component.create_security_pie_chart(model_result['device_attrs'])
                heatmap_chart = self.stats_component.create_activity_heatmap(model_result['enriched_df'])
                
                # Create success response
                return self._create_enhanced_success_response(
                    model_result['graph_elements'], enhanced_metrics, 
                    main_chart, security_chart, heatmap_chart,
                    show_style, show_stats_style, all_manual_classifications, stored_column_mapping_json
                )
            else:
                error_values = self._create_error_response(
                    model_result['error'], hide_style, stored_column_mapping_json
                )
                return error_values
                
        except Exception as e:
            traceback.print_exc()
            error_values = self._create_error_response(
                str(e), hide_style, stored_column_mapping_json
            )
            return error_values
    
    def _create_empty_figure(self, message: str = "No data available") -> go.Figure:
        """Create empty figure with message - FIXED: Uses update_layout for annotations"""
        fig = go.Figure()
        # Use update_layout with annotations instead of add_annotation for better compatibility
        fig.update_layout(
            annotations=[
                dict(
                    text=message,
                    showarrow=False,
                    xref="paper",
                    yref="paper",
                    x=0.5,
                    y=0.5,
                    font=dict(size=16, color='#F7FAFC')
                )
            ],
            plot_bgcolor='#0F1419',
            paper_bgcolor='#1A2332',
            font_color='#F7FAFC',
            xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
            yaxis=dict(showgrid=False, showticklabels=False, zeroline=False)
        )
        return fig
    
    def _generate_chart_by_type(self, chart_type: str, df: pd.DataFrame, device_attrs: Optional[pd.DataFrame]) -> Figure:
        """Generate specific chart type - FIXED: Proper return type"""
        try:
            if chart_type == 'hourly':
                return self.stats_component.create_hourly_activity_chart(df)
            elif chart_type == 'daily':
                return self._create_daily_trends_chart(df)
            elif chart_type == 'security':
                return self.stats_component.create_security_pie_chart(device_attrs)
            elif chart_type == 'floor':
                return self._create_floor_activity_chart(df, device_attrs)
            elif chart_type == 'users':
                return self._create_user_patterns_chart(df)
            elif chart_type == 'devices':
                return self._create_device_usage_chart(df, device_attrs)
            else:
                return self._create_empty_figure("Chart type not supported")
        except Exception as e:
            return self._create_empty_figure(f"Error generating chart: {str(e)}")
    
    def _create_daily_trends_chart(self, df: pd.DataFrame) -> Figure:
        """Create daily activity trends chart - FIXED"""
        if df is None or df.empty or self.TIMESTAMP_COL_DISPLAY not in df.columns:
            return self._create_empty_figure("No timestamp data available")
        
        try:
            df_copy = df.copy()
            df_copy['Date'] = df_copy[self.TIMESTAMP_COL_DISPLAY].dt.date
            daily_counts = df_copy['Date'].value_counts().sort_index()
            
            fig = px.line(
                x=daily_counts.index,
                y=daily_counts.values,
                title="Daily Access Trends",
                labels={'x': 'Date', 'y': 'Number of Events'},
                line_shape='spline'
            )
            
            fig.update_traces(line_color='#2196F3', line_width=3)
            fig.update_layout(
                plot_bgcolor='#0F1419',
                paper_bgcolor='#1A2332',
                font_color='#F7FAFC',
                title_font_color='#F7FAFC',
                xaxis=dict(gridcolor='#2D3748'),
                yaxis=dict(gridcolor='#2D3748')
            )
            
            return fig
        except Exception as e:
            return self._create_empty_figure(f"Error creating daily trends: {str(e)}")
    
    def _create_floor_activity_chart(self, df: pd.DataFrame, device_attrs: Optional[pd.DataFrame]) -> Figure:
        """Create floor-based activity chart - FIXED"""
        if df is None or df.empty or device_attrs is None or device_attrs.empty:
            return self._create_empty_figure("No floor data available")
        
        if 'Floor' not in device_attrs.columns or 'DoorID' not in device_attrs.columns:
            return self._create_empty_figure("No floor mapping available")
        
        try:
            # Map events to floors
            device_floor_map = device_attrs.set_index('DoorID')['Floor'].to_dict()
            df_copy = df.copy()
            df_copy['Floor'] = df_copy[self.DOORID_COL_DISPLAY].map(device_floor_map)
            
            floor_counts = df_copy['Floor'].value_counts().sort_index()
            
            fig = px.bar(
                x=floor_counts.index,
                y=floor_counts.values,
                title="Activity by Floor",
                labels={'x': 'Floor', 'y': 'Number of Events'},
                color=floor_counts.values,
                color_continuous_scale=['#1A2332', '#2196F3']
            )
            
            fig.update_layout(
                plot_bgcolor='#0F1419',
                paper_bgcolor='#1A2332',
                font_color='#F7FAFC',
                title_font_color='#F7FAFC'
            )
            
            return fig
        except Exception as e:
            return self._create_empty_figure(f"Error creating floor chart: {str(e)}")
    
    def _create_user_patterns_chart(self, df: pd.DataFrame) -> Figure:
        """Create user activity patterns chart - FIXED"""
        if df is None or df.empty or self.USERID_COL_DISPLAY not in df.columns:
            return self._create_empty_figure("No user data available")
        
        try:
            user_counts = df[self.USERID_COL_DISPLAY].value_counts().head(20)  # Top 20 users
            
            fig = px.bar(
                x=user_counts.values,
                y=user_counts.index,
                orientation='h',
                title="Top 20 Most Active Users",
                labels={'x': 'Number of Events', 'y': 'User ID'},
                color=user_counts.values,
                color_continuous_scale=['#1A2332', '#2196F3']
            )
            
            fig.update_layout(
                plot_bgcolor='#0F1419',
                paper_bgcolor='#1A2332',
                font_color='#F7FAFC',
                title_font_color='#F7FAFC',
                height=600
            )
            
            return fig
        except Exception as e:
            return self._create_empty_figure(f"Error creating user patterns: {str(e)}")
    
    def _create_device_usage_chart(self, df: pd.DataFrame, device_attrs: Optional[pd.DataFrame]) -> Figure:
        """Create device usage comparison chart - FIXED"""
        if df is None or df.empty or self.DOORID_COL_DISPLAY not in df.columns:
            return self._create_empty_figure("No device data available")
        
        try:
            device_counts = df[self.DOORID_COL_DISPLAY].value_counts().head(15)  # Top 15 devices
            
            # Add security level info if available
            colors = []
            if device_attrs is not None and 'SecurityLevel' in device_attrs.columns:
                security_map = device_attrs.set_index('DoorID')['SecurityLevel'].to_dict()
                color_mapping = {'green': '#2DBE6C', 'yellow': '#FFB020', 'red': '#E02020', 'unclassified': '#2D3748'}
                colors = [color_mapping.get(security_map.get(device, 'unclassified'), '#2196F3') 
                         for device in device_counts.index]
            else:
                colors = ['#2196F3'] * len(device_counts)
            
            fig = go.Figure(data=[
                go.Bar(
                    x=device_counts.index,
                    y=device_counts.values,
                    marker_color=colors,
                    text=device_counts.values,
                    textposition='auto'
                )
            ])
            
            fig.update_layout(
                title="Top 15 Most Active Devices",
                xaxis_title="Device ID",
                yaxis_title="Number of Events",
                plot_bgcolor='#0F1419',
                paper_bgcolor='#1A2332',
                font_color='#F7FAFC',
                title_font_color='#F7FAFC',
                xaxis_tickangle=-45
            )
            
            return fig
        except Exception as e:
            return self._create_empty_figure(f"Error creating device chart: {str(e)}")
    
    def _create_detailed_breakdown(self, metrics_data: Dict[str, Any]) -> html.Div:
        """Create detailed analytics breakdown - FIXED"""
        if not metrics_data:
            return html.Div("No data available for detailed breakdown")
        
        breakdown_items = []
        
        # Activity patterns section
        breakdown_items.append(html.Div([
            html.H5("📊 Activity Patterns", style={'color': '#2196F3', 'marginBottom': '10px'}),
            html.P(f"Traffic Pattern: {metrics_data.get('traffic_pattern', 'N/A')}"),
            html.P(f"Peak Activity: {metrics_data.get('peak_hour', 'N/A')} on {metrics_data.get('peak_day', 'N/A')}"),
            html.P(f"Busiest Location: {metrics_data.get('busiest_floor', 'N/A')}"),
        ], style={'marginBottom': '20px', 'color': '#E2E8F0'}))
        
        # Security analysis section
        breakdown_items.append(html.Div([
            html.H5("🔒 Security Analysis", style={'color': '#2DBE6C', 'marginBottom': '10px'}),
            html.P(f"Overall Security Score: {metrics_data.get('security_score', 'N/A')}"),
            html.P(f"High Security Devices: {metrics_data.get('high_security_devices', 'N/A')}"),
            html.P(f"Compliance Rating: {metrics_data.get('efficiency_score', 'N/A')}"),
        ], style={'marginBottom': '20px', 'color': '#E2E8F0'}))
        
        # User behavior section
        breakdown_items.append(html.Div([
            html.H5("👥 User Behavior", style={'color': '#FFB020', 'marginBottom': '10px'}),
            html.P(f"Total Unique Users: {metrics_data.get('unique_users', 'N/A')}"),
            html.P(f"Average Activity: {metrics_data.get('avg_events_per_user', 'N/A')}"),
            html.P(f"Most Active: {metrics_data.get('most_active_user', 'N/A')}"),
        ], style={'marginBottom': '20px', 'color': '#E2E8F0'}))
        
        # Anomaly detection section
        anomaly_count = metrics_data.get('anomaly_count', 0)
        anomaly_color = '#E02020' if anomaly_count > 0 else '#2DBE6C'
        breakdown_items.append(html.Div([
            html.H5("🚨 Anomaly Detection", style={'color': anomaly_color, 'marginBottom': '10px'}),
            html.P(f"Anomalies Detected: {anomaly_count}"),
            html.P("Status: " + ("⚠️ Review Required" if anomaly_count > 0 else "✅ Normal Activity")),
        ], style={'marginBottom': '20px', 'color': '#E2E8F0'}))
        
        return html.Div(breakdown_items, style={
            'padding': '20px',
            'backgroundColor': '#1A2332',
            'borderRadius': '8px',
            'border': '1px solid #2D3748'
        })
    
    def _get_default_enhanced_outputs(self, hide_style: Dict[str, str]) -> Tuple[Any, ...]:
        """Get default values for all enhanced outputs - FIXED: Proper return type"""
        empty_fig = self._create_empty_figure("No data available")
        
        return (
            # Original outputs
            [], "Missing data or button not clicked.", hide_style, hide_style, hide_style,
            
            # Enhanced statistics
            "0", "N/A", "N/A", "N/A",
            
            # User analytics
            "Users: 0", "N/A", "N/A", "N/A", "N/A",
            
            # Device analytics
            "0 devices", "0 entrances", "0 high security", 
            [html.Tr([html.Td("N/A", colSpan=2)])],
            
            # Peak activity
            "N/A", "N/A", "N/A", "N/A", "N/A",
            
            # Security overview
            [html.P("No security data", style={'color': '#A0AEC0'})], "N/A", "0 alerts",
            
            # Analytics insights
            "No Data", "N/A", "N/A", "0",
            
            # Charts
            empty_fig, empty_fig, empty_fig,
            
            # Storage
            no_update, no_update
        )
    
    def _create_enhanced_success_response(self, graph_elements: List[Dict], metrics: Dict[str, Any], 
                                        main_chart: Figure, security_chart: Figure, heatmap_chart: Figure,
                                        show_style: Dict, show_stats_style: Dict, all_manual_classifications: Dict, 
                                        stored_column_mapping_json: str) -> Tuple[Any, ...]:
        """Create enhanced success response with all metrics - FIXED"""
        
        # Security level breakdown
        security_breakdown = []
        if 'security_breakdown' in metrics and metrics['security_breakdown']:
            for level, count in metrics['security_breakdown'].items():
                color = {'green': '#2DBE6C', 'yellow': '#FFB020', 'red': '#E02020', 'unclassified': '#2D3748'}.get(level, '#2196F3')
                security_breakdown.append(
                    html.P(f"{level.title()}: {count} devices", 
                          style={'color': color, 'margin': '2px 0', 'fontSize': '0.9rem'})
                )
        else:
            security_breakdown = [html.P("No security data", style={'color': '#A0AEC0'})]
        
        # Calculate entry/exit ratio and weekend analysis
        entry_exit_ratio = "N/A"
        weekend_analysis = "N/A"
        
        if self.data_cache['enriched_df'] is not None and not self.data_cache['enriched_df'].empty:
            df = self.data_cache['enriched_df']
            if self.TIMESTAMP_COL_DISPLAY in df.columns:
                df_copy = df.copy()  # FIXED: Avoid modifying cached data
                df_copy['DayOfWeek'] = df_copy[self.TIMESTAMP_COL_DISPLAY].dt.day_name()
                weekday_events = len(df_copy[~df_copy['DayOfWeek'].isin(['Saturday', 'Sunday'])])
                weekend_events = len(df_copy[df_copy['DayOfWeek'].isin(['Saturday', 'Sunday'])])
                
                if weekend_events > 0:
                    ratio = weekday_events / weekend_events
                    weekend_analysis = f"Weekday/Weekend: {ratio:.1f}:1"
                else:
                    weekend_analysis = "Weekdays only"
                
                # Entry/exit analysis (simplified)
                if self.data_cache['device_attrs'] is not None:
                    entrance_devices = []
                    device_attrs = self.data_cache['device_attrs']
                    if 'IsOfficialEntrance' in device_attrs.columns:
                        # FIXED: Proper boolean filtering
                        entrance_mask = device_attrs['IsOfficialEntrance'] == True
                        entrance_devices = device_attrs[entrance_mask]['DoorID'].tolist()
                    
                    if entrance_devices:  # FIXED: Check if list is not empty
                        entrance_events = len(df[df[self.DOORID_COL_DISPLAY].isin(entrance_devices)])
                        total_events = len(df)
                        
                        if total_events > 0:
                            entrance_ratio = (entrance_events / total_events) * 100
                            entry_exit_ratio = f"Entry/Exit: {entrance_ratio:.1f}%"
        
        return (
            # Original outputs
            graph_elements, "Enhanced analytics generated successfully!", 
            show_style, show_stats_style, show_style,
            
            # Enhanced statistics
            str(metrics.get('total_events', '0')),
            metrics.get('date_range', 'N/A'),
            metrics.get('avg_events_per_day', 'N/A'),
            metrics.get('peak_activity_day', 'N/A'),
            
            # User analytics
            f"Users: {metrics.get('unique_users', 0)}",
            metrics.get('avg_events_per_user', 'N/A'),
            metrics.get('most_active_user', 'N/A'),
            metrics.get('avg_users_per_device', 'N/A'),
            metrics.get('peak_hour', 'N/A'),
            
            # Device analytics
            metrics.get('total_devices_count', '0 devices'),
            metrics.get('entrance_devices_count', '0 entrances'),
            metrics.get('high_security_devices', '0 high security'),
            self._format_active_devices_table(metrics),
            
            # Peak activity
            metrics.get('peak_hour', 'N/A'),
            metrics.get('peak_day', 'N/A'),
            metrics.get('busiest_floor', 'N/A'),
            entry_exit_ratio,
            weekend_analysis,
            
            # Security overview
            security_breakdown,
            f"Score: {metrics.get('security_score', 'N/A')}",
            f"{metrics.get('anomaly_count', 0)} detected",
            
            # Analytics insights
            metrics.get('traffic_pattern', 'No Data'),
            metrics.get('security_score', 'N/A'),
            metrics.get('efficiency_score', 'N/A'),
            str(metrics.get('anomaly_count', 0)),
            
            # Charts
            main_chart, security_chart, heatmap_chart,
            
            # Storage
            json.dumps(all_manual_classifications) if all_manual_classifications else no_update,
            stored_column_mapping_json
        )
    
    def _format_active_devices_table(self, metrics: Dict[str, Any]) -> List[html.Tr]:
        """Format active devices table from metrics - FIXED"""
        # Extract top devices from enriched data if available
        if self.data_cache['enriched_df'] is not None and not self.data_cache['enriched_df'].empty:
            try:
                device_counts = self.data_cache['enriched_df'][self.DOORID_COL_DISPLAY].value_counts().head(5)
                
                table_rows = []
                for device, count in device_counts.items():
                    device_str = str(device)
                    device_display = device_str[:15] + "..." if len(device_str) > 15 else device_str
                    table_rows.append(
                        html.Tr([
                            html.Td(device_display),
                            html.Td(f"{count:,}", style={'textAlign': 'right'})
                        ])
                    )
                
                return table_rows
            except Exception as e:
                return [html.Tr([html.Td(f"Error: {str(e)}", colSpan=2)])]
        
        return [html.Tr([html.Td("N/A", colSpan=2)])]
    
    def _create_error_response(self, error_msg: str, hide_style: Dict[str, str], 
                              stored_column_mapping_json: str) -> Tuple[Any, ...]:
        """Create comprehensive error response - FIXED"""
        empty_fig = self._create_empty_figure("Error: No data to display")
        
        return (
            # Original outputs
            [], f"Error: {error_msg}", hide_style, hide_style, hide_style,
            
            # Enhanced statistics
            "0", "Error", "Error", "Error",
            
            # User analytics  
            "Error", "Error", "Error", "Error", "Error",
            
            # Device analytics
            "Error", "Error", "Error", [html.Tr([html.Td("Error", colSpan=2)])],
            
            # Peak activity
            "Error", "Error", "Error", "Error", "Error",
            
            # Security overview
            [html.P("Error loading security data", style={'color': '#E02020'})], "Error", "Error",
            
            # Analytics insights
            "Error", "Error", "Error", "Error",
            
            # Charts
            empty_fig, empty_fig, empty_fig,
            
            # Storage
            no_update, stored_column_mapping_json
        )
    
    # Keep original methods for compatibility (simplified versions for brevity)
    def _process_classifications(self, manual_map_choice, all_door_ids_from_store, floor_values, floor_ids,
                                is_ee_values, is_ee_ids, is_stair_values, is_stair_ids,
                                security_slider_values, security_slider_ids, csv_headers, existing_saved_classifications_json):
        """Process door classifications from form inputs (unchanged implementation)"""
        
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
            floor_map = {f_id['index']: f_val for f_id, f_val in zip(floor_ids or [], floor_values or [])}
            is_ee_map = {ee_id['index']: 'is_ee' in (ee_val or []) for ee_id, ee_val in zip(is_ee_ids or [], is_ee_values or [])}
            is_stair_map = {st_id['index']: 'is_stair' in (st_val or []) for st_id, st_val in zip(is_stair_ids or [], is_stair_values or [])}
            
            security_map_slider_to_value = {
                s_id['index']: security_levels_map.get(s_val, {}).get("value", "unclassified")
                for s_id, s_val in zip(security_slider_ids or [], security_slider_values or [])
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
        """Process CSV data for onion model (unchanged implementation)"""
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
        """Run the onion model processing (enhanced)"""
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
                
                return {
                    'success': True,
                    'graph_elements': graph_elements,
                    'enriched_df': enriched_df,
                    'device_attrs': device_attrs,
                    'path_viz': path_viz,
                    'all_paths': all_paths
                }
            else:
                return {'success': False, 'error': "Error in processing: incomplete result."}
                
        except Exception as e:
            return {'success': False, 'error': str(e)}


# Factory function for easy handler creation
def create_enhanced_graph_handlers(app):
    """Factory function to create enhanced graph handlers"""
    return EnhancedGraphHandlers(app)

# Backward compatibility
def create_graph_handlers(app):
    """Backward compatibility alias"""
    return EnhancedGraphHandlers(app)