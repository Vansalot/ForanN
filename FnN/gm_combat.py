import gm_badguys, gm_charstats, gm_map
from random import randint
import time

def initiativeRoll(gameState):
    # When combat starts player and enemy rolls initiative, it is modified by agi. Returns who starts combat (str).
    playerInitiative = 0
    enemyInitiative = 0
    while playerInitiative == enemyInitiative:       
        # If player and enemy get the same initiative, reroll initiative.
        enemyInitiative = randint(1,20) + gameState.enemy[gameState.enemyIndex].enemy_agi
        playerInitiative = randint(1,20) + gameState.player.attributes.pl_agi
        
        if (enemyInitiative == playerInitiative) and (playerInitiative and enemyInitiative != 0):
            print('#Log: Identical initiative roll, rerolling')
        
        if playerInitiative > enemyInitiative:
            # A bit many lines of code, but they are for flavoring up the presentation of the initiative roll.
            print('# Initiative roll: %s: %s, ' % (gameState.player.name.title(), playerInitiative), end='')
            time.sleep(1)
            print('%s: %s' % (gameState.enemy[gameState.enemyIndex].enemy_name.title(), enemyInitiative),end='')
            time.sleep(1)
            print(' * %s begins combat *' % (gameState.player.name.title()),end='')            
            time.sleep(2)
            return 'player'
        
        elif enemyInitiative > playerInitiative:
            print('# Initiative roll: %s: %s, ' % (gameState.player.name.title(), playerInitiative), end='')
            time.sleep(1)
            print('%s: %s' % (gameState.enemy[gameState.enemyIndex].enemy_name.title(), enemyInitiative),end='')
            time.sleep(1)
            print(' * %s begins combat *' % (gameState.enemy[gameState.enemyIndex].enemy_name.title()),end='') 
            time.sleep(2)
            # print()
            return 'enemy'
            
def combatRoll():
    # Returns a random number in the range of 1-20.
    hitRoll = randint(7, 20) # changed for debug purposes default value (1,20)
    return hitRoll
    
def hitDecider(gameState, hit_roll, hitModifier, currentArmor, enemy):
    # If hit roll >= the opponents CurrentArmor(armorclass) it will result in a normal hit, then hitDecider returns 'Hit'.
    # If parry is in the picture call the parry function
        
    parryModifier = 0
    # If player of enemy is in parry mode:
    if enemy == True and 'parry' in gameState.player.statusEffects:
        parryModifier += round(gameState.player.attributes.pl_agi / 2) + 1
        # hitDecideParry(hit_roll, hitModifier, currentArmor, enemy)
    elif enemy == False and 'parry' in gameState.enemy[gameState.enemyIndex].enemy_statusEffects:
        parryModifier += round(gameState.enemy[gameState.enemyIndex].enemy_agi / 2) + 1
        
    # normal hit mode (not in parry mode)
    if hit_roll == 20:
        return 'CRITICAL'
    elif hit_roll == 1:
        return 'Fumble'
        #Add fumble mechanics and call it
    elif hit_roll + hitModifier >= (currentArmor + parryModifier) : 
        return 'Hit'
    else:
        return 'Miss'

def counterattack(gameState, enemy):
    # Takes over for the hit decider if the defender is in "parry" mode.
    # a character in parry mode has x more armor value, and if the attacker does not hit, the defender gets a chance to counterattack.
    # the counterattack roll does not have hit modifier, so that parry isn't too overpowered.
    print('# Rolling for counterattack...')
    time.sleep(1)
    if enemy == False: 
        # Player attempt counterattck
        hitRoll = combatRoll() 
        hitResult = hitDecider(gameState, hitRoll, 0, gameState.enemy[gameState.enemyIndex].enemy_currentArmor, gameState.player.isENEMY)
        
        # Own handling if critical hit or fumble is rolled. 
        if hitResult == 'CRITICAL':
            critHandling(gameState, gameState.player.isENEMY)
        # If the player get a hit, it goes through normal hit handling.
        if hitResult == 'Hit':
            print('# Counterattack: You rolled %s * %s *' % (hitRoll, hitResult))
            damageHandling(gameState, damageRoll(), gameState.player.isENEMY)
            time.sleep(2)
        else: # If player misses, it's the enemy's turn 
            print('# Counterattack: You rolled %s * %s *' % (hitRoll, hitResult))
            
    elif enemy == True:
        # enemy attempt counterattck
        hitRoll = combatRoll()
        hitResult = hitDecider(gameState, hitRoll, 0, gameState.player.attributes.pl_currentArmor, gameState.enemy[gameState.enemyIndex].isEnemy)
        
        # Own handling if critical hit, miss or fumble is rolled. 
        if hitResult == 'CRITICAL':
            critHandling(gameState, gameState.enemy[gameState.enemyIndex].isEnemy)
        elif hitResult == 'Hit':
            # If the enemy get a hit, it goes through normal hit handling.
            print('# Counterattack: %s rolled %s * %s *' % (gameState.enemy[gameState.enemyIndex].enemy_name.title(), hitRoll, hitResult))
            damageHandling(gameState, damageRoll(), gameState.enemy[gameState.enemyIndex].isEnemy)
            time.sleep(2)
        else: # Also known as 'miss'
            print('# Counterattack: %s rolled %s * %s *' % (gameState.enemy[gameState.enemyIndex].enemy_name.title(), hitRoll, hitResult))

