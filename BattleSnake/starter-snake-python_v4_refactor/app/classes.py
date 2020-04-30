import main
import math
import copy
from enum import Enum


class Gameboard():
	
	costMatrix = {
    "ownhead": 0,
	"empty": 1,
	"food": 5,
	"edge": 200,
	"corner": 300,
	"snakeheadclose": 799,
	"snakehead": 9999,
	"snakebody": 9999,
    "snaketail": 699,
    }


	def __init__(self, data):
		'''
		Object of the board, contains the tiles of the board.
		'''
		self.boardSize = [data["board"]["height"],data["board"]["width"]]
		self.foodCoords = data["board"]["food"] ##
		self.foodCount = len(self.foodCoords) ##
		self.ownSnake = data["you"]["body"] ##
		self.ownSnakeHead = data["you"]["body"][0] ##
		self.ownSnakeSize = len(self.ownSnakeHead) ##

		self.tiles = self.createTiles(self.boardSize)
		self.updateTiles(data)

	def createTiles(self, boardSize):
		'''
		Set up the board, using a class object for each tile on the board. 
		'''
		tiles = []
		for x in range(boardSize[0]):
			templist = []
			for y in range(boardSize[1]):
				templist.append(Tile())
			tiles.append(templist)
		return tiles
	
	
	def updateTiles(self, data):
		# update tile cost every round. 
		'''
		Update the cost of each tile, based on the json data received from the battlesnake engine.
		
		### set up fresh gridCost to make it ready for updated data ###
		boardWidth = gameData["board"]["width"]
		boardHeight = gameData["board"]["height"]
		boardSize = [boardWidth, boardHeight]
		gridCost = createGridCost([boardWidth, boardHeight])
		'''
		### Update cost based on edges and corners ###

		for indexX, listX in enumerate(self.tiles):
    		# Enumerate so that you can easily access indexes in the lists. 	
			for indexY, listY in enumerate(listX):
				# set cost for top left corner and top and left edges.
				if indexX == 0 or indexY == 0:
					self.tiles[indexX][indexY].cost = self.costMatrix["edge"]										
				if indexX == 0 and indexY == 0:
					self.tiles[indexX][indexY].cost = self.costMatrix["corner"]
			
				# set cost for bottom right corner, and bottom and left edges
				if indexX == self.boardSize[0] - 1 or indexY == self.boardSize[1] - 1:
    					self.tiles[indexX][indexY].cost = self.costMatrix["edge"]													
				if indexX == self.boardSize[0] - 1 and indexY == self.boardSize[1] - 1:
    					self.tiles[indexX][indexY].cost = self.costMatrix["corner"]

				# set cost for top right, and bottom left corner.		
				if indexX == self.boardSize[0] - 1 and indexY == 0:
					self.tiles[indexX][indexY].cost = self.costMatrix["corner"]	
				if indexX == 0 and indexY == self.boardSize[1] - 1:
    					self.tiles[indexX][indexY].cost = self.costMatrix["corner"]

'''
### ### ### 
28.02.20 avsluttet her. ser ut til at tiles listene blir bygd ok, og at vi får oppdatert cost på kanter og hjørner. 
Usikkerhet på om listene vs coords er omvendt. 

## ## # # # ## #
'''

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
		'''



		
	

class Tile():
	# one object for every tile on the board. 

	def __init__(self):
		self.cost = 1
