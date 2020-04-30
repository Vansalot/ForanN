import main
import math
import copy
from enum import Enum

	##############################################
	### Board setup, not used during "runtime" ###
	##############################################


def setupSectors(gridCost, boardSize):
	'''
	Set up 5 sectors in the gridcost dictionary, it will be populated with the total cost of each sector in another function.
	NB: The values in "coords" are range values meant to be used when calculating coords. e.g sector_1 coords: [0,5], [0,5] will mean that 
	sector 1 x cords are in range 0, 5, and y cords are in range 0,5. Which means that the sector is in the top left corner.
	
	**NNB**: Note that ranges for sector 2,3,4 will become longer than the actual coordinate list. E.g if the board is 
	0,9 / 0,9 coordinate wise, the ranges for the sector_2 will become [0, 5], [5, 10], this is so range will be used correctly
	when calculating sector cost.
	'''
	width = boardSize[0]
	height = boardSize[1]
	gridCost["sectors"] = {}

	gridCost["sectors"]["sector_1"] = {
	"coords": [[0, int(width / 2)], [0, int(height / 2)]],
	"cost": 0,
	}
	gridCost["sectors"]["sector_2"] = {
	"coords": [[int(width / 2), width],[0, int(height / 2)]],
	"cost": 0,
	}
	gridCost["sectors"]["sector_3"] = {
	"coords": [[0, int(width / 2)],[int(height / 2), height]],
	"cost": 0,
	}
	gridCost["sectors"]["sector_4"] = {
	"coords": [[int(width / 2), width - 1],[int(height / 2), height]],
	"cost": 0,
	}
	gridCost["sectors"]["sector_5"] = {
	"coords": [[int(width / 4), int((width / 4) * 3)],[int(height / 4), int((height / 4) * 3)]],
	"cost": 0,
	}
	return gridCost


def getSectorCost(gridCost):
	'''
	Divide the board into 5 sectors topleft, topright, bottomleft, bottomright and center. 
	Calculate the total cost of each sector and store it somewhere, so that we can find out where it is least dangerous to move.
	'''

	for sector in gridCost["sectors"]:
		currentsectorCost = 0
		for x in range(gridCost["sectors"][sector]["coords"][0][0], gridCost["sectors"][sector]["coords"][0][1]):
			for y in range(gridCost["sectors"][sector]["coords"][1][0], gridCost["sectors"][sector]["coords"][1][1]):
				currentsectorCost += gridCost[str(x) + ', ' + str(y)]
				#sectorCost += gridCost[getBoardLocation(x, y)]
		gridCost["sectors"][sector]["cost"] = currentsectorCost

	'''#debug:
	for sector in gridCost["sectors"]:
		print(sector, str(gridCost["sectors"][sector]["cost"]))
	'''

	
def createGridCost(boardSize):
	'''
	sets up the cost matrix for each node on the board with default value = 1.
	'''
	# remove
	gridCost = {}

	for column in range(boardSize[0]):
		for row in range(boardSize[1]):
            
			gridCost[str(column) + ', ' + str(row)] = 1
    
	gridCostWithSectors = setupSectors(gridCost, boardSize)

	return gridCostWithSectors


def getValidMoves(position, boardSize):
        '''
        input position and iterate through the possible directions to 
        check if the move is valid. Return the valid move coordinates.
        example: input coords [0, 0] should return valid moves [[1, 0], [0, 1]]
        '''
        neighbours = [ [-1, 0], [1, 0], [0, -1], [0, 1] ]
        validMoveCords = []

        for neighbour in neighbours:
            newPos = addPoint(position, neighbour)
            if isValidPoint(newPos, boardSize) == True:
                validMoveCords.append(newPos)
        
        return validMoveCords


def addPoint(a, b):
    '''
    return new coordinate based on the cordinate inputs. Used during 
    checking of neighbouring tiles.
    a = current position
    b = neighbor position
    '''
    return [a[0] + b[0], a[1] + b[1]]


