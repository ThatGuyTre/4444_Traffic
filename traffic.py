import matplotlib.animation as animation
import matplotlib.pyplot as plt
import networkx as nx
import osmnx as ox
import random

def gen_graph(address, distance):
    """
    Generate dictionaries of vertices and edges for a road network around the given address.

    Parameters:
    - address (str): The address to center the road network around.
    - distance (float): Distance around the address to consider for the road network.

    Returns:
    - dict: Dictionary of vertices with custom IDs as keys and vertex data as tuples.
    - dict: Dictionary of edges with custom IDs as keys and edge data as tuples.
    """

    # convert address into coordinate (long, lat)
    location = ox.geocode(address)

    # generate road graph centered at location
    G = ox.graph_from_point(location, distance, network_type='drive')

    nodes = {}
    edges = {}

    edge_id = 0

    # process nodes
    for node, data in G.nodes(data=True):
        is_traffic_signal = data.get('highway') == 'traffic_signals'
        color = random.choice(['red', 'green'])
        delay = random.randint(4, 8) if is_traffic_signal else 0
        delay_temp = delay
        nodes[node] = (
            data.get('highway', None),
            None,
            0,
            data['x'],
            data['y'],
            delay,
            delay_temp,
            color
        )

    # process edges
    for u, v, data in G.edges(data=True):
        edge_id = (u, v)
        edges[edge_id] = (
            u,
            v,
            data.get('name', None),
            'one-way' if data.get('oneway', False) else 'two-way',
            data.get('geometry', None),
            'major' if data.get('highway') in ['motorway', 'trunk', 'primary'] else 'minor',
            data['length'],
            data.get('maxspeed', None)
        )

    return nodes, edges

import matplotlib.pyplot as plt
import networkx as nx
import matplotlib.animation as animation

import matplotlib.pyplot as plt
import networkx as nx
import matplotlib.animation as animation

def animate_graph(vertices, edges, path_ids):
    """
    Animates the graph with the path from start to goal highlighted.

    Parameters:
    - vertices (dict): A dictionary of node information.
    - edges (dict): A dictionary of edge information.
    - path_ids (list): A list of node IDs representing the path from start to goal.

    Returns:
    - None
    """

    # Initialize a directed graph
    G = nx.DiGraph()

    # Add nodes to the graph
    sorted_vertices = sorted(vertices.items(), key=lambda x: x[0])
    for node_id, node_data in sorted_vertices:
        G.add_node(node_id, pos=(node_data[3], node_data[4]), type=node_data[0], color = node_data[-1])

    # Add edges to the graph
    for edge_id, edge_data in edges.items():
        G.add_edge(edge_data[0], edge_data[1], geometry=edge_data[4], direction=edge_data[3])

    # Node positions for plotting
    pos = {node_id: (node_data[3], node_data[4]) for node_id, node_data in vertices.items()}

    # Create plot
    fig, ax = plt.subplots()

    def update(num):
        ax.clear()

        # Draw nodes based on their type (only traffic signals and stop signs)
        traffic_signal_nodes = [node_id for node_id, node_data in vertices.items() if node_data[0] == 'traffic_signals']
        stop_sign_nodes = [node_id for node_id, node_data in vertices.items() if node_data[0] == 'stop']

        for node_id in traffic_signal_nodes:
            node_data = list(vertices[node_id])
            if node_data[-2] <= 1:
                node_data[-1] = 'green' if node_data[-1] == 'red' else 'red'
                node_data[-2] = node_data[-3]
            else:
                node_data[-2] = node_data[-2] - 1

            vertices[node_id] = tuple(node_data)

        node_colors = [vertices[node_id][-1] for node_id in traffic_signal_nodes]

        nx.draw_networkx_nodes(G, pos, nodelist=traffic_signal_nodes, node_size=50, node_color=node_colors, ax=ax)
        nx.draw_networkx_nodes(G, pos, nodelist=stop_sign_nodes, node_size=50, node_color='gray', ax=ax)

        # Draw all edges with thin lines, respecting geometry
        for u, v, data in G.edges(data=True):
            if 'geometry' in data and data['geometry'] is not None:
                points = list(data['geometry'].coords)
                plt.plot(*zip(*points), color='black', lw=1)
            else:
                point1 = pos[u]
                point2 = pos[v]
                plt.plot([point1[0], point2[0]], [point1[1], point2[1]], color='black', lw=1)

        # Draw path nodes and edges up to the current step
        if num > 0:
            path_edges = [(path_ids[i], path_ids[i+1]) for i in range(num-1)]
            for u, v in path_edges:
                if G[u][v]['geometry'] is not None:
                    points = list(G[u][v]['geometry'].coords)
                    plt.plot(*zip(*points), color='green', lw=2)
                else:
                    plt.plot([pos[u][0], pos[v][0]], [pos[u][1], pos[v][1]], color='green', lw=2)

        # Label the start and goal nodes with pink color
        if path_ids:
            start_node, goal_node = path_ids[0], path_ids[-1]
            nx.draw_networkx_labels(G, pos, labels={start_node: 'Start'}, font_color='blue', ax=ax)
            nx.draw_networkx_labels(G, pos, labels={goal_node: 'Goal'}, font_color='blue', ax=ax)

        ax.set_title(f"Step {num}/{len(path_ids)}")

    ani = animation.FuncAnimation(fig, update, frames=len(path_ids) + 1, interval=500, repeat=False)

    plt.show()

