# ui/components/upload.py
"""
Upload component - Refactored to remove circular dependencies
"""
from dash import html, dcc
import dash_bootstrap_components as dbc
from typing import Dict, Any, Optional
from config.unified_settings import get_settings
from ui.registry import ComponentConfig

class EnhancedUploadComponent:
    """Enhanced upload component without circular dependencies"""
    
    def __init__(self, config: ComponentConfig):
        self.config = config
        self.settings = get_settings()
        self.icons = config.icons
        self.theme = config.theme
    
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
                    src=self.icons.get('default', ''),
                    style={
                        'width': '120px',
                        'height': '120px',
                        'marginBottom': self.theme['spacing']['base'],
                        'opacity': '0.8',
                        'transition': f'all {self.theme["animations"]["normal"]}',
                    }
                )
            ], style={'textAlign': 'center'}),
            
            html.H3("Drop your CSV file here", style={
                'margin': '0',
                'fontSize': self.theme['typography']['text_lg'],
                'fontWeight': self.theme['typography']['font_semibold'],
                'color': self.theme['colors']['text_primary'],
                'marginBottom': self.theme['spacing']['xs']
            }),
            
            html.P("or click to browse", style={
                'margin': '0',
                'fontSize': self.theme['typography']['text_sm'],
                'color': self.theme['colors']['text_secondary'],
            }),
        ], style={
            'display': 'flex',
            'flexDirection': 'column',
            'alignItems': 'center',
            'justifyContent': 'center',
            'height': '100%',
            'padding': self.theme['spacing']['base']
        })
    
    def get_upload_style(self, state="initial"):
        """Get upload styles based on state"""
        colors = self.theme['colors']
        spacing = self.theme['spacing']
        
        base_style = {
            'width': '70%',
            'maxWidth': '600px',
            'minHeight': '180px',
            'borderRadius': self.theme['border_radius']['lg'],
            'textAlign': 'center',
            'margin': f"{spacing['base']} auto",
            'display': 'flex',
            'alignItems': 'center',
            'justifyContent': 'center',
            'cursor': 'pointer',
            'transition': f'all {self.theme["animations"]["normal"]}',
        }
        
        state_styles = {
            "initial": {
                'border': f'2px dashed {colors["border"]}',
                'backgroundColor': colors['surface'],
            },
            "success": {
                'border': f'2px solid {colors["success"]}',
                'backgroundColor': f"{colors['success']}10",
            },
            "error": {
                'border': f'2px solid {colors["critical"]}',
                'backgroundColor': f"{colors['critical']}10",
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
        """Creates setup container - delegates to registry"""
        from ui.registry import get_registry
        registry = get_registry()
        
        return html.Div(
            id='interactive-setup-container',
            style={
                'display': 'none',
                'padding': self.theme['spacing']['lg'],
                'backgroundColor': self.theme['colors']['surface'],
                'borderRadius': self.theme['border_radius']['lg'],
                'margin': f"{self.theme['spacing']['lg']} auto",
                'width': '85%',
                'maxWidth': '1000px',
                'border': f"1px solid {self.theme['colors']['border']}",
            },
            children=[
                html.Div(id='mapping-section-placeholder'),
                html.Div(id='classification-section-placeholder'), 
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
                'marginTop': self.theme['spacing']['lg'],
            }
        )

# Factory function
def create_enhanced_upload_component(config: ComponentConfig):
    """Factory function"""
    return EnhancedUploadComponent(config)