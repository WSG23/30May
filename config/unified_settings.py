# config/unified_settings.py
"""
Unified configuration - Single source of truth - ENHANCED
"""
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
import os

# SINGLE SOURCE OF TRUTH - Required CSV columns mapping
REQUIRED_INTERNAL_COLUMNS = {
    'Timestamp': 'Timestamp (Event Time)',
    'UserID': 'UserID (Person Identifier)',
    'DoorID': 'DoorID (Device Name)',
    'EventType': 'EventType (Access Result)'
}

# Security level definitions
SECURITY_LEVELS = {
    0: {"label": "⬜️ Unclassified", "color": "#2D3748", "value": "unclassified"},
    1: {"label": "🟢 Green (Public)", "color": "#2DBE6C", "value": "green"},
    2: {"label": "🟠 Orange (Semi-Restricted)", "color": "#FFB020", "value": "yellow"},
    3: {"label": "🔴 Red (Restricted)", "color": "#E02020", "value": "red"},
}

# File processing limits
FILE_LIMITS = {
    'max_file_size': 10 * 1024 * 1024,  # 10MB
    'max_rows': 1_000_000,
    'allowed_extensions': ['.csv'],
    'encoding': 'utf-8'
}

# Default icon paths
DEFAULT_ICONS = {
    'upload_default': '/assets/upload_file_csv_icon.png',
    'upload_success': '/assets/upload_file_csv_icon_success.png',
    'upload_fail': '/assets/upload_file_csv_icon_fail.png',
    'main_logo': '/assets/logo_white.png'
}

@dataclass
class DatabaseConfig:
    """Database configuration"""
    host: str = "localhost"
    port: int = 5432
    name: str = "yosai"

@dataclass
class FileConfig:
    """File processing configuration"""
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    max_rows: int = 1_000_000
    allowed_extensions: List[str] = field(default_factory=lambda: ['.csv'])
    encoding: str = 'utf-8'

@dataclass
class UIConfig:
    """UI configuration"""
    colors: Dict[str, str] = field(default_factory=lambda: {
        'primary': '#1B2A47',
        'accent': '#2196F3',
        'success': '#2DBE6C',
        'warning': '#FFB020',
        'critical': '#E02020',
        'background': '#0F1419',
        'surface': '#1A2332',
        'border': '#2D3748',
        'text_primary': '#F7FAFC',
        'text_secondary': '#E2E8F0',
        'text_tertiary': '#A0AEC0',
    })
    
    animations: Dict[str, str] = field(default_factory=lambda: {
        'fast': '0.15s',
        'normal': '0.3s',
        'slow': '0.5s'
    })

@dataclass
class ProcessingConfig:
    """Data processing configuration"""
    num_floors: int = 1
    top_n_heuristic_entrances: int = 5
    primary_positive_indicator: str = "ACCESS GRANTED"
    invalid_phrases_exact: List[str] = field(default_factory=lambda: ["INVALID ACCESS LEVEL"])
    invalid_phrases_contain: List[str] = field(default_factory=lambda: ["NO ENTRY MADE"])
    same_door_scan_threshold_seconds: int = 10
    ping_pong_threshold_minutes: int = 1

@dataclass
class AppSettings:
    """Main application settings"""
    debug: bool = field(default_factory=lambda: os.getenv('DEBUG', 'False').lower() == 'true')
    port: int = field(default_factory=lambda: int(os.getenv('PORT', '8050')))
    host: str = field(default_factory=lambda: os.getenv('HOST', '127.0.0.1'))
    
    # Required columns - SINGLE SOURCE OF TRUTH
    required_columns: Dict[str, str] = field(default_factory=lambda: REQUIRED_INTERNAL_COLUMNS)
    
    # Default icons configuration
    default_icons: Dict[str, str] = field(default_factory=lambda: DEFAULT_ICONS)
    
    # Sub-configurations
    database: DatabaseConfig = field(default_factory=DatabaseConfig)
    files: FileConfig = field(default_factory=FileConfig)
    ui: UIConfig = field(default_factory=UIConfig)
    processing: ProcessingConfig = field(default_factory=ProcessingConfig)

# Global settings instance
settings = AppSettings()

def get_settings() -> AppSettings:
    """Get application settings"""
    return settings

# Export constants for easy import
__all__ = [
    'get_settings', 
    'AppSettings',
    'REQUIRED_INTERNAL_COLUMNS',
    'SECURITY_LEVELS', 
    'FILE_LIMITS',
    'DEFAULT_ICONS'
]

print(f"🔧 Unified settings loaded: {len(REQUIRED_INTERNAL_COLUMNS)} required columns")