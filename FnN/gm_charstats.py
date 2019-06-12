import time, sys, random
import gm_combat, gm_map, gm_items, gm_scenarios, gm_locations
# Main file for the game, will also contain the game loop.
# Note that print() and time.sleep(x) statements have been added in most files to try and smooth the flow of information on the screen.

# *** Classes ***
class Player():
    # Player, which holds the player name, attributes are created from PlayerAttributes class.
    # Player is stored in the gamestate object.
    def __init__(self):
        # Initialise player
        # Contains player specific data that does not involve combat related stats.
        self.attributes = PlayerAttributes() # see playerattributes for more info
        self.name = ''
        self.inCombat = False # Used to determine if the player is in combat, this changes where the game loop goes.
        self.isENEMY = False # Used to determine if it's the player of enemy who does actions in combat, also a parameter for enemy class.
        self.dead = False # Used to determine if the player is dead and the game is over.
        self.statusEffects = [] # For now, only used for parry function, new effects can be added and put in here.
        self.abilityActive = [] # For storing abilities used in combat. (taking over for self.statusEffects)
        self.possibleCombatActions = ['hit', 'parry'] # Possible actions for player when in combat, new actions can be added if they are implemented.
        self.possibleMapActions = ['Map/move', 'Examine', 'Rest','Help'] # Possible actions for player not in combat, new actions can be added if they are implemented.
        self.moveActions = ['(W)est', '(E)ast', '(N)orth', '(S)outh'] # Possible move actions on the map
        self.totalPointsAllocated = 6 # Default points player can allocate to skills at the beginning of the game.
        self.inventory = []
        self.equipped = []

    def printHelpText(self):
        # Prints a screen with information based on what actions/items are available to the player. WIP
        import os
        os.system('cls')
        print('          +------------------------------ <<< Help >>> -----------------------------------+')
        print('Map actions:')
        for action in self.possibleMapActions:
	        if action.lower() in gm_scenarios.itemsAndAbilities:
		        print(gm_scenarios.itemsAndAbilities[action.lower()])
        print('\nCombat actions: ')
        for action in self.possibleCombatActions:
	        if action.lower() in gm_scenarios.itemsAndAbilities:
		        print(gm_scenarios.itemsAndAbilities[action.lower()])
        if len(self.equipped) > 0:
            for itemDict in range(len(self.equipped)):
                if self.equipped[itemDict]["type"] not in gm_scenarios.itemsAndAbilities:
                    print('# Log:', self.equipped[itemDict]["type"], 'Item not in gm_scenarios.itemsAndAbilities. From printHelpText()')
                    pass # This line could be removed. 
                else:
                    print(gm_scenarios.itemsAndAbilities[self.equipped[itemDict]["type"].lower()])
        input("Hit 'Enter' to continue... ")

    def printPlayerPossibleactions(self):
        # Prints the possible actions the player can perform, depending on if the player is in combat or not.
        if self.inCombat == True:
            print('You are in combat, your possible actions are: ', end='')
            print(*self.possibleCombatActions, sep=', ', end='') 
            print('.', end='')
        else:
            print('Your possible actions are: ', end='')
            print(*self.possibleMapActions, sep=', ', end='')

    def getInventoryForPrint(self):
        # Print the inventory
        spacing = 45 # set centerspace for the printed text
        if len(self.inventory) > 0:
            itemCount = len(self.inventory)
            inventoryinfo = ' Inventory: %s x %s' % (self.inventory[-1].title(), itemCount)
            inventoryinfoPrint = inventoryinfo.center(spacing)       
            return(inventoryinfoPrint)
        else:
            return None

    def getequippedForPrint(self):
        if len(self.equipped) > 0:
            # if player has something equipped
            spacing = 45 # set centerspace for the printed text
            equippedPrint = []
            for idemDict in range(len(self.equipped)):
                equippedPrint.append(self.equipped[idemDict]["type"])
                strEquipList = ', '.join(equippedPrint).title() # set eqipped list up as string with capital first letter.
                equipped = ' Equipped: %s' % (strEquipList) # put together another string with the list of items so that they can be .center(ed)
                equippedInfoPrint = equipped.center(spacing) # center the text
            return(equippedInfoPrint) # return the string
        else:
            return None

    def printMoveActions(self):
        # Prints directions that player can move. invoked when player enters "move" or "map".
        print('Please enter a direction to move: ', end='')
        print(*self.moveActions, sep=', ', end='')

    def examineLocation(self, gameState):
        # function for examining an area.
        playerLocation = gameState.map.theMap[gameState.map.currentPosition[1]][gameState.map.currentPosition[0]] # Set player loc to make more readable code.
        if playerLocation.beenExamined == True:
            # If the location has been examined, it can not be examined again.
            gm_map.printThis(gameState.scenario["alreadyexamined"][-1])
        elif playerLocation.examineable == False:
            # If the location is not examinable
            gm_map.printThis(gameState.scenario["notexaminable"][-1])
        elif playerLocation.examineable == True and playerLocation.beenExamined == False:
            # If the location is examinable, and haven't been examined before.
            examineRoll = random.randint(1,10) # !!! #
            examineChance = playerLocation.examineChance
            #examineChance = gameState.map.theMap[gameState.map.currentPosition[0]][gameState.map.currentPosition[0]].examineChance
            if examineRoll == 10 and gameState.map.specialItemFound == False:
                # If you roll a 10 on examine, and you have not found the "special" item yet, you can find it.
                #print('# Log: Critical Examine')
                gm_locations.setExamined(playerLocation) # Set examined to True, so that it can not be examined again.
                gm_items.specialItemFound(gameState)
            elif examineRoll >= examineChance:
                # If the examine roll succeeds
                gm_locations.setExamined(playerLocation) # Set examined to True, so that it can not be examined again.
                gm_items.itemFound(gameState)
            else:
                # if the examine roll fail
                gm_map.printThis(gameState.scenario["failedexamine"][random.randint(0, len(gameState.scenario["failedexamine"]) -1)])
        else:
            print('something strange is happening in examineLocation function')

    def rest(self):
        # Rest function, player can rest if it is not in combat, restores HP to full.
        time.sleep(1)
        print('You find a nice spot to rest. After a while you feel fresh and fit for another fight.')
        time.sleep(2)
        self.attributes.pl_current_hp = self.attributes.pl_maxhp


    '''  vvv Xp gain, check if player has leveled up, and levelup mechanics vvv '''
    
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
            pass

    def plLevelUp(self):
        # Asks which stat you want to increase when you level up and calls pl_stat_change to update the stat.
        # After stat, it calls updatePlayerCombatAttributes to update the player modifiers
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
        self.updatePlayerCombatAttributes()

    def playerStatChange(self, strength, agility, fortitude):
        # Procedure to change character stats. 
        self.attributes.pl_str += strength 
        self.attributes.pl_agi += agility
        self.attributes.pl_fort += fortitude

    def updatePlayerCombatAttributes(self):
        self.playerHpChange() # update hp
        self.playerArmChange() # update armor
        self.setupModifiers() # update hit, dmg and dmg reduction modifiers
        self.checkSkilLearn() # check if there's any skills to learn
        
    def checkSkilLearn(self):
        # During levelup, if player has an item, 
        if len(self.equipped) > 0:
            for itemDict in range(len(self.equipped)):
                if self.equipped[itemDict]["ability"] != None and self.equipped[itemDict]["ability"] not in self.possibleCombatActions:
                    self.possibleCombatActions.append(self.equipped[itemDict]["ability"])
                    print('\nYou have learned to use the "%s" ability with your %s!' % (self.equipped[itemDict]["ability"], self.equipped[itemDict]["type"]))
                if self.equipped[itemDict]["ability"] != None and self.equipped[itemDict]["ability"] in self.possibleCombatActions:
                    # print('# Log: No new abilities learned, ability is already learned')
                    input("Hit 'Enter' to continue...")
        else:
            pass
            #print('# Log: No new abilities learned, no items in equipped')

    def playerHpChange(self):
        # Part of the level up routine, updates hp and armor.
        self.attributes.pl_maxhp += self.attributes.pl_fort
        self.attributes.pl_current_hp = self.attributes.pl_maxhp

    def playerArmChange(self):
        # Update player current armor
        newArmModifier = self.attributes.pl_base_armor # Base armor
        newArmModifier += int(self.attributes.pl_agi / 2) # modified from lvl
        newArmModifier += self.attributes.pl_armorBonusFromEquipped # modified from equipped
        self.attributes.pl_currentArmor = newArmModifier

    def setupModifiers(self):
        # Sets up modifiers for dmg bonus modifier, dmg reduction modifier, and hit modifier

        # set up player dmg modifier
        self.attributes.pl_dmgFromStr = int(self.attributes.pl_str / 2) # change modifier based on strength
        newDmgModifier = 0
        newDmgModifier += self.attributes.pl_dmgFromStr
        newDmgModifier += self.attributes.pl_dmgBonusFromEquipped # add bonus based on equipped
        self.attributes.pl_totDmgBonus = newDmgModifier

        # Set up player dmg reduction
        newDmgReductionModifier = 0
        newDmgReductionModifier += int(self.attributes.pl_agi / 2) # modified from agi
        #newDmgReductionModifier += int(self.attributes.pl_currentArmor / 5) # modified from armor
        self.attributes.pl_dmgReduction = newDmgReductionModifier

        # Set up hit modifier
        newHitModifier = 0
        newHitModifier += int(self.attributes.pl_lvl / 2)
        newHitModifier += int(self.attributes.pl_str / 2)
        newHitModifier += self.attributes.pl_hitBonusFromEquipped
        if self.attributes.pl_lvl > 10: # If you hit lvl 10 add some more hit.
            newHitModifier += 2
        elif self.attributes.pl_lvl > 20: # If you hit lvl 20 add some more hit.
            newHitModifier += 4        
        self.attributes.pl_hitmod = newHitModifier # set the new hit modifier to the players attribute

        ''' ^^^ Levelup functions ^^^ '''


    def ItemBonusUpdate(self):
        # update bonuses from items in player attributes.
        if len(self.equipped) > 0: # incase of exceptions
            tothibB = 0
            totdmgB = 0
            totarmB = 0
            for dictionary in range(len(self.equipped)):
                hitB = self.equipped[dictionary]["hitbonus"]
                dmgB = self.equipped[dictionary]["dmgbonus"] 
                armB = self.equipped[dictionary]["armorbonus"]
                tothibB += hitB
                totdmgB += dmgB
                totarmB += armB
                # print('# LOG: type = %s tothitB = %s, totdmgB = %s, totarmB = %s' % (self.equipped[dictionary]["type"],tothibB, totdmgB, totarmB))
            self.attributes.pl_hitBonusFromEquipped = tothibB
            self.attributes.pl_dmgBonusFromEquipped = totdmgB
            self.attributes.pl_armorBonusFromEquipped = totarmB
            if tothibB > 0 or totdmgB > 0:
                self.setupModifiers() # update player hit modifier
            if totarmB > 0:
                self.playerArmChange() # update player armor

