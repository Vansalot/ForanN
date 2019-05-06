"""
    Initialization of enemies and bosses.
"""
import gm_charstats, gm_combat
import time, sys
from random import randint
from random import choice

# add class payexboi?

class Enemy:
    # Initializes Enemy
    def __init__(self, pl_lvl, gameState):
        # Enemy stats, level is based on the players level. 
        self.pl_lvl = pl_lvl
        self.enemy_lvl = randint(self.pl_lvl, self.pl_lvl + 2)
        self.nameList = ['Benny', 'bjarte', 'roger', 'bent', 'are', 'franz', 'preben', 'hans', 'patrick', 'Roy', 'egil', 'Kent', 'Robin', 'Ola', 'Jonny', 'Ronny', 'Raymond', 'Bendik', 'Henrik', 'Jens', 'Peder', 'Preben', 'William', 'Axel', 'Erlend', 'Fredrik', 'Hans', 'Jacob', 'Johan', 'Karl', 'Nicolai', 'Oscar', 'Sondre', 'Tobias']
        self.payexNames = ['Jens Egil', 'Jørn Efteland', 'Jørn Tharaldsen', 'Hallstein', 'Petter storaas', 'Jon Terje', 'Christian Slater', 'Andreas Jakobsen']
        self.enemy_name = choice(self.nameList) + '-' + choice(self.nameList)
        self.enemy_hitmod = round(self.enemy_lvl / 2)
        self.enemy_str = 1 * self.enemy_lvl
        self.enemy_agi = 1 * self.enemy_lvl
        self.enemy_fort = 1 * self.enemy_lvl
        self.enemy_base_hp = 10
        self.enemy_maxhp = self.enemy_base_hp + self.enemy_fort         
        self.enemy_current_hp = self.enemy_maxhp
        self.enemy_base_armor = 10
        self.enemy_currentArmor = self.enemy_base_armor + self.enemy_agi
        self.enemy_xp_reward = 250 * self.enemy_lvl
        self.enemy_statusEffects = []
        self.isEnemy = True
        self.setPayexName(gameState)

    def setPayexName(self, gameState):
        if gameState.payexMode == True:
            self.enemy_name = choice(self.payexNames)

    def printEnemyStats(self):
        # Print enemy stats when player is in combat. 
        # First set up alignment of the text to be printed (49 is the lengt of the player information frame). 
        headSpacing = 49
        eNameLvl = ' Enemy: %s Level: %s ' % (self.enemy_name.title(), self.enemy_lvl)
        eNameLvlPrint = eNameLvl.center(headSpacing)
        eArmHp = '    Armor: %s HP: %s / %s      ' % (self.enemy_currentArmor, self.enemy_current_hp, self.enemy_maxhp)
        eArmHpPrint = eArmHp.center(headSpacing)
        header = len(eNameLvl) * '#'
        headerPrint = header.center(headSpacing)
        print(' ', headerPrint)
        print(' ', eNameLvlPrint)
        print(' ', eArmHpPrint)
        print(' ', headerPrint)

class Boss:
    # Initializes Boss
    def __init__(self, pl_lvl):
        from random import choice
        # Boss stats, level is based on the players level. Level is higher than enemy will get. Stats might be further subject to change.

        self.pl_lvl = pl_lvl
        self.enemy_lvl = randint(1, self.pl_lvl + 2) + 1
        self.nameList = ['Da Governator','El prehidente', 'TrumPetten', 'Mr. Smith', 'Boba Futt', 'Shredder', 'Joffrey', 'lex luthor', 'bubba ho-tep']
        self.enemy_name = choice(self.nameList)
        self.enemy_hitmod = round(self.enemy_lvl / 2)
        self.enemy_str = 1 * self.enemy_lvl
        self.enemy_agi = 1 * self.enemy_lvl
        self.enemy_fort = 1 * self.enemy_lvl
        self.enemy_base_hp = 10
        self.enemy_maxhp = self.enemy_base_hp + self.enemy_fort         
        self.enemy_current_hp = self.enemy_maxhp
        self.enemy_base_armor = 10
        self.enemy_currentArmor = self.enemy_base_armor + self.enemy_agi
        self.enemy_xp_reward = 250 * self.enemy_lvl
        self.enemy_statusEffects = []
        self.isEnemy = True  

    def printEnemyStats(self):
        headSpacing = 49
        eNameLvl = ' Enemy: %s Level: %s ' % (self.enemy_name.title(), self.enemy_lvl)
        eNameLvlPrint = eNameLvl.center(headSpacing)
        eArmHp = '    Armor: %s HP: %s / %s      ' % (self.enemy_currentArmor, self.enemy_current_hp, self.enemy_maxhp)
        eArmHpPrint = eArmHp.center(headSpacing)
        header = len(eNameLvl) * '#'
        headerPrint = header.center(headSpacing)
        print(' ', headerPrint)
        print(' ', eNameLvlPrint)
        print(' ', eArmHpPrint)
        print(' ', headerPrint)


def createBoss(gameState):
    # Creates a boss that is more powerful than normal enemies.
    boss = Boss(gameState.player.attributes.pl_lvl)
    gameState.enemy.append(boss)
    time.sleep(2)
    print()
    print('A big ass mother dude lunges through the bushes. Screams that he\'s going to turn you into an ear ornament! DEFEND YOURSELF!')
    time.sleep(1)

def createEnemy(gameState):
    # creates a new enemy
    enemy = Enemy(gameState.player.attributes.pl_lvl, gameState)
    # Appends the enemy in gamestate list, so that the information is available.
    gameState.enemy.append(enemy)
    time.sleep(1)
    print()
    message = 'A raving madman who calls himself %s lunges through the bushes. He looks like he wants to introduce you to a can of whoop-ass! ' % (enemy.enemy_name.title())
    for character in message:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.02)
    time.sleep(1.5)
    message2 = 'DEFEND YOURSELF!'
    print(message2)
    time.sleep(2)
