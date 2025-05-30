# ui/components/upload.py
"""
Upload component - Fixed for actual directory structure
"""
from dash import html, dcc
import dash_bootstrap_components as dbc
from typing import Dict, Any, Optional

# Import from actual structure
from utils.constants import DEFAULT_ICONS
from ui.themes.style_config import COLORS, SPACING, BORDER_RADIUS, SHADOWS, TYPOGRAPHY


class EnhancedUploadComponent:
    """Enhanced upload component for actual directory structure"""
    
    def __init__(self, icon_default: str, icon_success: str, icon_fail: str):
        self.icons = {
            'default': icon_default,
            'success': icon_success, 
            'fail': icon_fail
        }
    
    def create_upload_area(self):
        """Creates upload area"""
        return dcc.Upload(
            id='upload-data',
            children=self.create_upload_content(),
            style=self.get_upload_style("initial"),
            multiple=False,
            accept='.csv',
            className="upload-area hover-lift"
        )
    
    def create_upload_content(self):
        """Creates upload content"""
        return html.Div([
            html.Div([
                html.Img(
                    id='upload-icon',
                    src=self.icons['default'],
                    style={
                        'width': '120px',
                        'height': '120px',
                        'marginBottom': SPACING['base'],
                        'opacity': '0.8',
                        'transition': f'all 0.3s ease',
                    }
                )
            ], style={'textAlign': 'center'}),
            
            html.H3("Drop your CSV file here", style={
                'margin': '0',
                'fontSize': TYPOGRAPHY['text_lg'],
                'fontWeight': TYPOGRAPHY['font_semibold'],
                'color': COLORS['text_primary'],
                'marginBottom': SPACING['xs']
            }),
            
            html.P("or click to browse", style={
                'margin': '0',
                'fontSize': TYPOGRAPHY['text_sm'],
                'color': COLORS['text_secondary'],
            }),
        ], style={
            'display': 'flex',
            'flexDirection': 'column',
            'alignItems': 'center',
            'justifyContent': 'center',
            'height': '100%',
            'padding': SPACING['base']
        })
    
    def get_upload_style(self, state="initial"):
        """Get upload styles based on state"""
        base_style = {
            'width': '70%',
            'maxWidth': '600px',
            'minHeight': '180px',
            'borderRadius': BORDER_RADIUS['lg'],
            'textAlign': 'center',
            'margin': f"{SPACING['base']} auto",
            'display': 'flex',
            'alignItems': 'center',
            'justifyContent': 'center',
            'cursor': 'pointer',
            'transition': 'all 0.3s ease',
        }
        
        state_styles = {
            "initial": {
                'border': f'2px dashed {COLORS["border"]}',
                'backgroundColor': COLORS['surface'],
            },
            "success": {
                'border': f'2px solid {COLORS["success"]}',
                'backgroundColor': f"{COLORS['success']}10",
            },
            "error": {
                'border': f'2px solid {COLORS["critical"]}',
                'backgroundColor': f"{COLORS['critical']}10",
            }
        }
        
        return {**base_style, **state_styles.get(state, {})}
    
    def get_upload_styles(self):
        """Returns styles dictionary for handlers"""
        return {
            'initial': self.get_upload_style('initial'),
            'success': self.get_upload_style('success'),
            'error': self.get_upload_style('error'),
        }
    
    def create_interactive_setup_container(self):
        """Creates setup container"""
        return html.Div(
            id='interactive-setup-container',
            style={
                'display': 'none',
                'padding': SPACING['lg'],
                'backgroundColor': COLORS['surface'],
                'borderRadius': BORDER_RADIUS['lg'],
                'margin': f"{SPACING['lg']} auto",
                'width': '85%',
                'maxWidth': '1000px',
                'border': f"1px solid {COLORS['border']}",
            },
            children=[
                # Mapping section placeholder
                html.Div(id='mapping-ui-section', style={'display': 'none'}),
                
                # Classification section placeholder  
                html.Div(id='entrance-verification-ui-section', style={'display': 'none'}),
                
                # Generate button
                self.create_generate_button()
            ]
        )
    
    def create_generate_button(self):
        """Creates generate button"""
        return dbc.Button(
            'Confirm Selections & Generate Onion Model',
            id='confirm-and-generate-button',
            n_clicks=0,
            color='primary',
            size='lg',
            className='w-100',
            style={
                'marginTop': SPACING['lg'],
            }
        )
    
    def _get_interactive_setup_style(self, visible=False):
        """Get interactive setup container style"""
        base_style = {
            'padding': SPACING['lg'],
            'backgroundColor': COLORS['surface'],
            'borderRadius': BORDER_RADIUS['lg'],
            'margin': f"{SPACING['lg']} auto",
            'width': '85%',
            'maxWidth': '1000px',
            'border': f"1px solid {COLORS['border']}",
        }
        
        if visible:
            base_style['display'] = 'block'
        else:
            base_style['display'] = 'none'
            
        return base_style
    
    def _get_button_style(self, variant='primary'):
        """Get button style"""
        return {
            'backgroundColor': COLORS['accent'],
            'border': 'none',
            'color': 'white',
            'padding': f"{SPACING['sm']} {SPACING['lg']}",
            'borderRadius': BORDER_RADIUS['md'],
            'cursor': 'pointer',
            'fontWeight': TYPOGRAPHY['font_semibold'],
        }


# Factory functions for easy component creation
def create_enhanced_upload_component(icon_default: str, icon_success: str, icon_fail: str):
    """Factory function to create enhanced upload component"""
    return EnhancedUploadComponent(icon_default, icon_success, icon_fail)

def create_upload_component(icon_default: str, icon_success: str, icon_fail: str):
    """Alias for backward compatibility"""
    return create_enhanced_upload_component(icon_default, icon_success, icon_fail)

def create_simple_upload_component(icon_path: str):
    """Create simple upload component with single icon"""
    return EnhancedUploadComponent(icon_path, icon_path, icon_path)