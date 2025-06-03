# ui/pages/enhanced_main_page.py
"""
Enhanced Main Page Layout - Integrates enhanced statistics with existing application
Maintains exact same style and flow while adding powerful new analytics capabilities
"""

from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import dash_cytoscape as cyto
import dash_bootstrap_components as dbc

# Import enhanced components
from ui.components.enhanced_stats import create_enhanced_stats_component

# Import existing theme constants
try:
    from ui.themes.style_config import COLORS, UI_VISIBILITY, UI_COMPONENTS, BORDER_RADIUS, SHADOWS
except ImportError:
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

# Import constants
try:
    from config.settings import REQUIRED_INTERNAL_COLUMNS
except ImportError:
    try:
        from utils.constants import REQUIRED_INTERNAL_COLUMNS
    except ImportError:
        REQUIRED_INTERNAL_COLUMNS = {
            'Timestamp': 'Timestamp (Event Time)',
            'UserID': 'UserID (Person Identifier)',
            'DoorID': 'DoorID (Device Name)',
            'EventType': 'EventType (Access Result)'
        }


def create_enhanced_main_layout(app_instance, main_logo_path, icon_upload_default, upload_component=None):
    """
    Creates the enhanced main application layout with comprehensive analytics
    Maintains compatibility with existing system while adding powerful new features
    """
    
    # If no upload component provided, create fallback
    if upload_component is None:
        upload_component = _create_fallback_upload_component(app_instance, icon_upload_default)

    layout = html.Div(
        children=[
            # Main Header Bar (unchanged)
            create_main_header(main_logo_path),

            # Upload Section (unchanged - uses existing component)
            create_upload_section(upload_component),

            # Interactive Setup Container: Mapping + Classification + Generate Button (unchanged)
            create_interactive_setup_container_fixed(),

            # Processing Status Indicator (unchanged)
            create_processing_status(),

            # === NEW: Enhanced Statistics Section ===
            html.Div(
                id='enhanced-analytics-section',
                style={'display': 'none'},  # Hidden until processing complete
                children=[
                    create_enhanced_stats_component().create_enhanced_stats_container()
                ]
            ),

            # === ORIGINAL: Graph Output Container (hidden until after processing) ===
            create_graph_container_hidden(),

            # Data Stores (enhanced with new stores)
            create_enhanced_data_stores(),
        ],
        style=get_main_container_style()
    )

    return layout


def create_enhanced_data_stores():
    """Create enhanced data stores including new analytics stores"""
    return html.Div([
        # Original stores (unchanged)
        dcc.Store(id='uploaded-file-store'),
        dcc.Store(id='csv-headers-store', storage_type='session'),
        dcc.Store(id='column-mapping-store', storage_type='local'),
        dcc.Store(id='ranked-doors-store', storage_type='session'),
        dcc.Store(id='current-entrance-offset-store', data=0, storage_type='session'),
        dcc.Store(id='manual-door-classifications-store', storage_type='local'),
        dcc.Store(id='num-floors-store', storage_type='session', data=1),
        dcc.Store(id='all-doors-from-csv-store', storage_type='session'),
        
        # === NEW: Enhanced Analytics Stores ===
        dcc.Store(id='enhanced-stats-data-store', storage_type='session'),
        dcc.Store(id='chart-data-store', storage_type='session'),
        dcc.Store(id='export-data-store', storage_type='session'),
        dcc.Store(id='analytics-config-store', storage_type='local', data={
            'auto_refresh': False,
            'refresh_interval': 30,
            'default_chart': 'hourly',
            'show_advanced_metrics': True
        }),
    ])


