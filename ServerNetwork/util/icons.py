from glob import glob
from pathlib import Path

from ServerNetwork.models import Service


def load_icons(icon_dir: str, output_dir: str) -> dict[str, list[str]]:
    """
    Load the icons from the icons directory
    :param icon_dir: The icon directory
    :param output_dir: The output directory for the HTML file
    :return: The icons
    """
    icons = dict[str, list[str]]()

    icon_files = glob(icon_dir + '/*.svg') + glob(icon_dir + '/*.png')

    for icon_file in icon_files:
        icon_path = Path(icon_file)
        icon_name = icon_path.stem.lower()

        relative_icon_path = icon_path.relative_to(output_dir).as_posix()

        if icon_name in icons:
            icons[icon_name].append(relative_icon_path)
        else:
            icons[icon_name] = [relative_icon_path]

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
