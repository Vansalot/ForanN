import gm_badguys, gm_charstats, gm_map, gm_items, gm_gameloop
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
        
    print('# Initiative roll: %s: %s, ' % (gameState.player.name.title(), playerInitiative), end='')
    time.sleep(gameState.sleepTimer * 1)
    print('%s: %s' % (gameState.enemy[gameState.enemyIndex].enemy_name.title(), enemyInitiative),end='')
    time.sleep(gameState.sleepTimer * 1)
        
    if playerInitiative > enemyInitiative:
        # if player wins the roll
        print(' * %s begins combat *\n' % (gameState.player.name.title()),end='')            
        time.sleep(2)
        return 'player'
    
    elif enemyInitiative > playerInitiative:
        # if enemy wins the roll
        print(' * %s begins combat *\n' % (gameState.enemy[gameState.enemyIndex].enemy_name.title()),end='') 
        time.sleep(2)
        return 'enemy'
            
def combatRoll(gameState):
    # Returns a random number in the range of 1-20.
    hitRoll = randint(8, 20) # changed for debug purposes default value (1,20)
    rollist = []
    rollPrint = ''
    # prints a more lively roll "animation", might be separated into an own function. 
    while len(rollist) < 10:
        rollist.append(randint(1, 20)) 
    rollPrint = ''.join(str(number) for numberj in rollist)
    print('# Rolling for hit',end='')
    gm_map.printThis('.....')
    gm_map.printThis(rollPrint, speed=0.04)
    gm_map.printThis('....'+str(hitRoll)+'!', speed=0.04)
    time.sleep(gameState.sleepTimer * 1)
    print()
    return hitRoll
    
def hitDecider(gameState, hit_roll, currentArmor, enemy):
    # If hit roll >= the opponents CurrentArmor(armorclass) it will result in a normal hit, then hitDecider returns 'Hit'.
    # If parry is in the picture call the parry function
    player = gameState.player # verbosification
    parryModifier = 0
    hitModifier = 0
    # Change hit modifier based on if it is player or enemy, and if there are abilities that change hit modifier.
    if enemy == True:
        hitModifier = gameState.enemy[gameState.enemyIndex].enemy_hitmod
    elif enemy == False:
        hitModifier = player.attributes.pl_hitmod
        if 'power attack' in player.abilityActive or 'shield bash' in player.abilityActive:
            hitpen = 2
            hitModifier -= hitpen # If powerattack or shield bash, hit modifier is reduced.
    
    # Change parry modifier if player or enemy has activated parry mode.
    if enemy == True and 'parry' in player.abilityActive:
        parryModifier += round(player.attributes.pl_agi / 2) + 1
    elif enemy == False and 'parry' in gameState.enemy[gameState.enemyIndex].enemy_abilityActive:
        parryModifier += round(gameState.enemy[gameState.enemyIndex].enemy_agi / 2) + 1
    
    # change hit modifier if it is an counterattack:
    if enemy == False and 'parry' in player.abilityActive:
        hitModifier = 0
    elif enemy == True and 'parry' in gameState.enemy[gameState.enemyIndex].enemy_abilityActive:
        hitModifier = 0

    # Check the result of the hit based on the modified values(above)
    if hit_roll == 20:
        return 'CRITICAL'
    elif hit_roll == 1:
        return 'Miss'
    elif hit_roll + hitModifier >= (currentArmor + parryModifier) :
        return 'Hit'
    else:
        return 'Miss'

def damageRoll():
    # Returns a random number between 1 and 6. Can also be called "Base damage".
    damageRoll = randint(1, 6)
    return damageRoll

def damageHandling(gameState, baseDamage, enemy):
    # updates hp for player and enemy
    if enemy == False: # For player
        modifiedDmg = modifiedDamage(gameState, baseDamage, gameState.player.isENEMY)
        hpUpdater(gameState, modifiedDmg, gameState.player.isENEMY)
    elif enemy == True: # For enemy
        modifiedDmg = modifiedDamage(gameState, baseDamage, gameState.enemy[gameState.enemyIndex].isEnemy)
        hpUpdater(gameState, modifiedDmg, gameState.enemy[gameState.enemyIndex].isEnemy)

