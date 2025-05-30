# ui/components/upload.py (ENHANCED - Cleaned UI)
"""
Enhanced upload component with improved UX/UI and removed unnecessary text sections
"""

from dash import html, dcc
import dash_bootstrap_components as dbc
from styles.style_config import COLORS, ANIMATIONS, TYPOGRAPHY, SPACING, BORDER_RADIUS, SHADOWS, COMPONENT_STYLES


class EnhancedUploadComponent:
    """Enhanced upload component with modern UX/UI and cleaned interface"""
    
    def __init__(self, icon_upload_default, icon_upload_success, icon_upload_fail):
        self.icon_upload_default = icon_upload_default
        self.icon_upload_success = icon_upload_success
        self.icon_upload_fail = icon_upload_fail
    
    def create_upload_area(self):
        """Creates an enhanced upload area with modern design and cleaned interface"""
        return dcc.Upload(
            id='upload-data',
            children=self.create_upload_content(),
            style=self.get_upload_style("initial"),
            multiple=False,
            accept='.csv',
            className="upload-area hover-lift"
        )
    
    def create_upload_content(self):
        """Creates the content inside the upload area - cleaned version"""
        return html.Div([
            # Upload icon with animation - REDUCED SIZE
            html.Div([
                html.Img(
                    id='upload-icon',
                    src=self.icon_upload_default,
                    style={
                        'width': '120px',  # Reduced from 96px
                        'height': '120px',  # Reduced from 96px
                        'marginBottom': SPACING['base'],
                        'opacity': '0.8',
                        'transition': f'all {ANIMATIONS["normal"]}',
                        'filter': 'brightness(1.1)',  # Slight brightness boost
                    }
                )
            ], style={'textAlign': 'center'}),
            
            # Main upload text
            html.H3("Drop your CSV file here", style={
                'margin': '0',
                'fontSize': TYPOGRAPHY['text_lg'],  # Reduced from text_xl
                'fontWeight': TYPOGRAPHY['font_semibold'],
                'color': COLORS['text_primary'],
                'marginBottom': SPACING['xs']
            }),
            
            # Secondary text
            html.P("or click to browse", style={
                'margin': '0',
                'fontSize': TYPOGRAPHY['text_sm'],  # Reduced from text_base
                'color': COLORS['text_secondary'],
                'fontWeight': TYPOGRAPHY['font_normal']
            }),
            
            # Removed file requirements section entirely
        ], style={
            'display': 'flex',
            'flexDirection': 'column',
            'alignItems': 'center',
            'justifyContent': 'center',
            'height': '100%',
            'padding': SPACING['base']  # Reduced from lg
        })
    
    def create_status_text(self, message="", status="initial"):
        """Creates enhanced status text with icons and colors - returns None if no message"""
        # Return None if no message provided (won't render anything)
        if not message:
            return None
            
        icon_map = {
            'initial': '📁',
            'processing': '⏳',
            'success': '✅',
            'error': '❌',
            'warning': '⚠️'
        }
        
        color_map = {
            'initial': COLORS['text_secondary'],
            'processing': COLORS['warning'],
            'success': COLORS['success'],
            'error': COLORS['critical'],
            'warning': COLORS['warning']
        }
        
        return html.Div([
            html.Span(icon_map.get(status, '📁'), style={'marginRight': SPACING['xs']}),
            html.Span(message)
        ], style={
            'textAlign': 'center',
            'marginBottom': SPACING['base'],  # Reduced from lg
            'fontSize': TYPOGRAPHY['text_sm'],  # Reduced from text_base
            'color': color_map.get(status, COLORS['text_secondary']),
            'fontWeight': TYPOGRAPHY['font_medium'],
            'padding': SPACING['sm'],  # Reduced from base
            'borderRadius': BORDER_RADIUS['md'],
            'backgroundColor': f"{color_map.get(status, COLORS['text_secondary'])}10",
            'border': f"1px solid {color_map.get(status, COLORS['text_secondary'])}30",
            'transition': f'all {ANIMATIONS["fast"]}'
        })
    
    def create_progress_bar(self, progress=0, show=False):
        """Creates a progress bar for upload processing"""
        return html.Div([
            html.Div([
                html.Div(style={
                    'width': f'{progress}%',
                    'height': '100%',
                    'backgroundColor': COLORS['accent'],
                    'borderRadius': BORDER_RADIUS['full'],
                    'transition': f'width {ANIMATIONS["normal"]}',
                    'background': f'linear-gradient(90deg, {COLORS["accent"]}, {COLORS["accent_light"]})'
                })
            ], style={
                'width': '100%',
                'height': '4px',
                'backgroundColor': COLORS['border'],
                'borderRadius': BORDER_RADIUS['full'],
                'overflow': 'hidden',
                'marginBottom': SPACING['sm']  # Reduced
            }),
            html.P(f"Processing... {progress}%", style={
                'textAlign': 'center',
                'fontSize': TYPOGRAPHY['text_xs'],  # Reduced
                'color': COLORS['text_secondary'],
                'margin': '0'
            }) if show else None
        ], style={
            'display': 'block' if show else 'none',
            'margin': f"{SPACING['sm']} auto",  # Reduced
            'width': '250px'  # Reduced from 300px
        })
    
    def create_file_preview(self, filename, file_size=None, row_count=None):
        """Creates a preview card for uploaded file"""
        return html.Div([
            html.Div([
                html.Div([
                    html.Span("📄", style={'fontSize': TYPOGRAPHY['text_xl'], 'marginRight': SPACING['sm']}),  # Reduced size
                    html.Div([
                        html.H4(filename, style={
                            'margin': '0',
                            'fontSize': TYPOGRAPHY['text_base'],  # Reduced from text_lg
                            'fontWeight': TYPOGRAPHY['font_semibold'],
                            'color': COLORS['text_primary']
                        }),
                        html.P([
                            file_size and f"Size: {file_size} • " or "",
                            row_count and f"Rows: {row_count:,}" or "Analyzing..."
                        ], style={
                            'margin': '0',
                            'fontSize': TYPOGRAPHY['text_xs'],  # Reduced from text_sm
                            'color': COLORS['text_secondary']
                        })
                    ], style={'flex': '1'})
                ], style={
                    'display': 'flex',
                    'alignItems': 'center',
                    'padding': SPACING['base']  # Reduced from lg
                })
            ], style={
                **COMPONENT_STYLES['card'],
                'margin': f"{SPACING['base']} auto",  # Reduced margin
                'maxWidth': '350px',  # Reduced from 400px
                'border': f"1px solid {COLORS['success']}",
                'backgroundColor': f"{COLORS['success']}10"
            })
        ])
    
    def get_upload_style(self, state="initial"):
        """Returns upload area styles based on state with reduced width"""
        base_style = {
            'width': '70%',  # REDUCED from 100% to 70%
            'maxWidth': '600px',  # NEW: Added max-width constraint
            'minHeight': '180px',  # Reduced from 160px
            'maxHeight': '200px',  # Reduced from 180px
            'borderRadius': BORDER_RADIUS['lg'],
            'textAlign': 'center',
            'margin': f"{SPACING['base']} auto",  # Reduced margin
            'display': 'flex',
            'alignItems': 'center',
            'justifyContent': 'center',
            'cursor': 'pointer',
            'transition': f'all {ANIMATIONS["normal"]}',
            'position': 'relative',
            'overflow': 'hidden'
        }
        
        if state == "initial":
            return {
                **base_style,
                'border': f'2px dashed {COLORS["border"]}',
                'backgroundColor': COLORS['surface'],
            }
        elif state == "dragover":
            return {
                **base_style,
                'border': f'2px dashed {COLORS["accent"]}',
                'backgroundColor': f"{COLORS['accent']}10",
                'transform': 'scale(1.02)',
            }
        elif state == "success":
            return {
                **base_style,
                'border': f'2px solid {COLORS["success"]}',
                'backgroundColor': f"{COLORS['success']}10",
            }
        elif state == "error":
            return {
                **base_style,
                'border': f'2px solid {COLORS["critical"]}',
                'backgroundColor': f"{COLORS['critical']}10",
            }
        else:
            return base_style
    
    def get_upload_styles(self):
        """Returns a dictionary of upload styles for different states (for handlers)"""
        return {
            'initial': self.get_upload_style('initial'),
            'dragover': self.get_upload_style('dragover'),
            'success': self.get_upload_style('success'),
            'error': self.get_upload_style('error'),
            'processing': self.get_upload_style('initial')  # Use initial style for processing
        }
    
    def _get_interactive_setup_style(self, visible=False):
        """Returns the style for the interactive setup container with reduced width"""
        base_style = {
            'padding': SPACING['lg'],
            'backgroundColor': COLORS['surface'],
            'borderRadius': BORDER_RADIUS['lg'],
            'margin': f"{SPACING['lg']} auto",
            'width': '85%',  # REDUCED from 95% to 85%
            'maxWidth': '1000px',  # REDUCED from 1200px to 1000px
            'boxShadow': SHADOWS['md'],  # Reduced from lg to md
            'border': f"1px solid {COLORS['border']}",
        }
        
        if visible:
            return {
                **base_style,
                'display': 'block',
                'animation': f'fadeIn {ANIMATIONS["normal"]}'
            }
        else:
            return {
                **base_style,
                'display': 'none'
            }
    
    def _get_button_style(self, button_type='primary', visible=True):
        """Returns button styles for different types and states"""
        base_style = {
            'fontSize': TYPOGRAPHY['text_base'],  # Reduced from text_lg
            'fontWeight': TYPOGRAPHY['font_semibold'],
            'padding': f"{SPACING['base']} {SPACING['lg']}",  # Reduced padding
            'borderRadius': BORDER_RADIUS['md'],  # Reduced from lg
            'marginTop': SPACING['lg'],  # Reduced from 2xl
            'boxShadow': SHADOWS['sm'],  # Reduced from md
            'transition': f'all {ANIMATIONS["fast"]}',
            'border': 'none',
            'cursor': 'pointer',
            'width': '100%'
        }
        
        if button_type == 'primary':
            button_style = {
                **base_style,
                'backgroundColor': COLORS['accent'],
                'color': 'white'
            }
        elif button_type == 'secondary':
            button_style = {
                **base_style,
                'backgroundColor': 'transparent',
                'color': COLORS['text_secondary'],
                'border': f"1px solid {COLORS['border']}"
            }
        else:
            button_style = base_style
        
        if not visible:
            button_style['display'] = 'none'
        
        return button_style
    
    def create_interactive_setup_container(self):
        """Creates enhanced interactive setup container with reduced width"""
        return html.Div(
            id='interactive-setup-container',
            style={
                'display': 'none',
                'padding': SPACING['lg'],
                'backgroundColor': COLORS['surface'],
                'borderRadius': BORDER_RADIUS['lg'],
                'margin': f"{SPACING['lg']} auto",
                'width': '85%',  # REDUCED from 95% to 85%
                'maxWidth': '1000px',  # REDUCED from 1200px to 1000px
                'boxShadow': SHADOWS['md'],  # Reduced shadow
                'border': f"1px solid {COLORS['border']}",
                'animation': f'fadeIn {ANIMATIONS["normal"]}'
            },
            children=[
                self.create_mapping_section(),
                self.create_entrance_verification_section(),
                self.create_generate_button()
            ]
        )
    
    def create_mapping_section(self):
        """Creates enhanced mapping section"""
        # Deferred import to avoid circular dependencies
        from ui.components.mapping import create_mapping_component  # type: ignore
        mapping_component = create_mapping_component()
        return mapping_component.create_mapping_section()
    
    def create_entrance_verification_section(self):
        """Creates enhanced entrance verification section"""
        # Deferred import to avoid circular dependencies
        from ui.components.classification import create_classification_component  # type: ignore
        classification_component = create_classification_component()
        return classification_component.create_entrance_verification_section()
    
    def create_generate_button(self):
        """Creates enhanced generate button with loading state"""
        return html.Div([
            dbc.Button(
                [
                    html.Span(id='generate-button-icon', children='🚀', style={'marginRight': SPACING['xs']}),
                    html.Span(id='generate-button-text', children='Confirm Selections & Generate Onion Model')
                ],
                id='confirm-and-generate-button',
                n_clicks=0,
                color='primary',
                size='lg',
                className='w-100',
                style={
                    'fontSize': TYPOGRAPHY['text_base'],  # Reduced
                    'fontWeight': TYPOGRAPHY['font_semibold'],
                    'padding': f"{SPACING['base']} {SPACING['lg']}",  # Reduced
                    'borderRadius': BORDER_RADIUS['md'],  # Reduced
                    'marginTop': SPACING['lg'],  # Reduced
                    'boxShadow': SHADOWS['sm'],  # Reduced
                    'transition': f'all {ANIMATIONS["fast"]}'
                }
            ),
            
            # Loading indicator (hidden by default)
            html.Div(
                id='generate-loading-indicator',
                children=[
                    html.Div(className='loading-shimmer', style={
                        'width': '100%',
                        'height': '4px',
                        'borderRadius': BORDER_RADIUS['full'],
                        'marginTop': SPACING['sm']  # Reduced
                    }),
                    html.P('Generating your security model...', style={
                        'textAlign': 'center',
                        'fontSize': TYPOGRAPHY['text_xs'],  # Reduced
                        'color': COLORS['text_secondary'],
                        'marginTop': SPACING['sm'],  # Reduced
                        'margin': '0'
                    })
                ],
                style={'display': 'none', 'marginTop': SPACING['sm']}  # Reduced
            )
        ])


