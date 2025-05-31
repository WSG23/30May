# layout/core_layout.py (FIXED LAYOUT)
"""
Updated core layout with properly included mapping and classification sections
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

# Try to import constants, with fallback
try:
    from config import REQUIRED_INTERNAL_COLUMNS
except ImportError:
    try:
        from utils.constants import REQUIRED_INTERNAL_COLUMNS
    except ImportError:
        # Fallback constants
        REQUIRED_INTERNAL_COLUMNS = {
            'Timestamp': 'Timestamp (Event Time)',
            'UserID': 'UserID (Person Identifier)',
            'DoorID': 'DoorID (Device Name)',
            'EventType': 'EventType (Access Result)'
        }

def create_main_layout(app_instance, main_logo_path, icon_upload_default, upload_component=None):
    """
    Creates the main application layout with proper mapping section
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
        
        # Interactive Setup Container (using provided component) - FIXED
        create_interactive_setup_container_fixed(),
        
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

def create_interactive_setup_container_fixed():
    """Creates the interactive setup container with proper mapping section structure"""
    return html.Div(
        id='interactive-setup-container',
        style={'display': 'none'},
        children=[
            # Mapping UI Section with complete structure - Use actual component
            create_mapping_section_with_fallback(),
            
            # Entrance Verification UI Section - Use actual classification component
            create_classification_section(),
            
            # Generate Button
            html.Button(
                'Confirm Selections & Generate Onion Model',
                id='confirm-and-generate-button',
                n_clicks=0,
                style={
                    'marginTop': '20px', 
                    'width': '100%',
                    'padding': '12px',
                    'backgroundColor': COLORS['accent'],
                    'color': 'white',
                    'border': 'none',
                    'borderRadius': '5px',
                    'fontSize': '1rem',
                    'fontWeight': 'bold',
                    'cursor': 'pointer'
                }
            )
        ]
    )

def _create_fallback_upload_component(app_instance, icon_upload_default):
    """Create upload component with simplified fallback"""
    class SimpleUploadComponent:
        def __init__(self, default_icon, success_icon, fail_icon):
            self.default_icon = default_icon
            self.success_icon = success_icon
            self.fail_icon = fail_icon
        
        def create_upload_area(self):
            return dcc.Upload(
                id='upload-data',
                children=html.Div([
                    html.Img(
                        id='upload-icon',
                        src=self.default_icon, 
                        style={'width': '96px', 'height': '96px', 'marginBottom': '15px'}
                    ),
                    html.H3("Drop your CSV file here", style={
                        'margin': '0',
                        'fontSize': '1.125rem',
                        'fontWeight': '600',
                        'color': COLORS['text_primary'],
                        'marginBottom': '5px'
                    }),
                    html.P("or click to browse", style={
                        'margin': '0',
                        'fontSize': '0.875rem',
                        'color': COLORS['text_secondary'],
                    }),
                ], style={'textAlign': 'center', 'padding': '20px'}),
                style={
                    'width': '70%',
                    'maxWidth': '600px',
                    'minHeight': '180px',
                    'borderRadius': '12px',
                    'textAlign': 'center',
                    'margin': '16px auto',
                    'display': 'flex',
                    'alignItems': 'center',
                    'justifyContent': 'center',
                    'cursor': 'pointer',
                    'transition': 'all 0.3s',
                    'border': f'2px dashed {COLORS["border"]}',
                    'backgroundColor': COLORS['surface'],
                },
                multiple=False,
                accept='.csv'
            )
        
        def get_upload_styles(self):
            """Returns styles for different states"""
            return {
                'initial': {
                    'border': f'2px dashed {COLORS["border"]}',
                    'backgroundColor': COLORS['surface'],
                },
                'success': {
                    'border': f'2px solid {COLORS["success"]}',
                    'backgroundColor': f"{COLORS['success']}10",
                },
                'error': {
                    'border': f'2px solid {COLORS["critical"]}',
                    'backgroundColor': f"{COLORS['critical']}10",
                }
            }
    
    return SimpleUploadComponent(
        icon_upload_default,
        app_instance.get_asset_url('upload_file_csv_icon_success.png'),
        app_instance.get_asset_url('upload_file_csv_icon_fail.png')
    )

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

