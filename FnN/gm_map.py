#     Game map and movement functions
# Movement will be issued by compass directions North, East, South and West.

import random, math, sys, time, os
import gm_charstats, gm_badguys, gm_scenarios, gm_locations, gm_items

class Board(list):

    def __str__(self):
        return "\n".join(" ".join(row) for row in self)

class WorldMap():
    from random import randint
    heroCurrentPos = "@"
    heroPrevPos = "¤"
    DIRECTIONS = ["west", '%', "east", "north", '%', "south"]
    START = [randint(0, 4), randint(0, 4)] # Starting location for the player
    STARTINGBOARD = []

    def __init__(self, scenario, scenarioIndex):
        self.createLocationDecider(scenario, scenarioIndex)
        self.theMap = Board(WorldMap.STARTINGBOARD)
        self.currentPosition = self.START[:]
        self.previousPosition = self.START[:]
        self.visitedPosition = []
        self.storyLocations = [] 
        self.storylocIndex = 0
        self.maxStorylocIndex = scenario["maxStorylocIndex"]
        self.victory = False
        self.specialItemFound = False
        self.setStartLoc(scenario, scenarioIndex) # Sets the starting location on the map
        self.setStoryLoc(scenario, scenarioIndex) # Set the story locations
        self.movesSinceCombat = 0

    def createLocationDecider(self,scenario, scenarioIndex):
        # Select which map constructior to use. If the first scenario, use random map gen. If not, use the map specific one.
        if scenarioIndex == 0:
            self.createLocations(scenario)
        else:
            self.createLocations4Scenario(scenario)

    def createLocations(self, scenario):
            # Set up objects for every location/tile on the map
            locations = [] # The complete list of 5 lists with 5 locations. [[5][5][5][5][5]]
            for i in range(5):
                templist = [] # Reset temp list for every iteration of the loop
                for i in range(5):
                    # Add flavor description for every location
                    description = scenario["description"][random.randint(0, len(scenario["description"]) -1)] 
                    examineText = scenario["examination"][random.randint(0, len(scenario["examination"]) -1)] 
                    templist.append(gm_locations.Locationforest(description, examineText)) # Call the constructur with desc that is defined in line above.
                locations.append(templist)
            WorldMap.STARTINGBOARD = locations

    def createLocations4Scenario(self, scenario):
        # Set up locations from the 2nd scenario and on. Sets a map that's not ranomized. Do not use for first scenario!!!
        # Set up objects for every location/tile on the map
            locations = [] # The complete list of 5 lists with 5 locations. [[5][5][5][5][5]]
            for description_list in scenario["description"]:
                templist = [] # Reset temp list for every iteration of the loop
                for string in description_list:
                    examineText = scenario["examination"][random.randint(0, len(scenario["examination"]) -1)]
                    templist.append(gm_locations.Locationforest(string, examineText))
                locations.append(templist)
            WorldMap.STARTINGBOARD = locations

    def setStoryLoc(self, scenario, scenarioIndex):
        # Set the story locations on the map, they will be hidden from the player, setting up 3 to start with, so increase the players chances of ladning on a storyloc.
        # When the player visit these locations it will get some flavortext.
        from random import randint
        if scenarioIndex == 0:
            while len(self.storyLocations) < 5:
                storyLoc = [randint(0, 4), randint(0, 4)]
                startingLocation = self.START[:]
                while storyLoc in startingLocation or storyLoc in self.storyLocations:
                    storyLoc = [randint(0, 4), randint(0, 4)]
                self.storyLocations.append(storyLoc)
        else:
            self.storyLocations = scenario["storylocations"]

    def checkIfOnStoryLoc(self, gameState):
        # change the board data structure with a sonar device character
        # Return False if this is an invalid move.
        index = gameState.scenarioIndex
        if index == 0: # If in first scenario
            smallestDistance = 100
            from math import sqrt
            x = self.currentPosition[0]
            y = self.currentPosition[1]
            for cx, cy in self.storyLocations:
                distance = math.sqrt((cx - x) * (cx - x) + (cy - y) * (cy - y))
                if distance < smallestDistance: # We want the closest story location
                    smallestDistance = distance
            if smallestDistance == 0:
                # Player is on a story location!
                self.storyLocations.remove([x,y])
                return True
            else:
                return False          

        else: # if other than first scenario
            if self.currentPosition == gameState.scenario["storylocations"][self.storylocIndex]:
                return True
            else:
                return False

    def printStoryLoc(self, gameState):
        # Prints flavortext for the story locations
        if self.storylocIndex == self.maxStorylocIndex:
            # If you reached the max amount of story locations, do this.
            if len(gameState.enemy) <= 0:
                print()
                printThis(gameState.scenario["storylocation"][self.storylocIndex], speed=0.05)
                gm_badguys.createBoss(gameState)
                gameState.player.inCombat = True
                self.victory = True
        else:            
            print()
            printThis(gameState.scenario["storylocation"][self.storylocIndex], speed=0.05)
            self.storylocIndex += 1
            if gameState.scenarioIndex == 0:
                self.setStoryLoc(gameState.scenario, gameState.scenarioIndex)
            time.sleep(3)

    def setStartLocFirstScenario(self, scenario, scenarioIndex):
        # Validates if the move entered is on the board and executes it.
        previousX, previousY = self.previousPosition
        currentX, currentY = self.currentPosition
        if (-1 < currentX < 5) and (-1 < currentY < 5):
            # If current move if on the board, the move will be performed.
            self.theMap[previousY][previousX].mapTile = WorldMap.heroPrevPos
            self.theMap[currentY][currentX].mapTile = WorldMap.heroCurrentPos
            self.theMap[currentY][currentX].visitedText = scenario["startlocationagain"] # Set flavor text on the starting location of the game.
            self.theMap[currentY][currentX].startLocation = True # Set startlocation to True so that we know where it is.

    def setStartLoc(self, scenario, scenarioIndex):
        # Set player position on the map according to the scenariotext
        if scenarioIndex == 0: # if the first scenario, proceed as before. 
            self.setStartLocFirstScenario(scenario, scenarioIndex)
        else: # If second or later scenario set up according to scenario.
            self.currentPosition = self.previousPosition = scenario["startinglocation"]
            currentX, currentY = self.currentPosition
            self.theMap[currentY][currentX].mapTile = WorldMap.heroCurrentPos
            self.theMap[currentY][currentX].visitedText = scenario["startlocationagain"] # Set flavor text on the starting location of the game.
            self.theMap[currentY][currentX].startLocation = True # Set startlocation to True so that we know where it is.

    def whatToDo(self, gameState):
        # Ask the player what to do when on the map, choices move, examine, rest. "move" takes you to the "submenu" where player is promted for a direction.
        # examine and rest calls their respective procedures.
        ctrl = ''
        while ctrl.isalpha() != True:
            gameState.player.printPlayerPossibleactions()
            ctrl = input('. What do you do? ').lower().strip()
        if ctrl.lower() == 'rest' or ctrl.lower().startswith('r'):
            gm_charstats.Player.rest(gameState.player)
            print('You get up and look around.')
            #gameState.player.printPlayerPossibleactions()
            self.whatToDo(gameState)
        elif ctrl.lower() == 'map' or ctrl.lower().startswith('m'):
            self.navigateTheMap(gameState)
        elif ctrl.lower() == 'help':
            gameState.player.printHelpText()
        elif ctrl.lower() == 'experience':
            # Added for debug purposes, remove or you got a decent cheat ;)
            print('# Log: You gain 500 experience. You CHEATER!')
            gameState.player.plXpGain(500)
            self.whatToDo(gameState)
        elif ctrl.lower() == 'item':
            print('# Log: Item cheat. CHEATER!')
            gm_items.specialItemFound(gameState)
            self.whatToDo(gameState)
        elif ctrl.lower() == 'examine' or ctrl.lower().startswith('e'):
            gameState.player.examineLocation(gameState)
            self.whatToDo(gameState)
        
    def move_player(self, gameState):
        # Validates if the move entered is on the board and executes it.
        previousX, previousY = self.previousPosition
        currentX, currentY = self.currentPosition
        if (-1 < currentX < 5) and (-1 < currentY < 5):
            # If current move if on the board, the move will be performed.
            playerLocation = gameState.map.theMap[gameState.map.currentPosition[1]][gameState.map.currentPosition[0]] # Set player loc to make more readable code.
            self.theMap[previousY][previousX].mapTile = WorldMap.heroPrevPos
            self.theMap[currentY][currentX].mapTile = WorldMap.heroCurrentPos
            self.visitedPosition.append(self.previousPosition) # might be removed must refactor
            self.theMap[currentY][currentX].visited = True
            if self.checkIfOnStoryLoc(gameState) == True:
                self.printStoryLoc(gameState)
            elif playerLocation.startLocation == True and playerLocation.visited == True:
                printThis(playerLocation.visitedText)
            else:
                # playerLocation = gameState.map.theMap[gameState.map.currentPosition[1]][gameState.map.currentPosition[0]] # Set player loc to make more readable code.
                printThis(playerLocation.description)
                time.sleep(1)
                gameState.player.inCombat = self.checkCombat(playerLocation.encounterChance) # Checks if the player gets into combat.
        else:
            self.currentPosition = self.previousPosition[:]
            self.navigateTheMap(gameState, tryAgain=True)

    def navigateTheMap(self, gameState, tryAgain=False):
        # Asks the player for a move action. should be implemented so that you got a list of possible actions e.g: rest, look for trouble o.l, and go in directions.
        # If direction is entered, then there should be a function that calls this function for movement. Might be changed so ensure proper state transitioning
        # e.g map -> show map actions -> direction selected -> call this function to initiate move.
        ctrl = ''
        if tryAgain == True:
            self.showmap(tryAgain=True)
        else:
            self.showmap()
        while ctrl.isalpha() != True:
            gameState.player.printMoveActions()
            ctrl = input('. Which direction yould you like to go? ').lower().strip()       
        for direction in WorldMap.DIRECTIONS:
            if direction.lower().startswith(ctrl):
                d = WorldMap.DIRECTIONS.index(direction)
                self.previousPosition = self.currentPosition[:]
                self.currentPosition[d > 2] += d - (1 if d < 3 else 4)
                self.move_player(gameState)
                break
        else:
            print('You entered an invalid direction')

    def checkCombat(self, encounterChance):
        # Randomly encounter checker, (0,1) = 50% chance of encounter
        checkCombatRoll = random.randint(1, 10)
        if checkCombatRoll > encounterChance:
            return True
        else:
            if encounterChance <= 4: # added mechanic, just in case you get a situation where you never end up in combat
                self.movesSinceCombat += 1 
                if (checkCombatRoll - self.movesSinceCombat) < encounterChance:
                    self.movesSinceCombat = 0
                    return True
            return False
    
    def drawMapOLD(self):
        # Old map drawing function. Keeping it here just in case. 
        # Draw the game map data structure.
        print('' + ('\t\t  +----MAP----+'))
        # Print each line of the rows.
        for column in range(len(self.theMap)):
            extraSpace = ''
            # Create the string for this row on the board.
            boardRow = ''
            for row in range(len(self.theMap)):
                boardRow += self.theMap[column][row].mapTile
                boardRow += ' '
            print('\t\t  %s%s %s%s' % (extraSpace, '|',boardRow, '|'))
        print('' + ('\t\t  +- You = @ -+'))

    def drawMap(self, gameState):
            # Merged printing of map together with printing of the player information.
            # setting up the player info prints:
            spacing = 48
            # Printed player information
            lvlIndex = gameState.player.attributes.pl_lvl - 1
            plInfoDashedLine = '+------------ <<< Player information >>> -----------'
            nameLvlXp = '  %s | Level: %s | %s / %s xp  ' % (gameState.player.name.title(), gameState.player.attributes.pl_lvl, gameState.player.attributes.pl_xp, gameState.player.attributes.levelup[lvlIndex])
            nameLvlXpPrint = nameLvlXp.center(spacing)
            dashedLine = '+---------------------------------------------------'
            #plAttributes= ' Str: %s  Agi: %s  Fort: %s | Armor: %s HP: %s / %s    ' % (gameState.player.attributes.pl_str, gameState.player.attributes.pl_agi, gameState.player.attributes.pl_fort, gameState.player.attributes.pl_currentArmor, gameState.player.attributes.pl_current_hp, gameState.player.attributes.pl_maxhp)
            plAttributes= ' Str: %s  Agi: %s  Fort: %s | AC: %s HP: %s / %s ' % (gameState.player.attributes.pl_str, gameState.player.attributes.pl_agi, gameState.player.attributes.pl_fort, gameState.player.attributes.pl_currentArmor, gameState.player.attributes.pl_current_hp, gameState.player.attributes.pl_maxhp)
            plAttributesPrint = plAttributes.center(spacing)
            
            # Set up boolean checks so that the right lines are printed at the right place. 
            nameLvlXpPrintP1 = False
            plAttributesP2 = False
            filler1 = False
            filler2 = False
            nlxpLine1P2 = False

            # Check if inventory needs to be printed
            inventoryinfoPrint = gameState.player.getInventoryForPrint()
            equippedPrint = gameState.player.getequippedForPrint()
            if inventoryinfoPrint == None:
                inventoryinfoPrint = ' Inventory: '
            if equippedPrint == None: 
                equippedPrint = ' Equipped: '

            # Draw the game map data structure together with the player information data structure.
            if gameState.player.inCombat == False:
                print()
            print('' + plInfoDashedLine + ('+- < MAP > -+'))
            # Print each line of the rows.
            for column in range(len(self.theMap)):
                extraSpace = ''
                # Create the string for this row on the board.
                boardRow = ''
                for row in range(len(self.theMap)):
                    boardRow += self.theMap[column][row].mapTile
                    boardRow += ' '
                if nameLvlXpPrintP1 == False:
                    print('  ' + nameLvlXpPrint.center(spacing) + '  %s%s %s%s' % (extraSpace, '|',boardRow, '|'))
                    nameLvlXpPrintP1 = True
                    continue
                if plAttributesP2 == False:
                    print('  ' + plAttributesPrint.center(spacing) + '  %s%s %s%s' % (extraSpace, '|',boardRow, '|'))
                    plAttributesP2 = True
                    continue
                if nlxpLine1P2 == False:
                    print(dashedLine + '%s%s %s%s' % (extraSpace, '|',boardRow, '|'))
                    nlxpLine1P2 = True
                    continue
                if filler1 == False:
                    print(inventoryinfoPrint.center(spacing) + '    %s%s %s%s' % (extraSpace, '|',boardRow, '|'))
                    filler1 = True
                    continue
                if filler2 == False:
                    print(equippedPrint.center(spacing) + '    %s%s %s%s' % (extraSpace, '|',boardRow, '|'))
                    filler2 = True
                    continue
                print('  %s%s %s%s' % (extraSpace, '|',boardRow, '|'))
                
            print('' + dashedLine + ('+- You = @ -+'))

    def showmap(self, tryAgain=False):
        # Draw the game map when it is called from command prompt
        os.system('cls')
        print('''                  _____________
                =(_ ___  __ __ )=
                  |           |''')
        # Print each line of the rows.
        for column in range(len(self.theMap)):
            extraSpace = ''
            # Create the string for this row on the board.
            boardRow = ''
            for row in range(len(self.theMap)):
                boardRow += self.theMap[column][row].mapTile
                boardRow += ' '
            print('\t\t  %s%s %s%s' % (extraSpace, '|',boardRow, '|'))
        print('''                  |__  ___   _|
                =(_____________)=''')
        print('Map: You are @, Unvisited location are #, visited location are ¤')
        if tryAgain == True:
            print(" * Can't go further in that direction, please select another direction. *")

def printThis(message, speed=0.02):
    # Possible usable function to call when you want to print fluid messages. time will show /12.03.19

    for character in message:
                    sys.stdout.write(character)
                    sys.stdout.flush()
                    time.sleep(speed)



TITLE2 = '''
   	    ###########################################################

	  ::::::::::    :::      ::::    :::
	 :+:         :+: :+:    :+:+:   :+:    : "¨'/\¨`@@@' \@\#_
	+:+        +:+   +:+   :+:+:+  +:+   * /\^`/##\@@@@@'\##/_@
       :#::+::#  +#++:++#++:  +#+ +:+ +#+    ^/##\/####\||@/\'##\ *
      +#+       +#+     +#+  +#+  +#+#+#     /####\#####\|/##\||`¨ 
     #+#       #+#     #+#  #+#   #+#+#     ~~~!!~~~!!~~!!~!!~!!~
    ###       ###     ###  ###    ####'''       

TITLE3 ='''  ############################################################
 ###                Forest's and Nåså's                   ###
############################################################\n'''