def modifiedDamage(gameState, baseDamage, enemy):
    # Returns damage modified by player/enemy stats
    modDmg = 0
    
    if enemy != True:       
        # If the player is doing damage
        strdmg = gameState.player.attributes.pl_dmgFromStr # for use in print
        if 'shield bash' in gameState.player.abilityActive:
            shieldBashpen = 2
            modDmg +=  baseDamage + strdmg - shieldBashpen 
            if modDmg <= 0:
                modDmg = 1
            gameState.enemy[gameState.enemyIndex].enemy_statusEffects.append('shield bash') # append shield bash status to enemy.
            print('# %s (base) + %s (mod from str) - %s (shield bash penalty) = %s damage dealt.' % (baseDamage, strdmg, shieldBashpen, modDmg))
            return modDmg
        
        equippeddmg = gameState.player.attributes.pl_dmgBonusFromEquipped # for use in print
        modDmg += baseDamage + gameState.player.attributes.pl_totDmgBonus # modified dmg is base + player total dmg bonus.
        if modDmg <= 0:
            modDmg = 1
        if 'power attack' in gameState.player.abilityActive:
            powerAttackDmg = 2
            modDmg += powerAttackDmg
            print('# %s (base) + %s (mod from str) + %s (mod from equipped items) + %s (power attack) = %s damage dealt.' % (baseDamage, strdmg, equippeddmg, powerAttackDmg, modDmg))
        if equippeddmg > 0 and 'power attack' not in gameState.player.abilityActive:
            print('# %s (base) + %s (mod from str) + %s (mod from equipped items) = %s damage dealt.' % (baseDamage, strdmg, equippeddmg, modDmg))
        if equippeddmg == 0:
            print('# %s (base) + %s (mod from str) = %s damage dealt.' % (baseDamage, strdmg, modDmg))

        return modDmg
    else:
        # If the enemy is doing damage
        modDmg = baseDamage + gameState.enemy[gameState.enemyIndex].enemy_dmgFromStr - gameState.player.attributes.pl_dmgReduction
        if modDmg <= 0:
            modDmg = 1
        # Modified from player agi should maybe be tweaked, high agi might cause full damage mitigation. 
        print('# %s (base) + %s (mod from enemy str) - %s (mod from player agi) = %s damage dealt.' % (baseDamage, gameState.enemy[gameState.enemyIndex].enemy_dmgFromStr, gameState.player.attributes.pl_dmgReduction, modDmg))
        return modDmg

def hpUpdater(gameState, modifiedDmg, enemy):
    # Updates player and enemy hp, also checks if the enemy is dead.
        if enemy != True:
            # the player deals damage 
            gameState.enemy[gameState.enemyIndex].enemy_current_hp -= modifiedDmg
            # Check if enemy is dead
            if gameState.enemy[gameState.enemyIndex].enemy_current_hp <= 0:
                print()
                print('The enemy has been defeated! You have earned', gameState.enemy[gameState.enemyIndex].enemy_xp_reward, 'xp.\n')
                time.sleep(gameState.sleepTimer * 1)
                gm_map.printThis('(Funky cool combat music fades away in the background)\n', speed=0.05)
                time.sleep(gameState.sleepTimer * 1)
                print()
                gameState.player.abilityActive = []
                gameState.player.plXpGain(gameState.enemy[gameState.enemyIndex].enemy_xp_reward) # update player xp
                gameState.player.inCombat = False # set player out of combat so it can traverse the map
                del gameState.enemy[gameState.enemyIndex] # remove enemy from enemy list
                
        # enemy deals damage
        elif enemy == True:
            gameState.player.attributes.pl_current_hp -= modifiedDmg
            if gameState.player.attributes.pl_current_hp <= 0:
                # Check if player hp is 0 or less, if so, set the player state as dead
                gameState.player.dead = True
                gameState.player.inCombat = False
            else:
                pass

