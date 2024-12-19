from glob import glob

import yaml
import networkx as nx

from models.Connection import Connection
from models.Service import Service
from renderers.PyVisRenderer import PyVisRenderer
from util import *

max_node_size = 25
min_node_size = 8

# Load the icons
icons = load_icons()
#images = {k: Image.open(fname) for k, fname in icons.items()}
#print(f'Loaded {len(images)} icons: {", ".join(images.keys())}')

# Load the data from the YAML files in the data directory and its subdirectories
data = dict()
max_incident_count = 0

for data_file in glob('data/**/*.y*ml', recursive=True):
    print(f'{data_file}: Loading data...')
    with open(data_file) as file:
        file_data = yaml.load(file, Loader=yaml.FullLoader)
        if not file_data:
            print(f'{data_file}: No data found. Skipping...')
            continue

        if not file_data['services']:
            print(f'{data_file}: No services found. Skipping...')
            continue

        service_count = len(file_data['services'])
        connection_count = 0
        for service in file_data['services']:
            if 'connections' not in service or not service['connections']:
                continue
            for protocol, v in service['connections'].items():
                for remote in v:
                    if isinstance(remote, dict):
                        connection_count += len(remote)
                    elif isinstance(remote, str):
                        connection_count += 1

        print(f'{data_file}: Found {service_count} services with {connection_count} connections')

        data.update(file_data)

# Check if the data is valid
if 'services' not in data:
    raise ValueError('Services are required')

if not data['services']:
    raise ValueError('At least one service is required')


# Parse the data
connections = []
services = []

for service_index, service in enumerate(data['services']):
    if 'name' not in service:
        raise ValueError('Service name is required')

    if 'url' in service and 'urls' in service:
        raise ValueError('URL and URLs can only be used mutually exclusively')

    if 'port' in service and 'ports' in service:
        raise ValueError('Port and Ports can only be used mutually exclusively')

    if 'url' in service:
        service['urls'] = [service['url']]

    if 'port' in service:
        service['ports'] = [service['port']]

    parsed_service = Service(
            service['name'],
            service['host'] if 'host' in service else None,
            service['comment'] if 'comment' in service else None,
            service['urls'] if 'urls' in service else [],
            service['ports'] if 'ports' in service else [],
            service['proxy'] if 'proxy' in service else None
        )
    services.append(parsed_service)

    if 'connections' not in service or not service['connections']:
        continue

    for i, (protocol, v) in enumerate(service['connections'].items()):
        for remote in v:
            if isinstance(remote, str):
                connections.append(Connection(protocol, parsed_service.id, str(remote).lower()))
            elif isinstance(remote, dict):
                remote_name = list(remote.keys())[0]
                remote_comment = remote[remote_name]['comment']
                connections.append(Connection(protocol, parsed_service.id, str(remote_name).lower(), remote_comment))

incident_count_per_service = {service.id: sum(con.remote == service.id for con in connections) for service in services}

max_incident_count = max(incident_count_per_service.values())

# Create the network graph using NetworkX
nx_graph = nx.MultiDiGraph()
nx_graph.name = 'Server Network'

protocols = set([con.protocol for con in connections])

for index, service in enumerate(services):
    # Get all connections that point to this service
    incoming_connections = [con for con in connections if con.remote == service.id] or []

    # Get the number of incidents
    incident_count = sum(con.remote == service.id for con in connections)
    # Get the most common incoming protocol for this service (if any)
    most_common_incoming_protocol = (max(set([con.protocol for con in incoming_connections]), key = [con.protocol for con in incoming_connections].count)) if incoming_connections else None

    has_custom_icon = service.id in icons

    node_attributes = {
        'imagePadding': 2 if has_custom_icon else 0,
        'shape': 'image' if has_custom_icon else 'dot',
        'host': service.host,
        'size': get_service_size(incident_count, min_node_size, max_node_size, has_custom_icon, max_incident_count),
        'title': get_title_string_for_service(service),
        'label': service.name,
        'group': most_common_incoming_protocol if most_common_incoming_protocol in protocols else None
    }

    if has_custom_icon:
        node_attributes['image'] = get_service_icon(service, icons)
        node_attributes['shapeProperties'] = {
            'useBorderWithImage': True
        }
        node_attributes['borderWidth'] = 2
        node_attributes['borderWidthSelected'] = 3
        node_attributes['color.background'] = '#ffffffff'

    nx_graph.add_node(service.id, **node_attributes)

for connection in connections:
    nx_graph.add_edge(
        connection.origin,
        connection.remote,
        label=connection.protocol,
        title=connection.comment if connection.comment else connection.protocol
    )


#MathPlotLibRenderer.render(nx_graph)
PyVisRenderer.render(nx_graph)