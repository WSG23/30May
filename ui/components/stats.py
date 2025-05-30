# ui/components/stats.py
"""
Statistics component for data overview and metrics display
Extracted from core_layout.py and graph_callbacks.py
"""

from dash import html
from styles.style_config import COLORS, UI_VISIBILITY


class StatsComponent:
    """Centralized statistics component with all metrics and data display"""
    
    def __init__(self):
        self.panel_style_base = {
            'flex': '1',
            'padding': '20px',
            'margin': '0 10px',
            'backgroundColor': COLORS['surface'],
            'borderRadius': '8px',
            'textAlign': 'center',
            'boxShadow': '2px 2px 5px rgba(0,0,0,0.2)'
        }
    
    def create_stats_container(self):
        """Creates the complete statistics panels container"""
        return html.Div(
            id='stats-panels-container',
            style=UI_VISIBILITY['show_flex_stats'],
            children=[
                self.create_access_events_panel(),
                self.create_statistics_panel(),
                self.create_active_devices_panel()
            ]
        )
    
    def create_custom_header(self, main_logo_path):
        """Creates the custom header shown after processing - matches Analytics Dashboard exactly"""
        return html.Div(
            id='yosai-custom-header',
            style=UI_VISIBILITY['show_header'],
            children=[
                html.Div([
                    # Logo matching the top header exactly
                    html.Img(
                        src=main_logo_path, 
                        style={
                            'height': '24px',        # Same height as Analytics Dashboard logo
                            'marginRight': '10px',   # Same spacing as top header
                            'verticalAlign': 'middle'
                        }
                    ),
                    # Data Overview text matching Analytics Dashboard style
                    html.Span(
                        "Data Overview",
                        style={
                            'fontSize': '18px',      # Same font size as "Analytics Dashboard"
                            'fontWeight': '400',     # Same font weight (normal)
                            'color': '#ffffff',      # Same white color
                            'fontFamily': 'system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
                            'verticalAlign': 'middle'
                        }
                    )
                ], style={
                    'display': 'flex',
                    'alignItems': 'center',
                    'justifyContent': 'center',  # Center horizontally like Analytics Dashboard
                    'padding': '16px 0',         # Same padding as top header
                    'margin': '0'
                })
            ]
        )
    
    def create_access_events_panel(self):
        """Creates the access events statistics panel"""
        panel_style = self.panel_style_base.copy()
        panel_style['borderLeft'] = f'5px solid {COLORS["accent"]}'
        
        return html.Div([
            html.H3("Access events", style={'color': COLORS['text_primary']}),
            html.H1(id="total-access-events-H1", style={'color': COLORS['text_primary']}),
            html.P(id="event-date-range-P", style={'color': COLORS['text_secondary']})
        ], style=panel_style)
    
    def create_statistics_panel(self):
        """Creates the general statistics panel"""
        panel_style = self.panel_style_base.copy()
        panel_style['borderLeft'] = f'5px solid {COLORS["warning"]}'
        
        return html.Div([
            html.H3("Statistics", style={'color': COLORS['text_primary']}),
            html.P(id="stats-date-range-P", style={'color': COLORS['text_secondary']}),
            html.P(id="stats-days-with-data-P", style={'color': COLORS['text_secondary']}),
            html.P(id="stats-num-devices-P", style={'color': COLORS['text_secondary']}),
            html.P(id="stats-unique-tokens-P", style={'color': COLORS['text_secondary']})
        ], style=panel_style)
    
    def create_active_devices_panel(self):
        """Creates the most active devices panel"""
        panel_style = self.panel_style_base.copy()
        panel_style['borderLeft'] = f'5px solid {COLORS["critical"]}'
        
        return html.Div([
            html.H3("Most active devices", style={'color': COLORS['text_primary']}),
            html.Table([
                html.Thead(html.Tr([
                    html.Th("DEVICE", style={'color': COLORS['text_primary']}),
                    html.Th("EVENTS", style={'color': COLORS['text_primary']})
                ])),
                html.Tbody(id='most-active-devices-table-body')
            ])
        ], style=panel_style)
    
    def create_enhanced_stats_panel(self):
        """Creates an enhanced statistics panel with more metrics"""
        return html.Div([
            html.H4("Enhanced Analytics", style={'color': COLORS['text_primary'], 'marginBottom': '15px'}),
            
            # Key Metrics Row
            html.Div([
                self.create_metric_card("Unique Users", "unique-users-metric", COLORS['success']),
                self.create_metric_card("Peak Hour", "peak-hour-metric", COLORS['warning']),
                self.create_metric_card("Avg. Daily Events", "avg-daily-events-metric", COLORS['accent'])
            ], style={'display': 'flex', 'justifyContent': 'space-between', 'marginBottom': '20px'}),
            
            # Security Breakdown
            html.Div([
                html.H5("Security Level Distribution", style={'color': COLORS['text_primary']}),
                html.Div(id='security-distribution-chart')
            ], style={'marginBottom': '20px'}),
            
            # Access Patterns
            html.Div([
                html.H5("Access Patterns", style={'color': COLORS['text_primary']}),
                html.Div(id='access-patterns-summary')
            ])
            
        ], style={
            'padding': '20px',
            'backgroundColor': COLORS['surface'],
            'borderRadius': '8px',
            'border': f'1px solid {COLORS["border"]}',
            'margin': '20px 0'
        })
    
    def create_metric_card(self, title, metric_id, color):
        """Creates a single metric card"""
        return html.Div([
            html.H6(title, style={'color': COLORS['text_secondary'], 'margin': '0', 'fontSize': '0.9em'}),
            html.H3(id=metric_id, style={'color': color, 'margin': '5px 0'})
        ], style={
            'padding': '15px',
            'backgroundColor': COLORS['background'],
            'borderRadius': '6px',
            'border': f'1px solid {color}',
            'textAlign': 'center',
            'flex': '1',
            'margin': '0 5px'
        })
    
    def create_classification_summary_panel(self):
        """Creates a summary panel for door classifications"""
        return html.Div([
            html.H4("Door Classification Summary", style={'color': COLORS['text_primary']}),
            html.Div(id='classification-summary-content', children=[
                html.P("No classification data available", style={'color': COLORS['text_secondary']})
            ])
        ], style={
            'padding': '20px',
            'backgroundColor': COLORS['surface'],
            'borderRadius': '8px',
            'border': f'1px solid {COLORS["border"]}',
            'margin': '20px 0'
        })
    
    def format_access_events_data(self, total_events, date_range=None):
        """Formats access events data for display"""
        return {
            'total': f"{total_events:,}",
            'date_range': date_range or "N/A"
        }
    
    def format_statistics_data(self, stats_dict):
        """Formats general statistics data for display"""
        return {
            'date_range': f"Date range: {stats_dict.get('date_range', 'N/A')}",
            'days_with_data': f"Days: {stats_dict.get('days', 'N/A')}",
            'num_devices': f"Devices: {stats_dict.get('devices', 'N/A')}",
            'unique_tokens': f"Tokens: {stats_dict.get('tokens', 'N/A')}"
        }
    
    def format_active_devices_table(self, device_counts):
        """Formats active devices data for table display"""
        if not device_counts:
            return [html.Tr([html.Td("N/A", colSpan=2)])]
        
        table_rows = []
        for device, count in device_counts.items():
            table_rows.append(
                html.Tr([
                    html.Td(device),
                    html.Td(f"{count:,}", style={'textAlign': 'right'})
                ])
            )
        
        return table_rows
    
    def create_security_distribution_chart(self, security_counts):
        """Creates a simple security distribution display"""
        if not security_counts:
            return html.P("No security data available", style={'color': COLORS['text_secondary']})
        
        total = sum(security_counts.values())
        if total == 0:
            return html.P("No security data available", style={'color': COLORS['text_secondary']})
        
        distribution_items = []
        colors = {
            'green': COLORS['success'],
            'yellow': COLORS['warning'],
            'red': COLORS['critical'],
            'unclassified': COLORS['border']
        }
        
        for level, count in security_counts.items():
            percentage = (count / total) * 100
            color = colors.get(level, COLORS['text_secondary'])
            
            distribution_items.append(
                html.Div([
                    html.Span(f"{level.title()}: ", style={'color': COLORS['text_primary']}),
                    html.Span(f"{count} ({percentage:.1f}%)", style={'color': color, 'fontWeight': 'bold'})
                ], style={'marginBottom': '5px'})
            )
        
        return html.Div(distribution_items)
    
    def create_access_patterns_summary(self, patterns_data):
        """Creates access patterns summary"""
        if not patterns_data:
            return html.P("No pattern data available", style={'color': COLORS['text_secondary']})
        
        return html.Div([
            html.P(f"Peak access time: {patterns_data.get('peak_hour', 'N/A')}", 
                   style={'color': COLORS['text_secondary']}),
            html.P(f"Most common path: {patterns_data.get('common_path', 'N/A')}", 
                   style={'color': COLORS['text_secondary']}),
            html.P(f"Average session length: {patterns_data.get('avg_session', 'N/A')}", 
                   style={'color': COLORS['text_secondary']})
        ])
    
    def get_default_stats_values(self):
        """Returns default values for all statistics"""
        return {
            'total_access_events': "0",
            'event_date_range': "N/A",
            'stats_date_range': "N/A",
            'stats_days_with_data': "0",
            'stats_num_devices': "0",
            'stats_unique_tokens': "0",
            'most_active_devices_table': [html.Tr([html.Td("N/A", colSpan=2)])]
        }
    
    def process_dataframe_for_stats(self, df, device_attrs=None):
        """Processes DataFrame to extract statistics"""
        if df is None or df.empty:
            return self.get_default_stats_values()
        
        # This would contain the logic to extract stats from the DataFrame
        # For now, return default values as the actual processing is in the callbacks
        return self.get_default_stats_values()


