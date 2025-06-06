# ui/pages/main_page.py - FIXED VERSION - Removes UI Conflicts

"""
Main page layout - STREAMLINED AND CONFLICT-FREE
All callbacks are handled by unified handler in app.py
"""

from dash import html, dcc
import dash_cytoscape as cyto
from ui.components.classification import create_classification_component
from ui.themes.style_config import COLORS
from config.settings import REQUIRED_INTERNAL_COLUMNS
# Instantiate the reusable classification component for entrance verification
classification_component = create_classification_component()

def create_main_layout(app_instance, main_logo_path, icon_upload_default):
    """
    Creates the main application layout - STREAMLINED VERSION
    """
    
    layout = html.Div(
        children=[
            # Main Header Bar
            create_main_header(main_logo_path),

            # Upload Section - SIMPLIFIED
            create_upload_section(icon_upload_default),

            # Interactive Setup Container - SIMPLIFIED
            create_interactive_setup_container(),

            # Processing Status
            html.Div(
                id='processing-status',
                style={
                    'marginTop': '20px',
                    'color': COLORS['accent'],
                    'textAlign': 'center',
                    'fontSize': '1rem',
                    'fontWeight': '500'
                }
            ),

            # Results Section - HIDDEN until processing
            create_results_section(),

            # Data Stores
            create_data_stores(),
        ],
        style={
            'backgroundColor': COLORS['background'],
            'padding': '20px',
            'minHeight': '100vh',
            'fontFamily': 'Inter, system-ui, sans-serif'
        }
    )

    return layout

def create_main_header(main_logo_path):
    """Creates the main header bar"""
    return html.Div(
        style={
            'display': 'flex',
            'alignItems': 'center',
            'justifyContent': 'center',
            'padding': '20px 30px',
            'backgroundColor': COLORS['surface'],
            'borderBottom': f'1px solid {COLORS["border"]}',
            'marginBottom': '30px',
            'borderRadius': '8px',
        },
        children=[
            html.Img(src=main_logo_path, style={'height': '40px', 'marginRight': '15px'}),
            html.H1(
                "Enhanced Analytics Dashboard",
                style={
                    'fontSize': '1.8rem',
                    'margin': '0',
                    'color': COLORS['text_primary'],
                    'fontWeight': '600'
                }
            )
        ]
    )

def create_upload_section(icon_upload_default):
    """Upload section - SIMPLIFIED"""
    return html.Div([
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                html.Img(
                    id='upload-icon',
                    src=icon_upload_default,
                    style={
                        'width': '96px',
                        'height': '96px',
                        'marginBottom': '15px',
                        'opacity': '0.8'
                    }
                ),
                html.H3(
                    "Drop your CSV or JSON file here",
                    style={
                        'margin': '0',
                        'fontSize': '1.2rem',
                        'fontWeight': '600',
                        'color': COLORS['text_primary'],
                        'marginBottom': '5px'
                    }
                ),
                html.P(
                    "or click to browse",
                    style={
                        'margin': '0',
                        'fontSize': '0.9rem',
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
                'margin': '0 auto 30px auto',
                'display': 'flex',
                'alignItems': 'center',
                'justifyContent': 'center',
                'cursor': 'pointer',
                'transition': 'all 0.3s ease',
                'border': f'2px dashed {COLORS["border"]}',
                'backgroundColor': COLORS['surface'],
            },
            multiple=False,
            accept='.csv,.json'
        )
    ])

def create_interactive_setup_container():
    """Interactive setup container - SIMPLIFIED"""
    return html.Div(
        id='interactive-setup-container',
        style={'display': 'none'},
        children=[
            # Step 1: CSV Header Mapping
            create_mapping_section(),

            # Step 2 & 3: Entrance Verification Section (facility setup and classification)
            classification_component.create_entrance_verification_section(),

            # Generate Button
            html.Button(
                'Confirm Selections & Generate Analysis',
                id='confirm-and-generate-button',
                n_clicks=0,
                style={
                    'width': '100%',
                    'maxWidth': '400px',
                    'margin': '30px auto',
                    'display': 'block',
                    'padding': '15px 25px',
                    'backgroundColor': COLORS['accent'],
                    'color': 'white',
                    'border': 'none',
                    'borderRadius': '8px',
                    'fontSize': '1.1rem',
                    'fontWeight': '600',
                    'cursor': 'pointer',
                    'transition': 'all 0.3s ease'
                }
            )
        ]
    )

