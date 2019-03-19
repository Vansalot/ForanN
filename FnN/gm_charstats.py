import time, sys, os
import gm_combat, gm_map, gm_badguys
# Main file for the game, will also contain the game loop.
# Note that print() and time.sleep(x) statements have been added in most files to try and smooth the flow of information on the screen.
#os.system('cls') Clear the screen, not sure if needed, keeping it here just in case.

# *** Classes ***
class Player():
    # Player, which holds the player name, attributes are created from PlayerAttributes class.
    # Player is stored in the gamestate object.
    def __init__(self):
        # Initialise player
        self.attributes = PlayerAttributes() # see playerattributes for more info
        self.name = ""
        self.inCombat = False # Used to determine if the player is in combat, this changes where the game loop goes.
        self.isENEMY = False # Used to determine if it's the player of enemy who does actions in combat, also a parameter for enemy class.
        self.dead = False # Used to determine if the player is dead and the game is over.
        self.statusEffects = [] # For now, only used for parry function, new effects can be added and put in here.
        self.possibleCombatActions = ['hit', 'parry'] # Possible actions for player when in combat, new actions can be added if they are implemented.
        self.possibleMapActions = ['(W)est', '(E)ast', '(N)orth', '(S)outh', '(R)est'] # Possible actions for player not in combat, new actions can be added if they are implemented.
        self.totalPointsAllocated = 6 # Default points player can allocate to skills at the beginning of the game.


    def printNameLevelXp(self):
        # Prints player information in a box structure. Used almost every time the player is asked to perform an action.
        index = self.attributes.pl_lvl - 1
        spacing = 45 # Value for centerspacing of the topInfo print message.
        topInfo = '%s | Level: %s | %s / %s xp' % (self.name.title(), self.attributes.pl_lvl, self.attributes.pl_xp,self.attributes.levelup[index])
        bottInfo = ' Str: %s  Agi: %s  Fort: %s | Armor: %s HP: %s / %s' % (self.attributes.pl_str,self.attributes.pl_agi, self.attributes.pl_fort, self.attributes.pl_currentArmor, self.attributes.pl_current_hp, self.attributes.pl_maxhp)
        topInfoPrint = topInfo.center(spacing) # Centers topInfo text
        printedLine = "+" + (len(bottInfo)) * '-' + "+" # Creates a +----+ structure based on how long the bottInfo message are.
        
        print(printedLine)
        print('           ### Player information: ###           ')
        print(printedLine)
        print(' ', topInfoPrint)
        print(printedLine)
        print(bottInfo)
        print(printedLine)

    def printPlayerPossibleactions(self):
        # Prints the possible actions the player can perform, depending on if the player is in combat or not.
        if self.inCombat == True:
            print('You are in combat, your possible actions are: ', end='')
            print(*self.possibleCombatActions, sep=', ', end='') 
            print('.', end='')
        else:
            print('Your possible actions are: ', end='')
            print(*self.possibleMapActions, sep=', ', end='')

    def rest(self):
        # Rest function, player can rest if it is not in combat, restores HP to full.
        time.sleep(1)
        print('You find a nice spot to rest. After a while you feel fresh and rested.')
        time.sleep(2)
        self.attributes.pl_current_hp = self.attributes.pl_maxhp

    #  vvv Xp gain, check if player has leveled up, and levelup mechanics vvv
    
    def plXpGain(self, enemy_xp_reward):
        # Updates experience gain of the player, and calls plCheckLvlup to check if the character has leveled up.
        self.attributes.pl_xp += enemy_xp_reward
        self.plCheckLvlup()
    
    def plCheckLvlup(self):
        # Checks if the player has leveled up, if so, calls the plLevelUp procedure, otherwise moves on. (added log line for now).
        # Levelup happpens at the xp limits set up in playerAttributes.
        index = self.attributes.pl_lvl -1
        if self.attributes.pl_xp >= self.attributes.levelup[index]:
            self.plLevelUp()
        else:
            print('# Log: No level up today.') # Added for debug purposes, so show that this function is called.

    def plLevelUp(self):
        # Asks which stat you want to increase when you level up and calls pl_stat_change to update the stat.
        print('* You have reached level %s! Current stats: Strength: %s  Agility: %s  Fortitude: %s *'  % (self.attributes.pl_lvl + 1, self.attributes.pl_str,self.attributes.pl_agi, self.attributes.pl_fort))
        chosenStat = ''
        possibleStats = ['s', 'a', 'f', 'str', 'agi', 'fort']
        while chosenStat not in possibleStats:
            chosenStat = (input('* LEVEL UP! Select stat to increase(str, agi, fort): ').lower())
            
            if chosenStat.lower() == 'str' or chosenStat.lower() == 's':
                self.attributes.pl_lvl += 1
                self.playerStatChange(1, 0, 0)
                    
            elif chosenStat.lower() == 'agi' or chosenStat.lower() == 'a':
                self.attributes.pl_lvl += 1
                self.playerStatChange(0, 1, 0)
                
            elif chosenStat.lower() == 'fort' or chosenStat.lower() == 'f':
                self.attributes.pl_lvl += 1
                self.playerStatChange(0, 0, 1)        
            else:
                print("Please enter a valid stat to increase(str, agi, fort).")
                print()    
    
    def playerStatChange(self, strength, agility, fortitude):
        # (int, int, int) -> (int, int, int)
        # Procedure to change character stats. 
        self.attributes.pl_str += strength 
        self.attributes.pl_agi += agility
        self.attributes.pl_fort += fortitude
        self.attributes.pl_maxhp += self.attributes.pl_fort
        self.attributes.pl_current_hp = self.attributes.pl_maxhp
        self.attributes.pl_currentArmor = self.attributes.pl_base_armor + self.attributes.pl_agi
        self.attributes.pl_hitmod = round(self.attributes.pl_lvl / 2)


