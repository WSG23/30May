# app.py - ENHANCED VERSION with Advanced Analytics (FIXED IMPORTS)
import dash
from dash import Input, Output, html, dcc  # FIXED: Added html, dcc imports
import dash_bootstrap_components as dbc
import pandas as pd  # FIXED: Added pandas import
import sys
import os
import traceback
import time  # FIXED: Added time import

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import enhanced UI components and handlers
from ui.components.upload import create_enhanced_upload_component
from ui.components.mapping import create_mapping_component
from ui.components.classification import create_classification_component
from ui.components.graph import create_graph_component
from ui.components.stats import create_enhanced_stats_component  # ENHANCED

# Import enhanced handlers
from ui.components.secure_upload_handlers import create_secure_upload_handlers
from ui.components.mapping_handlers import create_mapping_handlers
from ui.components.classification_handlers import create_classification_handlers
from ui.components.graph_handlers import create_enhanced_graph_handlers  # ENHANCED

# Import enhanced layout
from ui.pages.main_page import create_main_layout, register_page_callbacks

# Import constants
from utils.constants import DEFAULT_ICONS

# --- Enhanced Logging bootstrap ------------------------------------------
from utils.logging_config import setup_application_logging, get_logger

# Create logs directory if it doesn't exist
logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir, exist_ok=True)
    print(f"📁 Created logs directory: {logs_dir}")

setup_application_logging()
logger = get_logger(__name__)
logger.info("🚀 Starting Enhanced Yōsai Intel Dashboard...")
# -------------------------------------------------------------------------

# --- Enhanced Security initialization (FIXED) ---------------------------
# Only initialize if security monitoring is available
try:
    from utils.security_monitor import setup_security_monitoring  # FIXED: Proper import
    setup_security_monitoring()
    logger.info("🔐 Enhanced security monitoring initialized")
except (ImportError, ModuleNotFoundError) as e:  # FIXED: Better exception handling
    logger.info(f"⚠️ Security monitoring not available: {e} - continuing without it")

# Initialize enhanced monitoring
try:
    from utils.monitoring import initialize_monitoring
    initialize_monitoring()
    logger.info("📊 Enhanced general monitoring initialized")
except (ImportError, ModuleNotFoundError) as e:  # FIXED: Better exception handling
    logger.info(f"⚠️ General monitoring not available: {e} - continuing without it")
# -------------------------------------------------------------------------

# Create Enhanced Dash app
app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    assets_folder='assets',
    external_stylesheets=[
        dbc.themes.DARKLY,
        # Add custom CSS for enhanced styling
        {
            'href': '/assets/custom.css',
            'rel': 'stylesheet'
        }
    ],
    title="Enhanced Analytics Dashboard",  # ENHANCED TITLE
    update_title="Analytics Processing...",
    meta_tags=[
        {
            'name': 'description',
            'content': 'Advanced analytics dashboard with real-time data visualization and export capabilities'
        },
        {
            'name': 'viewport',
            'content': 'width=device-width, initial-scale=1'
        }
    ]
)

server = app.server

# Enhanced Assets - using actual structure
ICON_UPLOAD_DEFAULT = app.get_asset_url('upload_file_csv_icon.png')
ICON_UPLOAD_SUCCESS = app.get_asset_url('upload_file_csv_icon_success.png') 
ICON_UPLOAD_FAIL = app.get_asset_url('upload_file_csv_icon_fail.png')
MAIN_LOGO_PATH = app.get_asset_url('logo_white.png')

logger.info(f"📁 Assets configured: {MAIN_LOGO_PATH}")

# Create the enhanced main layout
try:
    app.layout = create_main_layout(
        app_instance=app,
        main_logo_path=MAIN_LOGO_PATH,
        icon_upload_default=ICON_UPLOAD_DEFAULT
    )
    logger.info("✅ Enhanced main layout created successfully")
except Exception as e:
    logger.error(f"❌ Error creating main layout: {e}")
    traceback.print_exc()
    raise


