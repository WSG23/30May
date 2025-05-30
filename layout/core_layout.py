# layout/core_layout.py (FIXED IMPORTS)
"""
Updated core layout with fixed imports for registry integration
"""

from dash import html, dcc
import dash_cytoscape as cyto
import dash_bootstrap_components as dbc

# Import existing components and styles
from ui.themes.style_config import COLORS, UI_VISIBILITY, UI_COMPONENTS, BORDER_RADIUS, SHADOWS
from ui.themes.graph_styles import (
    centered_graph_box_style,
    cytoscape_inside_box_style,
    tap_node_data_centered_style,
    actual_default_stylesheet_for_graph
)

def create_main_layout(app_instance, main_logo_path, icon_upload_default, upload_component=None):
    """
    Creates the main application layout with optional registry component
    """
    
    # If no upload component provided, create legacy one with proper import handling
    if upload_component is None:
        upload_component = _create_fallback_upload_component(
            app_instance, icon_upload_default
        )
    
    layout = html.Div(children=[
        # Main Header Bar
        create_main_header(main_logo_path),
        
        # Upload Section (using provided component)
        create_upload_section(upload_component),
        
        # Interactive Setup Container (using provided component)
        upload_component.create_interactive_setup_container(),
        
        # Processing Status
        create_processing_status(),
        
        # Custom Header (shown after processing)
        create_custom_header(main_logo_path),
        
        # Statistics Panels
        create_stats_panels(),
        
        # Graph Output Container
        create_graph_container(),
        
        # Data Stores
        create_data_stores()
        
    ], style=get_main_container_style())
    
    return layout

def _create_fallback_upload_component(app_instance, icon_upload_default):
    """Create upload component with proper error handling"""
    try:
        # Method 1: Try importing from ui.components directly
        from ui.components.upload import create_upload_component
        
        return create_upload_component(
            icon_upload_default,
            app_instance.get_asset_url('upload_file_csv_icon_success.png'),
            app_instance.get_asset_url('upload_file_csv_icon_fail.png')
        )
        
    except ImportError as e:
        print(f"⚠️ Failed to import from ui.components.upload: {e}")
        
        try:
            # Method 2: Try importing from ui.components package
            from ui.components import create_upload_component
            
            return create_upload_component(
                icon_upload_default,
                app_instance.get_asset_url('upload_file_csv_icon_success.png'),
                app_instance.get_asset_url('upload_file_csv_icon_fail.png')
            )
            
        except ImportError as e2:
            print(f"⚠️ Failed to import from ui.components package: {e2}")
            
            try:
                # Method 3: Direct import from the original file
                import sys
                import os
                sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
                
                from ui.components.upload import EnhancedUploadComponent, ComponentConfig
                from config.unified_settings import get_settings
                
                config = ComponentConfig(
                    icons={
                        'default': icon_upload_default,
                        'success': app_instance.get_asset_url('upload_file_csv_icon_success.png'),
                        'fail': app_instance.get_asset_url('upload_file_csv_icon_fail.png')
                    },
                    theme=get_settings(),
                    settings=get_settings()
                )
                
                return EnhancedUploadComponent(config)
                
            except Exception as e3:
                print(f"⚠️ All import methods failed: {e3}")
                
                # Method 4: Ultra-fallback - create a minimal upload component
                return _create_minimal_upload_component(icon_upload_default)