class Gamestate():
    def __init__(self):
        # Groups up all game information(hopefully) in one class, so that it can be passed around in the functions.
        self.player = Player()
        self.map = gm_map.WorldMap(self.player)
        self.enemy = []
        self.enemyIndex = len(self.enemy) - 1


class PlayerAttributes():
    # Initializes the player attributes, they are part of the Player class.
    def __init__(self):
        self.pl_lvl = 1 # Player level
        self.pl_hitmod = 0 # Player hit modifier, normally lvl / 2, which is added to attack rolls.
        self.pl_xp = 0 # player experience
        self.pl_str = 0 # player strenght
        self.pl_agi = 0 # player agility
        self.pl_fort = 0 # player foritude
        self.pl_base_hp = 10 # player base hp
        self.pl_maxhp = self.pl_base_hp + self.pl_fort # player max hp, base hp + fortitude.
        self.pl_current_hp = self.pl_maxhp # Current hp, to track how much hp you have during combat.
        self.pl_base_armor = 10 # player base armor
        self.pl_currentArmor = self.pl_base_armor + self.pl_agi # player armor modified by agility.
        self.levelup = [1000,2000,3500,5000,7000,8500,10000] # xp thresholds for levelup.


''' vvv End of classes, game procedures follows vvv '''
def getStarted(newPlayer):
    #starts the game, prompts for user to enter player name and calls playerStartingStats()
    playerName = ""
    # Set player name, with input validation.
    while len(playerName) == 0:
        playerName = (input('Please enter player name: ').lower())
        for letter in playerName:
            if letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz ':
                newPlayer.player.name = playerName
            else:
                print("Name must be written with letters, avoid numbers and special characters")
                playerName = ""
    
    # Set the starting attributes of the newPlayer
    getStartingStats(newPlayer.player)
    # player is returned to the main() function.
    return newPlayer

def getStartingStats(gameState):
    # Setting the starting stats of the player. Default max attribute points(variable: totalPointsAllocated) are changed by difficulty settings.
    minPointsAllowedInOneStat = 1 # You can not have less than 1 point in 1 stat.
    maxPointsAllowedInOneStat = gameState.totalPointsAllocated - 2 # When setting starting stats, you can not have all your points in one stat, atleast 2 points are reserved to the last 2 stats.
    modifiedmaxPointsAllowedInOneStat = gameState.totalPointsAllocated - 2 
    totalPointsLeft = gameState.totalPointsAllocated 
    # Setting variables for the calculation of allotted player stat points
    # Variables for the stats, s =strength a =agility f =fortitude
    str = 0
    agi = 0 
    fort = 0
    print()
    print("Now you have to enter your characters stats, they are Strenght, Agility and Fortitude. You got %s points to distribute between the stats." % (gameState.totalPointsAllocated))
    print("You can allocate 1-%s points to the first category." % (maxPointsAllowedInOneStat))
    print()
    # Calls getStartingAttribute which returns the value that the user enters for the strength stat
    str = getStartingAttribute( "Enter player strength: ", minPointsAllowedInOneStat, maxPointsAllowedInOneStat)
    totalPointsLeft = totalPointsLeft - str
    # Calculates the points that are lefts for the next stats and displays it to the user, the -1 is there to ensure that there is 1 point left for the last stat.
    modifiedmaxPointsAllowedInOneStat = gameState.totalPointsAllocated - str - 1
    print()
    print("You have",modifiedmaxPointsAllowedInOneStat,"point(s) left to use for the next stat.")
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
    time.sleep(2)
    print()
    print()
    # Print the player information after character creation is finished.
    gameState.printNameLevelXp()

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
           
