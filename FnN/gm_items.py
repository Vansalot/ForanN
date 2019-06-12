# items that are possible to get in the game.
import random
import gm_scenarios, gm_map

POSSIBLE_ITEMS = ['healing potion']

class Healingpotion():
    # NOT IN USE ATM
    def __init__(self, pl_lvl):
        # Initialize healing potion.
        self.name = 'healing potion'
        self.potionLvl = gameState.player.attributes.pl_lvl
        self.hpgained = 3 * potionLvl
        
def drinkHealingPot(gameState):
    # Using healing pot heals the player
    hpgained = 3 + gameState.player.attributes.pl_lvl # provisorisk kode
    if 'healing potion' in gameState.player.inventory:
        gameState.player.attributes.pl_current_hp += hpgained
        gameState.player.inventory.remove('healing potion')
        print('You use your healing potion, healing you for %s hp' % (hpgained))
        if 'healing potion' not in gameState.player.inventory:
            gameState.player.possibleCombatActions.remove('healing potion')
    else:
        pass

def itemFound(gameState):
    # If the search roll passes, this function designates what item is found
    playerLocation = gameState.map.theMap[gameState.map.currentPosition[0]][gameState.map.currentPosition[0]]
    itemFound = random.choice(POSSIBLE_ITEMS)
    gm_map.printThis(playerLocation.examineText)
    print('You have found a %s' % (itemFound.title()))
    # Set up stuff to add the item to the inventory
    if itemFound == 'healing potion' and itemFound not in gameState.player.inventory:
        gameState.player.possibleCombatActions.append('healing potion')
    gameState.player.inventory.append(itemFound)
    #print()
    
def specialItemFound(gameState):
    from random import choice
    playerLocation = gameState.map.theMap[gameState.map.currentPosition[0]][gameState.map.currentPosition[0]] # set up variable for playerlocation.
    itemFound = choice(itemlist) # Get a random item from the itemlist.
    while itemFound in gameState.player.equipped: # If the player already has the item, try again
         itemFound = choice(itemlist)
    itemName = itemFound["type"]
    gameState.map.specialItemFound = True # You can only find 1 special item per scenario.
    if gameState.map.victory == False:
        gm_map.printThis(playerLocation.examineText)
    if gameState.map.victory == True:
         gm_map.printThis('After finishing up the fight you lean down and... ')
    print('You have found a %s!' % (itemName.title()))
    # Set up stuff to add the item to the player, update stats based on item stats.
    if itemFound not in gameState.player.equipped: # Should set up own function for this!!
        gameState.player.equipped.append(itemFound) # append the item dict in equipped list.
        gameState.player.ItemBonusUpdate() # create this function


''' 
    ** Itemlist, for now, items can be represented in the following way: **
    'type' : sword / shield / breastplate / etc (string)
    'armorbonus' : int
    'hitbonus' : int
    'dmgbonus' : int
    'ability' : eg. cleave / power attack / point blank shot (string) / None if no ability is to be learned.

'''
# Possible equippable items to get in the game
itemlist = [
{'type':'sword', 'hitbonus': 2, 'dmgbonus': 1, 'armorbonus': 0, 'ability': 'power attack'},
{'type':'shield', 'hitbonus': 0, 'dmgbonus': 0, 'armorbonus': 1, 'ability': 'shield bash'},
{'type':'helmet', 'hitbonus': 0, 'dmgbonus': 0, 'armorbonus': 1, 'ability': None},
{'type':'chainmail', 'hitbonus': 0, 'dmgbonus': 0, 'armorbonus': 2, 'ability': None},
]