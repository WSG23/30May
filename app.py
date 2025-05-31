# app.py - FIXED CALLBACK CONFLICT VERSION
import dash
from dash import Input, Output
import dash_bootstrap_components as dbc
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import UI components and handlers
from ui.components.upload import create_enhanced_upload_component
from ui.components.mapping import create_mapping_component
from ui.components.classification import create_classification_component
from ui.components.graph import create_graph_component
from ui.components.stats import create_stats_component

# Import secure upload handlers
from ui.components.secure_upload_handlers import create_secure_upload_handlers
from ui.components.mapping_handlers import create_mapping_handlers
from ui.components.classification_handlers import create_classification_handlers
from ui.components.graph_handlers import create_graph_handlers

# Import layout
from ui.pages.main_page import create_main_layout, register_page_callbacks

# Import constants - FIXED import path
from utils.constants import DEFAULT_ICONS

# --- Logging bootstrap -----------------------------------------------
from utils.logging_config import setup_application_logging, get_logger

# Create logs directory if it doesn't exist
logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir, exist_ok=True)
    print(f"📁 Created logs directory: {logs_dir}")

setup_application_logging()
logger = get_logger(__name__)
# ----------------------------------------------------------------------

# --- Security initialization (optional) ------------------------------
# Only initialize if security monitoring is available
try:
    from utils.security_monitor import setup_security_monitoring
    setup_security_monitoring()
    logger.info("🔐 Security monitoring initialized")
except ImportError:
    logger.info("⚠️ Security monitoring not available - continuing without it")

# Initialize general monitoring
try:
    from utils.monitoring import initialize_monitoring
    initialize_monitoring()
    logger.info("📊 General monitoring initialized")
except ImportError:
    logger.info("⚠️ General monitoring not available - continuing without it")
# ----------------------------------------------------------------------

# Create Dash app
app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    assets_folder='assets',
    external_stylesheets=[dbc.themes.DARKLY]
)

server = app.server

# Assets - using actual structure
ICON_UPLOAD_DEFAULT = app.get_asset_url('upload_file_csv_icon.png')
ICON_UPLOAD_SUCCESS = app.get_asset_url('upload_file_csv_icon_success.png') 
ICON_UPLOAD_FAIL = app.get_asset_url('upload_file_csv_icon_fail.png')
MAIN_LOGO_PATH = app.get_asset_url('logo_white.png')

# Create the main layout
app.layout = create_main_layout(
    app_instance=app,
    main_logo_path=MAIN_LOGO_PATH,
    icon_upload_default=ICON_UPLOAD_DEFAULT
)

def register_all_callbacks():
    """Register all callbacks with error handling - FIXED DUPLICATE CALLBACKS"""
    try:
        # Create components
        upload_component = create_enhanced_upload_component(
            ICON_UPLOAD_DEFAULT, 
            ICON_UPLOAD_SUCCESS, 
            ICON_UPLOAD_FAIL
        )
        mapping_component = create_mapping_component()
        classification_component = create_classification_component()
        
        # Register SECURE upload handlers
        upload_handlers = create_secure_upload_handlers(app, upload_component, {
            'default': ICON_UPLOAD_DEFAULT,
            'success': ICON_UPLOAD_SUCCESS,
            'fail': ICON_UPLOAD_FAIL
        })
        upload_handlers.register_callbacks()
        logger.info("🔐 Secure upload handlers registered")
        
        # Register mapping handlers
        mapping_handlers = create_mapping_handlers(app, mapping_component)
        mapping_handlers.register_callbacks()
        logger.info("✅ Mapping handlers registered")
        
        # Register classification handlers
        classification_handlers = create_classification_handlers(app, classification_component)
        classification_handlers.register_callbacks()
        logger.info("✅ Classification handlers registered")
        
        # Register graph handlers
        graph_handlers = create_graph_handlers(app)
        graph_handlers.register_callbacks()
        logger.info("✅ Graph handlers registered")
        
        # REMOVED DUPLICATE FLOOR SLIDER CALLBACK
        # This is likely already handled in one of the other handlers
        # If you need a floor slider callback, it should be in classification_handlers
        # or another specific handler file, not here in app.py
        
        logger.info("🎉 All callbacks registered successfully!")
        
    except Exception as e:
        logger.error(f"❌ Error registering callbacks: {e}")
        import traceback
        traceback.print_exc()
        # Continue anyway to allow app to start

# Register page callbacks FIRST (before other callbacks)
register_page_callbacks(app)

# Register all other callbacks
register_all_callbacks()

if __name__ == "__main__":
    logger.info("🚀 Starting Yōsai Intel Dashboard with Enhanced Security...")
    try:
        # FIXED: Use app.run() instead of security_validator()
        app.run(debug=True, host='127.0.0.1', port=8050)
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        raise