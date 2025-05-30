# app.py (UPDATED to use new UI structure)
import dash
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dash_bootstrap_components as dbc

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import centralized UI components and handlers - type: ignore to suppress Pylance warnings
from ui.components.upload import create_enhanced_upload_component  # type: ignore
from ui.components.mapping import create_mapping_component  # type: ignore
from ui.components.classification import create_classification_component  # type: ignore
from ui.components.graph import create_graph_component  # type: ignore
from ui.components.stats import create_stats_component  # type: ignore
from ui.handlers.upload_handlers import create_upload_handlers  # type: ignore
from ui.handlers.mapping_handlers import create_mapping_handlers  # type: ignore
from ui.handlers.classification_handlers import create_classification_handlers  # type: ignore
from ui.handlers.graph_handlers import create_graph_handlers  # type: ignore

# Import existing modules (will be refactored in future phases)
from layout.core_layout import create_main_layout


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
    """
    Register all callbacks using the new modular system
    """
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
    
    # Mapping handlers
    mapping_component = create_mapping_component()
    mapping_handlers = create_mapping_handlers(app, mapping_component)
    mapping_handlers.register_callbacks()
    
    # Classification handlers
    classification_component = create_classification_component()
    classification_handlers = create_classification_handlers(app, classification_component)
    classification_handlers.register_callbacks()
    
    # Graph handlers
    graph_handlers = create_graph_handlers(app)
    graph_handlers.register_callbacks()
    
    # EXISTING: Register other callbacks (to be refactored in future phases)
    # register_mapping_callbacks(app)  # COMMENTED OUT - now using new system
    # register_graph_callbacks(app)

# Register all callbacks
register_all_callbacks()

if __name__ == "__main__":
    app.run(debug=True)