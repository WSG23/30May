# ui/pages/main_page.py - ENHANCED VERSION with Advanced Analytics

"""
Enhanced main page layout with advanced analytics, charts, and export features
"""

from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import dash_cytoscape as cyto
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from plotly.graph_objs import Figure

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
    Creates the enhanced main application layout with advanced analytics
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

            # Enhanced Custom Header (HIDDEN until after processing)
            create_enhanced_custom_header_hidden(main_logo_path),

            # Enhanced Statistics Panels with Analytics (HIDDEN until after processing)
            create_enhanced_stats_panels_hidden(),

            # NEW: Advanced Analytics Section (HIDDEN until after processing)
            create_analytics_section_hidden(),

            # NEW: Interactive Charts Section (HIDDEN until after processing)
            create_charts_section_hidden(),

            # NEW: Export and Reports Section (HIDDEN until after processing)
            create_export_section_hidden(),

            # Graph Output Container (HIDDEN until after processing)
            create_graph_container_hidden(),

            # Data Stores (dcc.Store elements)
            create_data_stores(),
        ],
        style=get_main_container_style()
    )

    return layout


def create_enhanced_custom_header_hidden(main_logo_path):
    """
    Enhanced custom header with analytics toggle - HIDDEN by default
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
                # Enhanced title
                html.Span(
                    "Enhanced Analytics Dashboard",  # UPDATED TITLE
                    style={
                        'fontSize': '18px',
                        'fontWeight': '400',
                        'color': '#ffffff',
                        'fontFamily': 'system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
                        'verticalAlign': 'middle'
                    }
                ),
                # NEW: Analytics toggle button
                html.Div([
                    html.Button(
                        "📊 Advanced View",
                        id='toggle-advanced-analytics',
                        style={
                            'marginLeft': '20px',
                            'padding': '5px 10px',
                            'backgroundColor': COLORS['accent'],
                            'color': 'white',
                            'border': 'none',
                            'borderRadius': '4px',
                            'fontSize': '0.8rem',
                            'cursor': 'pointer',
                            'transition': 'all 0.3s ease'
                        }
                    )
                ], style={'display': 'inline-block', 'verticalAlign': 'middle'})
            ], style={
                'display': 'flex',
                'alignItems': 'center',
                'justifyContent': 'center',
                'padding': '16px 0',
                'margin': '0'
            })
        ]
    )


def create_enhanced_stats_panels_hidden():
    """
    Enhanced statistics panels with additional metrics - HIDDEN by default
    """
    panel_style_base = {
        'flex': '1',
        'padding': '20px',
        'margin': '0 10px',
        'backgroundColor': COLORS['surface'],
        'borderRadius': '8px',
        'textAlign': 'center',
        'boxShadow': '2px 2px 5px rgba(0,0,0,0.2)',
        'minWidth': '200px'  # Ensure minimum width
    }
    
    return html.Div(
        id='stats-panels-container',
        style={'display': 'none'},  # EXPLICITLY HIDDEN
        children=[
            # Enhanced Access Events Panel
            html.Div([
                html.H3("Access Events", style={'color': COLORS['text_primary'], 'fontSize': '1.1rem'}),
                html.H1(id="total-access-events-H1", style={'color': COLORS['text_primary']}),
                html.P(id="event-date-range-P", style={'color': COLORS['text_secondary'], 'fontSize': '0.9rem'}),
                # NEW: Additional metrics
                html.P(id="avg-events-per-day", style={'color': COLORS['text_secondary'], 'fontSize': '0.8rem'}),
                html.P(id="peak-activity-day", style={'color': COLORS['text_secondary'], 'fontSize': '0.8rem'})
            ], style={**panel_style_base, 'borderLeft': f'5px solid {COLORS["accent"]}'}),
            
            # Enhanced User Analytics Panel (replaces old Statistics panel)
            html.Div([
                html.H3("User Analytics", style={'color': COLORS['text_primary'], 'fontSize': '1.1rem'}),
                html.P(id="stats-unique-users", style={'color': COLORS['text_secondary'], 'fontSize': '0.9rem'}),
                html.P(id="stats-avg-events-per-user", style={'color': COLORS['text_secondary'], 'fontSize': '0.8rem'}),
                html.P(id="stats-most-active-user", style={'color': COLORS['text_secondary'], 'fontSize': '0.8rem'}),
                html.P(id="stats-devices-per-user", style={'color': COLORS['text_secondary'], 'fontSize': '0.8rem'}),
                html.P(id="stats-peak-hour", style={'color': COLORS['text_secondary'], 'fontSize': '0.8rem'})
            ], style={**panel_style_base, 'borderLeft': f'5px solid {COLORS["warning"]}'}),
            
            # Enhanced Device Analytics Panel (replaces Active Devices panel)
            html.Div([
                html.H3("Device Analytics", style={'color': COLORS['text_primary'], 'fontSize': '1.1rem'}),
                html.P(id="total-devices-count", style={'color': COLORS['text_secondary'], 'fontSize': '0.9rem'}),
                html.P(id="entrance-devices-count", style={'color': COLORS['text_secondary'], 'fontSize': '0.8rem'}),
                html.P(id="high-security-devices", style={'color': COLORS['text_secondary'], 'fontSize': '0.8rem'}),
                html.Table([
                    html.Thead(html.Tr([
                        html.Th("DEVICE", style={'color': COLORS['text_primary'], 'fontSize': '0.7rem'}),
                        html.Th("EVENTS", style={'color': COLORS['text_primary'], 'fontSize': '0.7rem'})
                    ])),
                    html.Tbody(id='most-active-devices-table-body')
                ], style={'fontSize': '0.75rem', 'width': '100%'})
            ], style={**panel_style_base, 'borderLeft': f'5px solid {COLORS["critical"]}'}),
            
            # NEW: Peak Activity Panel
            html.Div([
                html.H3("Peak Activity", style={'color': COLORS['text_primary'], 'fontSize': '1.1rem'}),
                html.P(id="peak-hour-display", style={'color': COLORS['text_secondary'], 'fontSize': '0.9rem'}),
                html.P(id="peak-day-display", style={'color': COLORS['text_secondary'], 'fontSize': '0.8rem'}),
                html.P(id="busiest-floor", style={'color': COLORS['text_secondary'], 'fontSize': '0.8rem'}),
                html.P(id="entry-exit-ratio", style={'color': COLORS['text_secondary'], 'fontSize': '0.8rem'}),
                html.P(id="weekend-vs-weekday", style={'color': COLORS['text_secondary'], 'fontSize': '0.8rem'})
            ], style={**panel_style_base, 'borderLeft': f'5px solid {COLORS["success"]}'}),
            
            # NEW: Security Overview Panel
            html.Div([
                html.H3("Security Overview", style={'color': COLORS['text_primary'], 'fontSize': '1.1rem'}),
                html.Div(id="security-level-breakdown", children=[
                    html.P("Loading...", style={'color': COLORS['text_secondary'], 'fontSize': '0.8rem'})
                ]),
                html.P(id="compliance-score", style={'color': COLORS['text_secondary'], 'fontSize': '0.8rem'}),
                html.P(id="anomaly-alerts", style={'color': COLORS['text_secondary'], 'fontSize': '0.8rem'})
            ], style={**panel_style_base, 'borderLeft': f'5px solid {COLORS["info"]}'})
        ]
    )


def create_analytics_section_hidden():
    """
    NEW: Advanced analytics section with key insights - HIDDEN by default
    """
    return html.Div(
        id='analytics-section',
        style={'display': 'none'},  # EXPLICITLY HIDDEN
        children=[
            html.H4("Advanced Analytics", 
                   style={'color': COLORS['text_primary'], 'textAlign': 'center', 'marginBottom': '20px'}),
            
            html.Div([
                # Insights cards
                create_insight_card("Traffic Pattern", "traffic-pattern-insight", COLORS['accent']),
                create_insight_card("Security Score", "security-score-insight", COLORS['success']),
                create_insight_card("Usage Efficiency", "efficiency-insight", COLORS['warning']),
                create_insight_card("Anomaly Detection", "anomaly-insight", COLORS['critical'])
            ], style={
                'display': 'flex',
                'justifyContent': 'space-around',
                'marginBottom': '20px',
                'flexWrap': 'wrap',
                'gap': '10px'
            }),
            
            # Detailed breakdown (initially hidden, toggled by Advanced View button)
            html.Div(id="analytics-detailed-breakdown", style={'marginTop': '20px'})
            
        ]
    )


def create_charts_section_hidden():
    """
    NEW: Interactive charts section - HIDDEN by default
    """
    # Create default empty chart - FIXED
    def create_empty_chart():
        """Helper to create empty chart with proper annotation"""
        import plotly.express as px
        
        # Create base figure and clear it
        fig = px.scatter(x=[0], y=[0])
        fig.data = []  # Remove the scatter trace
        
        # Add annotation using layout
        fig.update_layout(
            annotations=[
                dict(
                    text="No data available",
                    showarrow=False,
                    xref="paper",
                    yref="paper",
                    x=0.5,
                    y=0.5,
                    font=dict(size=16, color=COLORS.get('text_secondary', '#E2E8F0'))
                )
            ],
            plot_bgcolor=COLORS['background'],
            paper_bgcolor=COLORS['surface'],
            font_color=COLORS['text_primary'],
            xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
            yaxis=dict(showgrid=False, showticklabels=False, zeroline=False)
        )
        
        return fig
    
    empty_fig = create_empty_chart()
    
    return html.Div(
        id='charts-section',
        style={'display': 'none'},  # EXPLICITLY HIDDEN
        children=[
            html.H4("Data Visualization", 
                   style={'color': COLORS['text_primary'], 'textAlign': 'center', 'marginBottom': '20px'}),
            
            # Chart controls
            html.Div([
                html.Label("Chart Type:", style={'color': COLORS['text_primary'], 'marginRight': '10px'}),
                dcc.Dropdown(
                    id='chart-type-selector',
                    options=[
                        {'label': 'Hourly Activity', 'value': 'hourly'},
                        {'label': 'Daily Trends', 'value': 'daily'},
                        {'label': 'Security Distribution', 'value': 'security'},
                        {'label': 'Floor Activity', 'value': 'floor'},
                        {'label': 'User Patterns', 'value': 'users'},
                        {'label': 'Device Usage', 'value': 'devices'}
                    ],
                    value='hourly',
                    style={
                        'width': '200px', 
                        'color': COLORS['text_primary'],
                        'backgroundColor': COLORS['surface']
                    }
                )
            ], style={'marginBottom': '20px', 'textAlign': 'center'}),
            
            # Main chart container
            html.Div([
                dcc.Graph(
                    id='main-analytics-chart',
                    figure=empty_fig,
                    config={'displayModeBar': True, 'toImageButtonOptions': {'format': 'png'}},
                    style={'height': '400px'}
                )
            ], style={
                'backgroundColor': COLORS['background'], 
                'borderRadius': '8px', 
                'padding': '10px',
                'border': f'1px solid {COLORS["border"]}'
            }),
            
            # Secondary charts row
            html.Div([
                html.Div([
                    html.H6("Security Distribution", style={'color': COLORS['text_primary'], 'textAlign': 'center'}),
                    dcc.Graph(id='security-pie-chart', figure=empty_fig, style={'height': '300px'})
                ], style={
                    'flex': '1', 
                    'margin': '0 10px',
                    'backgroundColor': COLORS['background'],
                    'borderRadius': '8px',
                    'padding': '10px',
                    'border': f'1px solid {COLORS["border"]}'
                }),
                
                html.Div([
                    html.H6("Activity Heatmap", style={'color': COLORS['text_primary'], 'textAlign': 'center'}),
                    dcc.Graph(id='heatmap-chart', figure=empty_fig, style={'height': '300px'})
                ], style={
                    'flex': '1', 
                    'margin': '0 10px',
                    'backgroundColor': COLORS['background'],
                    'borderRadius': '8px',
                    'padding': '10px',
                    'border': f'1px solid {COLORS["border"]}'
                })
            ], style={'display': 'flex', 'marginTop': '20px', 'gap': '10px'})
            
        ]
    )


def create_export_section_hidden():
    """
    NEW: Export and download section - HIDDEN by default
    """
    return html.Div(
        id='export-section',
        style={'display': 'none'},  # EXPLICITLY HIDDEN
        children=[
            html.H4("Export & Reports", 
                   style={'color': COLORS['text_primary'], 'textAlign': 'center', 'marginBottom': '20px'}),
            
            html.Div([
                html.Button(
                    "📊 Export Stats CSV",
                    id='export-stats-csv',
                    className='export-button',
                    style=get_export_button_style('secondary')
                ),
                html.Button(
                    "📈 Download Charts",
                    id='export-charts-png',
                    className='export-button',
                    style=get_export_button_style('secondary')
                ),
                html.Button(
                    "📄 Generate Report",
                    id='generate-pdf-report',
                    className='export-button',
                    style=get_export_button_style('primary')
                ),
                html.Button(
                    "🔄 Refresh Data",
                    id='refresh-analytics',
                    className='export-button',
                    style=get_export_button_style('secondary')
                )
            ], style={
                'display': 'flex',
                'justifyContent': 'center',
                'gap': '15px',
                'flexWrap': 'wrap'
            }),
            
            # Download components (hidden)
            dcc.Download(id="download-stats-csv"),
            dcc.Download(id="download-charts"),
            dcc.Download(id="download-report"),
            
            # Export status
            html.Div(id="export-status", style={'textAlign': 'center', 'marginTop': '10px'})
            
        ]
    )


def create_insight_card(title, content_id, color):
    """Create a small insight card"""
    return html.Div([
        html.H6(title, style={
            'color': COLORS['text_primary'], 
            'margin': '0', 
            'fontSize': '0.9rem',
            'marginBottom': '5px'
        }),
        html.H4(id=content_id, style={
            'color': color, 
            'margin': '5px 0', 
            'fontSize': '1.2rem',
            'fontWeight': 'bold'
        })
    ], style={
        'padding': '15px',
        'backgroundColor': COLORS['background'],
        'borderRadius': '6px',
        'border': f'1px solid {color}',
        'textAlign': 'center',
        'flex': '1',
        'margin': '0 5px',
        'minWidth': '150px',
        'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
        'transition': 'transform 0.2s ease'
    })


def get_export_button_style(variant='secondary'):
    """Get export button styles"""
    base_style = {
        'padding': '8px 16px',
        'border': 'none',
        'borderRadius': '5px',
        'fontSize': '0.9rem',
        'fontWeight': '500',
        'cursor': 'pointer',
        'transition': 'all 0.3s ease',
        'minWidth': '140px'
    }
    
    if variant == 'primary':
        base_style.update({
            'backgroundColor': COLORS['accent'],
            'color': 'white'
        })
    else:
        base_style.update({
            'backgroundColor': COLORS['surface'],
            'color': COLORS['text_primary'],
            'border': f'1px solid {COLORS["border"]}'
        })
    
    return base_style


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
                "Network Topology Model",  # ENHANCED TITLE
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
                children="Upload CSV, map headers, (optionally classify doors), then Confirm & Generate. Tap a node for enhanced details."
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

            # Final "Generate" Button (enhanced)
            html.Button(
                '🚀 Confirm Selections & Generate Enhanced Analytics',  # ENHANCED BUTTON TEXT
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
                    'cursor': 'pointer',
                    'transition': 'all 0.3s ease',
                    'boxShadow': '0 4px 8px rgba(33, 150, 243, 0.3)'
                }
            )
        ]
    )


# ALL OTHER FUNCTIONS REMAIN THE SAME (for brevity, I'll reference the key ones)

def _create_fallback_upload_component(app_instance, icon_upload_default):
    """
    Creates a simple CSV‐upload component if no custom upload UI is provided.
    (Same as original - no changes needed)
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
    """Step 1: Map CSV Headers - with fallback UI (same as original)"""
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
    """Enhanced classification section (same structure as original)"""
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

                # Modern Floors Slider
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
                            {'label': 'No', 'value': 'no'}, 
                            {'label': 'Yes', 'value': 'yes'}
                        ],
                        value='no',
                        inline=True
                    ),
                ], style={
                    'display': 'flex',
                    'justifyContent': 'center',
                    'alignItems': 'center'
                })
            ], style={
                'padding': '20px',
                'backgroundColor': COLORS['surface'],
                'borderRadius': '8px',
                'marginBottom': '20px',
                'border': f'1px solid {COLORS["border"]}',
                'maxWidth': '550px',
                'margin': '0 auto'
            }),

            # === Step 3: Door Classification Table Container ===
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
                        "Assign security levels and properties to each door:",  # ENHANCED TEXT
                        style={'color': COLORS['text_primary'], 'textAlign': 'center', 'marginBottom': '8px'}
                    ),
                    html.Div(id="door-classification-table")
                ]
            )
        ]
    )


