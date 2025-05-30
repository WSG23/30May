# config/ui_config.py
"""
UI and styling configuration
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional

@dataclass
class UIConfig:
    """UI configuration and styling"""
    
    # Color palette
    colors: Optional[Dict[str, str]] = None    
    # Animation settings
    animations: Optional[Dict[str, str]] = None

    # Typography
    typography: Optional[Dict[str, str]] = None    
    # Component visibility
    ui_visibility: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.colors is None:
            self.colors = {
                'primary': '#1B2A47',
                'accent': '#2196F3',
                'accent_light': '#42A5F5',
                'success': '#2DBE6C',
                'warning': '#FFB020',
                'critical': '#E02020',
                'info': '#2196F3',
                'background': '#0F1419',
                'surface': '#1A2332',
                'border': '#2D3748',
                'text_primary': '#F7FAFC',
                'text_secondary': '#E2E8F0',
                'text_tertiary': '#A0AEC0',
            }
            
        if self.animations is None:
            self.animations = {
                'fast': '0.15s',
                'normal': '0.3s',
                'slow': '0.5s'
            }
            
        if self.typography is None:
            self.typography = {
                'text_xs': '0.75rem',
                'text_sm': '0.875rem',
                'text_base': '1rem',
                'text_lg': '1.125rem',
                'text_xl': '1.25rem',
                'text_2xl': '1.5rem',
                'text_3xl': '1.875rem',
                'font_light': '300',
                'font_normal': '400',
                'font_medium': '500',
                'font_semibold': '600',
                'font_bold': '700',
            }
            
        if self.ui_visibility is None:
            self.ui_visibility = {
                'show_upload_section': True,
                'show_mapping_section': True,
                'show_classification_section': True,
                'show_graph_section': True,
                'show_stats_section': True,
                'show_debug_info': False,
                'hide': {'display': 'none'},
                'show_block': {'display': 'block'},
                'show_flex': {'display': 'flex'},
            }

def get_ui_config() -> UIConfig:
    """Get UI configuration"""
    return UIConfig()
