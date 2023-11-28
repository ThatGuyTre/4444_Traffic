# Import necessary modules
import random
import networkx as nx
from traffic import gen_graph, plot_graph, animate_graph
from search import RoadNetworkProblem
from aima3.search import astar_search

def get_random_start_goal(nodes):
    """
    Selects random start and goal node IDs from a given set of nodes.

    Parameters:
    - nodes (dict): A dictionary of nodes where keys are node IDs.

    Returns:
    - tuple: A tuple containing two randomly selected node IDs.
    """
    node_ids = list(nodes.keys())
    return random.sample(node_ids, 2)

def main():
    # Define the address and distance for the road network
    address = 'Louisiana State University, Baton Rouge, LA'
    distance = 2000

    # Generate graph nodes and edges
    nodes, edges = gen_graph(address, distance)

    # Get random start and goal IDs
    start_id, goal_id = get_random_start_goal(nodes)
    #start_id = list(nodes.keys())[59]
    #goal_id = list(nodes.keys())[22]

    # Create a directed graph for AIMA
    G = nx.DiGraph()
    for edge in edges.values():
        G.add_edge(edge[0], edge[1])  # Add edges using OSM IDs

    # Initialize and solve the road network problem
    problem = RoadNetworkProblem(start_id, goal_id, G, nodes, edges)
    result = astar_search(problem)

    # Extract node IDs from the path
    path_ids = [node.state for node in result.path()]

    # Output and plot the result
    print("Path found:", path_ids)
    #plot_graph(nodes, edges, path_ids)
    animate_graph(nodes, edges, path_ids)

if __name__ == "__main__":
    main()
