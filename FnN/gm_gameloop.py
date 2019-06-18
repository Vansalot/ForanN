import time, sys, random
import gm_combat, gm_map, gm_items, gm_scenarios, gm_locations, gm_charstats

#
# File that starts the game, sets up the game and contains the game loop.
# Contains the gamestate which contains the objects from the other classes.
#

class Gamestate():
    def __init__(self):
        # Groups up all game information(hopefully) in one class, so that it can be passed around in the functions.
        self.scenarioIndex = 0 # Index to iterate over scenarios
        self.scenario = gm_scenarios.SCENARIOS[self.scenarioIndex] # Inserts the dictionary of the scenario
        self.player = gm_charstats.Player()
        self.map = gm_map.WorldMap(self.scenario, self.scenarioIndex)
        self.payexMode = False
        self.gameIsDone = False
        self.enemy = []
        self.enemyIndex = len(self.enemy) - 1

    def iterateScenario(self):
        # updates gamestate when you change to the next scenario. 
        try:
            self.scenarioIndex += 1
            self.scenario = gm_scenarios.SCENARIOS[self.scenarioIndex] # Inserts the dictionary of the scenario
            self.map = gm_map.WorldMap(self.scenario, self.scenarioIndex) # set up the next map based on the dictionary in self.scenario
            self.map.victory = False # reset victory flag
        except IndexError:
            self.gameIsDone = True
            gm_map.printThis(gm_scenarios.ENDING_MSG)

def enterPlayerName(gameState):
    #starts the game, prompts for user to enter player name and calls playerStartingStats()
    playerName = ""
    # Set player name, with input validation.
    while len(playerName) == 0:
        playerName = (input('Please enter player name: ').lower())
        for letter in playerName:
            if letter in 'abcdefghijklmnopqrstuvwxyzæøå ':
                gameState.player.name = playerName
            else:
                print("Name must be written with letters, avoid numbers and special characters")
                playerName = ""
    
def setPlayerAttributes(gameState):
    # Set the starting attributes of the newPlayer
    getStartingStats(gameState.player)
    # update player stats based on the changes done prior.
    gameState.player.playerArmChange()
    gameState.player.playerHpChange()
    gameState.player.setupModifiers()
    # gameState is returned to the main() function.
    return gameState

def getStartingStats(gameState):
    # Setting the starting stats of the player. Default max attribute points(variable: totalPointsAllocated) are changed by difficulty settings.
    minPointsAllowedInOneStat = 1 # You can not have less than 1 point in each stat.
    maxPointsAllowedInOneStat = gameState.totalPointsAllocated - 2 # When setting starting stats, you can not have all your points in one stat, atleast 2 points are reserved to the last 2 stats.
    modifiedmaxPointsAllowedInOneStat = gameState.totalPointsAllocated - 2 
    totalPointsLeft = gameState.totalPointsAllocated 
    
    # Setting variables for the calculation of allotted player stat points
    # Variables for the stats, s =strength a =agility f =fortitude
    str = 0
    agi = 0 
    fort = 0
    print("\nNow you have to enter your characters stats, they are Strenght, Agility and Fortitude.\nYou got %s points to distribute between the stats." % (gameState.totalPointsAllocated))
    print("You can allocate 1-%s points to the first category.\n" % (maxPointsAllowedInOneStat))

    # Calls getStartingAttribute which returns the value that the user enters for the strength stat
    str = getStartingAttribute( "Enter player strength: ", minPointsAllowedInOneStat, maxPointsAllowedInOneStat)
    totalPointsLeft = totalPointsLeft - str
    # Calculates the points that are lefts for the next stats and displays it to the user, the -1 is there to ensure that there is 1 point left for the last stat.
    modifiedmaxPointsAllowedInOneStat = gameState.totalPointsAllocated - str - 1
    
    print("\nYou have",modifiedmaxPointsAllowedInOneStat,"point(s) left to use for the next stat.")
    # Checks that if there are less points available than max point allowed, then sets total points left -1(for last stat) as max points you can use for the next stat
    if totalPointsLeft < modifiedmaxPointsAllowedInOneStat:
        modifiedmaxPointsAllowedInOneStat = totalPointsLeft - 1
    print()
    # Calls getStartingAttribute which returns the value that the user enters for the agility stat
    agi = getStartingAttribute( "Enter player agility: ", minPointsAllowedInOneStat, modifiedmaxPointsAllowedInOneStat )
    # calculates the total points that are left for use after setting agility stat
    totalPointsLeft = totalPointsLeft - agi
    # assign the points that are left to fortitude.
    fort = totalPointsLeft
    # Call player stat change with the values that have been input by the user, to update player.        
    gameState.playerStatChange(str, agi, fort)
    time.sleep(1)
    print()