def create_processing_status():
    """Enhanced processing status indicator"""
    return html.Div(
        id='processing-status',
        style={
            'marginTop': '10px',
            'color': COLORS['accent'],
            'textAlign': 'center',
            'padding': '8px 16px',
            'backgroundColor': f"{COLORS['accent']}20",
            'borderRadius': '6px',
            'border': f'1px solid {COLORS["accent"]}40',
            'fontSize': '0.95rem',
            'fontWeight': '500'
        }
    )


def create_data_stores():
    """Create all dcc.Store() components for state management (same as original)"""
    return html.Div([
        dcc.Store(id='uploaded-file-store'),
        dcc.Store(id='csv-headers-store', storage_type='session'),
        dcc.Store(id='column-mapping-store', storage_type='local'),
        dcc.Store(id='ranked-doors-store', storage_type='session'),
        dcc.Store(id='current-entrance-offset-store', data=0, storage_type='session'),
        dcc.Store(id='manual-door-classifications-store', storage_type='local'),
        dcc.Store(id='num-floors-store', storage_type='session', data=1),
        dcc.Store(id='all-doors-from-csv-store', storage_type='session'),
        # NEW: Enhanced data stores
        dcc.Store(id='analytics-data-store', storage_type='session'),
        dcc.Store(id='chart-preferences-store', storage_type='local'),
    ])