class StatsDataProcessor:
    """Processes data for statistics display"""
    
    def __init__(self):
        self.stats_component = StatsComponent()
    
    def extract_basic_stats(self, enriched_df, device_attrs_df=None):
        """Extracts basic statistics from processed data"""
        if enriched_df is None or enriched_df.empty:
            return self.stats_component.get_default_stats_values()
        
        # Extract date range
        timestamp_col = 'Timestamp (Event Time)'  # Use display name
        if timestamp_col in enriched_df.columns:
            min_date = enriched_df[timestamp_col].min()
            max_date = enriched_df[timestamp_col].max()
            date_range = f"{min_date.strftime('%d.%m.%Y')} - {max_date.strftime('%d.%m.%Y')}"
            days_count = enriched_df[timestamp_col].dt.date.nunique()
        else:
            date_range = "N/A"
            days_count = 0
        
        # Extract device and user counts
        door_col = 'DoorID (Device Name)'  # Use display name
        user_col = 'UserID (Person Identifier)'  # Use display name
        
        device_count = enriched_df[door_col].nunique() if door_col in enriched_df.columns else 0
        user_count = enriched_df[user_col].nunique() if user_col in enriched_df.columns else 0
        
        # Get most active devices
        if door_col in enriched_df.columns:
            device_counts = enriched_df[door_col].value_counts().nlargest(5).to_dict()
        else:
            device_counts = {}
        
        return {
            'total_events': len(enriched_df),
            'date_range': date_range,
            'days_with_data': days_count,
            'num_devices': device_count,
            'unique_tokens': user_count,
            'device_counts': device_counts
        }
    
    def calculate_enhanced_metrics(self, enriched_df):
        """Calculates enhanced metrics for display"""
        if enriched_df is None or enriched_df.empty:
            return {}
        
        # Calculate additional metrics here
        # This is a placeholder for more complex analytics
        return {
            'avg_daily_events': 0,
            'peak_hour': 'N/A',
            'access_patterns': {}
        }


# Factory functions for easy component creation
def create_stats_component():
    """Factory function to create stats component instance"""
    return StatsComponent()

def create_stats_data_processor():
    """Factory function to create stats data processor instance"""
    return StatsDataProcessor()

# Convenience functions for individual elements (backward compatibility)
def create_stats_container():
    """Create the stats container"""
    component = StatsComponent()
    return component.create_stats_container()

def create_custom_header(main_logo_path):
    """Create the custom header"""
    component = StatsComponent()
    return component.create_custom_header(main_logo_path)