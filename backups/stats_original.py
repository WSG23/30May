# ui/components/stats.py - DEEP CACHE CLEAR FIX
"""
Statistics component - DEEP CACHE CLEAR to eliminate all persistent data
"""

from dash import html
from ui.themes.style_config import COLORS, UI_VISIBILITY


class StatsComponent:
    """Enhanced statistics component with additional metrics - DEEP CACHE CLEAR"""
    
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
        
        # ADD: Clear any cached state
        self._clear_all_cache()
    
    def _clear_all_cache(self):
        """Clear all cached data"""
        # Clear any instance variables that might cache data
        if hasattr(self, '_cached_stats'):
            delattr(self, '_cached_stats')
        if hasattr(self, '_last_result'):
            delattr(self, '_last_result')
    
    def create_statistics_panel(self):
        """Creates the enhanced general statistics panel with new metrics"""
        panel_style = self.panel_style_base.copy()
        panel_style['borderLeft'] = f'5px solid {COLORS["warning"]}'
        
        return html.Div([
            html.H3("Statistics", style={'color': COLORS['text_primary']}),
            
            # Existing stats
            html.P(id="stats-date-range-P", style={'color': COLORS['text_secondary']}),
            html.P(id="stats-days-with-data-P", style={'color': COLORS['text_secondary']}),
            html.P(id="stats-num-devices-P", style={'color': COLORS['text_secondary']}),
            html.P(id="stats-unique-tokens-P", style={'color': COLORS['text_secondary']}),
            
            # NEW ENHANCED STATS
            html.Hr(style={'borderColor': COLORS['border'], 'margin': '15px 0'}),
            
            # Non-Access Events (renamed from original "Unique Tokens")
            html.P(id="stats-non-access-events-P", style={
                'color': COLORS['accent'], 
                'fontWeight': '600',
                'fontSize': '0.95rem'
            }),
            
            # Duplicate Events
            html.P(id="stats-duplicate-events-P", style={
                'color': COLORS['warning'], 
                'fontWeight': '600',
                'fontSize': '0.95rem'
            }),
            
            # Uncommon Events (placeholder)
            html.P(id="stats-uncommon-events-P", style={
                'color': COLORS['critical'], 
                'fontWeight': '600',
                'fontSize': '0.95rem'
            })
            
        ], style=panel_style)
    
    def create_stats_container(self):
        """Creates the complete statistics panels container with enhanced stats"""
        return html.Div(
            id='stats-panels-container',
            style=UI_VISIBILITY['show_flex_stats'],
            children=[
                self.create_access_events_panel(),
                self.create_statistics_panel(),  # Enhanced version
                self.create_active_devices_panel()
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
    
    def create_custom_header(self, main_logo_path):
        """Creates the custom header shown after processing"""
        return html.Div(
            id='yosai-custom-header',
            style=UI_VISIBILITY['show_header'],
            children=[
                html.Div([
                    html.Img(
                        src=main_logo_path, 
                        style={
                            'height': '24px',
                            'marginRight': '10px',
                            'verticalAlign': 'middle'
                        }
                    ),
                    html.Span(
                        "Data Overview",
                        style={
                            'fontSize': '18px',
                            'fontWeight': '400',
                            'color': '#ffffff',
                            'fontFamily': 'system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
                            'verticalAlign': 'middle'
                        }
                    )
                ], style={
                    'display': 'flex',
                    'alignItems': 'center',
                    'justifyContent': 'center',
                    'padding': '16px 0',
                    'margin': '0'
                })
            ]
        )
    
    def get_default_stats_values(self):
        """Returns default values for all statistics including new ones"""
        return {
            'total_access_events': "0",
            'event_date_range': "N/A",
            'stats_date_range': "N/A",
            'stats_days_with_data': "0",
            'stats_num_devices': "0",
            'stats_unique_tokens': "0",
            'most_active_devices_table': [html.Tr([html.Td("N/A", colSpan=2)])],
            
            # NEW ENHANCED STATS DEFAULTS
            'stats_non_access_events': "Non-Access: 0 (0%)",
            'stats_duplicate_events': "Duplicates: 0 (0%)", 
            'stats_uncommon_events': "Uncommon: 0 (0%)"
        }
    
    def format_enhanced_statistics_data(self, stats_dict):
        """DEEP CACHE CLEAR: Formats enhanced statistics data for display"""
        
        print("🔍 DEEP DEBUG - format_enhanced_statistics_data called with:")
        print(f"   stats_dict keys: {list(stats_dict.keys()) if stats_dict else 'None'}")
        for key, value in (stats_dict or {}).items():
            print(f"   {key}: {value}")
        
        # FORCE FRESH CALCULATION - no caching
        total_events = int(stats_dict.get('total_events', 0))
        original_total = int(stats_dict.get('original_total', 0))
        non_access_count = int(stats_dict.get('non_access_events', 0))
        duplicate_count = int(stats_dict.get('duplicate_events', 0))
        uncommon_count = int(stats_dict.get('uncommon_events', 0))
        
        print(f"🔍 DEEP DEBUG - EXTRACTED VALUES:")
        print(f"   total_events: {total_events}")
        print(f"   original_total: {original_total}")
        print(f"   non_access_count: {non_access_count}")
        print(f"   duplicate_count: {duplicate_count}")
        print(f"   uncommon_count: {uncommon_count}")
        
        # FIXED CALCULATION: Use original_total as denominator for non-access percentage
        if original_total > 0:
            non_access_pct = (non_access_count / original_total) * 100
        else:
            non_access_pct = 0
            
        # For other percentages, use total_events (the cleaned data count)
        if total_events > 0:
            duplicate_pct = (duplicate_count / total_events) * 100
            uncommon_pct = (uncommon_count / total_events) * 100
        else:
            duplicate_pct = 0
            uncommon_pct = 0
        
        print(f"🔍 DEEP DEBUG - CALCULATED PERCENTAGES:")
        print(f"   non_access_pct: {non_access_pct:.1f}%")
        print(f"   duplicate_pct: {duplicate_pct:.1f}%")
        print(f"   uncommon_pct: {uncommon_pct:.1f}%")
        
        # FORCE FRESH FORMATTING - no cached strings
        result = {
            'date_range': f"Date range: {stats_dict.get('date_range', 'N/A')}",
            'days_with_data': f"Days: {stats_dict.get('days', 'N/A')}",
            'num_devices': f"Devices: {stats_dict.get('devices', 'N/A')}",
            'unique_tokens': f"Users: {stats_dict.get('tokens', 'N/A')}",
            
            # FORCE FRESH FORMATTED STATS - recalculate every time
            'non_access_events': f"Non-Access: {non_access_count:,} ({non_access_pct:.1f}%)",
            'duplicate_events': f"Duplicates: {duplicate_count:,} ({duplicate_pct:.1f}%)",
            'uncommon_events': f"Uncommon: {uncommon_count:,} ({uncommon_pct:.1f}%)"
        }
        
        print(f"🔍 DEEP DEBUG - FINAL RESULT:")
        for key, value in result.items():
            print(f"   {key}: {value}")
        
        return result


class DeepCacheClearStatsDataProcessor:
    """DEEP CACHE CLEAR data processor - eliminates all persistent state"""
    
    def __init__(self):
        self.stats_component = StatsComponent()
        # FORCE: Clear any cached state
        self._clear_all_processor_cache()
    
    def _clear_all_processor_cache(self):
        """Deep clear all processor cache"""
        print("🧹 DEEP CACHE CLEAR: Clearing all processor cache...")
        # Clear any instance variables that might persist data
        for attr in list(self.__dict__.keys()):
            if attr.startswith('_cache') or attr.startswith('_last') or attr.startswith('_previous'):
                delattr(self, attr)
                print(f"   Cleared cached attribute: {attr}")
    
    def extract_enhanced_stats(self, enriched_df, original_df=None, processing_info=None):
        """DEEP CACHE CLEAR: Extracts enhanced statistics with ZERO caching"""
        
        print("🔍 DEEP DEBUG - extract_enhanced_stats called")
        print(f"   enriched_df: {type(enriched_df)} with {len(enriched_df) if enriched_df is not None else 0} rows")
        print(f"   original_df: {type(original_df)} with {len(original_df) if original_df is not None else 0} rows")
        print(f"   processing_info: {processing_info}")
        
        # FORCE: Clear any cached state before processing
        self._clear_all_processor_cache()
        
        if enriched_df is None or enriched_df.empty:
            print("🔍 DEEP DEBUG - No enriched data, returning defaults")
            return self.stats_component.get_default_stats_values()
        
        # Import constants properly
        try:
            from utils.constants import REQUIRED_INTERNAL_COLUMNS
        except ImportError:
            try:
                from config.settings import REQUIRED_INTERNAL_COLUMNS
            except ImportError:
                # Fallback
                REQUIRED_INTERNAL_COLUMNS = {
                    'Timestamp': 'Timestamp (Event Time)',
                    'UserID': 'UserID (Person Identifier)',
                    'DoorID': 'DoorID (Device Name)',
                    'EventType': 'EventType (Access Result)'
                }
        
        # Get column names using display names
        timestamp_col = REQUIRED_INTERNAL_COLUMNS['Timestamp']
        door_col = REQUIRED_INTERNAL_COLUMNS['DoorID'] 
        user_col = REQUIRED_INTERNAL_COLUMNS['UserID']
        eventtype_col = REQUIRED_INTERNAL_COLUMNS['EventType']
        
        print(f"🔍 DEEP DEBUG - Using columns:")
        print(f"   timestamp_col: '{timestamp_col}'")
        print(f"   door_col: '{door_col}'")
        print(f"   user_col: '{user_col}'")
        print(f"   eventtype_col: '{eventtype_col}'")
        print(f"   enriched_df.columns: {list(enriched_df.columns)}")
        
        # FORCE FRESH CALCULATION - Basic stats from CURRENT enriched data only
        total_events = len(enriched_df)  # Count from current processed data
        
        # FORCE FRESH COUNT from original data - NO CACHING
        if original_df is not None and not original_df.empty:
            original_total = len(original_df)  # Count from current original data
            print(f"🔍 DEEP DEBUG - FRESH original_total calculated: {original_total}")
        else:
            original_total = total_events
            print(f"🔍 DEEP DEBUG - No original data, using total_events: {original_total}")
        
        print(f"🔍 DEEP DEBUG - FRESH COUNTS:")
        print(f"   total_events (processed): {total_events}")
        print(f"   original_total (raw CSV): {original_total}")
        
        # Extract date range - FRESH calculation
        if timestamp_col in enriched_df.columns:
            try:
                min_date = enriched_df[timestamp_col].min()
                max_date = enriched_df[timestamp_col].max()
                date_range = f"{min_date.strftime('%d.%m.%Y')} - {max_date.strftime('%d.%m.%Y')}"
                days_count = enriched_df[timestamp_col].dt.date.nunique()
                print(f"🔍 DEEP DEBUG - Date range calculated: {date_range}, days: {days_count}")
            except Exception as e:
                print(f"🔍 DEEP DEBUG - Error processing timestamp: {e}")
                date_range = "N/A"
                days_count = 0
        else:
            print(f"🔍 DEEP DEBUG - Timestamp column '{timestamp_col}' not found")
            date_range = "N/A"
            days_count = 0
        
        # Device and user counts - FRESH calculation
        device_count = enriched_df[door_col].nunique() if door_col in enriched_df.columns else 0
        user_count = enriched_df[user_col].nunique() if user_col in enriched_df.columns else 0
        
        print(f"🔍 DEEP DEBUG - FRESH device/user counts:")
        print(f"   device_count: {device_count}")
        print(f"   user_count: {user_count}")
        
        # Most active devices - FRESH calculation
        if door_col in enriched_df.columns:
            device_counts = enriched_df[door_col].value_counts().nlargest(5).to_dict()
        else:
            device_counts = {}
        
        # DEEP CACHE CLEAR ENHANCED CALCULATIONS - FORCE FRESH
        
        # 1. Non-Access Events Count - FORCE FRESH calculation
        non_access_events = self._calculate_non_access_events_deep_clear(original_total, total_events)
        
        # 2. Duplicate Events Count - placeholder
        duplicate_events = 0  # Placeholder for now
        
        # 3. Uncommon Events Count - FRESH calculation
        uncommon_events = self._calculate_uncommon_events_deep_clear(enriched_df, timestamp_col)
        
        print(f"🔍 DEEP DEBUG - FINAL enhanced stats calculated:")
        print(f"   non_access_events: {non_access_events}")
        print(f"   duplicate_events: {duplicate_events}")
        print(f"   uncommon_events: {uncommon_events}")
        
        # FORCE FRESH RESULT - no caching of the return value
        result = {
            'total_events': total_events,           # Processed data count (for display in main panel)
            'original_total': original_total,       # Original CSV count (for percentage calculation)
            'date_range': date_range,
            'days': days_count,
            'devices': device_count,
            'tokens': user_count,
            'device_counts': device_counts,
            
            # NEW ENHANCED STATS - FORCE FRESH
            'non_access_events': non_access_events,
            'duplicate_events': duplicate_events, 
            'uncommon_events': uncommon_events
        }
        
        print(f"🔍 DEEP DEBUG - FINAL RESULT to return:")
        for key, value in result.items():
            print(f"   {key}: {value}")
        
        return result
    
    def _calculate_non_access_events_deep_clear(self, original_total, processed_total):
        """DEEP CACHE CLEAR: Calculate non-access events with forced fresh calculation"""
        
        print(f"🔍 DEEP DEBUG - _calculate_non_access_events_deep_clear:")
        print(f"   INPUT original_total: {original_total} (type: {type(original_total)})")
        print(f"   INPUT processed_total: {processed_total} (type: {type(processed_total)})")
        
        # FORCE FRESH CONVERSION - ensure we're working with fresh integers
        original_fresh = int(original_total)
        processed_fresh = int(processed_total)
        
        print(f"   FRESH original_fresh: {original_fresh}")
        print(f"   FRESH processed_fresh: {processed_fresh}")
        
        # Non-access events = events that were filtered out during processing
        if original_fresh > processed_fresh:
            non_access_count = original_fresh - processed_fresh
            print(f"   CALCULATED non_access_count: {original_fresh} - {processed_fresh} = {non_access_count}")
            return non_access_count
        else:
            # If original <= processed, something's wrong with our data flow
            print(f"   WARNING: original ({original_fresh}) <= processed ({processed_fresh})")
            return 0
    
    def _calculate_uncommon_events_deep_clear(self, enriched_df, timestamp_col):
        """DEEP CACHE CLEAR: Calculate uncommon/unusual events"""
        
        if enriched_df.empty or timestamp_col not in enriched_df.columns:
            return 0
        
        try:
            # Simple definition: events outside business hours (6 AM - 6 PM)
            after_hours_mask = (
                (enriched_df[timestamp_col].dt.hour < 6) | 
                (enriched_df[timestamp_col].dt.hour >= 18)
            )
            uncommon_count = int(after_hours_mask.sum())  # Force fresh int conversion
            print(f"🔍 DEEP DEBUG - Uncommon events (after hours): {uncommon_count}")
            return uncommon_count
            
        except Exception as e:
            print(f"🔍 DEEP DEBUG - Error calculating uncommon events: {e}")
            return 0


# Factory functions for easy component creation
def create_enhanced_stats_component():
    """Factory function to create DEEP CACHE CLEAR enhanced stats component instance"""
    return StatsComponent()

def create_enhanced_stats_data_processor():
    """Factory function to create DEEP CACHE CLEAR enhanced stats data processor instance"""
    return DeepCacheClearStatsDataProcessor()

# Convenience functions for backward compatibility
def create_stats_component():
    """Create the stats component"""
    return StatsComponent()

def create_stats_data_processor():
    """Create the stats data processor"""
    return DeepCacheClearStatsDataProcessor()

def create_stats_container():
    """Create the stats container"""
    component = StatsComponent()
    return component.create_stats_container()

def create_custom_header(main_logo_path):
    """Create the custom header"""
    component = StatsComponent()
    return component.create_custom_header(main_logo_path)