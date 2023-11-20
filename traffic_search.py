from search import *

# Functions within TrafficProblem are documented within search.py

def findVertexFromCoordinates(longitude, latitude, vertices):
	"""
	Find the vertex with the given coordinates.
	May be unneeded.

	Parameters:
	- longitude (float): Longitude of the vertex.
	- latitude (float): Latitude of the vertex.
	- vertices (list): List of vertices.

	Returns:
	- Vertex: Vertex with the given coordinates.
	"""
	for vertex in vertices:
		if vertex.longitude == longitude and vertex.latitude == latitude:
			return vertex
	return None

def getEdgesFromVertex(vertex, edges):
    """
    Gets all edges that are connected to the vertex.

    Parameters:
    - vertex (Vertex): The vertex to find edges for.
    - edges (list): List of edges.

    Returns:
    - list: List of edges connected to the vertex.
    """
    edgesFromVertex = []
    for edge in edges:
        if edge.u == vertex.ID or edge.v == vertex.ID:
            edgesFromVertex.append(edge)
    return edgesFromVertex

class TrafficProblem(Problem):

	# Initialize the problem with the root node cost = 0
	def __init__ (self, initial_state, goal_state=()):
		super().__init__(initial_state, goal_state)
		self.overall_cost = 0

	def actions(self, state):
		# Actions: Visit a new node through the intersection
		# Create list of possible actions
		actionList = getEdgesFromVertex(self, state.edges)

		return actionList
	
	def result(self, state, action):
		# This is the successor function.

		# The state is simply the map of the environment, with disabled/enabled nodes based on the time

		# Get the current node the agent is at
		# Get the current map of the environment

		# Using the action, determine the new state of the agent (as in, change self to the new Vertex)
		# Use a list to make the tuple mutable (may not be relevant for traffic problem)


		#* This will also be where the "time" is advanced to change the state of the traffic lights and levels
	 
		return state
	
	def path_cost(self, c, state1, action, state2):

		# For the traffic problem, this will take into account the traffic level of the node,
		# the speed limit, and the distance to the node. Probably should be revised.
		# Most likely - no traffic = 1.1* the speed limit 		(1)
		# 			 light traffic = 1.0* the speed limit 		(2)
		#			 moderate traffic = 0.7* the speed limit 	(3)
		#			 heavy traffic = 0.5* the speed limit 		(4)
		#			 gridlock = 0.1* the speed limit 			(5)

		# Iterate through the list of porential actions
		for edge in state1.edges:
			# If the action is the current edge
			if edge == action:
				# Get the traffic level of the edge
				trafficLevel = edge.traffic
				# Get the speed limit of the edge
				speedLimit = edge.speed_limit
				# Get the distance to the edge
				distance = edge.distance
				# Calculate the cost of the edge
				cost = c # Previous cost
				# If the traffic level is 0, the cost is 1.1* the speed limit
				if trafficLevel == 1:
					cost += 1 / (1.1*speedLimit * distance)
				# If the traffic level is 1, the cost is 1.0* the speed limit
				elif trafficLevel == 2:
					cost += 1 / (1.0*speedLimit * distance)
				# If the traffic level is 2, the cost is 0.7* the speed limit
				elif trafficLevel == 3:
					cost += 1 / (0.7*speedLimit * distance)
				# If the traffic level is 3, the cost is 0.5* the speed limit
				elif trafficLevel == 4:
					cost += 1 / (0.5*speedLimit * distance)
				# If the traffic level is 4, the cost is 0.1* the speed limit
				elif trafficLevel == 5:
					cost += 1 / (0.1*speedLimit * distance)
				# Return the cost
				return cost
		# If the action is not in the list of edges, return -1
		return -1
	
	# Made for programming project. May not be needed for this.
	def goal_test(self, state):
		# Goal test: self Vertex is the same as the goal Vertex
		return self

	# Made for programming project. May not be needed for this.
	def ws(self, state):	
		# w(s) = number of dirty squares in the state
		return len(state[1])
	
		# w(s) is likely the estimated time to get somewhere based on how the traffic is in the current state.
	
	
	# Heuristic functions. h1 uses just the distance along with the activatedness of the node
	# Both of these are unchanged from my programming project so far
	def h1n(self, node):
		# h1(n) = w(n) + dist(n)
		# h1 looks at the number of dirty squares
		# and the distance to the nearest dirty square
		return self.ws(node.state) + self.dist(node.state)
	
	# h2 looks at h1 in addition to the traffic levels.
	def h2n(self, node):
		# h2(n) = 2*w(n) - 1 + dist(n)
		# h2 looks at the number of actions to clean dirty squares
		# and the distance to the nearest dirty square
		return 2*self.ws(node.state) - 1 + self.dist(node.state)
	
# Now that we have defined the problem, states, and actions, we can create the problem!

def runTrafficProblem(startingLocation, goalState, vertices, edges):
	# Starting state should be the whole map, startingLocation is the location of the agent
	startingState = (vertices, edges)
	trafficProblem = TrafficProblem(startingLocation, startingState, ())
	# Goal state should be the map where the agent is at the goal location
	# May not be needed for this problem
	trafficProblem.goal_test = goalState

	print("Beginning Traffic Problem with A* Search and h1(n) heuristic:")

	nodesExpanded = 0

	h1Iteration = astar_search(trafficProblem, trafficProblem.h1n, True)

	# Output the path taken by the agent
	for path in h1Iteration.path():
		print('{!s:60s} Action taken: {!s:10s} Path Cost: {}'.format(path, path.action, path.path_cost))
		nodesExpanded += 1

	print("Total nodes expanded: " + str(nodesExpanded) + "\n")

	#

	print("Beginning Traffic Problem with A* Search and h2(n) heuristic:")

	nodesExpanded = 0

	h2Iteration = astar_search(trafficProblem, trafficProblem.h2n, True)

	# Output the path taken by the agent
	for path in h2Iteration.path():
		print('{!s:60s} Action taken: {!s:10s} Path Cost: {}'.format(path, path.action, path.path_cost))
		nodesExpanded += 1

	print("Total nodes expanded: " + str(nodesExpanded) + "\n")