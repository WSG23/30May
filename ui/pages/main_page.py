# ui/pages/main_page.py

"""
Main page layout (CSV mapping + Facility Setup + Door Classification + Generate button) 
with a dark‐themed, glow‐effect slider for “Floors.” 

All original helper functions have been preserved, and the slider callback is registered
via a `register_page_callbacks(app)` function to avoid “app is not defined” errors.
"""

from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import dash_cytoscape as cyto
import dash_bootstrap_components as dbc

# Import your theme constants
from ui.themes.style_config import COLORS, UI_VISIBILITY, UI_COMPONENTS, BORDER_RADIUS, SHADOWS
from ui.themes.graph_styles import (
    centered_graph_box_style,
    cytoscape_inside_box_style,
    tap_node_data_centered_style,
    actual_default_stylesheet_for_graph
)

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
    Creates the main application layout with properly included mapping and classification sections.
    If `upload_component` is None, uses a simple fallback CSV‐upload UI.
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

            # Custom Header (shown after processing)
            create_custom_header(main_logo_path),

            # Statistics Panels (hidden until needed)
            create_stats_panels(),

            # Graph Output Container (hidden until needed)
            create_graph_container(),

            # Data Stores (dcc.Store elements)
            create_data_stores(),
        ],
        style=get_main_container_style()
    )

    return layout


