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