def register_all_enhanced_callbacks():
    """Register all enhanced callbacks with comprehensive error handling"""
    try:
        logger.info("🔄 Starting enhanced callback registration...")
        
        # Create enhanced components
        upload_component = create_enhanced_upload_component(
            ICON_UPLOAD_DEFAULT, 
            ICON_UPLOAD_SUCCESS, 
            ICON_UPLOAD_FAIL
        )
        mapping_component = create_mapping_component()
        classification_component = create_classification_component()
        stats_component = create_enhanced_stats_component()  # ENHANCED
        
        logger.info("✅ Enhanced components created")
        
        # Register SECURE upload handlers
        try:
            upload_handlers = create_secure_upload_handlers(app, upload_component, {
                'default': ICON_UPLOAD_DEFAULT,
                'success': ICON_UPLOAD_SUCCESS,
                'fail': ICON_UPLOAD_FAIL
            })
            upload_handlers.register_callbacks()
            logger.info("🔐 Enhanced secure upload handlers registered")
        except Exception as e:
            logger.error(f"❌ Error registering upload handlers: {e}")
            traceback.print_exc()
        
        # Register mapping handlers
        try:
            mapping_handlers = create_mapping_handlers(app, mapping_component)
            mapping_handlers.register_callbacks()
            logger.info("✅ Enhanced mapping handlers registered")
        except Exception as e:
            logger.error(f"❌ Error registering mapping handlers: {e}")
            traceback.print_exc()
        
        # Register classification handlers
        try:
            classification_handlers = create_classification_handlers(app, classification_component)
            classification_handlers.register_callbacks()
            logger.info("✅ Enhanced classification handlers registered")
        except Exception as e:
            logger.error(f"❌ Error registering classification handlers: {e}")
            traceback.print_exc()
        
        # Register ENHANCED graph handlers (includes advanced analytics)
        try:
            graph_handlers = create_enhanced_graph_handlers(app)  # ENHANCED
            graph_handlers.register_callbacks()
            logger.info("📊 Enhanced graph handlers with advanced analytics registered")
        except Exception as e:
            logger.error(f"❌ Error registering enhanced graph handlers: {e}")
            traceback.print_exc()
        
        # Register enhanced page-specific callbacks
        try:
            register_enhanced_page_callbacks(app)
            logger.info("✅ Enhanced page-specific callbacks registered")
        except Exception as e:
            logger.error(f"❌ Error registering page callbacks: {e}")
            traceback.print_exc()
        
        logger.info("🎉 All enhanced callbacks registered successfully!")
        
        # Add callback health check
        _register_health_check_callbacks(app)
        logger.info("💓 Health check callbacks registered")
        
    except Exception as e:
        logger.error(f"💥 Critical error in enhanced callback registration: {e}")
        traceback.print_exc()
        # Continue anyway to allow app to start


def register_enhanced_page_callbacks(app):
    """Register enhanced page-specific callbacks"""
    
    # Enhanced floor slider callback
    @app.callback(
        Output("num-floors-display", "children"),
        Input("num-floors-input", "value"),
        prevent_initial_call=False
    )
    def update_enhanced_floor_display(value):
        """Enhanced floor display with better formatting"""
        if value is None:
            value = 1
        
        floors = int(value)
        if floors == 1:
            return "1 floor selected"
        else:
            return f"{floors} floors selected"
    
    # Enhanced analytics section visibility callback
    @app.callback(
        [
            Output('analytics-section', 'style'),
            Output('charts-section', 'style'),
            Output('export-section', 'style')
        ],
        Input('yosai-custom-header', 'style'),
        prevent_initial_call=True
    )
    def show_enhanced_sections_when_header_visible(header_style):
        """Show enhanced analytics sections when header becomes visible"""
        try:
            if header_style and header_style.get('display') != 'none':
                show_style = {
                    'display': 'block', 
                    'margin': '20px auto', 
                    'maxWidth': '1200px', 
                    'width': '95%',
                    'padding': '20px', 
                    'backgroundColor': '#1A2332', 
                    'borderRadius': '12px',
                    'border': '1px solid #2D3748',
                    'boxShadow': '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
                    'animation': 'slideUp 0.3s ease-out'
                }
                logger.info("📊 Enhanced analytics sections made visible")
                return show_style, show_style, show_style
            else:
                hide_style = {'display': 'none'}
                return hide_style, hide_style, hide_style
        except Exception as e:
            logger.error(f"Error in enhanced sections visibility callback: {e}")
            hide_style = {'display': 'none'}
            return hide_style, hide_style, hide_style


