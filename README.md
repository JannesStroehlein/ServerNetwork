![example.png](assets/example.png)

# Server Network Visualizer
[Example](#example) | [Features](#features) | [Installation](#installation) | [Usage](#usage) | [CLI Arguments](#command-line-arguments) | [Service Icons](#service-icons) | [License](#license) | [Acknowledgments](#acknowledgments)

If you self host with multiple servers you might come to the point where you wonder: "What does this thing?"
This tool helps you to build an inventory of your services and their relationships so that if you wonder what something does you can just easily look it up.

### Example
You can take a look at the data that produces the example graph at the top in the [example.yml](data/example.yml) file.
All the icons used in the example graph are located in the [icons](icons) directory.


### Features
- Display the network of a server in a graph format
- Interact with the graph by zooming in and out, panning, and selecting nodes to view more information about them
- Display the IP address of the server and the port number to connect to the server
- Add icons for services
- Filter the graph by any service attribute


## Installation
```shell
git clone https://github.com/JannesStroehlein/ServerNetwork.git
cd ServerNetwork
pip install -r requirements.txt
```

## Usage
To run the network visualizer you need to provide the data that should be displayed. 
The data is provided in a YAML file with the following structure. Currently the main.py script looks for all YAML files in the `data` directory and loads them. 

```yaml
services:
  # The name of the service is the key of the service you can use in connections. It is case-insensitive.
  - name: <string>
    
    # (Optional) Add a comment to the service.
    comment: <string>
    
    # (Optional) Specify the host is the name of the node/server the service is running on.
    host: <string>
    
    # (Optional) Set another service as the reverse proxy for this service.
    proxy: <string>
    
    # (Optional) Specify a port the service is running on.
    port: <number> 
    # You can also specify multiple ports the service is running on.
    # In this case the 'port' field should not be set
    # ports: [<number>, <number>, ...]

    # (Optional) Specify URLs that this service is reachable under.
    url: <string>
    # You can also specify multiple URLs the service is reachable under.
    # In this case the 'url' field should not be set
    # urls: [<string>, <string>, ...]

    connections:
      # The type of the connection is the key of the connection.
      # This can be a protocol like 'http' or 'https' or any other type of connection.
      <string>:
        # The name of the service the connection is pointing to.
        - <string>: 
            # (Optional) Add a comment to the connection.
            comment: <string>
        # Add more connections using the same connection type
        - <string>
      # Add more connection types 
      # <string>:
      # - <string>
  
  
  # Add more services
  - name: <string>
    connections:
      <string>:
        - <string>
```

After you have create the YAML file you can run the network visualizer with the following command:
```shell
python main.py
```
The network visualizer will create a file called `network.html`. You can open this file in your browser to view the network graph.

### Command Line Arguments
The following command line arguments are available:

| Short | Long          | Description                             | Example                              |
|-------|---------------|-----------------------------------------|--------------------------------------|
| -h    | --help        | Show the help message and exit          | `python main.py -h`                  |
| -d    | --data-file   | Specify the data file to use            | `python main.py -d data/example.yml` |
| -D    | --data-dir    | Specify the data directory to use       | `python main.py -D data`             |
| -I    | --image-dir   | Specify the path to the image directory | `python main.py --image-path icons`  |
| -o    | --output-file | Specify the output file                 | `python main.py -o my_network.html`  |

### Service Icons
This tool can display icons for services. To do this you need to provide icons (.png or .svg) in the `icons` directory.
Setting the filename of the icon to the service id in the YAML file will display the icon for that service.

For example:

| YAML                     | Icon File Location           |
|--------------------------|------------------------------|
| `name: my-service`       | `icons/my-service.png`       |
| `name: my other service` | `icons/my other service.svg` |


## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
This project uses the following libraries:
- PyYAML - MIT - [GitHub](https://github.com/yaml/pyyaml) [PyPI](https://pypi.org/project/PyYAML/)
- NetworkX - BSD-3-Clause - [GitHub](https://github.com/networkx/networkx) [PyPI](https://pypi.org/project/networkx/)
- PyVis - BSD-3-Clause - [GitHub](https://github.com/WestHealth/pyvis) [PyPI](https://pypi.org/project/pyvis/)

Icons used in the example graph:
- "[Solar Icon Set](https://www.figma.com/community/file/1166831539721848736/solar-icons-set)" by [480 Design](https://www.figma.com/@480design) is licensed under CC BY 4.0