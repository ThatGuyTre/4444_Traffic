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
    
    x1, y1 = nodes[node1][3], nodes[node1][4]  
    x2, y2 = nodes[node2][3], nodes[node2][4]  
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


class RoadNetworkProblem(Problem):

    def __init__(self, initial, goal, graph, nodes, edges):
        super().__init__(initial, goal)
        self.graph = graph
        self.nodes = nodes  
        self.edges = edges

    def actions(self, state):
        return list(self.graph.successors(state))
    
    def result(self, state, action):
        return action
    
    def path_cost(self, c, state1, action, state2):

        node_color = self.nodes[state1][-1]
        node_delay = self.nodes[state1][-2]

        edge_key = (state1, state2)

        if edge_key in self.edges:
            edge_length = self.edges[edge_key][-1]
        else:
            edge_length = 0

        speed_limit = 45 if self.nodes[state1][-2] == 'major' else 25
        speed_limit_factor = edge_length / speed_limit

        #print(f"Edge from {state1} to {state2}: Length = {edge_length}")
        
        if node_color == 'red':
            return c + node_delay + (speed_limit_factor / 100)
        else:
            return c + 1 + speed_limit_factor

    
    def h(self, node):
        return heuristic(node.state, self.goal, self.nodes)  