def critHandling(gameState, enemy):
    # Handling of critical hits.
    # First there will occur a new roll for hit, if hit occurs again, critical damage is dealt. If hit does not occur, normal damage is called.
    if enemy == False:
        # Handling for player
        print('# You: Critical chance!')
        time.sleep(0.5)
        hitRoll = combatRoll(gameState)
        hitResult = hitDecider(gameState, hitRoll, gameState.enemy[gameState.enemyIndex].enemy_currentArmor, enemy)
        if hitResult == 'Hit' or hitResult == 'CRITICAL':
            time.sleep(gameState.sleepTimer * 1)
            if 'parry' in gameState.player.abilityActive:
                print('# You rolled %s ' % (hitRoll), end='')
            if 'parry' not in gameState.player.abilityActive:
                print('# You rolled %s + %s (hit modifier) = %s ' % (hitRoll, gameState.player.attributes.pl_hitmod, hitRoll + gameState.player.attributes.pl_hitmod), end='')
            time.sleep(gameState.sleepTimer * 1)
            print('CRITICAL HIT!!!')
            time.sleep(gameState.sleepTimer * 1)
            critDmg = damageRoll() + damageRoll()
            damageHandling(gameState, critDmg, gameState.player.isENEMY)
        else:
            print('Miss, crit becomes normal attack')
            damageHandling(gameState, damageRoll(), gameState.player.isENEMY)
    
    elif enemy == True:
        # Handling for enemy
        print('# %s Critical chance!' % (gameState.enemy[gameState.enemyIndex].enemy_name.title()), end='')
        time.sleep(0.5)
        hitRoll = combatRoll(gameState)
        hitResult = hitDecider(gameState, hitRoll, gameState.player.attributes.pl_currentArmor, enemy)
        if hitResult == 'Hit' or hitResult == 'CRITICAL':
            time.sleep(gameState.sleepTimer * 1)
            if 'parry' not in gameState.enemy[gameState.enemyIndex].enemy_abilityActive:
                print('# %s rolled %s + %s (hit modifier) = %s ' % (gameState.enemy[gameState.enemyIndex].enemy_name.title(), hitRoll, gameState.enemy[gameState.enemyIndex].enemy_hitmod, hitRoll + gameState.enemy[gameState.enemyIndex].enemy_hitmod), end='')
            if 'parry' in gameState.enemy[gameState.enemyIndex].enemy_abilityActive:
                print('# %s rolled %s ' % (gameState.enemy[gameState.enemyIndex].enemy_name.title(), hitRoll), end='')
            time.sleep(gameState.sleepTimer * 1)
            print('CRITICAL HIT!!!')
            time.sleep(gameState.sleepTimer * 1)
            critDmg = damageRoll() + damageRoll()
            damageHandling(gameState, critDmg, gameState.enemy[gameState.enemyIndex].isEnemy)
        else:
            print('Miss, crit becomes normal attack')
            damageHandling(gameState, damageRoll(), gameState.enemy[gameState.enemyIndex].isEnemy)

def counterattack(gameState, enemy):
    # Takes over for the hit decider if the defender is in "parry" mode.
    # a character in parry mode has x more armor value, and if the attacker does not hit, the defender gets a chance to counterattack.
    # the counterattack roll does not have hit modifier, so that parry isn't too overpowered.
    print('\n# Attack was parried, provoking a counterattack!')
    time.sleep(gameState.sleepTimer * 1)
    if enemy == False: 
        # Player attempt counterattck
        hitRoll = combatRoll(gameState) 
        hitResult = hitDecider(gameState, hitRoll, gameState.enemy[gameState.enemyIndex].enemy_currentArmor, gameState.player.isENEMY)
        # Own handling if critical hit is rolled. 
        if hitResult == 'CRITICAL':
            critHandling(gameState, gameState.player.isENEMY)
        # If the player get a hit, it goes through normal hit handling.
        elif hitResult == 'Hit':
            print('# Counterattack: You rolled %s * %s *' % (hitRoll, hitResult))
            damageHandling(gameState, damageRoll(), gameState.player.isENEMY)
            time.sleep(2)
        else: # If player misses, it's the enemy's turn 
            print('# Counterattack: You rolled %s * %s *' % (hitRoll, hitResult))
            
    elif enemy == True:
        # enemy attempt counterattck
        hitRoll = combatRoll(gameState)
        hitResult = hitDecider(gameState, hitRoll, gameState.player.attributes.pl_currentArmor, gameState.enemy[gameState.enemyIndex].isEnemy)
        
        # Own handling if critical hit, miss is rolled. 
        if hitResult == 'CRITICAL':
            critHandling(gameState, gameState.enemy[gameState.enemyIndex].isEnemy)
        elif hitResult == 'Hit':
            # If the enemy get a hit, it goes through normal hit handling.
            print('# Counterattack: %s rolled %s * %s *' % (gameState.enemy[gameState.enemyIndex].enemy_name.title(), hitRoll, hitResult))
            damageHandling(gameState, damageRoll(), gameState.enemy[gameState.enemyIndex].isEnemy)
            time.sleep(2)
        else: # Also known as 'miss'
            print('# Counterattack: %s rolled %s * %s *' % (gameState.enemy[gameState.enemyIndex].enemy_name.title(), hitRoll, hitResult))

def powerAttack(gameState):
    message = 'You take a deep breath and swing your blade like you mean it!\n'
    gm_map.printThis(message)
    hitRoll = combatRoll(gameState)
    hitResult = hitDecider(gameState, hitRoll, gameState.enemy[gameState.enemyIndex].enemy_currentArmor, gameState.player.isENEMY)
    return hitResult

