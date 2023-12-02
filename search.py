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
        acts = set(self.graph.successors(state))
        print("ACTIONS FOR " + str(self) + ": " + str(acts))

        # WIP - remove red nodes from actions
        # to get this to start doing stuff, change line below to
        # modified_acts = set()
        modified_acts = set(acts)

        for act in acts:
            if self.nodes[act][7] != 'red':
                modified_acts.add(act)
            else:
                print(str(act) + " was red and therefore removed from " + str(acts))

        modified_acts.add(state)

        return list(modified_acts)
    
    def result(self, state, action):
        return action
    
    def path_cost(self, c, state1, action, state2):

        node_color = self.nodes[state1][7]
        node_delay = self.nodes[state1][6]

        edge_key = (state1, state2)

        if edge_key not in self.edges:
            return float('inf')  # or any other appropriate value to indicate an invalid edge

        edge_length = self.edges[edge_key][6]
        length_miles = edge_length / 0.000621371 # convert meters to miles

        # Get the maxspeed attribute of the edge
        speed_attribute = self.edges[edge_key][7]
        # Make sure it's a string and not a list
        speed_string = speed_attribute[0] if isinstance(speed_attribute, list) and speed_attribute else speed_attribute
        # Extract the speed limit from the string
        speed_limit = int(speed_string.split(maxsplit=1)[0]) if speed_string is not None else 30
        # Calculate the speed limit factor by incorporating the edge length
        minutes_to_complete = length_miles / speed_limit * 60 # miles / (miles / hour) * (minutes / hour) = minutes

        #print(f"Edge from {state1} to {state2}: Length = {edge_length}")
        
        if node_color == 'red':
            # Cost plus 10 seconds per light "step", plus the time it takes to go down the road
            return c + (node_delay / 6) + minutes_to_complete
        else:
            # Cost plus the time it takes to go down thw road
            return c + minutes_to_complete

    
    def h(self, node):
        return heuristic(node.state, self.goal, self.nodes)  