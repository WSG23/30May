# config/constants.py
"""
Deprecated - Use config.unified_settings instead
"""
import warnings
from config.unified_settings import get_settings

warnings.warn(
    "config.constants is deprecated. Use config.unified_settings instead.", 
    DeprecationWarning, 
    stacklevel=2
)

settings = get_settings()

# Backward compatibility exports
REQUIRED_INTERNAL_COLUMNS = settings.required_columns

SECURITY_LEVELS = {
    0: {"label": "⬜️ Unclassified", "color": "#2D3748", "value": "unclassified"},
    1: {"label": "🟢 Green (Public)", "color": "#2DBE6C", "value": "green"},
    2: {"label": "🟠 Orange (Semi-Restricted)", "color": "#FFB020", "value": "yellow"},
    3: {"label": "🔴 Red (Restricted)", "color": "#E02020", "value": "red"},
}

# FIXED: Add missing DEFAULT_ICONS
DEFAULT_ICONS = {
    'upload_default': '/assets/upload_file_csv_icon.png',
    'upload_success': '/assets/upload_file_csv_icon_success.png',
    'upload_fail': '/assets/upload_file_csv_icon_fail.png',
    'main_logo': '/assets/logo_white.png'
}

FILE_LIMITS = {
    'max_file_size': settings.files.max_file_size,
    'max_rows': settings.files.max_rows,
    'allowed_extensions': settings.files.allowed_extensions,
    'encoding': settings.files.encoding
}

# FIXED: Define directly instead of importing from config
REQUIRED_INTERNAL_COLUMNS = {
    'Timestamp': 'Timestamp (Event Time)',
    'UserID': 'UserID (Person Identifier)',
    'DoorID': 'DoorID (Device Name)',
    'EventType': 'EventType (Access Result)'
}
# Debug print to verify constants
print(f"DEBUG: REQUIRED_INTERNAL_COLUMNS = {REQUIRED_INTERNAL_COLUMNS}")