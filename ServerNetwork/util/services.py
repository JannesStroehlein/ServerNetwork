import math

from ServerNetwork.models import Service

def get_title_string_for_service(service : Service):
    """
    Get the title string for a service
    :param service: The service
    :return: The title string
    """

    bg_color = '#121212'
    accent_color = '#ff6d00'
    accent_style = f'style="color: {accent_color};"'
    text_color = '#fafafa'

    template = f"""
    <div style="background-color: {bg_color}; color: {text_color}; padding: 10px; border-radius: 5px;">
        <h5>{service.name}</h5>
        <hr>
        {f'<div style="background-color: #242424; padding: 3px; border-radius: 5px;"><p>{service.comment}</p></div>' if service.comment else ''}
        {f'<p>{f"<b>Host</b>: <span {accent_style}>{service.host}</span>" if service.host else ""}{", " if service.host and service.proxy else ""}{f"<b>Proxy</b>: <span {accent_style}>{service.proxy}</span>" if service.proxy else ""}' if service.host or service.proxy else ''}
        <div style="display: flex;flex-direction: row;flex-wrap: wrap-reverse;justify-content: flex-start;align-items: normal;align-content: flex-end;">
            {(f'<div style="display: block;"><p>URLs</p>'
              f'<ul style="line-height:100%;">%URL_LIST%</ul></div>') if service.urls else ''}
            {(f'<div style="display: block;"><p>Ports:</p>'
              f'<ul style="line-height:100%;">%PORT_LIST%</ul></div>') if service.ports else ''}
        </div>
    </div>
    """

    if service.urls:
        url_list = ''.join([f'<li><span {accent_style}>{url}</span></li>' for url in service.urls])
        template = template.replace('%URL_LIST%', url_list)

    if service.ports:
        port_list = ''.join([f'<li><span {accent_style}>{port}</span></li>' for port in service.ports])
        template = template.replace('%PORT_LIST%', port_list)

    print(template)
    return template

    # Name
    result = f'{service.name}'

    # Comment
    result += f'\n{service.comment}' if service.comment else ''

    # Add a newline if there are URLs, proxy, host or ports to follow
    result += '\n' if service.urls or service.proxy or service.host or service.ports else ''

    # Host and proxy
    if service.host or service.proxy:
        result += '\n' + \
            ((f'Host: {service.host}' if service.host else '')
            + (f', ' if service.host and service.proxy else '')
             + (f'Proxy: {service.proxy}' if service.proxy else ''))

    # URLs
    result += f'\nURLs: {", ".join(service.urls)}' if service.urls else ''

    # Ports
    result += f'\nPorts: {", ".join(map(str, service.ports))}' if service.ports else ''
    return result

def get_service_size(incident_count : int, min_size : int, max_size : int, has_custom_icon : bool, max_incident_count : int):
    """
    Get the size of a service node
    :param incident_count: The number of incidents
    :param min_size: The minimum size
    :param max_size: The maximum size
    :param has_custom_icon: Whether the service has a custom icon
    :param max_incident_count: The maximum number of incidents for any service
    :return: The size
    """

    relative_size = (incident_count + 1) / (max_incident_count + 1)

    return ease_in_out_quad(relative_size) * (max_size - min_size) + min_size


def ease_quad_out(x : float):
    """
    Apply a quadratic ease-out function to a value
    :param x: The input value
    :return: The output value
    """
    return 1 - (1 - x) * (1 - x)

def ease_in_out_quad(x : float):
    return 2 * x * x if x < 0.5 else 1 - math.pow(-2 * x + 2, 2) / 2