def testHero(pl):
    # Generating a test hero. Needs change to have the desired result. 
    pl.name = "TestBoi Von Testison"
    pl.playerStatChange(4, 4, 4)
    pl.printNameLevelXp()

def titleScreen():
    gm_map.TITLE() # prints the title.
    # Create a new gamestate with player.
    newPlayer = Gamestate()
    difficulties = ['easy', 'medium', 'hard']
    print('Please input difficulty')
    difficulty = input('easy, medium, hard: ').lower()
    # Set game difficulty, with input validation.
    while difficulty.lower() not in difficulties:
        difficulty = input('Please input difficulty easy, medium, hard: ').lower()
    if difficulty == 'easy':
        newPlayer.player.totalPointsAllocated = 10
    elif difficulty == 'medium':
        pass # totalPointsAllocated default = 6 so no change is needed.
    elif difficulty == 'hard':
        newPlayer.player.totalPointsAllocated = 4
    getStarted(newPlayer) # Set up new player, This will also print prompts and player information to the player.
    return newPlayer

def main():
    # Main game loop
    gameState = titleScreen()
    gameState.map.drawMap() # Draw the map on the screen.
    gm_map.printIntro() # Print Intro message for the player.
    time.sleep(1)
    gameState.map.navigateTheMap(gameState)
    while True:
        # Start of the loop when traversing the map
        # player stats is printed on the screen with the map.
        # and you are prompted to move in a direction
        if gameState.map.victory == True and gameState.player.inCombat == False:
            # If the game is finished, print game ending messages.
            print(gm_map.ENDING)
            print()
            print(gm_map.ENDING_MSG)
        if gameState.player.inCombat == True:
            # If the player is in combat prior to movement, call the combat loop.
            gm_combat.combatLoop(gameState)
        
        time.sleep(1)
        gameState.player.printNameLevelXp() # print player information 
        gameState.map.drawMap() # draw the map
        gameState.map.navigateTheMap(gameState) # If the player is not in combat, it will be looped around the map
        time.sleep(1)
        
        if gameState.player.inCombat == True:
            # check If the player is in combat after movement.
            gm_combat.combatLoop(gameState) 
            
        if gameState.player.dead == True: #if the player is dead, print game over, and ask if you want to play again.
            print('''
                       ::::::::      :::       :::   :::   ::::::::::          ::::::::  :::     ::: :::::::::: :::::::::   ::: 
                     :+:    :+:   :+: :+:    :+:+: :+:+:  :+:                :+:    :+: :+:     :+: :+:        :+:    :+:  :+:  
                    +:+         +:+   +:+  +:+ +:+:+ +:+ +:+                +:+    +:+ +:+     +:+ +:+        +:+    +:+  +:+   
                   :#:        +#++:++#++: +#+  +:+  +#+ +#++:++#           +#+    +:+ +#+     +:+ +#++:++#   +#++:++#:   +#+    
                  +#+   +#+# +#+     +#+ +#+       +#+ +#+                +#+    +#+  +#+   +#+  +#+        +#+    +#+  +#+     
                 #+#    #+# #+#     #+# #+#       #+# #+#                #+#    #+#   #+#+#+#   #+#        #+#    #+#          
                 ########  ###     ### ###       ### ##########          ########      ###     ########## ###    ###  ###       ''')
            time.sleep(2)
            print()
            print('Do you want to play again? (yes or no)')
            if not input().lower().startswith('y'):
                sys.exit()
            else:
                main()
    
    print("# Game loop has ended.") # Print that the application is out of the loop, meant for debug purposes.

if (__name__ == "__main__"):
    main()
