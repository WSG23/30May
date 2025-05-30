# styles/style_config.py (UPDATED - Consistent background colors)
"""
Comprehensive style configuration with consistent background colors
"""

# Color palette - UPDATED for consistency
COLORS = {
    # Primary colors
    'primary': '#1B2A47',
    'accent': '#2196F3',
    'accent_light': '#42A5F5',
    
    # Status colors
    'success': '#2DBE6C',
    'warning': '#FFB020',
    'critical': '#E02020',
    'info': '#2196F3',
    
    # Background colors - UPDATED for consistency
    'background': '#0F1419',        # Main background - dark blue-gray
    'surface': '#1A2332',           # Card/component surfaces - slightly lighter
    'surface_elevated': '#1E2936',  # Elevated surfaces (modals, dropdowns)
    'border': '#2D3748',            # Border color
    
    # Text colors
    'text_primary': '#F7FAFC',      # Primary text - white
    'text_secondary': '#E2E8F0',    # Secondary text - light gray
    'text_tertiary': '#A0AEC0',     # Tertiary text - medium gray
    'text_on_accent': '#FFFFFF',    # Text on accent backgrounds
}

# Animation durations
ANIMATIONS = {
    'fast': '0.15s',
    'normal': '0.3s',
    'slow': '0.5s'
}

# Typography
TYPOGRAPHY = {
    # Font sizes
    'text_xs': '0.75rem',
    'text_sm': '0.875rem',
    'text_base': '1rem',
    'text_lg': '1.125rem',
    'text_xl': '1.25rem',
    'text_2xl': '1.5rem',
    'text_3xl': '1.875rem',
    'text_4xl': '2.25rem',
    
    # Font weights
    'font_light': '300',
    'font_normal': '400',
    'font_medium': '500',
    'font_semibold': '600',
    'font_bold': '700',
    
    # Line heights
    'leading_tight': '1.25',
    'leading_normal': '1.5',
    'leading_relaxed': '1.75',
}

# Spacing
SPACING = {
    'xs': '0.25rem',
    'sm': '0.5rem', 
    'base': '1rem',
    'lg': '1.5rem',
    'xl': '2rem',
    '2xl': '3rem',
    '3xl': '4rem'
}

# Border radius
BORDER_RADIUS = {
    'sm': '0.125rem',
    'md': '0.375rem',
    'lg': '0.5rem',
    'xl': '0.75rem',
    '2xl': '1rem',
    'full': '9999px'
}

# Shadows
SHADOWS = {
    'sm': '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
    'md': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
    'lg': '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
    'xl': '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
    'inner': 'inset 0 2px 4px 0 rgba(0, 0, 0, 0.06)',
    'outline': '0 0 0 3px rgba(33, 150, 243, 0.5)'  # Focus outline
}

# Component styles - UPDATED with new color scheme
COMPONENT_STYLES = {
    'card': {
        'background-color': COLORS['surface'],
        'border': f"1px solid {COLORS['border']}",
        'border-radius': BORDER_RADIUS['xl'],
        'box-shadow': SHADOWS['lg'],
        'padding': SPACING['xl']
    },
    'card_elevated': {
        'background-color': COLORS['surface_elevated'],
        'border': f"1px solid {COLORS['border']}",
        'border-radius': BORDER_RADIUS['xl'],
        'box-shadow': SHADOWS['xl'],
        'padding': SPACING['xl']
    },
    'button_primary': {
        'background-color': COLORS['accent'],
        'color': COLORS['text_on_accent'],
        'border': 'none',
        'padding': f"{SPACING['sm']} {SPACING['lg']}",
        'border-radius': BORDER_RADIUS['lg'],
        'font-weight': TYPOGRAPHY['font_semibold'],
        'cursor': 'pointer',
        'transition': f'all {ANIMATIONS["fast"]}',
        'box-shadow': SHADOWS['md']
    },
    'button_secondary': {
        'background-color': 'transparent',
        'color': COLORS['text_secondary'],
        'border': f"1px solid {COLORS['border']}",
        'padding': f"{SPACING['sm']} {SPACING['lg']}",
        'border-radius': BORDER_RADIUS['lg'],
        'font-weight': TYPOGRAPHY['font_medium'],
        'cursor': 'pointer',
        'transition': f'all {ANIMATIONS["fast"]}'
    },
    'input': {
        'background-color': COLORS['surface'],
        'border': f"1px solid {COLORS['border']}",
        'border-radius': BORDER_RADIUS['md'],
        'padding': SPACING['sm'],
        'color': COLORS['text_primary'],
        'font-size': TYPOGRAPHY['text_base'],
        'transition': f'border-color {ANIMATIONS["fast"]}'
    }
}