def isValidPoint(pos, boardSize):
    '''
    input coordinate, return true if the coordinate is on the board
    '''
    return pos[0] >= 0 and pos[1] >= 0 and pos[0] < boardSize[0] and pos[1] < boardSize[1]


	#######################
	### Board setup END ###
	#######################

def createGrid(boardSize, gridCost):
	'''
	Creates a dictionary of all the cords on the board with cost related to the adjacent tiles.
	e.g '1, 1: {'0, 1': 200, '1, 0': 200, '1, 2': 1, '2, 1': 1}
	This means that tile "1, 1" borders tile 0, 1 which have a cost of 200, tile 1, 0, with cost 200, 1,2 with cost 1, etc.
	This dict is what dijkstra uses when calculating the shortest path.
	'''
	import random
	grid = {}
	for column in range(boardSize[0]):
		for row in range(boardSize[1]):
            
			grid[str(column) + ', ' + str(row)] = {}
            
			validMoveCords = []
			validMoveCords = getValidMoves([column, row], boardSize)

			for move in validMoveCords:
				grid[str(column) + ', ' + str(row)]  [str(move[0]) + ', ' + str(move[1])] = gridCost[str(move[0]) + ', ' + str(move[1])]
	return grid


def getBoardLocation(x, y):
	'''
	input a coordinate, and get the coordinate as a string in return.
	'''
	return str(x) + ', ' + str(y)


def getSnakeLocation(gameData, index):
	'''
	return a list of strings of locations to a snake, based on the index.
	'''
	snakeCordsList = []
	for location in gameData["board"]["snakes"][index]["body"]:
		snakeCordsList.append(str(location["x"]) + ', ' + str(location["y"]))
	
	return snakeCordsList


def updateGridCost(costMatrix, gameData):
	'''
	Update the cost of each tile, based on the json data received from the battlesnake engine.
	'''
	### set up fresh gridCost to make it ready for updated data ###
	boardWidth = gameData["board"]["width"]
	boardHeight = gameData["board"]["height"]
	boardSize = [boardWidth, boardHeight]
	gridCost = createGridCost([boardWidth, boardHeight])

	### Update cost based on edges and corners ###

	for x in range(boardWidth):
		for y in range(boardHeight):		
			# set cost for top left corner and top and left edges.
			if x == 0 or y == 0:
				if x == 0 and y == 0:
					gridCost[getBoardLocation(x, y)] = costMatrix["corner"]
				else:
					gridCost[getBoardLocation(x, y)] = costMatrix["edge"]

			# set cost for bottom right corner, and bottom and left edges
			if y == boardHeight - 1 or x == boardWidth -1:
				gridCost[getBoardLocation(x, y)] = costMatrix["edge"]
			if y == boardHeight - 1 and x == boardWidth -1:
				gridCost[getBoardLocation(x, y)] = costMatrix["corner"]

			# set cost for top right, and bottom left corner.		
			if y == 0 and x == boardWidth - 1:
				gridCost[getBoardLocation(x, y)] = costMatrix["corner"]
			if y == boardHeight - 1 and x == 0:
				gridCost[getBoardLocation(x, y)] = costMatrix["corner"]

	### Update cost based on snake locations ### 

	# set id of your own snake, to be used to ensure own head location
	ownSnakeId = gameData["you"]["id"]

	index = 0 # to be used to find the correct snake in the gameData list.
	for snake in gameData["board"]["snakes"]:
		# set up a list of stringed up locations for a snake
		singleSnakeLocations = getSnakeLocation(gameData, index)
		gridCost[singleSnakeLocations[-1]] = costMatrix["snaketail"]
		index += 1
		
		if snake["id"] == ownSnakeId:
			# If it's your own snake set cost = ownhead cost.
			gridCost[singleSnakeLocations[0]] = costMatrix["ownhead"]
		else:
            # If it's other snakes head, set cost = snakehead.
			gridCost[singleSnakeLocations[0]] = costMatrix["snakehead"]

		# set up cost for the snake body.
		for location in singleSnakeLocations[1:-1]:
			gridCost[location] = costMatrix["snakebody"]
	
		
	### Update for food tiles ### 
	index = 0
	for food in gameData["board"]["food"]:
		#gridCost[food["x"]] + ', ' + [food["y"]]
		gridCost[getBoardLocation(food["x"], food["y"])] = costMatrix["food"]



		# close to other snake heads
	getSectorCost(gridCost)

	return gridCost