def damageRoll():
    # Returns a random number between 1 and 6. Can also be called "Base damage".
    from random import randint
    damageRoll = randint(1, 6)
    return damageRoll

def modifiedDamage(gameState, baseDamage, enemy):
    # Returns damage modified by player/enemy stats
    modDmg = 0
    if enemy != True:       
        # If the player is doing damage
        modDmg = baseDamage + gameState.player.attributes.pl_str
        if modDmg < 0:
            modDmg = 0
        print('# %s (base) + %s (mod from str) = %s damage dealt.' % (baseDamage, gameState.player.attributes.pl_str, modDmg))
        return modDmg
    else:
        # If the enemy is doing damage
        modDmg = baseDamage + gameState.enemy[gameState.enemyIndex].enemy_str - gameState.player.attributes.pl_agi
        if modDmg < 0:
            modDmg = 0
        # Modified from player agi should maybe be tweaked, high agi might cause full damage mitigation. 
        print('# %s (base) + %s (mod from enemy str) - %s (mod from player agi) = %s damage dealt.' % (baseDamage, gameState.enemy[gameState.enemyIndex].enemy_str, gameState.player.attributes.pl_agi, modDmg))
        return modDmg

def hpUpdater(gameState, modifiedDmg, enemy):
    # Updates player and enemys hp, also checks if the enemy is dead.
        if enemy != True:
            # the player deals damage 
            gameState.enemy[gameState.enemyIndex].enemy_current_hp -= modifiedDmg
            # Check if enemy is dead
            if gameState.enemy[gameState.enemyIndex].enemy_current_hp <= 0:
                print()
                print('The enemy has been defeated! You have earned', gameState.enemy[gameState.enemyIndex].enemy_xp_reward, 'xp.\n')
                time.sleep(1)
                gm_map.printThis('(Funky cool combat music fades away in the background)\n')
                print()
                gameState.player.plXpGain(gameState.enemy[gameState.enemyIndex].enemy_xp_reward) # update player xp
                gameState.player.inCombat = False # set player out of combat so it can traverse the map
                del gameState.enemy[gameState.enemyIndex] # remove enemy from enemy list
                if 'parry' in gameState.player.statusEffects:
                    gameState.player.statusEffects.remove('parry') # remove parry if it is there, so it does not carry over to next fight.
        
        # enemy deals damage
        elif enemy == True:
            gameState.player.attributes.pl_current_hp -= modifiedDmg
            if gameState.player.attributes.pl_current_hp <= 0:
                # Check if player hp is 0 or less, if so, set the player state as dead
                gameState.player.dead = True
                gameState.player.inCombat = False
            else:
                print()

