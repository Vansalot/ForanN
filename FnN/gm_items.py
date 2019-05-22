# items that are possible to get in the game.
import random
import gm_scenarios, gm_map

POSSIBLE_ITEMS = ['healing potion']

class Healingpotion():

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
    
def critItemFound(gameState):
    playerLocation = gameState.map.theMap[gameState.map.currentPosition[0]][gameState.map.currentPosition[0]]
    itemFound = gameState.scenario["specialitem"]["type"]["ability"]
    gm_map.printThis(playerLocation.examineText)
    print('You have found a %s!' % (itemFound.title()))
    # Set up stuff to add the item to the inventory
    if itemFound not in gameState.player.weapon:
        gameState.player.specialItem = gameState.scenario["specialitem"]
        gameState.player.weapon.append(itemFound)
        gameState.player.playerHitModChange()