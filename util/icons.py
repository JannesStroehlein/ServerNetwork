from glob import glob
from pathlib import Path

from models import Service


def load_icons():
    """
    Load the icons from the icons directory
    :return: The icons
    """
    icon_dir = 'icons'
    icons = dict[str, list[str]]()

    icon_files = glob(icon_dir + '/*.svg') + glob(icon_dir + '/*.png')

    for icon_file in icon_files:
        icon_name = Path(icon_file).stem.lower()
        if icon_name in icons:
            icons[icon_name].append(str(icon_file))
        else:
            icons[icon_name] = [str(icon_file)]

    return icons


def get_service_icon(service : Service, icons : dict[str, list[str]]):
    """
    Get the icon for a service
    :param service: The service
    :param icons: The icons
    :return: The icon
    """
    use_svg = True

    icon_key = 'default' if service.id not in icons else service.id

    if icon_key is None:
        raise ValueError(f'No valid icon found for {service.id} in {icons}')

    return get_icon(icon_key, use_svg, icons)


def get_icon(name: str, use_svg : bool, icons : dict[str, list[str]]):
    """
    Get the icon for a service
    :param name: The name of the service
    :param use_svg: Whether to prefer SVG icons
    :param icons: The icons
    :return: The icon
    """

    if use_svg and any(icon.lower().endswith('.svg') for icon in icons[name]):
        for icon in icons[name]:
            if icon.endswith('.svg'):
                return icon

    for i, icon in enumerate(icons[name]):
        if not icon.endswith('.svg'):
            return icon

    raise ValueError(f'No valid icon found for {name} in {icons[name]}')