def getSafeSector(gridCostsectors):
	'''
	input the gridCost of the sectors and returns the 2 safest sectors.
	'''
	gridCostsectorsCopy = gridCostsectors.copy()
	lowestVal = 99999999999
	lowestValSector = '' 
	
	secondlowestValSector = ''
	
	safeSectors = []

	lowCheckVal = 99999999999
	lowCheckValSector = ''
	for sector in gridCostsectorsCopy:
		if gridCostsectorsCopy[sector]["cost"] < lowCheckVal:
			lowCheckVal = gridCostsectorsCopy[sector]["cost"]
			lowCheckValSector = sector

	lowestVal = lowCheckVal
	lowestValSector = str(lowCheckValSector)
	
	del gridCostsectorsCopy[sector]

	lowCheckVal2 = 99999999999
	for sector in gridCostsectorsCopy:
		if gridCostsectorsCopy[sector]["cost"] < lowCheckVal2:
			lowCheckVal2 = gridCostsectorsCopy[sector]["cost"]
			lowCheckValSector = sector


	if lowCheckVal2 < lowestVal:
		secondlowestValSector = str(lowestValSector)
		lowestValSector = str(lowCheckValSector)

	else: 
		secondlowestValSector = str(lowCheckValSector)

	print('# debug: Safest sectors are: ', lowestValSector, secondlowestValSector)
	return lowestValSector, secondlowestValSector
	


	#### DIJKSTRA MAGIC ####
	#### DIJKSTRA MAGIC ####
	#### DIJKSTRA MAGIC ####

def dijkstra(grid, start, goal, gridCost):
	'''
	This is where the magic happens.
	'''
	shortest_distance = {} # records cost to reach that node, updated as we iterate through the nodes
	track_predecessor = {} # keep track of path has led us to this node.
	unseenNodes = grid.copy() # to iterate through the graph
	infinity = 9999 # large number
	track_path = [] # trace journey back to the sorce node. optimal route

	for node in unseenNodes:
		# set distances for dijkstra
		shortest_distance[node] = infinity
	# set start distance to 0
	shortest_distance[start] = 0

	while unseenNodes:
		
		min_distance_node = None

		# find out which node is closer(has less cost.)
		for node in unseenNodes:
			if min_distance_node is None:
				min_distance_node = node
			elif shortest_distance[node] < shortest_distance[min_distance_node]:
				min_distance_node = node

		# set up path options for the closest node. 
		path_options = grid[min_distance_node].items()

		for child_node, weight in path_options:
			# update distance to the nodes. 
			if weight + shortest_distance[min_distance_node] < shortest_distance[child_node]:
				shortest_distance[child_node] = weight + shortest_distance[min_distance_node]
				track_predecessor[child_node] = min_distance_node

		# pop out the min distance node, cause we are done processing it.
		unseenNodes.pop(min_distance_node)

	currentNode = goal

	while currentNode != start:
		try:
			track_path.insert(0, currentNode)
			currentNode = track_predecessor[currentNode]
			# Keyerror exception, whyyyyyy

		except KeyError:
			print('Path is not reachable')
			return None

	track_path.insert(0, start)

	if shortest_distance[goal] != infinity:
		print("Path from " + start + " to " + goal + ":")
		print("Shortest distance is " + str(shortest_distance[goal]), "Step count: " + str(len(track_path)))
		print("Optimal path is " + str(track_path))

		return(track_path[1])