# Enhanced factory function
def create_enhanced_upload_component(icon_upload_default, icon_upload_success, icon_upload_fail):
    """Factory function to create enhanced upload component instance"""
    return EnhancedUploadComponent(icon_upload_default, icon_upload_success, icon_upload_fail)

# Backward compatibility
def create_upload_component(icon_upload_default, icon_upload_success, icon_upload_fail):
    """Factory function that now creates enhanced component"""
    return create_enhanced_upload_component(icon_upload_default, icon_upload_success, icon_upload_fail)

# Simple wrapper for easy importing without parameters
def create_simple_upload_component():
    """Creates a simple upload component without requiring icon parameters"""
    # Default placeholder icons
    default_icon = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='64' height='64' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2'%3E%3Cpath d='M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4'/%3E%3Cpolyline points='7,10 12,15 17,10'/%3E%3Cline x1='12' y1='15' x2='12' y2='3'/%3E%3C/svg%3E"
    success_icon = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='64' height='64' viewBox='0 0 24 24' fill='none' stroke='%2322c55e' stroke-width='2'%3E%3Cpath d='M9 12l2 2 4-4'/%3E%3Ccircle cx='12' cy='12' r='10'/%3E%3C/svg%3E"
    error_icon = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='64' height='64' viewBox='0 0 24 24' fill='none' stroke='%23ef4444' stroke-width='2'%3E%3Ccircle cx='12' cy='12' r='10'/%3E%3Cline x1='15' y1='9' x2='9' y2='15'/%3E%3Cline x1='9' y1='9' x2='15' y2='15'/%3E%3C/svg%3E"
    
    return create_enhanced_upload_component(default_icon, success_icon, error_icon)