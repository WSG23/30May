# app.py - MINIMAL FIX (Remove problematic imports)
import dash
from dash import Input, Output
import dash_bootstrap_components as dbc
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import only what exists and works
try:
    from ui.components.upload import create_enhanced_upload_component
except ImportError:
    print("⚠️ Could not import upload component")
    create_enhanced_upload_component = None

try:
    from ui.components.mapping import create_mapping_component
except ImportError:
    print("⚠️ Could not import mapping component")
    create_mapping_component = None

try:
    from ui.components.classification import create_classification_component
except ImportError:
    print("⚠️ Could not import classification component")
    create_classification_component = None

try:
    from ui.components.graph import create_graph_component
except ImportError:
    print("⚠️ Could not import graph component")
    create_graph_component = None

# REMOVED: problematic stats import that's causing the error
# from ui.components.stats import create_stats_component

# Import handlers only if they exist
try:
    from ui.components.secure_upload_handlers import create_secure_upload_handlers
except ImportError:
    try:
        from ui.components.upload_handlers import create_upload_handlers as create_secure_upload_handlers
    except ImportError:
        print("⚠️ Could not import upload handlers")
        create_secure_upload_handlers = None

try:
    from ui.components.mapping_handlers import create_mapping_handlers
except ImportError:
    print("⚠️ Could not import mapping handlers")
    create_mapping_handlers = None

try:
    from ui.components.classification_handlers import create_classification_handlers
except ImportError:
    print("⚠️ Could not import classification handlers")
    create_classification_handlers = None

try:
    from ui.components.graph_handlers import create_graph_handlers
except ImportError:
    print("⚠️ Could not import graph handlers")
    create_graph_handlers = None

# Import layout
try:
    from ui.pages.main_page import create_main_layout
except ImportError:
    print("❌ Could not import main_page layout - this is required!")
    # Create a minimal fallback layout
    def create_main_layout(app_instance, main_logo_path, icon_upload_default):
        from dash import html
        return html.Div([
            html.H1("Analytics Dashboard"),
            html.P("Layout import failed - check ui/pages/main_page.py")
        ])

# Import constants
try:
    from utils.constants import DEFAULT_ICONS
except ImportError:
    print("⚠️ Could not import constants")
    DEFAULT_ICONS = {
        'upload_default': '/assets/upload_file_csv_icon.png',
        'upload_success': '/assets/upload_file_csv_icon_success.png',
        'upload_fail': '/assets/upload_file_csv_icon_fail.png',
        'main_logo': '/assets/logo_white.png'
    }

# --- Logging bootstrap -----------------------------------------------
try:
    from utils.logging_config import setup_application_logging, get_logger
    
    # Create logs directory if it doesn't exist
    logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir, exist_ok=True)
        print(f"📁 Created logs directory: {logs_dir}")

    setup_application_logging()
    logger = get_logger(__name__)
except ImportError:
    print("⚠️ Logging not available, using print statements")
    class SimpleLogger:
        def info(self, msg): print(f"INFO: {msg}")
        def error(self, msg): print(f"ERROR: {msg}")
    logger = SimpleLogger()
# ----------------------------------------------------------------------

# --- Security initialization (optional) ------------------------------
try:
    from utils.security_monitor import setup_security_monitoring
    setup_security_monitoring()
    logger.info("🔐 Security monitoring initialized")
except ImportError:
    logger.info("⚠️ Security monitoring not available - continuing without it")

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

# Assets
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
    """Register all available callbacks with error handling"""
    try:
        logger.info("🔄 Starting callback registration...")
        
        # Only register callbacks for components that exist
        registered_count = 0
        
        # Upload handlers
        if create_secure_upload_handlers and create_enhanced_upload_component:
            try:
                upload_component = create_enhanced_upload_component(
                    ICON_UPLOAD_DEFAULT, 
                    ICON_UPLOAD_SUCCESS, 
                    ICON_UPLOAD_FAIL
                )
                upload_handlers = create_secure_upload_handlers(app, upload_component, {
                    'default': ICON_UPLOAD_DEFAULT,
                    'success': ICON_UPLOAD_SUCCESS,
                    'fail': ICON_UPLOAD_FAIL
                })
                upload_handlers.register_callbacks()
                logger.info("✅ Upload handlers registered")
                registered_count += 1
            except Exception as e:
                logger.error(f"❌ Upload handlers failed: {e}")
        
        # Mapping handlers
        if create_mapping_handlers and create_mapping_component:
            try:
                mapping_component = create_mapping_component()
                mapping_handlers = create_mapping_handlers(app, mapping_component)
                mapping_handlers.register_callbacks()
                logger.info("✅ Mapping handlers registered")
                registered_count += 1
            except Exception as e:
                logger.error(f"❌ Mapping handlers failed: {e}")
        
        # Classification handlers
        if create_classification_handlers and create_classification_component:
            try:
                classification_component = create_classification_component()
                classification_handlers = create_classification_handlers(app, classification_component)
                classification_handlers.register_callbacks()
                logger.info("✅ Classification handlers registered")
                registered_count += 1
            except Exception as e:
                logger.error(f"❌ Classification handlers failed: {e}")
        
        # Graph handlers
        if create_graph_handlers:
            try:
                graph_handlers = create_graph_handlers(app)
                graph_handlers.register_callbacks()
                logger.info("✅ Graph handlers registered")
                registered_count += 1
            except Exception as e:
                logger.error(f"❌ Graph handlers failed: {e}")
        
        if registered_count > 0:
            logger.info(f"🎉 Successfully registered {registered_count} handler groups!")
        else:
            logger.error("❌ No handlers could be registered - check your imports")
        
    except Exception as e:
        logger.error(f"❌ Error in callback registration: {e}")
        import traceback
        traceback.print_exc()

# Register callbacks
register_all_callbacks()

if __name__ == "__main__":
    logger.info("🚀 Starting Yōsai Intel Dashboard...")
    
    try:
        app.run(debug=True, host='127.0.0.1', port=8050)
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        raise