def critHandling(gameState, enemy):
    # Handling of critical hits.
    # First there will occur a new roll for hit, if hit occurs again, critical damage is dealt. If hit does not occur, normal damage is called.
    hitRoll = combatRoll()
    
    if enemy == False:
        # Handling for player
        print('# You: Critical chance, rolling for hit: ', end='')
        hitResult = hitDecider(gameState, hitRoll, gameState.player.attributes.pl_hitmod, gameState.enemy[gameState.enemyIndex].enemy_currentArmor, enemy)
        if hitResult == 'Hit' or hitResult == 'CRITICAL':
            time.sleep(1)
            print('# You rolled %s (+%s hit modifier) = %s ' % (hitRoll, gameState.player.attributes.pl_hitmod, hitRoll + gameState.player.attributes.pl_hitmod), end='')
            time.sleep(1)
            print('CRITICAL HIT!!!')
            time.sleep(1)
            critDmg = damageRoll() + damageRoll()
            damageHandling(gameState, critDmg, gameState.player.isENEMY)
        else:
            print('Miss, crit becomes normal attack')
            damageHandling(gameState, damageRoll(), gameState.player.isENEMY)
    
    elif enemy == True:
        # Handling for enemy
        print('# %s Critical chance, rolling for hit: ' % (gameState.enemy[gameState.enemyIndex].enemy_name.title()), end='')
        hitResult = hitDecider(gameState, hitRoll, gameState.enemy[gameState.enemyIndex].enemy_hitmod, gameState.player.attributes.pl_currentArmor, enemy)
        if hitResult == 'Hit' or hitResult == 'CRITICAL':
            time.sleep(1)
            print('# %s rolled %s (+%s hit modifier) = %s ' % (gameState.enemy[gameState.enemyIndex].enemy_name.title(), hitRoll, gameState.enemy[gameState.enemyIndex].enemy_hitmod, hitRoll + gameState.enemy[gameState.enemyIndex].enemy_hitmod), end='')
            time.sleep(1)
            print('CRITICAL HIT!!!')
            time.sleep(1)
            critDmg = damageRoll() + damageRoll()
            damageHandling(gameState, critDmg, gameState.enemy[gameState.enemyIndex].isEnemy)
        else:
            print('Miss, crit becomes normal attack')
            damageHandling(gameState, damageRoll(), gameState.enemy[gameState.enemyIndex].isEnemy)

def damageHandling(gameState, baseDamage, enemy):
    # rolls damage for player, applies modifiers and sends it to the hpupdater.
    if enemy == False: # For player
        modifiedDmg = modifiedDamage(gameState, baseDamage, gameState.player.isENEMY)
        hpUpdater(gameState, modifiedDmg, gameState.player.isENEMY)
    elif enemy == True: # For enemy
        modifiedDmg = modifiedDamage(gameState, baseDamage, gameState.enemy[gameState.enemyIndex].isEnemy)
        hpUpdater(gameState, modifiedDmg, gameState.enemy[gameState.enemyIndex].isEnemy)