def getStartingAttribute(prompt, min_value, max_value):
    # When starting the game, player are prompted to enter value for the different stats.
    # this checks if the value is valid according to input from getStartingStats()
    while 1:
        value = input(prompt)
        if value.isnumeric():
            value = int(value)
            if value >= min_value and value <= max_value:
               return value
            else:
                print("You entered a value that is too high, or too low.")
        else:
            print("You did not enter a number, please enter a number.")

def enterDifficulty(gameState):
    # Set game difficulty, with input validation.
    difficulty = ''
    while True:
        print('Please enter difficulty (easy, medium, hard): ', end='')
        difficulty = input().lower()
        if difficulty == 'easy' or difficulty == 'e':
            gameState.player.totalPointsAllocated = 10
            break
        elif difficulty == 'medium' or difficulty == 'm':
            break # totalPointsAllocated default = 6 so no change is needed.
        elif difficulty == 'hard' or difficulty == 'h':
            gameState.player.totalPointsAllocated = 4
            break
        elif difficulty == 'god': # god mode, for show and tell
            gameState.player.totalPointsAllocated = 30
            break

def setPayexMode(gameState):
    # Set payex mode, it's just for naming enemies differently. For funs.
    mode = input('Do you want PayEx mode? (\'yes\' for yes, any other input for NO. PayEx mode is a internal thing): ').lower()
    if mode == 'yes':
        gameState.payexMode = True

def nextScenario(gameState):
    # When a scenario is finished, ititiate the next scenario.
    gameState.iterateScenario() # Set up the next scenario in gamestate object.
    gameState.player.attributes.pl_current_hp = gameState.player.attributes.pl_maxhp # Reset player hp to max.
    # Print scenario stuff
    gm_map.printThis(gameState.scenario["intro"])
    input("\nHit 'Enter' to continue...")
    gameLoop(gameState) # go back to the game loop after the setup is complete.

def titleScreen():
    # prints the title of the game.
    print(gm_map.TITLE1) 
    print()
    print(gm_map.TITLE2)
    time.sleep(2)

def main():
    # Starts the game, calls the game loop
    titleScreen() # print the title of the game.    
    
    # Setting the game up
    gameState = Gamestate()
    setPayexMode(gameState) # Can be commented out to remove payex functionality.
    enterDifficulty(gameState) # Set up difficulty
    enterPlayerName(gameState) # Set up new player, This will also print prompts and player information to the player.
    setPlayerAttributes(gameState)
    
    # Game is starting Print map info and introduction text.    
    gameState.map.drawMap(gameState) # Draw the map on the screen.
    gm_map.printThis(gameState.scenario["intro"])
    time.sleep(1)
    gameState.map.whatToDo(gameState) # Start the first "what would you like to do dialogue" before entering the game loop.
    
    # Move on to the game loop
    gameLoop(gameState)

def gameLoop(gameState):
    # Main game loop
    while True:
        if gameState.gameIsDone == True:
            # If all scenarios are complete, print message stating that you are done, but can continue playing for fun.
            print(gm_scenarios.ENDING_MSG)
            gameState.gameIsDone = False

        if gameState.map.victory == True and gameState.player.inCombat == False:
            # Check if the victory conditions are met, start prep for next scenario and print game ending messages.
            if gameState.map.specialItemFound == False:
                gm_items.specialItemFound(gameState) # if special item is not found yet, player recieve it at the end of the scenario
            gm_map.printThis(gameState.scenario["ending"])
            time.sleep(4)
            print(gm_scenarios.VICTORY) # print victory ascii art
            time.sleep(4)
            nextScenario(gameState) # start a new scenario.

        if gameState.player.inCombat == True:
            # Before starting map movement check if player is in combat, if so, call the combat loop.
            gm_combat.combatLoop(gameState)
        
        # Movement loop
        gameState.map.drawMap(gameState) # draw the map
        gameState.map.whatToDo(gameState) # ask the player what to do
        
        if gameState.player.inCombat == True:
            # check If the player is in combat after movement.
            gm_combat.combatLoop(gameState) 
            
        if gameState.player.dead == True: # if the player is dead, print game over, and ask if you want to play again.
            gm_scenarios.gameOver()
    
    print("# Game loop has ended.") # Print that the application is out of the loop, meant for debug purposes.

if (__name__ == "__main__"):
    main()