def _create_minimal_upload_component(icon_upload_default):
    """Create a minimal upload component as last resort"""
    class MinimalUploadComponent:
        def __init__(self, icon):
            self.icon = icon
        
        def create_upload_area(self):
            return dcc.Upload(
                id='upload-data',
                children=html.Div([
                    html.Img(src=self.icon, style={'width': '64px', 'height': '64px'}),
                    html.H3("Drop CSV file here")
                ], style={'textAlign': 'center', 'padding': '20px'}),
                style={
                    'width': '70%',
                    'height': '150px',
                    'lineHeight': '150px',
                    'borderWidth': '2px',
                    'borderStyle': 'dashed',
                    'borderColor': '#2D3748',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px auto',
                    'cursor': 'pointer'
                },
                multiple=False,
                accept='.csv'
            )
        
        def create_interactive_setup_container(self):
            return html.Div(
                id='interactive-setup-container',
                style={'display': 'none'},
                children=[
                    html.Div(id='mapping-ui-section', style={'display': 'none'}),
                    html.Div(id='entrance-verification-ui-section', style={'display': 'none'}),
                    html.Button(
                        'Generate Model',
                        id='confirm-and-generate-button',
                        style={'marginTop': '20px', 'width': '100%'}
                    )
                ]
            )
    
    return MinimalUploadComponent(icon_upload_default)

def create_main_header(main_logo_path):
    """Creates the main application header"""
    return html.Div(
        style={
            'display': 'flex',
            'alignItems': 'center',
            'padding': '15px 30px',
            'backgroundColor': COLORS['background'],
            'borderBottom': f'1px solid {COLORS["border"]}',
            'marginBottom': '30px',
            'position': 'relative',
            'width': '100%',
        },
        children=[
            html.Img(src=main_logo_path, style={'height': '40px', 'marginRight': '15px'}),
            html.H1("Analytics Dashboard",
                   style={
                       'fontSize': '1.8rem',
                       'margin': '0',
                       'color': COLORS['text_primary'],
                       'position': 'absolute',
                       'left': '50%',
                       'transform': 'translateX(-50%)'
                   })
        ]
    )

def create_upload_section(upload_component):
    """Creates the upload section using the provided component"""
    return html.Div([
        upload_component.create_upload_area(),
    ], style={'marginBottom': '20px'})

def create_processing_status():
    """Creates the processing status indicator"""
    return html.Div(
        id='processing-status', 
        style={
            'marginTop': '10px', 
            'color': COLORS['accent'], 
            'textAlign': 'center'
        }
    )

def create_custom_header(main_logo_path):
    """Creates the custom header shown after processing"""
    try:
        from ui.components.stats import create_stats_component
        stats_component = create_stats_component()
        return stats_component.create_custom_header(main_logo_path)
    except ImportError:
        return html.Div(id='yosai-custom-header', style={'display': 'none'})

def create_stats_panels():
    """Creates the statistics panels"""
    try:
        from ui.components.stats import create_stats_component
        stats_component = create_stats_component()
        return stats_component.create_stats_container()
    except ImportError:
        return html.Div(id='stats-panels-container', style={'display': 'none'})

def create_graph_container():
    """Creates the graph visualization container"""
    try:
        from ui.components.graph import create_graph_component
        graph_component = create_graph_component()
        return graph_component.create_graph_container()
    except ImportError:
        return html.Div(id='graph-output-container', style={'display': 'none'})

def create_data_stores():
    """Creates all the dcc.Store components for state management"""
    return html.Div([
        dcc.Store(id='uploaded-file-store'),
        dcc.Store(id='csv-headers-store', storage_type='session'),
        dcc.Store(id='column-mapping-store', storage_type='local'),
        dcc.Store(id='ranked-doors-store', storage_type='session'),
        dcc.Store(id='current-entrance-offset-store', data=0, storage_type='session'),
        dcc.Store(id='manual-door-classifications-store', storage_type='local'),
        dcc.Store(id='num-floors-store', storage_type='session', data=1),
        dcc.Store(id='all-doors-from-csv-store', storage_type='session'),
    ])

def get_main_container_style():
    """Returns the main container styling"""
    return {
        'backgroundColor': COLORS['background'], 
        'padding': '20px', 
        'minHeight': '100vh', 
        'fontFamily': 'Arial, sans-serif'
    }

# Legacy function for backward compatibility
def create_main_layout_legacy(app_instance, main_logo_path, icon_upload_default):
    """Legacy function name for backward compatibility"""
    return create_main_layout(app_instance, main_logo_path, icon_upload_default)