import matplotlib.pyplot as plt
import networkx as nx

def plot_graph(vertices, edges, path_ids):
    """
    Plots the graph with the path from start to goal highlighted.

    Parameters:
    - vertices (dict): A dictionary of node information.
    - edges (dict): A dictionary of edge information.
    - path_ids (list): A list of node IDs representing the path from start to goal.

    Returns:
    - None
    """

    # Initialize a directed graph
    G = nx.DiGraph()

    # Add nodes to the graph
    sorted_vertices = sorted(vertices.items(), key=lambda x: x[0])
    for node_id, node_data in sorted_vertices:
        G.add_node(node_id, pos=(node_data[3], node_data[4]), type=node_data[0], color = node_data[-1])

    # Add edges to the graph
    for edge_id, edge_data in edges.items():
        G.add_edge(edge_data[0], edge_data[1], geometry=edge_data[4], direction=edge_data[3])

    # Node positions for plotting
    pos = {node_id: (node_data[3], node_data[4]) for node_id, node_data in vertices.items()}

    # Create plot
    fig, ax = plt.subplots()

    # Draw nodes based on their type (only traffic signals and stop signs)
    traffic_signal_nodes = [node_id for node_id, node_data in vertices.items() if node_data[0] == 'traffic_signals']
    stop_sign_nodes = [node_id for node_id, node_data in vertices.items() if node_data[0] == 'stop']

    node_colors = [vertices[node_id][-1] for node_id in traffic_signal_nodes]

    nx.draw_networkx_nodes(G, pos, nodelist=traffic_signal_nodes, node_size=50, node_color=node_colors, ax=ax)
    nx.draw_networkx_nodes(G, pos, nodelist=stop_sign_nodes, node_size=50, node_color='gray', ax=ax)

    # Draw all edges with thin lines, respecting geometry
    for u, v, data in G.edges(data=True):
        if 'geometry' in data and data['geometry'] is not None:
            points = list(data['geometry'].coords)
            plt.plot(*zip(*points), color='black', lw=1)
        else:
            point1 = pos[u]
            point2 = pos[v]
            plt.plot([point1[0], point2[0]], [point1[1], point2[1]], color='black', lw=1)

    # Draw path nodes and edges
    if path_ids:
        path_edges = [(path_ids[i], path_ids[i+1]) for i in range(len(path_ids)-1)]
        for u, v in path_edges:
            if G[u][v]['geometry'] is not None:
                points = list(G[u][v]['geometry'].coords)
                plt.plot(*zip(*points), color='green', lw=2)
            else:
                plt.plot([pos[u][0], pos[v][0]], [pos[u][1], pos[v][1]], color='green', lw=2)

        # Label the start and goal nodes with blue color
        start_node, goal_node = path_ids[0], path_ids[-1]
        nx.draw_networkx_labels(G, pos, labels={start_node: 'Start'}, font_color='blue', ax=ax)
        nx.draw_networkx_labels(G, pos, labels={goal_node: 'Goal'}, font_color='blue', ax=ax)

    plt.show()


def list_nodes(vertices):
    """
    Print details of each node in the vertices dictionary.

    Parameters:
    - vertices (dict): Dictionary of vertices.
    """
    print("Nodes:")
    for node_id, node_data in vertices.items():
        print(f"ID: {node_id}, OSM ID: {node_data[0]}, Type: {node_data[1]}, State: {node_data[2]}, Traffic: {node_data[3]}, Longitude: {node_data[4]}, Latitude: {node_data[5]}")

def list_edges(edges):
    """
    Print details of each edge in the edges dictionary.

    Parameters:
    - edges (dict): Dictionary of edges.
    """
    print("Edges:")
    for edge_id, edge_data in edges.items():
        print(f"ID: {edge_id}, From: {edge_data[0]}, To: {edge_data[1]}, Name: {edge_data[2]}, Direction: {edge_data[3]}, Geometry: {edge_data[4]}, State: {edge_data[5]}")