def create_interactive_setup_container_fixed():
    """
    Creates the interactive‐setup container with:
      1) Mapping UI Section (Step 1)
      2) Classification UI Section (Step 2 + Step 3)
      3) Confirm & Generate Button
    The entire container is initially hidden (`display: none`) until a file is uploaded and parsed.
    """
    return html.Div(
        id='interactive-setup-container',
        style={'display': 'none'},
        children=[
            # Step 1: CSV Header Mapping (actual component or fallback)
            create_mapping_section_with_fallback(),

            # Step 2 & 3: Facility Setup (with slider) + Door Classification
            create_classification_section(),

            # Final “Generate” Button
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
    Returns an object with `.create_upload_area()` and `.get_upload_styles()`.
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
            """
            Returns style dictionaries for different upload states (initial, success, error).
            Useful if you want to change the border/background based on upload state.
            """
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
    """
    Creates the main header bar at the top of the app, showing a logo and title.
    The title is centered via CSS transform.
    """
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
    """
    Wraps the provided upload component in a container. This is shown before any file is loaded.
    """
    return html.Div(
        [upload_component.create_upload_area()],
        style={'marginBottom': '20px'}
    )


def create_mapping_section_with_fallback():
    """
    Step 1: “Map CSV Headers.” If you have a real mapping component (ui/components/mapping.py),
    import and use it. Otherwise, render a fallback UI:
      - A header
      - Instructions
      - A Details/UL describing each field
      - A placeholder `html.Div(id='dropdown-mapping-area')`
      - A “Confirm Header Mapping & Proceed” button
    """
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
                    }),
                    html.Details([
                        html.Summary(
                            "What do these fields mean?",
                            style={'color': COLORS['accent'], 'cursor': 'pointer', 'fontSize': '0.9rem'}
                        ),
                        html.Ul([
                            html.Li([html.Strong("Timestamp: "), "When the access event occurred"]),
                            html.Li([html.Strong("UserID: "), "Person identifier (badge number, employee ID, etc.)"]),
                            html.Li([html.Strong("DoorID: "), "Device or door identifier"]),
                            html.Li([html.Strong("EventType: "), "Access result (granted, denied, etc.)"])
                        ], style={'color': COLORS['text_secondary'], 'fontSize': '0.8rem'})
                    ])
                ], style={'marginBottom': '12px'}),

                # Placeholder for dropdowns that map CSV headers:
                html.Div(id='dropdown-mapping-area'),

                # Hidden validation message div
                html.Div(id='mapping-validation-message', style={'display': 'none'}),

                # Step 1 “Confirm Header Mapping & Proceed” button
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
    """
    Step 2 & 3: “Facility Setup” + “Door Classification.” If you have a real classification
    component (ui/components/classification.py), import and use it. Otherwise, render a fallback:
      - A “Step 2: Facility Setup” card with:
          • A “Floors:” label
          • A dark‐themed slider (1–20) that highlights the selected number
          • An always-visible div (`num-floors-display`) to show the integer (e.g. “4”)
          • A minimal helper line “Above ground only”
          • A “Manual Map?” RadioItems (Yes/No)
      - A “Step 3: Door Classification” container (hidden until triggered)
    """
    try:
        from ui.components.classification import create_classification_component
        classification_component = create_classification_component()
        return classification_component.create_entrance_verification_section()

    except ImportError:
        # FALLBACK UI for Steps 2 & 3
        return html.Div(
            id='entrance-verification-ui-section',
            style={'display': 'none'},
            children=[

                # === Step 2: Facility Setup Card ===
                html.Div(
                    [
                        html.H4(
                            "Facility Setup",
                            style={
                                'color': COLORS['text_primary'],
                                'textAlign': 'center',
                                'marginBottom': '16px',
                                'fontSize': '1.3rem'
                            }
                        ),

                        # ── “Floors:” Label ─────────────────────────────────────────────────
                        html.Label(
                            "Floors:",
                            style={
                                'color': COLORS['text_primary'],
                                'fontWeight': 'bold',
                                'fontSize': '1rem',
                                'marginBottom': '8px',
                                'textAlign': 'center',
                                'display': 'block'
                            }
                        ),

                        # ── Slider from 1 to 50 ─────────────────────────────────────────────
                        dcc.Slider(
                            id="num-floors-slider",
                            min=1,
                            max= 51,
                            step=1,
                            value=1,   # default (1 floor)
                            marks={i: str(i) for i in range(1, 51)},
                            tooltip={"always_visible": False, "placement": "bottom"},
                            updatemode="drag",
                            className="floor-slider",  # CSS hook for dark track + glow
                            style={'marginBottom': '6px'}
                        ),

                        # ── Live Display of Slider Value (just the integer) ────────────────
                        html.Div(
                            id="num-floors-display",
                            style={
                                "fontSize": "0.9rem",
                                "color": "#DDD",
                                "marginTop": "6px",
                                "textAlign": "center"
                            }
                        ),

                        # ── Minimal Helper Text ──────────────────────────────────────────────
                        html.Div(
                            "Above ground only",
                            style={
                                "fontSize": "0.8rem",
                                "color": "#777",
                                "marginTop": "4px",
                                "textAlign": "center"
                            }
                        ),

                        # ── “Manual Map?” Toggle (Yes / No) ─────────────────────────────────
                        html.Label(
                            "Manual Map?",
                            style={
                                'color': COLORS['text_primary'],
                                'fontWeight': 'bold',
                                'fontSize': '1rem',
                                'marginTop': '24px',
                                'marginBottom': '8px',
                                'textAlign': 'center',
                                'display': 'block'
                            }
                        ),
                        dcc.RadioItems(
                            id='manual-map-toggle',
                            options=[
                                {'label': 'Yes', 'value': 'yes'},
                                {'label': 'No',  'value': 'no'}
                            ],
                            value='yes',
                            inline=True,
                            labelStyle={'marginRight': '24px', 'color': COLORS['text_primary']},
                            inputStyle={'marginRight': '6px'}
                        ),
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

                # === Step 3: Door Classification Table Container (initially hidden) ===
                html.Div(
                    id="door-classification-table-container",
                    style={'display': 'none'},
                    children=[
                        html.H4(
                            "Door Classification",
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
    """
    Step 4: A simple status indicator (e.g., “Processing…”). 
    Initially hidden; shown while backend is processing the CSV.
    """
    return html.Div(
        id='processing-status',
        style={
            'marginTop': '10px',
            'color': COLORS['accent'],
            'textAlign': 'center'
        }
    )


def create_custom_header(main_logo_path):
    """
    Step 5: Custom header shown after processing. 
    If ui/components/stats.py is available, use it; otherwise, render an empty div.
    """
    try:
        from ui.components.stats import create_stats_component
        stats_component = create_stats_component()
        return stats_component.create_custom_header(main_logo_path)
    except ImportError:
        return html.Div(id='yosai-custom-header', style={'display': 'none'})


def create_stats_panels():
    """
    Step 6: Statistics panels (e.g., summary metrics). 
    If ui/components/stats.py is available, use it; otherwise, hidden.
    """
    try:
        from ui.components.stats import create_stats_component
        stats_component = create_stats_component()
        return stats_component.create_stats_container()
    except ImportError:
        return html.Div(id='stats-panels-container', style={'display': 'none'})


def create_graph_container():
    """
    Step 7: Graph visualization container (e.g., cytoscape component). 
    If ui/components/graph.py is available, use it; otherwise, hidden.
    """
    try:
        from ui.components.graph import create_graph_component
        graph_component = create_graph_component()
        return graph_component.create_graph_container()
    except ImportError:
        return html.Div(id='graph-output-container', style={'display': 'none'})


def create_data_stores():
    """
    Step 8: Create all dcc.Store() components for state management. 
    These hold parsed CSV, mapped columns, door lists, floor count, etc.
    """
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
    """
    Returns the style for the main container.
    """
    return {
        'backgroundColor': COLORS['background'],
        'padding': '20px',
        'minHeight': '100vh',
        'fontFamily': 'Arial, sans-serif'
    }


def register_page_callbacks(app):
    """
    Call this from your server‐setup code (e.g., in app.py) after instantiating Dash:
    
        from ui.pages.main_page import register_page_callbacks
        app = Dash(__name__, external_stylesheets=[…])
        register_page_callbacks(app)
    
    Wiring:
      • Updates the “num-floors-display” div whenever “num-floors-slider” changes.
    """
    @app.callback(
    [
        Output("num-floors-display", "children"),
        Output("num-floors-store", "data")  # Add this line
    ],
    Input("num-floors-slider", "value"),
)
    def update_floor_number(n):
        # Return both the display text and the value for the store
        display_text = f"{n} floor{'s' if n != 1 else ''}"
        return display_text, n  # Return both values
