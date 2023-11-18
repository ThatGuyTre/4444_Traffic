from search import *

class TrafficProblem(Problem):

	# Initialize the problem with the root node cost = 0
	def __init__ (self, initial_state, goal_state=()):
		super().__init__(initial_state, goal_state)
		self.overall_cost = 0

	def actions(self, state):
		# Actions: Visit a new node through the intersection

		# Create list of possible actions
		actionList = []
		# Current location of agent
		agentX, agentY = state[0]

		return actionList
	
	def result(self, state, action):
		# This is the successor function.

		# The state can be shown by a tuple of information:
			# (currentNode the agent is at, the numpy graph, the current time)

		# Get the current node the agent is at
		# Get the current map of the environment

		# Using the action, determine the new state of the agent and the node it should be at
		# Use a list to make the tuple mutable (may not be relevant for traffic problem)


		# ***This will also be where the "time" is advanced to change the state of the traffic lights and levels


		resultState = list(state)
  
		# Make the entire resulting state back into the original tuple form and return it.
		resultState = tuple(resultState)
	 
		return resultState
	
	def path_cost(self, c, state1, action, state2):

		# For the traffic problem, this will take into account the traffic level of the node,
		# the speed limit, and the distance to the node.
		# Most likely - no traffic = 1.1* the speed limit
		# 			 light traffic = 1.0* the speed limit (10-20 percent?)
		#			 moderate traffic = 0.7* the speed limit (30-50 percent?)
		#			 heavy traffic = 0.5* the speed limit (60-80 percent?)
		#			 gridlock = 0.1* the speed limit (80-100 percent?)

		# Potential lerping between these threshold (like a fan curve)

		# Path cost is the cost of the action + the cost of the state.
		# State2 is used if the agent performed suck
		if action == "suck":
			self.overall_cost = c + 1 + 2*len(state2[1])
		else:
			self.overall_cost = c + 1 + 2*len(state1[1])

		return self.overall_cost
	
	def goal_test(self, state):
		# If there are no dirty spaces remaining, return True. Else, return False.
		# self.goal defaults to an empty list
		return state[1] == self.goal
	
		# Testing to see if the agent is at the goal location

	def ws(self, state):	
		# w(s) = number of dirty squares in the state
		return len(state[1])
	
		# w(s) is likely the estimated time to get somewhere based on how the traffic is in the current state.
	
	def dist(self, state):
		# Get location of agent
		agentX, agentY = state[0]

		# Calculate manhattan distance to nearest dirty square
		minDist = 10 # 10 is the maximum distance for a 5x5 map
		# Iterate through the map and find the distance to the nearest dirty square
		for dirtySpace in state[1]:
			# Calculate the distance to the dirty square
			dist = abs(agentX - dirtySpace[0]) + abs(agentY - dirtySpace[1])
			# If the distance is less than the current minimum, update the minimum
			if(dist < minDist):
				minDist = dist
		# Return the minimum distance
		return minDist
	
	# Heuristic functions. h1 uses just the distance along with the activatedness of the node
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

def runTrafficProblem():
	startingSquare = (1, 1)
	dirtySquares = ((1, 5), (2, 5), (3, 5), (4, 5), (5, 5))

	trafficProblem = TrafficProblem((startingSquare, dirtySquares), ())

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