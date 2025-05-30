# layout/core_layout.py (UPDATED)
"""
Updated core layout using the new UI component system
Upload component is now centralized in ui/components/
"""

from dash import html, dcc
import dash_cytoscape as cyto
import dash_bootstrap_components as dbc

# Import centralized UI components
from ui.components.upload import create_upload_component
from styles.style_config import COLORS, UI_VISIBILITY, UI_COMPONENTS, BORDER_RADIUS, SHADOWS
from styles.graph_styles import (
    centered_graph_box_style,
    cytoscape_inside_box_style,
    tap_node_data_centered_style,
    actual_default_stylesheet_for_graph
)

# Define Security Levels for the slider (MUST BE CONSISTENT)
SECURITY_LEVELS_SLIDER_MAP = {
    0: {"label": "⬜️ Unclassified", "color": COLORS['border'], "value": "unclassified"},
    1: {"label": "🟢 Green (Public)", "color": COLORS['success'], "value": "green"},
    2: {"label": "🟠 Orange (Semi-Restricted)", "color": COLORS['warning'], "value": "yellow"},
    3: {"label": "🔴 Red (Restricted)", "color": COLORS['critical'], "value": "red"},
}


def create_main_layout(app_instance, main_logo_path, icon_upload_default):
    """
    Creates the main application layout using centralized UI components
    """
    # Initialize upload component
    upload_component = create_upload_component(
        icon_upload_default,
        app_instance.get_asset_url('upload_file_csv_icon_success.png'),
        app_instance.get_asset_url('upload_file_csv_icon_fail.png')
    )
    
    layout = html.Div(children=[
        # Main Header Bar
        create_main_header(main_logo_path),
        
        # Upload Section (using new component)
        create_upload_section(upload_component),
        
        # Interactive Setup Container (using new component)
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
        'position': 'relative', # Essential for absolute positioning of children
        'width': '100%',        # Ensure the div takes full width to center effectively
                                # (often default, but good to be explicit)
    },
    children=[
        html.Img(src=main_logo_path, style={'height': '40px', 'marginRight': '15px'}),
        html.H1("Analytics Dashboard",
               style={
                   'fontSize': '1.8rem',
                   'margin': '0',
                   'color': COLORS['text_primary'],
                   'position': 'absolute',   # Make the H1 positioned absolutely
                   'left': '50%',            # Move its left edge to the horizontal center
                   'transform': 'translateX(-50%)' # Shift it back by half its own width
                                                   # to truly center it
               })
    ]
    )

def create_upload_section(upload_component):
    """Creates the upload section using the new upload component - FIXED: Removed empty container"""
    return html.Div([
        upload_component.create_upload_area(),
        # REMOVED: upload_component.create_status_text() - This was creating the empty box
    ], style={'marginBottom': '20px'})  # Added margin for spacing

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
    """Creates the custom header shown after processing with improved styling"""
    # Import stats component here to avoid circular imports
    from ui.components.stats import create_stats_component
    
    stats_component = create_stats_component()
    return stats_component.create_custom_header(main_logo_path)


def create_stats_panels():
    """Creates the statistics panels"""
    # Import stats component here to avoid circular imports
    from ui.components.stats import create_stats_component
    
    stats_component = create_stats_component()
    return stats_component.create_stats_container()


def create_graph_container():
    """Creates the graph visualization container"""
    # Import graph component here to avoid circular imports
    from ui.components.graph import create_graph_component
    
    graph_component = create_graph_component()
    return graph_component.create_graph_container()


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


# Legacy function for backward compatibility during transition
def create_main_layout_legacy(app_instance, main_logo_path, icon_upload_default):
    """
    Legacy function name for backward compatibility
    Remove this after migration is complete
    """
    return create_main_layout(app_instance, main_logo_path, icon_upload_default)