def combatLoop(gameState):
    # General combat loop for the game.
    if len(gameState.enemy) <= 0:
        # If there are no enemies in the list, create new enemy
        gm_badguys.createEnemy(gameState)
    print()        
    gm_map.printThis('(Que funky cool combat music) DU DU DU DU DU DU DU DU DUUUUUUUUUUU DU DU DUDUDU...\n')
    time.sleep(1)
    print()
    turn = initiativeRoll(gameState)
    print()

    while gameState.player.inCombat == True:
        ###
        # Player's turn to act in combat.
        ###
        if turn == 'player':
            if 'parry' in gameState.player.statusEffects:
                gameState.player.statusEffects.remove('parry')
            if gameState.player.dead == True: # If the player is dead, break out of the loop.
                break
            
            time.sleep(1)
            print()    
            gameState.enemy[gameState.enemyIndex].printEnemyStats() # print enemy stats
            gameState.player.printNameLevelXp() # print player stats
            gameState.player.printPlayerPossibleactions() # print player's possible actions
            action = ''
            
            while action not in gameState.player.possibleCombatActions: # Loop that will ask the player to enter correct action.
                action = input(' Please enter your action: ').lower()
                print()
            if action == 'parry' or action.startswith('p'):
                gameState.player.statusEffects.append(action)
                print('You hunker down into a defensive pose.')
                time.sleep(1)
                turn = 'enemy'
                continue
            
            elif action == 'hit' or action.startswith('h'):
                # Roll for hit, and check the result of the hit roll.
                hitRoll = combatRoll() 
                hitResult = hitDecider(gameState, hitRoll, gameState.player.attributes.pl_hitmod, gameState.enemy[gameState.enemyIndex].enemy_currentArmor, gameState.player.isENEMY)
                # Own handling if critical hit or fumble is rolled. 
                if hitResult == 'CRITICAL':
                    critHandling(gameState, gameState.player.isENEMY)
                    turn = 'enemy'
                    continue
                elif hitResult == 'Fumble':
                    print('fumble')
                    turn = 'enemy'
                    continue
            
            # If the player get a hit, it goes through normal hit handling.
            print('# You rolled %s (+%s hit modifier) = %s. * %s *' % (hitRoll, gameState.player.attributes.pl_hitmod, hitRoll + gameState.player.attributes.pl_hitmod, hitResult))
            if hitResult == 'Hit':
                damageHandling(gameState, damageRoll(), gameState.player.isENEMY)
                turn = 'enemy'
                time.sleep(2)
            elif hitResult == 'Miss' and 'parry' in gameState.enemy[gameState.enemyIndex].enemy_statusEffects:
                # If player misses when enemy is in parry mode
                print('# You rolled %s (+%s hit modifier) = %s. * Parry *' % (hitRoll, gameState.player.attributes.pl_hitmod, hitRoll + gameState.player.attributes.pl_hitmod))
                time.sleep(0.5)
                counterattack(gameState, gameState.enemy[gameState.enemyIndex].isEnemy)
                turn = 'enemy'    
                continue
            else: # If player misses, it's the enemy's turn
                turn = 'enemy'    
                continue
        
        #
        # Enemy's turn to act in combat
        #
        elif turn == 'enemy':
            time.sleep(1)
            if 'parry' in gameState.enemy[gameState.enemyIndex].enemy_statusEffects:
                # If enemy in parrymode remove parrymode at the start of his next turn.
                gameState.enemy[gameState.enemyIndex].enemy_statusEffects.remove('parry')
            if gameState.enemy[gameState.enemyIndex].enemy_current_hp < (gameState.enemy[gameState.enemyIndex].enemy_maxhp / 2):
                # If the enemy is under half hp, he will have a chance to enter parrymode.
                if randint(0,10) > 4: #  ~60% chance of going into parry mode.
                    gameState.enemy[gameState.enemyIndex].enemy_statusEffects.append('parry')
                    print('%s hunker down into a defensive pose.' % (gameState.enemy[gameState.enemyIndex].enemy_name.title()))
                    time.sleep(1)
                    turn = 'player'
                    continue
            
            # Roll for hit, and check the result of the hit roll.
            hitRoll = combatRoll()
            hitResult = hitDecider(gameState, hitRoll, gameState.enemy[gameState.enemyIndex].enemy_hitmod, gameState.player.attributes.pl_currentArmor, gameState.enemy[gameState.enemyIndex].isEnemy)
            print()
            # Own handling if critical hit, miss or fumble is rolled. 
            if hitResult == 'CRITICAL':
                critHandling(gameState, gameState.enemy[gameState.enemyIndex].isEnemy)
                turn = 'player'
                continue
            elif hitResult == 'Fumble':
                print('fumble')
                turn = 'player'
                continue
            elif hitResult == 'Hit':
                print('# %s rolled %s (+%s hit modifier) = %s. * %s *' % (gameState.enemy[gameState.enemyIndex].enemy_name.title(), hitRoll, gameState.enemy[gameState.enemyIndex].enemy_hitmod, hitRoll + gameState.enemy[gameState.enemyIndex].enemy_hitmod, hitResult))
                damageHandling(gameState, damageRoll(), gameState.enemy[gameState.enemyIndex].isEnemy)
                turn = 'player'
                time.sleep(2)
            elif hitResult == 'Miss' and 'parry' in gameState.player.statusEffects:
                # If enemy misses when player is in parry mode
                print('# %s rolled %s (+%s hit modifier) = %s. * Parry *' % (gameState.enemy[gameState.enemyIndex].enemy_name.title(), hitRoll, gameState.enemy[gameState.enemyIndex].enemy_hitmod, hitRoll + gameState.enemy[gameState.enemyIndex].enemy_hitmod))
                time.sleep(0.5)
                counterattack(gameState, gameState.player.isENEMY)
                turn = 'player'
            else: # Also known as 'miss'
                print('# %s rolled %s (+%s hit modifier) = %s. * %s *' % (gameState.enemy[gameState.enemyIndex].enemy_name.title(), hitRoll, gameState.enemy[gameState.enemyIndex].enemy_hitmod, hitRoll + gameState.enemy[gameState.enemyIndex].enemy_hitmod, hitResult))
                turn = 'player'
        if gameState.player.dead == True: # If player is dead when enemy turn is finished, exit the loop.
                break