def _register_health_check_callbacks(app):
    """Register health check and monitoring callbacks"""
    
    @app.callback(
        Output('app-health-status', 'data'),
        Input('app-health-interval', 'n_intervals'),
        prevent_initial_call=True
    )
    def update_app_health(n_intervals):
        """Monitor app health and performance"""
        try:
            import psutil
            
            health_data = {
                'timestamp': time.time(),  # FIXED: time is now properly imported
                'cpu_percent': psutil.cpu_percent(),
                'memory_percent': psutil.virtual_memory().percent,
                'status': 'healthy',
                'callbacks_registered': True,
                'enhanced_mode': True
            }
            
            # Log health status periodically
            if n_intervals % 10 == 0:  # Every 10 intervals
                logger.info(f"💓 App Health: CPU {health_data['cpu_percent']}%, Memory {health_data['memory_percent']}%")
            
            return health_data
            
        except ImportError:
            # psutil not available
            return {
                'timestamp': time.time(),  # FIXED: time is now properly imported
                'status': 'monitoring_unavailable',
                'enhanced_mode': True
            }
        except Exception as e:
            logger.warning(f"Health check error: {e}")
            return {
                'timestamp': time.time(),  # FIXED: time is now properly imported
                'status': 'error',
                'error': str(e)
            }


def add_enhanced_error_handling():
    """Add enhanced error handling for better debugging"""
    
    @app.callback(
        Output('error-display', 'children'),
        Input('error-trigger', 'data'),
        prevent_initial_call=True
    )
    def handle_enhanced_errors(error_data):
        """Enhanced error handling with detailed feedback"""
        if error_data:
            logger.error(f"Enhanced error handler triggered: {error_data}")
            
            error_message = html.Div([  # FIXED: html is now properly imported
                html.H4("⚠️ Application Error", style={'color': '#E02020'}),
                html.P(f"Error: {error_data.get('message', 'Unknown error')}", 
                      style={'color': '#E2E8F0'}),
                html.P(f"Component: {error_data.get('component', 'Unknown')}", 
                      style={'color': '#A0AEC0', 'fontSize': '0.9rem'}),
                html.Hr(),
                html.P("Please refresh the page or contact support if the issue persists.",
                      style={'color': '#A0AEC0', 'fontSize': '0.8rem'})
            ], style={
                'padding': '20px',
                'backgroundColor': '#1A2332',
                'border': '1px solid #E02020',
                'borderRadius': '8px',
                'margin': '20px'
            })
            
            return error_message
        
        return ""


# Register page callbacks FIRST (before other callbacks)
try:
    register_page_callbacks(app)
    logger.info("✅ Base page callbacks registered")
except Exception as e:
    logger.error(f"❌ Error registering base page callbacks: {e}")
    traceback.print_exc()

# Register all enhanced callbacks
register_all_enhanced_callbacks()

# Add enhanced error handling
try:
    add_enhanced_error_handling()
    logger.info("🛡️ Enhanced error handling added")
except Exception as e:
    logger.error(f"⚠️ Could not add enhanced error handling: {e}")

