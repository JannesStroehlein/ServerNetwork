from networkx.classes import MultiDiGraph
from pyvis.network import Network

class PyVisRenderer:
    @staticmethod
    def render(graph : MultiDiGraph):
        # Create the network
        net = Network(notebook=True, cdn_resources="remote",
                      directed=True, filter_menu=True,
                      select_menu=True,
                      bgcolor="#222222",
                      font_color="white",
                      height="750px",
                      width="100%"
                      )

        net.from_nx(graph)
        net.toggle_physics(True)
        net.show_buttons()
        net.options.nodes = {
            'borderWidth': 1,
            'borderWidthSelected': 2,
            'color': {
                'border': '#2B7CE9',
                'background': '#97C2FC',
                'highlight': {
                    'border': '#2B7CE9',
                    'background': '#D2E5FF'
                },
                'hover': {
                    'border': '#2B7CE9',
                    'background': '#D2E5FF'
                }
            },
            'font': {
                'color': 'white',
                'size': 10,
                'face': 'verdana',
                'background': 'none',
                'strokeWidth': 0
            },
            'opacity': 1,
            'labelHighlightBold': True,
            'shape': 'ellipse',
        }
        net.options.edges.arrows = {
            "middle": {
                "enabled": True,
                "scaleFactor": 0.5
            },
            "to": {
                "enabled": True,
                "scaleFactor": 0.5
            },
            "from": {
                "enabled": True,
                "scaleFactor": 0.5
            }
        }
        net.options.edges.font = {
            "color": "#ffffff",
            "strokeWidth": 0,
            "size": 10
        }
        net.options.edges.dashes = True
        net.options.edges.color = '#fafafa'

        net.show("network.html")

        PyVisRenderer.enable_html_titles("network.html")

    @staticmethod
    def enable_html_titles(filename:str):
        with (open(filename, 'r') as file):
            file_data = file.read()
            tom_select_index = file_data.index("TomSelect")

            everything_after_tom_select = file_data[tom_select_index:]
            semicolon_index = everything_after_tom_select.index(";")

            insert_function_index = tom_select_index + semicolon_index + 1

            file_data = file_data[:insert_function_index] + "\n" + \
            """
            /// Add in this js function here after the global variables declaration
            function htmlTitle(html) {
                const container = document.createElement("div");
                container.innerHTML = html;
                return container;
            };
            """ \
               + file_data[insert_function_index:]
            
            node_json, node_json_start_index, node_json_end_index = PyVisRenderer.get_json_data(file_data, 'nodes = new vis.DataSet(', ');\n')
            edge_json, edge_json_start_index, edge_json_end_index = PyVisRenderer.get_json_data(file_data, 'edges = new vis.DataSet(', ');\n')

            insertion_index = node_json_start_index

            node_line_length = node_json_end_index - node_json_start_index
            edge_line_length = edge_json_end_index - edge_json_start_index

            print(len(file_data))
            node_line = file_data[node_json_start_index:node_json_end_index]
            edge_line = file_data[edge_json_start_index:edge_json_end_index]
            file_data = file_data.replace(node_line, "")
            file_data = file_data.replace(edge_line, "")

            file_data = file_data[:insertion_index] + "\n" + \
            f"""
            // parsing and collecting nodes and edges from the python
            // Under this section, parse the array of objects both nodes and edges
            // call the htmlTitle func following if-else check for "title" key before putting to new vis.Dataset()

            let jsonNodes = {node_json};
            let jsonEdges = {edge_json};

            for (let mynode of jsonNodes) {{
                if ("title" in mynode) {{
                    mynode.title =htmlTitle(mynode.title);
                  }} else {{
                      console.log("Object does not have title key");
                      }}
                  }}
                  console.log(jsonNodes);

                  for (let myedge of jsonEdges) {{
                      if ("title" in myedge) {{
                    myedge.title =htmlTitle(myedge.title);
                  }} else {{
                      console.log("Object does not have title key");
                      }}
                  }}
                  console.log(jsonEdges);

                  nodes = new vis.DataSet(jsonNodes);
                  edges = new vis.DataSet(jsonEdges);
            """ \
               + file_data[insertion_index:]

        with open(filename, 'w') as file:
            file.write(file_data)

            
    @staticmethod
    def get_json_data(data : str, line_start : str, line_end : str):
        start_index = data.index(line_start)
        end_index = start_index + data[start_index:].index(line_end)
        return data[start_index + len(line_start): end_index], start_index, end_index + len(line_end)