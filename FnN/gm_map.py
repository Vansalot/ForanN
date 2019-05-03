#     Game map
# Movement will be issued by compass directions North, East, South and West.
# What do you want to do? print allowed actions, e.g : print stats, rest(get full hp(chance to get encounter?)), go direction."""
import random, math, sys, time, os
import gm_charstats, gm_badguys, gm_scenarios, gm_locations

STARTINGLOC_Visited = 'After a while of struggling through a shrubbery you finally get into a clearing in the forest, you look around and find out that this is the place that you woke up earlier. You immidiately find out that you have to move on.'
STORYLOC = ["You traverse through some bushes and come out into a clearing. In front of you stand a Nissemann, he tells you that 'it's hard to be a nissemann'.\nHe asks you if you can find his friends 'Frits' and 'Gunther'.\nHe doesn't know where to find them, so you just have to start somewhere.\n",
    'You hear some screaming close by, after you pass some rocks you see a Nisse who\'s lying on the ground. He is badly injured. You ask him if he\'s feeling under the weather.\nThe response you get is "that is a good vending, maybe we should use that in another episode", so you guess he\'s not as badly hurt as you first thought.\nAfter talking for a while you hear from him that his friend Gunther is missing, and that he might have been taken by one of the nasty Nåså\'s.\nYou tell him where you found his friend Hansi, and tell him to wait for you there.\n',
    'last story']
ENDING = '''
   :::     ::: ::::::::::: :::::::: ::::::::::: ::::::::  :::::::::  :::   :::  ::: 
  :+:     :+:     :+:    :+:    :+:    :+:    :+:    :+: :+:    :+: :+:   :+:  :+:  
 +:+     +:+     +:+    +:+           +:+    +:+    +:+ +:+    +:+  +:+ +:+   +:+   
+#+     +:+     +#+    +#+           +#+    +#+    +:+ +#++:++#:    +#++:    +#+    
+#+   +#+      +#+    +#+           +#+    +#+    +#+ +#+    +#+    +#+     +#+     
#+#+#+#       #+#    #+#    #+#    #+#    #+#    #+# #+#    #+#    #+#             
 ###     ########### ########     ###     ########  ###    ###    ###     ###       '''
ENDING_MSG = 'You have completed the initial story, feel free to roam around.'

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
    #STARTINGBOARD = ["#" * 5 for x in range(5)] # Set up the starting map


    def __init__(self):
        self.createLocations()
        self.theMap = Board(WorldMap.STARTINGBOARD)
        self.currentPosition = self.START[:]
        self.previousPosition = self.START[:]
        self.visitedPosition = []
        self.storyLocations = [] 
        self.storylocIndex = 0
        self.maxStorylocIndex = 2
        self.victory = False
        self.setStartLoc() # Sets the starting location on the map
        self.setStoryLoc() # Set the story locations

    def createLocations(self):
            # Set up objects for every location/tile on the map
            locations = [] # The complete list of 5 lists with 5 locations. [[5][5][5][5][5]]
            for i in range(5):
                templist = [] # Reset temp list for every iteration of the loop
                for i in range(5):
                    # Add flavor description for every location
                    description = gm_scenarios.forest["description"][random.randint(0, len(gm_scenarios.forest["description"]) -1)] 
                    templist.append(gm_locations.Locationforest(description)) # Call the constructur with desc that is defined in line above.
                locations.append(templist)
            WorldMap.STARTINGBOARD = locations

    def setStoryLoc(self):
        # Set the story locations on the map, they will be hidden from the player, setting up 3 to start with, so increase the players chances of ladning on a storyloc.
        # When the player visit these locations it will get some flavortext.
        from random import randint
        while len(self.storyLocations) < 3:
            storyLoc = [randint(0, 4), randint(0, 4)]
            startingLocation = self.START[:]
            while storyLoc in startingLocation or storyLoc in self.storyLocations:
                storyLoc = [randint(0, 4), randint(0, 4)]
            self.storyLocations.append(storyLoc)

    def checkIfOnStoryLoc(self):
        # change the board data structure with a sonar device character
        # Return False if this is an invalid move.
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

    def printStoryLoc(self, gameState):
        # Prints flavortext for the story locations
        if self.storylocIndex == self.maxStorylocIndex:
            # If you reached the max amount of story locations, do this.
            # Run boss encounter?
            if len(gameState.enemy) <= 0:
                print()
                #print(STORYLOC[self.storylocIndex])
                for character in STORYLOC[self.storylocIndex]:
                    sys.stdout.write(character)
                    sys.stdout.flush()
                    time.sleep(0.05)
                time.sleep(3)
                gm_badguys.createBoss(gameState)
                gameState.player.inCombat = True
                self.victory = True
            
        else:            
            print()
            for character in STORYLOC[self.storylocIndex]:
                    sys.stdout.write(character)
                    sys.stdout.flush()
                    time.sleep(0.05)
            self.storylocIndex += 1
            self.setStoryLoc()

    def setStartLoc(self):
        # Validates if the move entered is on the board and executes it.
        previousX, previousY = self.previousPosition
        currentX, currentY = self.currentPosition
        if (-1 < currentX < 5) and (-1 < currentY < 5):
            # If current move if on the board, the move will be performed.
            self.theMap[previousY][previousX].mapTile = WorldMap.heroPrevPos
            self.theMap[currentY][currentX].mapTile = WorldMap.heroCurrentPos
            #self.theMap[currentY][currentX] = WorldMap.heroCurrentPos

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
        elif ctrl.lower() == 'examine' or ctrl.lower().startswith('e'):
            gameState.player.examineLocation(gameState)
            self.whatToDo(gameState)

    def move_player(self, gameState):
        # Validates if the move entered is on the board and executes it.
        previousX, previousY = self.previousPosition
        currentX, currentY = self.currentPosition
        if (-1 < currentX < 5) and (-1 < currentY < 5):
            # If current move if on the board, the move will be performed.
            self.theMap[previousY][previousX].mapTile = WorldMap.heroPrevPos
            self.theMap[currentY][currentX].mapTile = WorldMap.heroCurrentPos
            self.visitedPosition.append(self.previousPosition) # might be removed must refactor
            self.theMap[currentY][currentX].visited = True
            if self.checkIfOnStoryLoc() == True:
                self.printStoryLoc(gameState)
            else:
                playerLocation = gameState.map.theMap[gameState.map.currentPosition[1]][gameState.map.currentPosition[0]] # Set player loc to make more readable code.
                printThis(playerLocation.description)
                time.sleep(1)
                gameState.player.inCombat = self.checkCombat(playerLocation.encounterChance) # Checks if the player gets into combat.
        else:
            #print("Can't go further in that direction, please select another direction.")
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

    def checkCombat(self, encounterChance):
        # Randomly encounter checker, (0,1) = 50% chance of encounter
        checkCombatRoll = random.randint(0, 10)
        # print('# Log: Roll: %s vs Chance: %s' % (checkCombatRoll, encounterChance)) # Logline for testing
        if checkCombatRoll < encounterChance:
            return True
        else:
            # print('# Log: no combat')
            return False
    
    def drawMap(self):
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

    def showmap(self, tryAgain=False):
        # Draw the game map when it is called from command prompt
        #print('' + ('\t\t  +----MAP----+'))
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