# UI visibility settings - UPDATED with consistent background
UI_VISIBILITY = {
    # Boolean visibility flags
    'show_upload_section': True,
    'show_mapping_section': True,
    'show_classification_section': True,
    'show_graph_section': True,
    'show_stats_section': True,
    'show_controls_section': True,
    'show_debug_info': False,
    'show_advanced_options': False,
    
    # CSS Style objects for components
    'hide': {'display': 'none'},
    'show_block': {
        'display': 'block',
        'animation': f'fadeIn {ANIMATIONS["normal"]}',
    },
    'show_flex': {
        'display': 'flex',
        'animation': f'slideUp {ANIMATIONS["normal"]}',
    },
    'show_flex_stats': {
        'display': 'flex',
        'flexDirection': 'row',
        'justifyContent': 'space-around',
        'gap': SPACING['lg'],
        'marginBottom': SPACING['2xl'],
        'animation': f'fadeIn {ANIMATIONS["normal"]}',
    },
    'show_header': {
        'display': 'flex',
        'flexDirection': 'row',
        'alignItems': 'center',
        'padding': f"{SPACING['lg']} {SPACING['xl']}",
        'backgroundColor': COLORS['background'],  # UPDATED to match main background
        'borderBottom': f'1px solid {COLORS["border"]}',
        'boxShadow': SHADOWS["sm"],
        'marginBottom': SPACING['xl'],
        'backdropFilter': 'blur(10px)',
    }
}

# UI components configuration
# UI components configuration
UI_COMPONENTS = {
    'upload': {
        'enabled': True,
        'accept_types': ['.csv'],
        'max_file_size': '10MB',
        'multiple_files': False,
        'icon_size': '120px',  # NEW: Larger icon size
        'container_width': '70%',  # NEW: Wider container
        'border_thickness': '3px'  # NEW: Thicker border
    },
    'mapping': {
        'enabled': True,
        'required_fields': ['timestamp', 'user_id', 'door_id', 'event_type'],
        'optional_fields': ['floor', 'building', 'access_level']
    },
    'classification': {
        'enabled': True,
        'card_style': {
            'backgroundColor': COLORS['surface'],
            'borderRadius': BORDER_RADIUS['md'],
            'border': f"1px solid {COLORS['border']}",
            'boxShadow': SHADOWS['sm'],
            'transition': 'all 0.2s ease'
        },
        'pill_style': {
            'backgroundColor': COLORS['surface'],
            'color': COLORS['text_secondary'],
            'borderRadius': BORDER_RADIUS['full'],
            'border': f"1px solid {COLORS['border']}",
            'cursor': 'pointer',
            'transition': 'all 0.2s ease'
        },
        'pill_style_active': {
            'backgroundColor': COLORS['accent'],
            'color': 'white',
            'borderColor': COLORS['accent']
        },
        'auto_classify': True,
        'security_levels': ['Public', 'Restricted', 'Highly Restricted'],
        'default_level': 'Public'
    },
    'graph': {
        'enabled': True,
        'default_layout': 'cose',
        'show_legend': True,
        'interactive': True,
        'export_formats': ['png', 'json']
    },
    'stats': {
        'enabled': True,
        'show_summaries': True,
        'show_charts': True,
        'refresh_interval': 5000
    }
}

# Layout configuration
LAYOUT_CONFIG = {
    'container_padding': '0',  # UPDATED: No padding for full-width background
    'section_spacing': SPACING['xl'],
    'max_width': '1200px',
    'responsive_breakpoints': {
        'mobile': '768px',
        'tablet': '1024px',
        'desktop': '1200px'
    }
}

# CSS Animations (can be added to CSS file)
CSS_ANIMATIONS = """
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes slideUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes slideDown {
    from { opacity: 0; transform: translateY(-10px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}

@keyframes spin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}

.hover-lift {
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.hover-lift:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
}

.loading-shimmer {
    background: linear-gradient(90deg, 
        transparent, 
        rgba(33, 150, 243, 0.4), 
        transparent
    );
    animation: shimmer 1.5s infinite;
}

@keyframes shimmer {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(100%); }
}
"""

# Utility Functions
def get_hover_style(base_style, hover_color=None):
    """Generate hover styles for interactive elements"""
    hover_style = base_style.copy()
    if hover_color:
        hover_style["backgroundColor"] = hover_color
    else:
        hover_style["opacity"] = "0.8"
    hover_style["transform"] = "translateY(-1px)"
    return hover_style

def get_focus_style(base_style):
    """Generate focus styles for form elements"""
    focus_style = base_style.copy()
    focus_style["borderColor"] = COLORS["accent"]
    focus_style["boxShadow"] = SHADOWS["outline"]
    return focus_style

def get_disabled_style(base_style):
    """Generate disabled styles for elements"""
    disabled_style = base_style.copy()
    disabled_style["opacity"] = "0.5"
    disabled_style["cursor"] = "not-allowed"
    disabled_style["pointerEvents"] = "none"
    return disabled_style

# Export all configurations
__all__ = [
    'COLORS',
    'ANIMATIONS', 
    'TYPOGRAPHY',
    'SPACING',
    'BORDER_RADIUS',
    'SHADOWS',
    'COMPONENT_STYLES',
    'UI_VISIBILITY',
    'UI_COMPONENTS',
    'LAYOUT_CONFIG',
    'CSS_ANIMATIONS',
    'get_hover_style',
    'get_focus_style', 
    'get_disabled_style'
]