
#    # # # # # # # # # # # # # # # # # # # # # # # # # #
#    # # # # # # # # # # # # # # # # # # # # # # # # # #
#    #                   locations                     #
#    # # # # # # # # # # # # # # # # # # # # # # # # # #
#    # # # # # # # # # # # # # # # # # # # # # # # # # #
#
# Locations class, holds an object for every location on the map
# 

import gm_scenarios
import random

class Locationforest():
    # Create an object of every location(coordinate) on the map
    def __init__(self, description, examineText):
        self.description = description #gameState.scenario["description"][random.randint(0, len(gameState.scenario["description"]) -1)] # Flavortext that is printed when entering a new location.
        self.encounterChance = random.randint(0, 9) # chance for encounter when entering the new area.
        self.visited = False # set if the location has been visited before.
        self.examineable = random.choice([True, False]) 
        self.examineChance = random.randint(1, 8) # Chance for successful examination.
        self.examineText = examineText # Flavortext when you examine. 
        self.visitedText = ''
        self.beenExamined = False # If the location has been examined before, it can not be examined again. 
        self.description = description
        self.mapTile = '#' # Set maptile function? For future use, if tiles are e.g impassable.
        self.startLocation = False
        self.validDirections = []



def setExamined(location):
    # Set self.examined to True when a player has examined location.
    location.beenExamined = True


def setTileImpassable(location):
    # RFU 
    # Set tiles impassable marked as e.g X on the map. 
    pass