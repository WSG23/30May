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