class PlayerAttributes():
    # Initializes the player attributes, they are part of the Player class.
    def __init__(self):
        self.pl_lvl = 1 # Player level
        self.pl_xp = 0 # player experience
        self.levelup = [1000, 2000, 3500, 5000, 7000, 8500, 10000, 12500, 15000, 17500, 20000, 23000, 26000, 30000, 35000, 41000, 47000, 52000, 58000, 65000] # xp thresholds for levelup.
        
        self.pl_str = 0 # player strenght
        self.pl_hitmod = 0 # Player hit modifier, modified by lvl, str, and items
        self.pl_dmgFromStr = 0
        self.pl_totDmgBonus = 0

        self.pl_agi = 0 # player agility
        self.pl_dmgReduction = 0
        self.pl_base_armor = 10 # player base armor, will be modified by agi and items
        self.pl_currentArmor = self.pl_base_armor + self.pl_agi # player armor modified by agility.
        
        self.pl_fort = 0 # player foritude
        self.pl_base_hp = 10 # player base hp
        self.pl_maxhp = self.pl_base_hp + self.pl_fort # player max hp, base hp + fortitude.
        self.pl_current_hp = self.pl_maxhp # Current hp, to track how much hp you have during combat.
        
        self.pl_hitBonusFromEquipped = 0    # vvv Affects pl_hitmod
        self.pl_dmgBonusFromEquipped = 0    # bonuses from items, used in combat calculations
        self.pl_armorBonusFromEquipped = 0  # ^^^ Affects pl_currentArmor
        