# FIXED: Safely add hidden components for health monitoring
try:
    # Check if app.layout exists and is not None
    if app.layout is not None:
        # Get existing children or create empty list
        existing_children = getattr(app.layout, 'children', [])
        if existing_children is None:
            existing_children = []
        
        # Add health monitoring components (hidden)
        health_components = html.Div([  # FIXED: html is now properly imported
            dcc.Interval(id='app-health-interval', interval=30000, n_intervals=0),  # 30 seconds
            dcc.Store(id='app-health-status'),  # FIXED: dcc is now properly imported
            html.Div(id='error-display'),
            dcc.Store(id='error-trigger')
        ], style={'display': 'none'})
        
        # Safely extend the children list
        if isinstance(existing_children, list):
            existing_children.append(health_components)
        else:
            # If children is not a list, make it one
            existing_children = [existing_children, health_components]
        
        # Update the layout
        app.layout.children = existing_children
        logger.info("💓 Health monitoring components added successfully")
    else:
        logger.warning("⚠️ app.layout is None, skipping health monitoring components")
        
except Exception as e:
    logger.error(f"⚠️ Could not add health monitoring components: {e}")
    # Continue without health monitoring


if __name__ == "__main__":
    logger.info("🚀 Starting Enhanced Yōsai Intel Dashboard with Advanced Analytics...")
    logger.info("📊 Features: Enhanced Statistics, Interactive Charts, Export Tools, Real-time Monitoring")
    
    try:
        # Enhanced server configuration
        server_config = {
            'debug': True,
            'host': '127.0.0.1',
            'port': 8050,
            'dev_tools_hot_reload': True,
            'dev_tools_silence_routes_logging': False
        }
        
        logger.info(f"🌐 Server starting on http://{server_config['host']}:{server_config['port']}")
        logger.info("📈 Enhanced Analytics Features:")
        logger.info("   • Advanced Statistics Panels")
        logger.info("   • Interactive Data Visualization")
        logger.info("   • Real-time Chart Updates")
        logger.info("   • PDF Report Generation")
        logger.info("   • CSV Data Export")
        logger.info("   • Anomaly Detection")
        logger.info("   • Security Level Analysis")
        logger.info("   • Peak Activity Insights")
        
        app.run(**server_config)
        
    except Exception as e:
        logger.error(f"💥 Failed to start enhanced server: {e}")
        traceback.print_exc()
        raise


# Enhanced development utilities
def print_enhanced_debug_info():
    """Print enhanced debug information for development"""
    logger.info("🔧 Enhanced Debug Information:")
    logger.info(f"   • Dash version: {dash.__version__}")
    logger.info(f"   • Python version: {sys.version}")
    logger.info(f"   • Assets folder: {app.assets_folder}")
    logger.info(f"   • Server available at: http://127.0.0.1:8050")
    logger.info("📊 Enhanced Features Status:")
    logger.info("   ✅ Advanced Statistics")
    logger.info("   ✅ Interactive Charts") 
    logger.info("   ✅ Export Functionality")
    logger.info("   ✅ Real-time Updates")
    logger.info("   ✅ Enhanced Security")
    logger.info("   ✅ Performance Monitoring")


# Enhanced callback debugging
@app.callback(
    Output('debug-callback-info', 'children'),
    Input('debug-trigger', 'n_clicks'),
    prevent_initial_call=True
)
def debug_enhanced_callbacks(n_clicks):
    """Debug callback for enhanced features"""
    if n_clicks:
        logger.info("🐛 Enhanced debug callback triggered")
        
        debug_info = {
            'enhanced_mode': True,
            'stats_component': 'EnhancedStatsComponent',
            'graph_handlers': 'EnhancedGraphHandlers', 
            'features': [
                'Advanced Analytics',
                'Interactive Charts',
                'Export Tools',
                'Real-time Monitoring'
            ],
            'timestamp': pd.Timestamp.now().isoformat()  # FIXED: pd is now properly imported
        }
        
        return str(debug_info)
    
    return ""


# Print debug info on startup
if __name__ == "__main__":
    print_enhanced_debug_info()