def create_graph_container_hidden():
    """
    Graph container that is HIDDEN by default - only shown after processing
    Enhanced to work alongside the new analytics section
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
            # Section title
            html.Div([
                html.H2(
                    "Network Visualization",
                    style={
                        'textAlign': 'center',
                        'color': COLORS['text_primary'],
                        'marginBottom': '20px',
                        'fontSize': '1.8rem'
                    }
                ),
                
                # View toggle buttons
                html.Div([
                    dbc.ButtonGroup([
                        dbc.Button("📊 Analytics View", id="view-analytics-btn", color="primary", size="sm"),
                        dbc.Button("🌐 Network View", id="view-network-btn", color="outline-primary", size="sm")
                    ])
                ], style={'textAlign': 'center', 'marginBottom': '20px'})
            ]),
            
            # Graph area
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
                children="Click 'Analytics View' for comprehensive statistics or explore the network visualization above."
            )
        ]
    )


def create_interactive_setup_container_fixed():
    """
    Creates the interactive setup container - initially hidden until file upload
    Enhanced with better integration points for analytics
    """
    return html.Div(
        id='interactive-setup-container',
        style={'display': 'none'},  # Hidden until file uploaded
        children=[
            # Step 1: CSV Header Mapping
            create_mapping_section_with_fallback(),

            # Step 2 & 3: Facility Setup + Door Classification
            create_classification_section(),

            # Enhanced Generate Button with analytics preview
            html.Div([
                dbc.Button(
                    [
                        html.I(className="fas fa-chart-line me-2"),
                        'Generate Analytics Dashboard'
                    ],
                    id='confirm-and-generate-button',
                    n_clicks=0,
                    color='primary',
                    size='lg',
                    className='w-100 mb-3',
                    style={
                        'background': f'linear-gradient(135deg, {COLORS["accent"]}, {COLORS["success"]})',
                        'border': 'none',
                        'boxShadow': '0 4px 15px rgba(33, 150, 243, 0.3)',
                        'transition': 'all 0.3s ease'
                    }
                ),
                
                # Processing preview
                html.Div(
                    id='processing-preview',
                    style={'display': 'none'},
                    children=[
                        html.Div([
                            html.Div(className="spinner-border spinner-border-sm me-2"),
                            "Processing data and generating comprehensive analytics..."
                        ], style={
                            'textAlign': 'center',
                            'color': COLORS['text_secondary'],
                            'padding': '10px'
                        })
                    ]
                )
            ])
        ]
    )


def create_mapping_section_with_fallback():
    """Step 1: Map CSV Headers - with fallback UI (unchanged)"""
    try:
        from ui.components.mapping import create_mapping_component
        mapping_component = create_mapping_component()
        return mapping_component.create_mapping_section()
    except ImportError:
        # Fallback UI (same as original)
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
    """Enhanced classification section with better visual integration"""
    return html.Div(
        id='entrance-verification-ui-section',
        style={'display': 'none'},
        children=[
            # === Step 2: Facility Setup Card ===
            html.Div([
                html.H4(
                    "Step 2: Facility Setup",
                    style={
                        'color': COLORS['text_primary'],
                        'textAlign': 'center',
                        'marginBottom': '16px',
                        'fontSize': '1.3rem'
                    }
                ),

                # Enhanced Floors Slider
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
                    id="num-floors-input",
                    min=1,
                    max=20,
                    step=1,
                    value=1,
                    marks={i: str(i) for i in range(1, 21, 5)},
                    tooltip={"always_visible": False, "placement": "bottom"},
                    updatemode="drag",
                    className="ui-slider"
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

                # Enhanced Toggle Switch
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
                
                html.Div([
                    dcc.RadioItems(
                        id='manual-map-toggle',
                        options=[
                            {'label': 'No (Auto-classify)', 'value': 'no'}, 
                            {'label': 'Yes (Manual setup)', 'value': 'yes'}
                        ],
                        value='no',
                        inline=True,
                        className='enhanced-radio-toggle'
                    ),
                ], style={
                    'display': 'flex',
                    'justifyContent': 'center',
                    'alignItems': 'center',
                    'marginBottom': '10px'
                }),
                
                # Enhanced description
                html.Div([
                    html.P(
                        "Auto-classify uses smart defaults based on access patterns. Manual setup allows custom security levels per door.",
                        style={
                            'color': COLORS['text_tertiary'],
                            'fontSize': '0.8rem',
                            'textAlign': 'center',
                            'margin': '10px 0'
                        }
                    )
                ])
                
            ], style={
                'padding': '20px',
                'backgroundColor': COLORS['surface'],
                'borderRadius': '8px',
                'marginBottom': '20px',
                'border': f'1px solid {COLORS["border"]}',
                'maxWidth': '550px',
                'margin': '0 auto 20px auto',
                'boxShadow': '0 4px 12px rgba(0,0,0,0.1)'
            }),

            # === Step 3: Door Classification Table Container ===
            html.Div(
                id="door-classification-table-container",
                style={'display': 'none'},
                children=[
                    html.Div([
                        html.H4(
                            "Step 3: Door Classification",
                            style={
                                'color': COLORS['text_primary'],
                                'textAlign': 'center',
                                'marginBottom': '12px',
                                'fontSize': '1.3rem'
                            }
                        ),
                        html.P([
                            "Assign security levels and types to each door. This will enhance the analytics with detailed insights.",
                            html.Br(),
                            html.Small("💡 Higher security levels (red) indicate restricted access areas", 
                                     style={'color': COLORS['text_tertiary']})
                        ], style={
                            'color': COLORS['text_primary'], 
                            'textAlign': 'center', 
                            'marginBottom': '15px'
                        }),
                        html.Div(id="door-classification-table")
                    ], style={
                        'padding': '20px',
                        'backgroundColor': COLORS['surface'],
                        'borderRadius': '8px',
                        'border': f'1px solid {COLORS["border"]}',
                        'boxShadow': '0 4px 12px rgba(0,0,0,0.1)'
                    })
                ]
            )
        ]
    )


def create_main_header(main_logo_path):
    """Creates the main header bar at the top of the app (unchanged)"""
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
                "Enhanced Analytics Dashboard",
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
    """Wraps the provided upload component in a container (unchanged)"""
    return html.Div(
        [upload_component.create_upload_area()],
        style={'marginBottom': '20px'}
    )


def create_processing_status():
    """Enhanced processing status indicator"""
    return html.Div([
        html.Div(
            id='processing-status',
            style={
                'marginTop': '10px',
                'color': COLORS['accent'],
                'textAlign': 'center',
                'padding': '10px',
                'borderRadius': '5px',
                'backgroundColor': 'rgba(33, 150, 243, 0.1)',
                'border': f'1px solid rgba(33, 150, 243, 0.3)',
                'display': 'none'
            }
        )
    ])


def get_main_container_style():
    """Returns the style for the main container (unchanged)"""
    return {
        'backgroundColor': COLORS['background'],
        'padding': '20px',
        'minHeight': '100vh',
        'fontFamily': 'Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif'
    }


def _create_fallback_upload_component(app_instance, icon_upload_default):
    """
    Creates a simple CSV upload component if no custom upload UI is provided (unchanged)
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


