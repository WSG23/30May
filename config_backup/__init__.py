# config/__init__.py
"""
Configuration package - Working with current structure
"""

# Import from unified settings as single source of truth
from .unified_settings import (
    get_settings, 
    AppSettings,
    REQUIRED_INTERNAL_COLUMNS,
    SECURITY_LEVELS,
    FILE_LIMITS,
    DEFAULT_ICONS
)

# Simple aliases
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