# utils/constants.py - FIXED VERSION - Centralized Constants

"""
Centralized constants and configuration - SINGLE SOURCE OF TRUTH
This file resolves import conflicts and provides consistent constants
"""

# ============================================================================
# REQUIRED CSV COLUMNS - CORE MAPPING
# ============================================================================

REQUIRED_INTERNAL_COLUMNS = {
    'Timestamp': 'Timestamp (Event Time)',
    'UserID': 'UserID (Person Identifier)',
    'DoorID': 'DoorID (Device Name)',
    'EventType': 'EventType (Access Result)'
}

# ============================================================================
# SECURITY LEVEL DEFINITIONS
# ============================================================================

SECURITY_LEVELS = {
    0: {"label": "⬜️ Unclassified", "color": "#2D3748", "value": "unclassified"},
    1: {"label": "⬜️ Unclassified", "color": "#2D3748", "value": "unclassified"},
    2: {"label": "⬜️ Unclassified", "color": "#2D3748", "value": "unclassified"},
    3: {"label": "🟢 Green (Public)", "color": "#2DBE6C", "value": "green"},
    4: {"label": "🟢 Green (Public)", "color": "#2DBE6C", "value": "green"},
    5: {"label": "🟢 Green (Public)", "color": "#2DBE6C", "value": "green"},
    6: {"label": "🟠 Orange (Semi-Restricted)", "color": "#FFB020", "value": "yellow"},
    7: {"label": "🟠 Orange (Semi-Restricted)", "color": "#FFB020", "value": "yellow"},
    8: {"label": "🔴 Red (Restricted)", "color": "#E02020", "value": "red"},
    9: {"label": "🔴 Red (Restricted)", "color": "#E02020", "value": "red"},
    10: {"label": "🔴 Red (Restricted)", "color": "#E02020", "value": "red"},
}

# ============================================================================
# ASSET PATHS
# ============================================================================

DEFAULT_ICONS = {
    'upload_default': '/assets/upload_file_csv_icon.png',
    'upload_success': '/assets/upload_file_csv_icon_success.png',
    'upload_fail': '/assets/upload_file_csv_icon_fail.png',
    'main_logo': '/assets/logo_white.png'
}

# ============================================================================
# UI THEME COLORS
# ============================================================================

UI_COLORS = {
    'primary': '#1B2A47',
    'accent': '#2196F3',
    'accent_light': '#42A5F5',
    'accent_dark': '#1976D2',
    'success': '#2DBE6C',
    'warning': '#FFB020',
    'critical': '#E02020',
    'info': '#2196F3',
    'background': '#0F1419',
    'surface': '#1A2332',
    'surface_elevated': '#1E2936',
    'border': '#2D3748',
    'border_hover': '#4A5568',
    'text_primary': '#F7FAFC',
    'text_secondary': '#E2E8F0',
    'text_tertiary': '#A0AEC0',
}

# ============================================================================
# PROCESSING CONFIGURATION
# ============================================================================

PROCESSING_CONFIG = {
    'num_floors': 4,
    'top_n_heuristic_entrances': 5,
    'primary_positive_indicator': '',  # Empty to include all events
    'invalid_phrases_exact': [],        # No exact phrase filtering
    'invalid_phrases_contain': [],      # No contain phrase filtering
    'same_door_scan_threshold_seconds': 10,
    'ping_pong_threshold_minutes': 1,
    'max_processing_time': 300,         # 5 minutes
    'chunk_size': 10000
}

# ============================================================================
# FILE LIMITS AND VALIDATION
# ============================================================================

FILE_LIMITS = {
    'max_file_size': 10 * 1024 * 1024,  # 10MB
    'max_rows': 1_000_000,
    'allowed_extensions': ['.csv'],
    'encoding': 'utf-8',
    'max_columns': 100,
    'min_rows': 1
}

# ============================================================================
# UI COMPONENT CONFIGURATION
# ============================================================================

UI_COMPONENTS = {
    'upload': {
        'enabled': True,
        'accept_types': ['.csv'],
        'max_file_size': '10MB',
        'multiple_files': False,
        'icon_size': '96px',
        'container_width': '70%',
        'border_thickness': '2px'
    },
    'mapping': {
        'enabled': True,
        'required_fields': list(REQUIRED_INTERNAL_COLUMNS.keys()),
        'auto_detect_columns': True,
        'show_validation': True
    },
    'classification': {
        'enabled': True,
        'auto_classify': False,
        'security_levels': list(SECURITY_LEVELS.keys()),
        'default_level': 5,
        'max_doors': 1000
    },
    'graph': {
        'enabled': True,
        'default_layout': 'cose',
        'show_legend': True,
        'interactive': True,
        'export_formats': ['png', 'json'],
        'max_nodes': 500
    },
    'stats': {
        'enabled': True,
        'show_summaries': True,
        'show_charts': True,
        'refresh_interval': 5000,
        'export_enabled': True
    }
}

# ============================================================================
# LAYOUT STYLES
# ============================================================================

UI_STYLES = {
    'hide': {'display': 'none'},
    'show_block': {'display': 'block'},
    'show_flex': {'display': 'flex'},
    'show_flex_stats': {
        'display': 'flex',
        'flexDirection': 'row',
        'justifyContent': 'space-around',
        'gap': '20px',
        'marginBottom': '30px'
    },
    'container_standard': {
        'display': 'block',
        'width': '90%',
        'maxWidth': '1200px',
        'margin': '0 auto',
        'padding': '20px',
        'backgroundColor': UI_COLORS['surface'],
        'borderRadius': '8px',
        'border': f"1px solid {UI_COLORS['border']}",
        'marginBottom': '20px'
    }
}

# ============================================================================
# VALIDATION PATTERNS
# ============================================================================