def create_mapping_section_with_fallback():
    """Creates the mapping section using the actual component with fallback"""
    try:
        from ui.components.mapping import create_mapping_component
        mapping_component = create_mapping_component()
        return mapping_component.create_mapping_section()
    except ImportError:
        # Fallback mapping section
        return html.Div(
            id='mapping-ui-section',
            style={'display': 'none'},
            children=[
                html.H4(
                    "Step 1: Map CSV Headers", 
                    className="text-center", 
                    style={'color': COLORS['text_primary'], 'fontSize': '1.3rem', 'marginBottom': '1rem'}
                ),
                html.Div([
                    html.P([
                        "Map your CSV columns to the required fields. ",
                        html.Strong("All four fields are required"), 
                        " for the analysis to work properly."
                    ], style={
                        'color': COLORS['text_secondary'], 
                        'fontSize': '0.85rem',
                        'marginBottom': '8px'
                    }),
                    html.Details([
                        html.Summary("What do these fields mean?", 
                                   style={'color': COLORS['accent'], 'cursor': 'pointer', 'fontSize': '0.9rem'}),
                        html.Ul([
                            html.Li([html.Strong("Timestamp: "), "When the access event occurred"]),
                            html.Li([html.Strong("UserID: "), "Person identifier (badge number, employee ID, etc.)"]),
                            html.Li([html.Strong("DoorID: "), "Device or door identifier"]),
                            html.Li([html.Strong("EventType: "), "Access result (granted, denied, etc.)"])
                        ], style={'color': COLORS['text_secondary'], 'fontSize': '0.8rem'})
                    ])
                ], style={'marginBottom': '12px'}),
                # This is the key element that was missing
                html.Div(id='dropdown-mapping-area'),
                html.Div(id='mapping-validation-message', style={'display': 'none'}),
                html.Button(
                    'Confirm Header Mapping & Proceed',
                    id='confirm-header-map-button',
                    n_clicks=0,
                    style={
                        'padding': '8px 16px',
                        'border': 'none',
                        'borderRadius': '5px',
                        'backgroundColor': COLORS['accent'],
                        'color': 'white',
                        'fontSize': '0.9rem',
                        'fontWeight': 'bold',
                        'cursor': 'pointer',
                        'display': 'block',
                        'margin': '15px auto 0',
                        'transition': 'background-color 0.3s ease'
                    }
                )
            ]
        )

def create_classification_section():
    """Creates the classification section using the actual component"""
    try:
        from ui.components.classification import create_classification_component
        classification_component = create_classification_component()
        return classification_component.create_entrance_verification_section()
    except ImportError:
        # Fallback classification section
        return html.Div(
            id='entrance-verification-ui-section', 
            style={'display': 'none'},
            children=[
                # Facility Setup Card
                html.Div([
                    html.H4("Step 2: Facility Setup", style={'color': COLORS['text_primary'], 'textAlign': 'center'}),
                    html.Div([
                        html.Label(
                            "How many floors are in the facility?", 
                            style={'color': COLORS['text_primary'], 'fontWeight': 'bold', 'marginBottom': '8px'}
                        ),
                        dcc.Dropdown(
                            id="num-floors-input",
                            options=[{"label": str(i), "value": i} for i in range(1, 11)],
                            value=4,
                            clearable=False,
                            style={'marginBottom': '16px'}
                        ),
                        html.Label(
                            "Enable Manual Door Classification?", 
                            style={'color': COLORS['text_primary'], 'fontWeight': 'bold', 'marginBottom': '8px'}
                        ),
                        dcc.RadioItems(
                            id='manual-map-toggle',
                            options=[
                                {'label': 'Yes', 'value': 'yes'}, 
                                {'label': 'No', 'value': 'no'}
                            ],
                            value='yes', 
                            inline=True,
                            style={'marginBottom': '16px'}
                        )
                    ])
                ], style={
                    'padding': '20px',
                    'backgroundColor': COLORS['surface'],
                    'borderRadius': '8px',
                    'marginBottom': '20px',
                    'border': f'1px solid {COLORS["border"]}'
                }),
                
                # Door Classification Table Container
                html.Div(
                    id="door-classification-table-container",
                    style={'display': 'none'},
                    children=[
                        html.H4("Step 3: Door Classification", style={'color': COLORS['text_primary'], 'textAlign': 'center'}),
                        html.P("Assign a security level to each door below:", style={'color': COLORS['text_primary']}),
                        html.Div(id="door-classification-table"),
                    ]
                )
            ]
        )

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