def shieldBash(gameState):
    message = 'You lean back and swing your hip like you mean it(hips don\'t lie), and slam your shield towards the enemy!\n'
    gm_map.printThis(message)
    hitRoll = combatRoll(gameState)
    hitResult = hitDecider(gameState, hitRoll, gameState.enemy[gameState.enemyIndex].enemy_currentArmor, gameState.player.isENEMY)
    if hitResult == 'CRITICAL':
        hitResult = 'Hit'
    return hitResult

def checkValidAction(gameState):
    # Validating input during combat. Checks if the input is in the valid combat actions list. if not you are asked to enter the correct action.
    enteredAction = ''
    while enteredAction.replace(" ", "").isalpha() != True: # Loop that will ask the player to enter correct action.
        gameState.player.printPlayerPossibleactions() # print player's possible actions
        enteredAction = input('\nPlease enter your action: ').lower()
        #print()
        if enteredAction == 'medic': 
            # in combat cheat, meant for debug purposes
            gameState.player.attributes.pl_current_hp = gameState.player.attributes.pl_maxhp
        if enteredAction not in gameState.player.possibleCombatActions:
            print('Entered action is not valid, try again.\n')
            enteredAction = ''

    return enteredAction

def combatLoop(gameState):
    # General combat loop for the game.
    if len(gameState.enemy) <= 0:
        # If there are no enemies in the list, create new enemy
        gm_badguys.createEnemy(gameState)
    print('\n(Que funky cool combat music)', end='')
    time.sleep(gameState.sleepTimer * 0.3)
    gm_map.printThis(' * DU DU DU DU DU DU DU DU DUUUUUUUUUUU DU DU DUDUDU... *\n\n',speed=0.05)
    time.sleep(gameState.sleepTimer * 1)
    turn = initiativeRoll(gameState)
    
    # Making enemy and player less verbose
    currentEnemy = gameState.enemy[gameState.enemyIndex]
    player = gameState.player

    while player.inCombat == True:
        # Combat loop
        if turn == 'player':
            ###
            # Player's turn to act in combat.
            ###
            if len(player.abilityActive) > 0: 
                player.abilityActive = [] # Remove all active abilities so that it does not carry over to the current round.
            
            if player.attributes.pl_current_hp <= 0:
                # If the player is dead, break out of the loop.
                break

            print('\nYour turn. Press enter to continue...',end='')
            music = randint(1,2)
            if music == 1:
                gm_map.printThis(' * DU DU DU DU DU DUUUUUU DU DU DU *\n')
            input()

            # Print player and enemy information
            currentEnemy.printEnemyStats()
            gameState.map.drawMap(gameState)

            # Get action from player and check if it is valid.
            enteredAction = checkValidAction(gameState)
            print()

            
            if enteredAction != 'hit': # power attack, parry or shield bash. 
                player.abilityActive.append(enteredAction)
                # Power attack # 
                if enteredAction == 'power attack':
                    hitResult = powerAttack(gameState)
                    if hitResult == 'CRITICAL': # If power attack crits
                        critHandling(gameState, player.isENEMY)
                        turn = 'enemy'
                        continue
                # Shield Bash # 
                elif enteredAction == 'shield bash':                                     
                    hitResult = shieldBash(gameState)
                # Parry # 
                elif enteredAction == 'parry':
                    print('You hunker down into a defensive pose.')
                    time.sleep(gameState.sleepTimer * 1)
                    turn = 'enemy'
                    continue

            # Hit action 
            elif enteredAction == 'hit' or enteredAction == 'h':
                hitRoll = combatRoll(gameState) 
                hitResult = hitDecider(gameState, hitRoll, currentEnemy.enemy_currentArmor, player.isENEMY)
                # Own handling if critical hit is rolled. 
                if hitResult == 'CRITICAL':
                    critHandling(gameState, player.isENEMY)
                    turn = 'enemy'
                    continue
            # Use healing potion
            elif enteredAction == 'heal' or enteredAction == 'healing potion':
                gm_items.drinkHealingPot(gameState)
                turn = 'enemy'
                continue
            else:
                print(enteredAction + ', not valid command.')

            # Checking result after doing hit command
            if hitResult == 'Hit':
                # If the player get a hit, it goes through normal hit handling.
                if 'power attack' in player.abilityActive or 'shield bash' in player.abilityActive:
                    hitpen = 2
                    print('# You rolled %s + %s (hit modifier) = %s. * %s *' % (hitRoll, player.attributes.pl_hitmod - hitpen, hitRoll + player.attributes.pl_hitmod - hitpen, hitResult))     
                else:    
                    print('# You rolled %s + %s (hit modifier) = %s. * %s *' % (hitRoll, player.attributes.pl_hitmod, hitRoll + player.attributes.pl_hitmod, hitResult))
                damageHandling(gameState, damageRoll(), player.isENEMY)
                turn = 'enemy'
                continue
            elif hitResult == 'Miss' and 'parry' in currentEnemy.enemy_abilityActive:
                # If player misses when enemy is in parry mode
                print('# You rolled %s + %s (hit modifier) = %s. * Parry *' % (hitRoll, player.attributes.pl_hitmod, hitRoll + player.attributes.pl_hitmod))
                counterattack(gameState, currentEnemy.isEnemy)
                turn = 'enemy'    
                continue
            else: # If player misses, it's the enemy's turn
                print('# You rolled %s + %s (hit modifier) = %s. * %s *' % (hitRoll, player.attributes.pl_hitmod, hitRoll + player.attributes.pl_hitmod, hitResult))
                turn = 'enemy'    
                continue

        elif turn == 'enemy':
            #
            # Enemy's turn to act in combat #
            #
            try:
                input('\n# %s\'s turn. Press enter to continue...\n' % (currentEnemy.enemy_name.title()))
            except EOFError:
                continue
            if len(currentEnemy.enemy_abilityActive) > 0: 
                currentEnemy.enemy_abilityActive = [] # Remove all active abilities so that it does not carry over to the current round.

            if 'shield bash' in gameState.enemy[gameState.enemyIndex].enemy_statusEffects:
                # If enemy is affected by shield bash he might loose his round. saving throw.
                if randint(1, 20) < 15:
                    gm_map.printThis('%s got smacked senseless from your shield bash and can\'t perform an action this round.\n' % (currentEnemy.enemy_name.title()))
                    turn = 'player'
                    gameState.enemy[gameState.enemyIndex].enemy_statusEffects.remove('shield bash')
                    continue
                else:
                    gm_map.printThis('%s got smacked good from your shield bash, he shakes his head and roars "DISAPPOINTED!!!"\n' % (currentEnemy.enemy_name.title()))
                    gameState.enemy[gameState.enemyIndex].enemy_statusEffects.remove('shield bash')
                    
            if currentEnemy.enemy_current_hp < (currentEnemy.enemy_maxhp / 2):
                # If the enemy is under half hp, he will have a chance to enter parrymode.
                if randint(0,10) > 4: #  ~60% chance of going into parry mode.
                    currentEnemy.enemy_abilityActive.append('parry')
                    print('%s hunker down into a defensive pose.' % (currentEnemy.enemy_name.title()))
                    turn = 'player'
                    continue
            
            # Roll for hit, and check the result of the hit roll.
            hitRoll = combatRoll(gameState)
            hitResult = hitDecider(gameState, hitRoll, player.attributes.pl_currentArmor, currentEnemy.isEnemy)
            # Own handling if critical hit or miss
            if hitResult == 'CRITICAL':
                critHandling(gameState, currentEnemy.isEnemy)
                turn = 'player'
            elif hitResult == 'Hit':
                print('# %s rolled %s + %s (hit modifier) = %s. * %s *' % (currentEnemy.enemy_name.title(), hitRoll, currentEnemy.enemy_hitmod, hitRoll + currentEnemy.enemy_hitmod, hitResult))
                damageHandling(gameState, damageRoll(), currentEnemy.isEnemy)
                turn = 'player'
            elif hitResult == 'Miss' and 'parry' in player.abilityActive:
                # If enemy misses when player is in parry mode
                print('# %s rolled %s + %s (hit modifier) = %s. * Parry *' % (currentEnemy.enemy_name.title(), hitRoll, currentEnemy.enemy_hitmod, hitRoll + currentEnemy.enemy_hitmod))
                counterattack(gameState, player.isENEMY)
                turn = 'player'
            else: # Also known as 'miss'
                print('# %s rolled %s + %s (hit modifier) = %s. * %s *' % (currentEnemy.enemy_name.title(), hitRoll, currentEnemy.enemy_hitmod, hitRoll + currentEnemy.enemy_hitmod, hitResult))
                turn = 'player'
        if player.dead == True: # If player is dead when enemy turn is finished, exit the loop.
                break