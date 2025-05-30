# app.py - FIXED for actual directory structure
import dash
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dash_bootstrap_components as dbc

# Import UI components and handlers from actual structure
from ui.components.upload import create_enhanced_upload_component
from ui.components.mapping import create_mapping_component
from ui.components.classification import create_classification_component
from ui.components.graph import create_graph_component
from ui.components.stats import create_stats_component
from ui.components.upload_handlers import create_upload_handlers
from ui.components.mapping_handlers import create_mapping_handlers
from ui.components.classification_handlers import create_classification_handlers
from ui.components.graph_handlers import create_graph_handlers

# Import layout from actual structure
from ui.pages.main_page import create_main_layout

# Import constants from actual location
from utils.constants import DEFAULT_ICONS

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
    """
    Register all callbacks using the actual modular system
    """
    try:
        # Upload handlers
        upload_component = create_enhanced_upload_component(
            ICON_UPLOAD_DEFAULT, 
            ICON_UPLOAD_SUCCESS, 
            ICON_UPLOAD_FAIL
        )
        upload_handlers = create_upload_handlers(app, upload_component, {
            'default': ICON_UPLOAD_DEFAULT,
            'success': ICON_UPLOAD_SUCCESS,
            'fail': ICON_UPLOAD_FAIL
        })
        upload_handlers.register_callbacks()
        print("✅ Upload handlers registered")
        
        # Mapping handlers
        mapping_component = create_mapping_component()
        mapping_handlers = create_mapping_handlers(app, mapping_component)
        mapping_handlers.register_callbacks()
        print("✅ Mapping handlers registered")
        
        # Classification handlers
        classification_component = create_classification_component()
        classification_handlers = create_classification_handlers(app, classification_component)
        classification_handlers.register_callbacks()
        print("✅ Classification handlers registered")
        
        # Graph handlers
        graph_handlers = create_graph_handlers(app)
        graph_handlers.register_callbacks()
        print("✅ Graph handlers registered")
        
        print("🎉 All callbacks registered successfully!")
        
    except Exception as e:
        print(f"❌ Error registering callbacks: {e}")
        import traceback
        traceback.print_exc()

# Register all callbacks
register_all_callbacks()

if __name__ == "__main__":
    print("🚀 Starting Yōsai Intel Dashboard...")
    app.run(debug=True, host='127.0.0.1', port=8050)