def create_mapping_section():
    """Step 1: Map CSV Headers (wrapped in mapping-ui-section for callback control)"""
    return html.Div(
        id='mapping-ui-section',  # ✅ Enables callback to toggle visibility
        style={
            'display': 'none',  # Hidden by default until needed
            'backgroundColor': COLORS['surface'],
            'padding': '25px',
            'borderRadius': '8px',
            'marginBottom': '20px',
            'border': f'1px solid {COLORS["border"]}'
        },
        children=[
            html.H4(
                "Step 1: Map CSV Headers",
                style={
                    'color': COLORS['text_primary'],
                    'fontSize': '1.3rem',
                    'marginBottom': '15px',
                    'textAlign': 'center'
                }
            ),
            html.P(
                "Map your CSV columns to the required fields below:",
                style={
                    'color': COLORS['text_secondary'],
                    'fontSize': '0.9rem',
                    'marginBottom': '20px',
                    'textAlign': 'center'
                }
            ),

            # Dropdown area
            html.Div(id='dropdown-mapping-area'),

            # Confirm button
            html.Button(
                'Confirm Header Mapping',
                id='confirm-header-map-button',
                n_clicks=0,
                style={
                    'display': 'none',  # Hidden until dropdowns are created
                    'margin': '20px auto',
                    'padding': '10px 20px',
                    'backgroundColor': COLORS['success'],
                    'color': 'white',
                    'border': 'none',
                    'borderRadius': '6px',
                    'cursor': 'pointer'
                }
            )
        ]
    )

def create_facility_setup():
    """Step 2: Facility Setup"""
    return html.Div([
        html.H4(
            "Step 2: Facility Setup",
            style={
                'color': COLORS['text_primary'],
                'fontSize': '1.3rem',
                'marginBottom': '15px',
                'textAlign': 'center'
            }
        ),
        
        # Number of floors
        html.Div([
            html.Label(
                "How many floors are in the facility?",
                style={
                    'color': COLORS['text_primary'],
                    'fontWeight': '600',
                    'fontSize': '1rem',
                    'marginBottom': '10px',
                    'display': 'block',
                    'textAlign': 'center'
                }
            ),
            dcc.Slider(
                id="num-floors-input",
                min=1,
                max=20,
                step=1,
                value=4,
                marks={i: str(i) for i in range(0, 101, 5)},
                tooltip={"always_visible": False, "placement": "bottom"}
            ),
            html.Div(
                id="num-floors-display",
                children="4 floors",
                style={
                    "fontSize": "0.9rem",
                    "color": COLORS['text_secondary'],
                    "marginTop": "10px",
                    "textAlign": "center",
                    "fontWeight": "600"
                }
            ),
        ], style={'marginBottom': '25px'}),
        
        # Manual classification toggle
        html.Div([
            html.Label(
                "Enable Manual Door Classification?",
                style={
                    'color': COLORS['text_primary'],
                    'fontWeight': '600',
                    'fontSize': '1rem',
                    'marginBottom': '15px',
                    'display': 'block',
                    'textAlign': 'center'
                }
            ),
            dcc.RadioItems(
                id='manual-map-toggle',
                options=[
                    {'label': ' No (Automatic)', 'value': 'no'},
                    {'label': ' Yes (Manual)', 'value': 'yes'}
                ],
                value='no',
                inline=True,
                style={'textAlign': 'center'},
                labelStyle={
                    'display': 'inline-block',
                    'marginRight': '20px',
                    'padding': '10px 20px',
                    'backgroundColor': COLORS['border'],
                    'color': COLORS['text_secondary'],
                    'borderRadius': '20px',
                    'cursor': 'pointer',
                    'transition': 'all 0.3s ease'
                }
            ),
        ])
    ], style={
        'backgroundColor': COLORS['surface'],
        'padding': '25px',
        'borderRadius': '8px',
        'marginBottom': '20px',
        'border': f'1px solid {COLORS["border"]}'
    })

def create_classification_section():
    """Step 3: Door Classification (conditional)"""
    return html.Div(
        id="door-classification-table-container",
        style={'display': 'none'},
        children=[
            html.Div([
                html.H4(
                    "Step 3: Door Classification",
                    style={
                        'color': COLORS['text_primary'],
                        'fontSize': '1.3rem',
                        'marginBottom': '15px',
                        'textAlign': 'center'
                    }
                ),
                html.P(
                    "Classify each door below:",
                    style={
                        'color': COLORS['text_secondary'],
                        'marginBottom': '20px',
                        'textAlign': 'center'
                    }
                ),
                html.Div(id="door-classification-table")
            ], style={
                'backgroundColor': COLORS['surface'],
                'padding': '25px',
                'borderRadius': '8px',
                'border': f'1px solid {COLORS["border"]}'
            })
        ]
    )

def create_results_section():
    """Results section - hidden until processing complete"""
    return html.Div([
        # Custom Header (hidden)
        html.Div(
            id='yosai-custom-header',
            style={'display': 'none'},
            children=[
                html.Div([
                    html.H2(
                        "📊 Analysis Results",
                        style={
                            'color': COLORS['text_primary'],
                            'textAlign': 'center',
                            'margin': '0',
                            'fontSize': '1.6rem'
                        }
                    )
                ], style={
                    'padding': '20px',
                    'backgroundColor': COLORS['surface'],
                    'borderRadius': '8px',
                    'marginBottom': '20px',
                    'border': f'1px solid {COLORS["border"]}'
                })
            ]
        ),

        # Statistics Panels (hidden)
        create_stats_panels(),

        # Graph Container (hidden)
        create_graph_container(),

        # Analytics Section (initially hidden)
        html.Div(
            id='analytics-section',
            style={'display': 'none'},
            children=[
                html.H2("📈 Advanced Analytics", style={'textAlign': 'center'}),
                html.Div(id='analytics-detailed-breakdown')
            ]
        ),

        # Charts Section (hidden until data is ready)
        html.Div(
            id='charts-section',
            style={'display': 'none'},
            children=[
                html.H2("📊 Data Visualization", style={'textAlign': 'center'})
            ]
        ),

        # Export Section (hidden until data is ready)
        html.Div(
            id='export-section',
            style={'display': 'none'},
            children=[
                html.H2("📤 Export & Reports", style={'textAlign': 'center'})
            ]
        )
    ])


