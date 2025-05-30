# config/__init__.py
"""
Unified configuration package for Yōsai Intel application - SIMPLIFIED
"""

# Import from unified settings as primary source
from .unified_settings import get_settings, AppSettings

# Define constants directly to avoid circular imports
REQUIRED_INTERNAL_COLUMNS = {
    'Timestamp': 'Timestamp (Event Time)',
    'UserID': 'UserID (Person Identifier)',
    'DoorID': 'DoorID (Device Name)',
    'EventType': 'EventType (Access Result)'
}

SECURITY_LEVELS = {
    0: {"label": "⬜️ Unclassified", "color": "#2D3748", "value": "unclassified"},
    1: {"label": "🟢 Green (Public)", "color": "#2DBE6C", "value": "green"},
    2: {"label": "🟠 Orange (Semi-Restricted)", "color": "#FFB020", "value": "yellow"},
    3: {"label": "🔴 Red (Restricted)", "color": "#E02020", "value": "red"},
}

DEFAULT_ICONS = {
    'upload_default': '/assets/upload_file_csv_icon.png',
    'upload_success': '/assets/upload_file_csv_icon_success.png',
    'upload_fail': '/assets/upload_file_csv_icon_fail.png',
    'main_logo': '/assets/logo_white.png'
}

FILE_LIMITS = {
    'max_file_size': 10 * 1024 * 1024,  # 10MB
    'max_rows': 1_000_000,
    'allowed_extensions': ['.csv'],
    'encoding': 'utf-8'
}

# Simple aliases to avoid type conflicts
def get_config():
    """Get main application configuration"""
    return get_settings()

def get_ui_config():
    """Get UI configuration"""
    return get_settings().ui

def get_processing_config():
    """Get processing configuration"""
    return get_settings().processing

__all__ = [
    'get_settings',
    'AppSettings',
    'get_config',
    'get_ui_config',
    'get_processing_config',
    'REQUIRED_INTERNAL_COLUMNS',
    'SECURITY_LEVELS',
    'DEFAULT_ICONS',
    'FILE_LIMITS'
]