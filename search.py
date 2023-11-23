from aima3.search import Problem, astar_search
import math

def heuristic(node1, node2, nodes):
    """
    Heuristic function estimating the cost between two nodes.

    Parameters:
    - node1, node2 (int): The node IDs for which the heuristic cost is to be calculated.
    - nodes (dict): A dictionary of node information including coordinates.

    Returns:
    - float: The estimated cost between node1 and node2.
    """
    
    x1, y1 = nodes[node1][3], nodes[node1][4]  # Adjusted indices
    x2, y2 = nodes[node2][3], nodes[node2][4]  # Adjusted indices
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


class RoadNetworkProblem(Problem):

    def __init__(self, initial, goal, graph, nodes):
        super().__init__(initial, goal)
        self.graph = graph
        self.nodes = nodes  # Store the nodes dictionary

    def actions(self, state):
        return list(self.graph.successors(state))
    
    def result(self, state, action):
        return action
    
    def path_cost(self, c, state1, action, state2):
        return c + 1
    
    def h(self, node):
        return heuristic(node.state, self.goal, self.nodes)  # Use the nodes dictionary
