# ui/pages/main_page.py - FIXED VERSION

"""
Main page layout - FIXED to hide stats panels initially
"""

from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import dash_cytoscape as cyto
import dash_bootstrap_components as dbc

# Import your theme constants
try:
    from ui.themes.style_config import COLORS, UI_VISIBILITY, UI_COMPONENTS, BORDER_RADIUS, SHADOWS
except ImportError:
    # Fallback colors if theme not available
    COLORS = {
        'primary': '#1B2A47',
        'accent': '#2196F3',
        'success': '#2DBE6C',
        'warning': '#FFB020',
        'critical': '#E02020',
        'background': '#0F1419',
        'surface': '#1A2332',
        'border': '#2D3748',
        'text_primary': '#F7FAFC',
        'text_secondary': '#E2E8F0',
        'text_tertiary': '#A0AEC0',
    }

# Try to import constants; fallback if missing
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
    Creates the main application layout with properly hidden stats panels
    """
    # If no upload component provided, create fallback
    if upload_component is None:
        upload_component = _create_fallback_upload_component(app_instance, icon_upload_default)

    layout = html.Div(
        children=[
            # Main Header Bar
            create_main_header(main_logo_path),

            # Upload Section (uses either the passed‐in component or fallback)
            create_upload_section(upload_component),

            # Interactive Setup Container: Mapping + Classification + Generate Button
            create_interactive_setup_container_fixed(),

            # Processing Status Indicator (hidden until needed)
            create_processing_status(),

            # Custom Header (HIDDEN until after processing)
            create_custom_header_hidden(main_logo_path),

            # Statistics Panels (HIDDEN until after processing)
            create_stats_panels_hidden(),

            # Graph Output Container (HIDDEN until after processing)
            create_graph_container_hidden(),

            # Data Stores (dcc.Store elements)
            create_data_stores(),
        ],
        style=get_main_container_style()
    )

    return layout


def create_custom_header_hidden(main_logo_path):
    """
    Custom header that is HIDDEN by default - only shown after processing
    """
    return html.Div(
        id='yosai-custom-header',
        style={'display': 'none'},  # EXPLICITLY HIDDEN
        children=[
            html.Div([
                # Logo matching the top header exactly
                html.Img(
                    src=main_logo_path, 
                    style={
                        'height': '24px',
                        'marginRight': '10px',
                        'verticalAlign': 'middle'
                    }
                ),
                # Data Overview text
                html.Span(
                    "Data Overview",
                    style={
                        'fontSize': '18px',
                        'fontWeight': '400',
                        'color': '#ffffff',
                        'fontFamily': 'system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
                        'verticalAlign': 'middle'
                    }
                )
            ], style={
                'display': 'flex',
                'alignItems': 'center',
                'justifyContent': 'center',
                'padding': '16px 0',
                'margin': '0'
            })
        ]
    )


def create_stats_panels_hidden():
    """
    Statistics panels that are HIDDEN by default - only shown after processing
    """
    panel_style_base = {
        'flex': '1',
        'padding': '20px',
        'margin': '0 10px',
        'backgroundColor': COLORS['surface'],
        'borderRadius': '8px',
        'textAlign': 'center',
        'boxShadow': '2px 2px 5px rgba(0,0,0,0.2)'
    }
    
    return html.Div(
        id='stats-panels-container',
        style={'display': 'none'},  # EXPLICITLY HIDDEN
        children=[
            # Access Events Panel
            html.Div([
                html.H3("Access events", style={'color': COLORS['text_primary']}),
                html.H1(id="total-access-events-H1", style={'color': COLORS['text_primary']}),
                html.P(id="event-date-range-P", style={'color': COLORS['text_secondary']})
            ], style={**panel_style_base, 'borderLeft': f'5px solid {COLORS["accent"]}'}),
            
            # Statistics Panel
            html.Div([
                html.H3("Statistics", style={'color': COLORS['text_primary']}),
                html.P(id="stats-date-range-P", style={'color': COLORS['text_secondary']}),
                html.P(id="stats-days-with-data-P", style={'color': COLORS['text_secondary']}),
                html.P(id="stats-num-devices-P", style={'color': COLORS['text_secondary']}),
                html.P(id="stats-unique-tokens-P", style={'color': COLORS['text_secondary']})
            ], style={**panel_style_base, 'borderLeft': f'5px solid {COLORS["warning"]}'}),
            
            # Active Devices Panel
            html.Div([
                html.H3("Most active devices", style={'color': COLORS['text_primary']}),
                html.Table([
                    html.Thead(html.Tr([
                        html.Th("DEVICE", style={'color': COLORS['text_primary']}),
                        html.Th("EVENTS", style={'color': COLORS['text_primary']})
                    ])),
                    html.Tbody(id='most-active-devices-table-body')
                ])
            ], style={**panel_style_base, 'borderLeft': f'5px solid {COLORS["critical"]}'})
        ]
    )


def create_graph_container_hidden():
    """
    Graph container that is HIDDEN by default - only shown after processing
    """
    try:
        from ui.themes.graph_styles import (
            centered_graph_box_style,
            cytoscape_inside_box_style,
            tap_node_data_centered_style,
            actual_default_stylesheet_for_graph
        )
    except ImportError:
        # Fallback styles
        centered_graph_box_style = {
            'width': '90%',
            'margin': '0 auto',
            'padding': '20px',
            'backgroundColor': COLORS['surface'],
            'borderRadius': '8px'
        }
        cytoscape_inside_box_style = {
            'width': '100%',
            'height': '600px'
        }
        tap_node_data_centered_style = {
            'textAlign': 'center',
            'padding': '10px',
            'color': COLORS['text_primary']
        }
        actual_default_stylesheet_for_graph = []

    return html.Div(
        id='graph-output-container',
        style={'display': 'none'},  # EXPLICITLY HIDDEN
        children=[
            html.H2(
                "Area Layout Model",
                id="area-layout-model-title",
                style={
                    'textAlign': 'center',
                    'color': COLORS['text_primary'],
                    'marginBottom': '20px',
                    'fontSize': '1.8rem'
                }
            ),
            html.Div(
                id='cytoscape-graphs-area',
                style=centered_graph_box_style,
                children=[
                    cyto.Cytoscape(
                        id='onion-graph',
                        layout={
                            'name': 'cose',
                            'idealEdgeLength': 100,
                            'nodeOverlap': 20,
                            'refresh': 20,
                            'fit': True,
                            'padding': 30,
                            'randomize': False,
                            'componentSpacing': 100,
                            'nodeRepulsion': 400000,
                            'edgeElasticity': 100,
                            'nestingFactor': 5,
                            'gravity': 80,
                            'numIter': 1000,
                            'coolingFactor': 0.95,
                            'minTemp': 1.0
                        },
                        style=cytoscape_inside_box_style,
                        elements=[],
                        stylesheet=actual_default_stylesheet_for_graph
                    )
                ]
            ),
            html.Pre(
                id='tap-node-data-output',
                style=tap_node_data_centered_style,
                children="Upload CSV, map headers, (optionally classify doors), then Confirm & Generate. Tap a node for its details."
            )
        ]
    )


def create_interactive_setup_container_fixed():
    """
    Creates the interactive‐setup container - initially hidden until file upload
    """
    return html.Div(
        id='interactive-setup-container',
        style={'display': 'none'},  # Hidden until file uploaded
        children=[
            # Step 1: CSV Header Mapping
            create_mapping_section_with_fallback(),

            # Step 2 & 3: Facility Setup + Door Classification
            create_classification_section(),

            # Final "Generate" Button
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
    """
    Creates a simple CSV‐upload component if no custom upload UI is provided.
    """
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
                    html.H3(
                        "Drop your CSV file here",
                        style={
                            'margin': '0',
                            'fontSize': '1.125rem',
                            'fontWeight': '600',
                            'color': COLORS['text_primary'],
                            'marginBottom': '5px'
                        }
                    ),
                    html.P(
                        "or click to browse",
                        style={
                            'margin': '0',
                            'fontSize': '0.875rem',
                            'color': COLORS['text_secondary'],
                        }
                    ),
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
    """Creates the main header bar at the top of the app"""
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
            html.H1(
                "Analytics Dashboard",
                style={
                    'fontSize': '1.8rem',
                    'margin': '0',
                    'color': COLORS['text_primary'],
                    'position': 'absolute',
                    'left': '50%',
                    'transform': 'translateX(-50%)'
                }
            )
        ]
    )


def create_upload_section(upload_component):
    """Wraps the provided upload component in a container"""
    return html.Div(
        [upload_component.create_upload_area()],
        style={'marginBottom': '20px'}
    )


def create_mapping_section_with_fallback():
    """Step 1: Map CSV Headers - with fallback UI"""
    try:
        from ui.components.mapping import create_mapping_component
        mapping_component = create_mapping_component()
        return mapping_component.create_mapping_section()
    except ImportError:
        # Fallback UI
        return html.Div(
            id='mapping-ui-section',
            style={'marginBottom': '40px'},
            children=[
                html.H4(
                    "Step 1: Map CSV Headers",
                    style={
                        'color': COLORS['text_primary'],
                        'fontSize': '1.3rem',
                        'marginBottom': '1rem',
                        'textAlign': 'center'
                    }
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
                    })
                ], style={'marginBottom': '12px'}),

                # Placeholder for dropdowns
                html.Div(id='dropdown-mapping-area'),

                # Hidden validation message div
                html.Div(id='mapping-validation-message', style={'display': 'none'}),

                # Confirm button
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
    """Step 2 & 3: Facility Setup + Door Classification with modern UI"""
    try:
        from ui.components.classification import create_classification_component
        classification_component = create_classification_component()
        return classification_component.create_entrance_verification_section()
    except ImportError:
        # Fallback UI with modern components
        return html.Div(
            id='entrance-verification-ui-section',
            style={'display': 'none'},
            children=[
                # === Step 2: Facility Setup Card ===
                html.Div(
                    [
                        html.H4(
                            "Step 2: Facility Setup",
                            style={
                                'color': COLORS['text_primary'],
                                'textAlign': 'center',
                                'marginBottom': '16px',
                                'fontSize': '1.3rem'
                            }
                        ),

                        # ── Modern Floors Slider (replacing dropdown) ─────────────────────────
                        html.Label(
                            "How many floors are in the facility?",
                            style={
                                'color': COLORS['text_primary'],
                                'fontWeight': 'bold',
                                'fontSize': '1rem',
                                'marginBottom': '8px',
                                'textAlign': 'center',
                                'display': 'block'
                            }
                        ),
                        dcc.Slider(
                            id="num-floors-input",  # Keep same ID for compatibility
                            min=1,
                            max=20,
                            step=1,
                            value=4,  # Default 4 floors
                            marks={i: str(i) for i in range(1, 21, 2)},  # Every 2nd number
                            tooltip={"always_visible": False, "placement": "bottom"},
                            updatemode="drag",
                            className="modern-floor-slider",
                            style={'marginBottom': '6px'}
                        ),
                        html.Div(
                            id="num-floors-display",
                            style={
                                "fontSize": "0.9rem",
                                "color": COLORS['text_secondary'],
                                "marginTop": "6px",
                                "textAlign": "center",
                                "fontWeight": "600"
                            }
                        ),
                        html.Div(
                            "Count floors above ground including mezzanines and secure zones",
                            style={
                                "fontSize": "0.8rem",
                                "color": COLORS['text_tertiary'],
                                "marginTop": "4px",
                                "textAlign": "center",
                                "marginBottom": "24px"
                            }
                        ),
                        # ── End Modern Floors Slider ──────────────────────────────────────────

                        # ── Modern Toggle Switch (replacing radio items) ──────────────────────
                        html.Label(
                            "Enable Manual Door Classification?",
                            style={
                                'color': COLORS['text_primary'],
                                'fontWeight': 'bold',
                                'fontSize': '1rem',
                                'marginBottom': '12px',
                                'textAlign': 'center',
                                'display': 'block'
                            }
                        ),
                        
                        # Modern Toggle Switch Container
                        html.Div([
                            # Hidden radio items for functionality (keep existing logic)
                            dcc.RadioItems(
                                id='manual-map-toggle',
                                options=[
                                    {'label': '', 'value': 'no'}, 
                                    {'label': '', 'value': 'yes'}
                                ],
                                value='no',  # Default to No
                                style={'display': 'none'}  # Hide the actual radio items
                            ),
                            
                            # Visual Toggle Switch
                            html.Div([
                                html.Div([
                                    html.Span("No", className="toggle-label-left"),
                                    html.Div([
                                        html.Div(className="toggle-slider")
                                    ], className="toggle-switch"),
                                    html.Span("Yes", className="toggle-label-right")
                                ], className="toggle-container", id="visual-toggle")
                            ], className="modern-toggle-wrapper")
                        ], style={
                            'display': 'flex',
                            'justifyContent': 'center',
                            'alignItems': 'center'
                        })
                        # ── End Modern Toggle Switch ───────────────────────────────────────────
                    ],
                    style={
                        'padding': '20px',
                        'backgroundColor': COLORS['surface'],
                        'borderRadius': '8px',
                        'marginBottom': '20px',
                        'border': f'1px solid {COLORS["border"]}',
                        'maxWidth': '550px',
                        'margin': '0 auto'
                    }
                ),

                # === Step 3: Door Classification Table Container (hidden initially) ===
                html.Div(
                    id="door-classification-table-container",
                    style={'display': 'none'},
                    children=[
                        html.H4(
                            "Step 3: Door Classification",
                            style={
                                'color': COLORS['text_primary'],
                                'textAlign': 'center',
                                'marginBottom': '12px',
                                'fontSize': '1.3rem'
                            }
                        ),
                        html.P(
                            "Assign a security level to each door below:",
                            style={'color': COLORS['text_primary'], 'textAlign': 'center', 'marginBottom': '8px'}
                        ),
                        html.Div(id="door-classification-table")
                    ]
                )
            ]
        )


def create_processing_status():
    """Processing status indicator"""
    return html.Div(
        id='processing-status',
        style={
            'marginTop': '10px',
            'color': COLORS['accent'],
            'textAlign': 'center'
        }
    )


def create_data_stores():
    """Create all dcc.Store() components for state management"""
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
    """Returns the style for the main container"""
    return {
        'backgroundColor': COLORS['background'],
        'padding': '20px',
        'minHeight': '100vh',
        'fontFamily': 'Arial, sans-serif'
    }


def register_page_callbacks(app):
    """Register page-specific callbacks"""
    @app.callback(
        [
            Output("num-floors-display", "children"),
            Output("num-floors-store", "data")
        ],
        Input("num-floors-slider", "value"),
    )
    def update_floor_number(n):
        display_text = f"{n} floor{'s' if n != 1 else ''}"
        return display_text, n