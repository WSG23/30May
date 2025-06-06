from .style_config import COMPONENT_STYLES, COLORS, SPACING, BORDER_RADIUS, SHADOWS, ANIMATIONS, TYPOGRAPHY


def _convert_keys(style_dict):
    """Convert kebab-case keys to camelCase for Dash."""
    converted = {}
    for key, value in style_dict.items():
        if '-' in key:
            parts = key.split('-')
            camel = parts[0] + ''.join(p.title() for p in parts[1:])
            converted[camel] = value
        else:
            converted[key] = value
    return converted


def get_component_style(name):
    """Return component style from CONFIG with camelCase keys."""
    style = COMPONENT_STYLES.get(name, {}).copy()
    return _convert_keys(style)


def get_card_style(elevated=False):
    """Return standard card style."""
    key = 'card_elevated' if elevated else 'card'
    return get_component_style(key)


def get_button_style(variant='primary'):
    """Return standardized button style."""
    return get_component_style(f'button_{variant}')


def get_input_style():
    """Return standardized input style."""
    return get_component_style('input')