def register_enhanced_page_callbacks(app):
    """
    Register enhanced page-specific callbacks
    Including view switching between analytics and network views
    """
    
    @app.callback(
        [
            Output('enhanced-analytics-section', 'style'),
            Output('graph-output-container', 'style'),
            Output('view-analytics-btn', 'color'),
            Output('view-network-btn', 'color')
        ],
        [
            Input('view-analytics-btn', 'n_clicks'),
            Input('view-network-btn', 'n_clicks'),
            Input('confirm-and-generate-button', 'n_clicks')
        ],
        prevent_initial_call=True
    )
    def toggle_views(analytics_clicks, network_clicks, generate_clicks):
        """Toggle between analytics and network views"""
        from dash import ctx
        
        if not generate_clicks:
            # Before generation - hide both
            return (
                {'display': 'none'}, 
                {'display': 'none'},
                'primary', 'outline-primary'
            )
        
        # After generation - determine which view to show
        if not ctx.triggered:
            # Default to analytics view
            return (
                {'display': 'block'}, 
                {'display': 'none'},
                'primary', 'outline-primary'
            )
        
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        
        if button_id == 'view-analytics-btn':
            return (
                {'display': 'block'}, 
                {'display': 'none'},
                'primary', 'outline-primary'
            )
        elif button_id == 'view-network-btn':
            return (
                {'display': 'none'}, 
                {'display': 'block'},
                'outline-primary', 'primary'
            )
        else:
            # Default to analytics
            return (
                {'display': 'block'}, 
                {'display': 'none'},
                'primary', 'outline-primary'
            )
    
    @app.callback(
        Output('processing-preview', 'style'),
        [Input('confirm-and-generate-button', 'n_clicks')],
        prevent_initial_call=True
    )
    def show_processing_preview(n_clicks):
        """Show processing preview when generate button is clicked"""
        if n_clicks:
            return {'display': 'block'}
        return {'display': 'none'}