def create_stats_panels():
    """Statistics panels"""
    panel_style = {
        'flex': '1',
        'padding': '20px',
        'margin': '0 10px',
        'backgroundColor': COLORS['surface'],
        'borderRadius': '8px',
        'textAlign': 'center',
        'border': f'1px solid {COLORS["border"]}',
        'minWidth': '200px'
    }

    return html.Div(
        id='stats-panels-container',
        style={'display': 'none'},
        children=[
            # Access Events Panel
            html.Div([
                html.H3("Access Events", style={'color': COLORS['text_primary'], 'marginBottom': '10px'}),
                html.H1(id="total-access-events-H1", style={'color': COLORS['accent'], 'margin': '10px 0'}),
                html.P(id="event-date-range-P", style={'color': COLORS['text_secondary'], 'fontSize': '0.9rem'})
            ], style=panel_style),

            # Statistics Panel
            html.Div([
                html.H3("Summary", style={'color': COLORS['text_primary'], 'marginBottom': '10px'}),
                html.P(id="stats-date-range-P", style={'color': COLORS['text_secondary'], 'fontSize': '0.8rem'}),
                html.P(id="stats-days-with-data-P", style={'color': COLORS['text_secondary'], 'fontSize': '0.8rem'}),
                html.P(id="stats-num-devices-P", style={'color': COLORS['text_secondary'], 'fontSize': '0.8rem'}),
                html.P(id="stats-unique-tokens-P", style={'color': COLORS['text_secondary'], 'fontSize': '0.8rem'})
            ], style=panel_style),

            # Active Devices Panel
            html.Div([
                html.H3("Top Devices", style={'color': COLORS['text_primary'], 'marginBottom': '10px'}),
                html.Table([
                    html.Thead(html.Tr([
                        html.Th("Device", style={'color': COLORS['text_primary'], 'fontSize': '0.8rem'}),
                        html.Th("Events", style={'color': COLORS['text_primary'], 'fontSize': '0.8rem'})
                    ])),
                    html.Tbody(id='most-active-devices-table-body')
                ], style={'width': '100%', 'fontSize': '0.8rem'})
            ], style=panel_style)
        ]
    )

def create_graph_container():
    """Graph visualization container"""
    return html.Div(
        id='graph-output-container',
        style={'display': 'none'},
        children=[
            html.H2(
                "🗺️ Facility Layout Model",
                style={
                    'textAlign': 'center',
                    'color': COLORS['text_primary'],
                    'marginBottom': '20px',
                    'fontSize': '1.6rem'
                }
            ),
            html.Div(
                children=[
                    cyto.Cytoscape(
                        id='onion-graph',
                        layout={'name': 'cose', 'fit': True},
                        style={
                            'width': '100%',
                            'height': '500px',
                            'backgroundColor': COLORS['background'],
                            'borderRadius': '8px'
                        },
                        elements=[],
                        stylesheet=[
                            {
                                'selector': 'node',
                                'style': {
                                    'background-color': COLORS['accent'],
                                    'label': 'data(label)',
                                    'color': 'white',
                                    'text-valign': 'center',
                                    'width': 40,
                                    'height': 40
                                }
                            },
                            {
                                'selector': 'edge',
                                'style': {
                                    'line-color': COLORS['border'],
                                    'width': 2
                                }
                            }
                        ]
                    )
                ],
                style={
                    'backgroundColor': COLORS['surface'],
                    'padding': '20px',
                    'borderRadius': '8px',
                    'border': f'1px solid {COLORS["border"]}'
                }
            ),
            html.Pre(
                id='tap-node-data-output',
                children="Generate analysis to see the facility layout. Tap nodes for details.",
                style={
                    'backgroundColor': COLORS['surface'],
                    'color': COLORS['text_secondary'],
                    'padding': '15px',
                    'borderRadius': '8px',
                    'marginTop': '20px',
                    'textAlign': 'center',
                    'border': f'1px solid {COLORS["border"]}',
                    'fontSize': '0.9rem'
                }
            )
        ]
    )

def create_data_stores():
    """Create all data store components"""
    return html.Div([
        dcc.Store(id='uploaded-file-store'),
        dcc.Store(id='csv-headers-store'),
        dcc.Store(id='column-mapping-store', storage_type='local'),
        dcc.Store(id='all-doors-from-csv-store'),
        dcc.Store(id='manual-door-classifications-store', storage_type='local'),
        dcc.Store(id='num-floors-store', data=4),
    ])