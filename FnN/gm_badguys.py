"""
    Initialization of enemies and bosses.
"""
import gm_charstats, gm_combat, gm_map, gm_scenarios, gm_gameloop
import time, sys
from random import randint
from random import choice
        
class Enemy:
    # Initializes Enemy
    def __init__(self, pl_lvl, gameState, levelMod=0):
        # Enemy stats, level is based on the players level. 
        self.pl_lvl = pl_lvl
        self.enemy_lvl = randint(self.pl_lvl, self.pl_lvl + 2) + levelMod
        self.enemy_name = choice(gm_scenarios.ENEMYNAMES) + '-' + choice(gm_scenarios.ENEMYNAMES)
        self.enemy_str = 1 * self.enemy_lvl
        self.enemy_dmgFromStr = int(self.enemy_str / 4) # might be changed. Need to test how weak the enemy gets"
        self.enemy_hitmod = int(self.enemy_lvl / 4) + int(self.enemy_str / 4)
        self.enemy_agi = 1 * self.enemy_lvl
        self.enemy_fort = 1 * self.enemy_lvl
        self.enemy_base_hp = 10
        self.enemy_maxhp = self.enemy_base_hp + self.enemy_fort         
        self.enemy_current_hp = self.enemy_maxhp
        self.enemy_base_armor = 10
        self.enemy_currentArmor = self.enemy_base_armor + int(self.enemy_agi / 3)
        self.enemy_xp_reward = self.calculateXpReward()
        self.enemy_statusEffects = []
        self.enemy_abilityActive = [] # For storing abilities used in combat. (taking over for self.statusEffects)
        self.isEnemy = True
        self.setPayexName(gameState)

    def setPayexName(self, gameState):
        # if payex mode is activated, use payexNames for enemy names
        if gameState.payexMode == True:
            self.enemy_name = choice(gm_scenarios.PAYEXNAMES)
        else:
            pass

    def printEnemyStats(self):
        # Print enemy stats when player is in combat. 
        # First set up alignment of the text to be printed (49 is the lenght of the player information frame). 
        spacing = 64
        header = '┌─────────────<<< Enemy information >>>───────────────────────────┐'
                    
        eNameLvl = 'Enemy: %s Level: %s ' % (self.enemy_name.title(), self.enemy_lvl)
        eNameLvlPrint = eNameLvl.center(spacing)
        eArmHp = '   Armor: %s HP: %s / %s      ' % (self.enemy_currentArmor, self.enemy_current_hp, self.enemy_maxhp)
        eArmHpPrint = eArmHp.center(spacing)
        filler = ''
        fillerP = filler.center(spacing)
        print(header)
        print('│', end='')
        print(eNameLvlPrint, '│')
        print('│', end='')
        print(eArmHpPrint, '│')
        print('│', end='')
        print(fillerP,'│')

    def calculateXpReward(self):
        # Scale xp reward down the higher level the enemy gets. Flat number gets too high at higher levels
        xpMultiplier = 150
        if self.enemy_lvl >= 30:
            xpMultiplier = 100
        if self.enemy_lvl >= 25:
            xpMultiplier = 105
        if self.enemy_lvl >= 20:
            xpMultiplier = 115
        if self.enemy_lvl >= 15:
            xpMultiplier = 125
        if self.enemy_lvl >= 10:
            xpMultiplier = 135
        if self.enemy_lvl >= 5:            
            xpMultiplier = 145
        enemy_xp_reward = xpMultiplier * self.enemy_lvl
        return enemy_xp_reward

class Boss(Enemy):
    # Subclass of enemy, inherits enemy functions.
    def __init__(self, pl_lvl, gameState, levelMod=3):
        super().__init__(pl_lvl, gameState, levelMod=3)
        self.enemy_name = choice(gm_scenarios.BOSSNAMES) # Get the boss object to use a bossname instead of a "regular" name.

class BossOLD:
    # Initializes Boss
    def __init__(self, pl_lvl):
        from random import choice
        # Boss stats, level is based on the players level. Level is higher than enemy will get. Stats might be further subject to change.

        self.pl_lvl = pl_lvl
        self.enemy_lvl = randint(self.pl_lvl, self.pl_lvl + 3) + 2
        self.nameList = ['Da Governator','El prehidente', 'TrumPetten', 'Mr. Smith', 'Boba Futt', 'Shredder', 'Joffrey', 'lex luthor', 'bubba ho-tep', 'B.J. Blazkowicz', 'The Sherminator']
        self.enemy_name = choice(self.nameList)
        self.enemy_str = 1 * self.enemy_lvl
        self.enemy_dmgFromStr = int(self.enemy_str / 4)
        self.enemy_hitmod = int(self.enemy_lvl / 4) + int(self.enemy_str / 4)
        self.enemy_agi = 1 * self.enemy_lvl
        self.enemy_fort = 1 * self.enemy_lvl
        self.enemy_base_hp = 10
        self.enemy_maxhp = self.enemy_base_hp + self.enemy_fort         
        self.enemy_current_hp = self.enemy_maxhp
        self.enemy_base_armor = 10
        self.enemy_currentArmor = self.enemy_base_armor + int(self.enemy_agi / 4)
        self.enemy_xp_reward = 300 * self.enemy_lvl
        self.enemy_statusEffects = []
        self.enemy_abilityActive = [] # For storing abilities used in combat. (taking over for self.statusEffects)
        self.isEnemy = True  

def createBoss(gameState):
    # Creates a boss that is more powerful than normal enemies.
    boss = Boss(gameState.player.attributes.pl_lvl, gameState)
    if boss.enemy_currentArmor > 18:
        boss.enemy_currentArmor = 18
    gameState.enemy.append(boss)
    time.sleep(gameState.sleepTimer * 2)
    print()
    gm_map.printThis('A big ass mother dude lunges at you. He\'s yelling that he\'s going to turn you into an ear ornament! DEFEND YOURSELF!')
    time.sleep(gameState.sleepTimer * 1)

def createEnemy(gameState):
    # creates a new enemy, Appends the enemy in gamestate list, so that the information is available.
    enemy = Enemy(gameState.player.attributes.pl_lvl, gameState)
    gameState.enemy.append(enemy)
    
    # Flavor print. When you get an enemy encounter.
    from random import randint
    time.sleep(gameState.sleepTimer * 1)
    print()
    
    # Flavor print. When you get an enemy encounter.
    # Setting up the strings
    combamsgStart = gm_scenarios.COMBAT_FLAVOR["combatintrostart"][randint(0, len(gm_scenarios.COMBAT_FLAVOR["combatintrostart"]) -1)]
    combamsgEnd = gm_scenarios.COMBAT_FLAVOR["combatintroending"][randint(0, len(gm_scenarios.COMBAT_FLAVOR["combatintroending"]) -1)]

    # Combine the strings into one message.
    CombatMessage = combamsgStart + enemy.enemy_name.title() + ' ' + combamsgEnd 
    gm_map.printThis(CombatMessage)
    time.sleep(gameState.sleepTimer * 1.5)
    print('DEFEND YOURSELF!')
    time.sleep(gameState.sleepTimer * 2)