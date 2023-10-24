import matplotlib.pyplot as plt
import networkx as nx
import osmnx as ox
import numpy as np

class Vertice:
    def __init__(self, ID, type_, state, traffic, longitude, latitude):
        self.ID = ID
        self.type = type_               # node type: traffic light, stop sign, None
        self.state = state              # state for traffic light (green, red)
        self.traffic = traffic          # traffic level (0-5)
        self.longitude = longitude      # longitude
        self.latitude = latitude        # latitude

    def __repr__(self):
        return f"<Vertice(ID={self.ID}, traffic={self.traffic})>"
    
class Edge:
    def __init__(self, u, v, name, speed_limit, direction, geometry, state):
        self.u = u                      # Starting node
        self.v = v                      # Ending node
        self.name = name                # Street name
        self.speed_limit = speed_limit  # Speed limit
        self.direction = direction      # One way or two way
        self.geometry = geometry        # Road geometry
        self.state = state              # Major or minor

    def __repr__(self):
        return f"<Edge(name={self.name}, state={self.state})>"
    
def generate_graph(address, distance):

    """
    Generate vertices and edges for a road network around the given address.

    Parameters:
    - address (str): The address to center the road network around.
    - distance (float): Distance around the address to consider for the road network.

    Returns:
    - list: List of vertices (as dictionaries).
    - list: List of edges (as tuples containing start node, end node, and a dictionary of edge attributes).
    """

    # convert address into coordinate (longitude, latitude)
    location = ox.geocode(address)

    # generate road graph centered at location coordinate
    G = ox.graph_from_point(location, distance, network_type='drive')       

    # extract nodes and edges from graph and convert to numpy arrays        
    node_data = np.array(list(G.nodes(data=True)))
    edge_data = np.array(list(G.edges(data=True)))

    # construct vertice list
    vertices = [
        Vertice(
            ID=node,
            type_=data.get('highway', None),
            state=None,
            traffic=0,
            longitude=data['x'],
            latitude=data['y']
        )
        for node, data in node_data
    ]

    # construct edge list
    edges = [
        Edge(
            u=u,
            v=v,
            name=data.get('name', None),
            speed_limit=data.get('maxspeed', None),
            direction='one-way' if data.get('oneway', False) else 'two-way',
            geometry=data.get('geometry', None),
            state='major' if data.get('highway') in ['motorway', 'trunk', 'primary'] else 'minor'
        )
        for u, v, data in edge_data
    ]

    return vertices, edges

def draw_graph(vertices, edges):

    """
    Visualize a bi-directional graph using provided vertices and edges.     

    Nodes are colored based on their type:
    - Red for stop signs
    - Green for traffic signals
    - Blue for none

    Edges are colored based on their direction:
    - Pink for one-way roads
    - Black for bi-directional roads

    Parameters:
    - vertices (list): List of vertices.
    - edges (list): List of edges.
    """

    # initialize multi-directional graph
    G = nx.MultiDiGraph()

    # generate dictionary of node positions using ID as key and longitude, latitude pairs as values
    pos = {v.ID: (v.longitude, v.latitude) for v in vertices}

    # determine node colors (red if stop sign, green if traffic signal, blue if None)
    node_colors = np.array(['red' if v.type == 'stop' else 'green' if v.type == 'traffic_signals' else 'blue' for v in vertices])

    # determine edge colors (black for bi-directional, pink for one-way)    
    edge_colors = np.array(['pink' if e.direction == 'one-way' else 'black' for e in edges])

    # add edges to graph: use geometry if possible, straight line otherwise.
    for e in edges:
        G.add_edge(e.u, e.v, path=e.geometry.coords if e.geometry else None)

    # adjust render size for figure
    plt.figure(figsize=(12, 12), dpi=150)

    # draw edges
    for u, v, data in G.edges(data=True):
        edge_object = next(edge for edge in edges if edge.u == u and edge.v == v)
        color_idx = edges.index(edge_object)
        coords = data.get('path', [pos[u], pos[v]])
        if coords:  # Ensure coords is not None
            plt.plot(*zip(*coords), color=edge_colors[color_idx], linewidth=1.5)

    # Draw nodes (draw nodes last to ensure they're on top)
    nx.draw_networkx_nodes(G, pos, node_size=40, node_color=node_colors)    

    plt.show()⏎ 