VALIDATION_PATTERNS = {
    'timestamp_formats': [
        '%Y-%m-%d %H:%M:%S',
        '%m/%d/%Y %H:%M:%S',
        '%d/%m/%Y %H:%M:%S',
        '%Y-%m-%d',
        '%m/%d/%Y',
        '%d/%m/%Y',
        '%Y-%m-%dT%H:%M:%S',
        '%Y-%m-%dT%H:%M:%SZ'
    ],
    'user_id_patterns': [
        r'^\d+$',           # Numeric IDs
        r'^[A-Z]\d+$',      # Letter + numbers
        r'^[A-Z]{2,}\d+$',  # Multiple letters + numbers
        r'^.{1,50}$'        # Any string up to 50 chars
    ],
    'door_id_patterns': [
        r'^[A-Z]+_\d+$',    # DOOR_123
        r'^Door\s*\d+$',    # Door 123
        r'^[A-Z]+\d+$',     # ABC123
        r'^.{1,100}$'       # Any string up to 100 chars
    ]
}

# ============================================================================
# ERROR MESSAGES
# ============================================================================

ERROR_MESSAGES = {
    'file_too_large': f"File size exceeds {FILE_LIMITS['max_file_size'] // (1024*1024)}MB limit",
    'invalid_file_type': f"Only {', '.join(FILE_LIMITS['allowed_extensions'])} files are allowed",
    'no_data': "No data found in the uploaded file",
    'missing_columns': "Required columns are missing from the CSV file",
    'invalid_data': "The data format is not recognized",
    'processing_failed': "Data processing failed. Please check your file format",
    'mapping_incomplete': "Please map all required columns before proceeding",
    'no_doors_found': "No door/device identifiers found in the data",
    'timeout': "Processing timed out. Please try with a smaller file"
}

# ============================================================================
# SUCCESS MESSAGES
# ============================================================================

SUCCESS_MESSAGES = {
    'file_uploaded': "File uploaded successfully",
    'mapping_complete': "Column mapping completed",
    'classification_complete': "Door classification completed", 
    'processing_complete': "Data processing completed successfully",
    'export_complete': "Export completed successfully"
}

# ============================================================================
# DEMO DATA (for testing/fallback)
# ============================================================================

DEMO_DATA = {
    'doors': [
        'Main_Entrance', 'Emergency_Exit_1', 'Loading_Bay', 'Side_Access',
        'Parking_Gate', 'Stair_A_Floor_1', 'Stair_B_Floor_1', 'Elevator_Bank_1',
        'Conference_Room_A', 'Server_Room', 'Executive_Suite', 'Cafeteria_Entry'
    ],
    'users': [f'User_{i:04d}' for i in range(1, 101)],
    'event_types': ['ACCESS GRANTED', 'ACCESS DENIED', 'DOOR FORCED', 'DOOR HELD'],
    'floors': ['1', '2', '3', '4'],
    'security_levels': ['green', 'yellow', 'red']
}

# ============================================================================
# EXPORT FORMATS
# ============================================================================

EXPORT_FORMATS = {
    'csv': {
        'extension': '.csv',
        'mime_type': 'text/csv',
        'description': 'Comma Separated Values'
    },
    'json': {
        'extension': '.json',
        'mime_type': 'application/json',
        'description': 'JavaScript Object Notation'
    },
    'png': {
        'extension': '.png',
        'mime_type': 'image/png',
        'description': 'Portable Network Graphics'
    },
    'pdf': {
        'extension': '.pdf',
        'mime_type': 'application/pdf',
        'description': 'Portable Document Format'
    }
}

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_security_level_info(level):
    """Get security level information by numeric level"""
    return SECURITY_LEVELS.get(level, SECURITY_LEVELS[0])

def get_security_level_by_value(value):
    """Get security level by string value"""
    for level, info in SECURITY_LEVELS.items():
        if info['value'] == value:
            return level
    return 0

def validate_file_size(file_size):
    """Check if file size is within limits"""
    return file_size <= FILE_LIMITS['max_file_size']

def validate_file_extension(filename):
    """Check if file extension is allowed"""
    extension = '.' + filename.split('.')[-1].lower()
    return extension in FILE_LIMITS['allowed_extensions']

def get_ui_color(color_name, fallback='#FFFFFF'):
    """Get UI color by name with fallback"""
    return UI_COLORS.get(color_name, fallback)

def get_component_config(component_name):
    """Get component configuration"""
    return UI_COMPONENTS.get(component_name, {})

def is_component_enabled(component_name):
    """Check if component is enabled"""
    config = get_component_config(component_name)
    return config.get('enabled', False)

# ============================================================================
# VERSION INFO
# ============================================================================

VERSION_INFO = {
    'version': '2.0.0',
    'build': 'fixed',
    'date': '2024-12-19',
    'description': 'Enhanced Analytics Dashboard - Fixed Version'
}

# ============================================================================
# EXPORTS
# ============================================================================

__all__ = [
    'REQUIRED_INTERNAL_COLUMNS',
    'SECURITY_LEVELS',
    'DEFAULT_ICONS',
    'UI_COLORS',
    'PROCESSING_CONFIG',
    'FILE_LIMITS',
    'UI_COMPONENTS',
    'UI_STYLES',
    'VALIDATION_PATTERNS',
    'ERROR_MESSAGES',
    'SUCCESS_MESSAGES',
    'DEMO_DATA',
    'EXPORT_FORMATS',
    'VERSION_INFO',
    'get_security_level_info',
    'get_security_level_by_value',
    'validate_file_size',
    'validate_file_extension',
    'get_ui_color',
    'get_component_config',
    'is_component_enabled'
]

# Print loading confirmation
print(f"✅ Constants loaded - Version {VERSION_INFO['version']} ({VERSION_INFO['build']})")