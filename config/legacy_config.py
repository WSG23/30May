# config/__init__.py
"""
Unified configuration package for Yōsai Intel application
"""

from .app_config import AppConfig, get_config
from .ui_config import UIConfig, get_ui_config
from .processing_config import ProcessingConfig, get_processing_config
from .constants import (
    REQUIRED_INTERNAL_COLUMNS,
    SECURITY_LEVELS,
    DEFAULT_ICONS,
    FILE_LIMITS
)

__all__ = [
    'AppConfig',
    'UIConfig', 
    'ProcessingConfig',
    'get_config',
    'get_ui_config',
    'get_processing_config',
    'REQUIRED_INTERNAL_COLUMNS',
    'SECURITY_LEVELS',
    'DEFAULT_ICONS',
    'FILE_LIMITS'
]

# config/constants.py
"""
Shared constants for the application
"""

# Column mapping constants
REQUIRED_INTERNAL_COLUMNS = {
    'Timestamp': 'Timestamp (Event Time)',
    'UserID': 'UserID (Person Identifier)',
    'DoorID': 'DoorID (Device Name)',
    'EventType': 'EventType (Access Result)'
}

# Security level configuration
SECURITY_LEVELS = {
    0: {"label": "⬜️ Unclassified", "color": "#2D3748", "value": "unclassified"},
    1: {"label": "🟢 Green (Public)", "color": "#2DBE6C", "value": "green"},
    2: {"label": "🟠 Orange (Semi-Restricted)", "color": "#FFB020", "value": "yellow"},
    3: {"label": "🔴 Red (Restricted)", "color": "#E02020", "value": "red"},
}

# Default icon configuration
DEFAULT_ICONS = {
    'upload_default': '/assets/upload_file_csv_icon.png',
    'upload_success': '/assets/upload_file_csv_icon_success.png',
    'upload_fail': '/assets/upload_file_csv_icon_fail.png',
    'main_logo': '/assets/logo_white.png'
}

# File processing limits
FILE_LIMITS = {
    'max_file_size': 10 * 1024 * 1024,  # 10MB
    'max_rows': 1_000_000,
    'allowed_extensions': ['.csv'],
    'encoding': 'utf-8'
}

# config/app_config.py
"""
Main application configuration
"""

import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class AppConfig:
    """Main application configuration"""
    debug: bool = False
    port: int = 8050
    host: str = '127.0.0.1'
    suppress_callback_exceptions: bool = True
    assets_folder: str = 'assets'
    
    # Security settings
    secret_key: Optional[str] = None
    csrf_protection: bool = False
    
    # Performance settings
    cache_timeout: int = 3600
    max_workers: int = 4
    
    # Logging settings
    log_level: str = 'INFO'
    log_file: Optional[str] = None
    
    @classmethod
    def from_env(cls) -> 'AppConfig':
        """Create configuration from environment variables"""
        return cls(
            debug=os.getenv('DEBUG', 'False').lower() == 'true',
            port=int(os.getenv('PORT', '8050')),
            host=os.getenv('HOST', '127.0.0.1'),
            secret_key=os.getenv('SECRET_KEY'),
            cache_timeout=int(os.getenv('CACHE_TIMEOUT', '3600')),
            max_workers=int(os.getenv('MAX_WORKERS', '4')),
            log_level=os.getenv('LOG_LEVEL', 'INFO'),
            log_file=os.getenv('LOG_FILE')
        )

def get_config() -> AppConfig:
    """Get application configuration"""
    return AppConfig.from_env()

# config/ui_config.py
"""
UI and styling configuration
"""

from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class UIConfig:
    """UI configuration and styling"""
    
    # Color palette
    colors: Dict[str, str] = None
    
    # Animation settings
    animations: Dict[str, str] = None
    
    # Typography
    typography: Dict[str, str] = None
    
    # Component visibility
    ui_visibility: Dict[str, Any] = None
    
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

# config/processing_config.py
"""
Data processing configuration
"""

from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class ProcessingConfig:
    """Data processing configuration"""
    
    # Facility settings
    num_floors: int = 1
    top_n_heuristic_entrances: int = 5
    
    # Event filtering
    primary_positive_indicator: str = "ACCESS GRANTED"
    invalid_phrases_exact: List[str] = None
    invalid_phrases_contain: List[str] = None
    
    # Cleaning thresholds
    same_door_scan_threshold_seconds: int = 10
    ping_pong_threshold_minutes: int = 1
    
    # Performance limits
    max_processing_time: int = 300  # 5 minutes
    chunk_size: int = 10000
    
    def __post_init__(self):
        if self.invalid_phrases_exact is None:
            self.invalid_phrases_exact = ["INVALID ACCESS LEVEL"]
            
        if self.invalid_phrases_contain is None:
            self.invalid_phrases_contain = ["NO ENTRY MADE"]

def get_processing_config() -> ProcessingConfig:
    """Get processing configuration"""
    return ProcessingConfig()