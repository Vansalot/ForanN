# items that are possible to get in the game.
import random
import gm_scenarios

POSSIBLE_ITEMS = ['Healing potion']

class Healingpotion():

    def __init__(self, pl_lvl):
        # Initialize healing potion.
        self.name = 'Healing potion'
        self.potionlvl = pl_lvl
        self.hpgained = 3 * pl_lvl
        
    def drinkHealingPot(self):
        # Using healing pot heals the player
        gamestate.player.attributes.pl_current_hp += self.hpgained
        # insert code to remove healing pot from inventory.


def itemFound(gameState):
    # If the search roll passes, this function designates what item is found
    playerLocation = gameState.map.theMap[gameState.map.currentPosition[0]][gameState.map.currentPosition[0]]
    itemFound = random.choice(POSSIBLE_ITEMS)
    print(gm_scenarios.forest["examination"][random.randint(0, len(gm_scenarios.forest["examination"]) -1)]) # Flavortext that is printed when entering a new location.)
    print('You have found a %s' % (itemFound))
    # Set up stuff to add the item to the inventory
    gameState.player.inventory.append(itemFound)
    #print()
    
    