def get_main_container_style():
    """Returns the enhanced style for the main container"""
    return {
        'backgroundColor': COLORS['background'],
        'padding': '20px',
        'minHeight': '100vh',
        'fontFamily': 'Inter, Arial, sans-serif',  # Enhanced font
        'lineHeight': '1.5'
    }


def register_page_callbacks(app):
    """
    Register enhanced page-specific callbacks
    """
    # Floor slider callback (if not handled elsewhere)
    @app.callback(
        Output("num-floors-display", "children"),
        Input("num-floors-input", "value"),
        prevent_initial_call=False
    )
    def update_floor_display(value):
        """Update the floor display text based on slider value"""
        if value is None:
            value = 1
        
        floors = int(value)
        if floors == 1:
            return "1 floor"
        else:
            return f"{floors} floors"
    
    # NEW: Analytics section visibility callback
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
        """Show enhanced sections when header becomes visible"""
        if header_style and header_style.get('display') != 'none':
            show_style = {'display': 'block', 'margin': '20px auto', 'maxWidth': '1200px', 'width': '90%',
                         'padding': '20px', 'backgroundColor': COLORS['surface'], 'borderRadius': '8px',
                         'border': f'1px solid {COLORS["border"]}'}
            return show_style, show_style, show_style
        else:
            hide_style = {'display': 'none'}
            return hide_style, hide_style, hide_style