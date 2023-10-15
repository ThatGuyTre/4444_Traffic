import matplotlib.pyplot as plt
import networkx as nx
import osmnx as ox
import numpy as np

"""
Generates graph data around given address using a specified distance.

Vertices represnt intersections or endpoints with attributes: ID, type (traffic light,
stop light, None), state (red, green), traffic (0-5), longitude, and latitude.

Edges signify roads connecting vertices with attributes: name, speed limit, type (one-way
or bi-directional), and geometry (keep or else we lose fancy graphs).
"""
def generate_graph(address, distance):
    
    # convert address into coordinate (longitude, latitude)
    location = ox.geocode(address)
    
    # generate road graph centered at location coordinate
    G = ox.graph_from_point(location, distance, network_type='drive')
    
    # extract nodes and edges from graph and convert to numpy arrays
    node_data = np.array(list(G.nodes(data=True)))
    edge_data = np.array(list(G.edges(data=True)))
    
    # construct vertice list
    vertices = [
        {
            'ID': node,                           # node ID
            'type': data.get('highway', None),    # node type: traffic light, stop sign, None
            'state': None,                        # state for traffic light (green, red)
            'traffic': 0 ,                        # traffic level (0-5)
            'longitude': data['x'],               # longitude
            'latitude': data['y']                 # latitude
        }
        for node, data in node_data
    ]
    # construct edge list
    edges = [
        (
            u,
            v,
            {
                'name': data.get('name', None),                                        # street name
                'speed_limit': data.get('maxspeed', None),                             # speed limit
                'direction': 'one-way' if data.get('oneway', False) else 'two-way',    # one way? or two way
                'geometry': data.get('geometry', None)                                 # road geometry (needed for cool graphs)
            }
        )
        for u, v, data in edge_data
    ]
    
    return vertices, edges

"""
Visualize bi-directional graph given provided vertices and edges.

Nodes are distinguished by type (red if stop sign, green if traffic
light, blue if None) and edges by directionality (pink if one-way
or black if bi-directional).
"""
def draw_graph(vertices, edges):
    
    # initialize multi-directional graph
    G = nx.MultiDiGraph()
    
    # generate dictionary of node positions using ID as key and longitude, latitude pairs as values
    pos = {v['ID']: (v['longitude'], v['latitude']) for v in vertices}
    
    # determine node colors (red if stop sign, green if traffic signal, blue if None)
    node_colors = np.array(['red' if v['type'] == 'stop' else 'green' if v['type'] == 'traffic_signals' else 'blue' for v in vertices])
    
    # determine edge colors (black  bi-directional, pink one-way)
    edge_colors = np.array(['pink' if e[2]['direction'] == 'one-way' else 'black' for e in edges])
    
    # add edges to graph: use geometry if possible, straight line otherwise.
    for u, v, data in edges:
        G.add_edge(u, v, path=data.get('geometry', None).coords if data['geometry'] else None)

    # adjust render size for figure
    plt.figure(figsize=(12, 12), dpi=150)  # Increased DPI for higher resolution

    # draw edges
    for u, v, data in G.edges(data=True):
        color_idx = np.where((u, v) == np.array(edges)[:, :2])[0][0]
        coords = data.get('path', [pos[u], pos[v]])
        if coords:  # Ensure coords is not None
            plt.plot(*zip(*coords), color=edge_colors[color_idx], linewidth=1.5)

    # Draw nodes (draw nodes last or else they render ugly)
    nx.draw_networkx_nodes(G, pos, node_size=40, node_color=node_colors)
    
    plt.show()

vertices, edges = generate_graph('Louisiana State University, Baton Rouge, Louisiana, USA', 1000)

draw_graph(vertices, edges)
