# constants/constants.py
"""
Constants - Import from unified settings
"""
from config.unified_settings import get_settings

settings = get_settings()

# Re-export for backward compatibility
REQUIRED_INTERNAL_COLUMNS = settings.required_columns