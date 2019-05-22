


# Scenario file. Contains map data. Thought is that you can generate a new map/scenario after completing first scenario based on data in this file. 

#
# Scenario 1. Forest data
#
forest = {
    "intro": '\nYou wake up lying on the ground, you are confused and wondering where you are, around you are a lush forest.\nBirds are chirping, and the noonday sun shines above you.\n',

    "description": [
    'You come through to a clearing in the forest, there\'s traces of a firepit next to some rocks. From the looks of it, someone camped here perhaps a week ago.\n',
    'Cursing after getting stung by a thorn bush, you turn back to the direction you were traveling in and see what you have already been seeing for a while... Trees.\n',
    'You come out from the trees and see a small stream of water. The sun has just moved behind some clouds, you\'re wondering if you should take a break.\n',
    'The terrain is going uphill, you hear a stream somewhere, you aren\'t sure of the direction cause you can\'t see the sun.\n',
    'Just as you climb over a fallen tree, you see a fox that rushes away from you.\n',
    'You almost fall when you hear what you might think is a scream, it sounded like it was wery far away.\n',
    'It\'s getting darker as you get further and further into the forest, you are thinking about HEY! What was that!?! oh.... a dead mouse...\n',
    'You reach a high stone ridge. You can not climb up. You think that you might have to go around it.\n',
    'As you walk down a path you are wondering about why people don\'t spikk as much as they used to.\n',
    'Thousands of vendings kvern around in your head as you wander further into the forest.\n',
    'Tired, you wander along the path in front of you, if you only had some juløl.\n',
    'Humming to the song "knuckle pokel man" you gaze further into the deep forest. You can only hear some rustling in the bushes nearby\n',
    ],

    "startlocationagain": ['After a while of struggling through a shrubbery you finally get into a clearing in the forest, you look around and find out that this is the place that you woke up earlier.\nYou immidiately find out that you have to move on.\n'],
    
    "examination": [
    'You find a tree with a hole in it, you put your hand inside.... Hey, what\'s this? \n', 
    'You almost fall over a treestump, after regaining your balance you see something shining on the ground.\n', 
    'You look around the nearby bushes, you look in a birds nest...\n',
    'You search through the rubble and...\n'
    ],
    
    "failedexamine": [
    'You look around the nearby bushes and realise that there\'s nothing here.\n',
    'The area does not seem to contain anything of interest.\n',
    'You find nothing.\n'
    ],
    
    "alreadyexamined": ['You have already examined this location. You look around, but there\'s nothing of interest.\n'],
    
    "notexaminable": ['You take a quick sweep over the area and decide that there\'s not much to find here.\n'],
    
    "storylocation": [
    "You traverse through some bushes and come out into a clearing. In front of you stand a Nissemann, he tells you that 'it's hard to be a nissemann'.\nHe asks you if you can find his friends 'Frits' and 'Gunther'.\nHe doesn't know where to find them, so you decide to just continue on your journey.\n",
    "You hear some screaming close by, after you pass some rocks you see a Nisse who\'s lying on the ground. He seems badly injured. You ask him if he\'s feeling under the weather.\nThe response you get is 'that is a good vending, maybe we should use that in another episode', so you guess he\'s not as badly hurt as you first thought.\nAfter talking for a while you hear from him that his friend Gunther is missing, and that he might have been taken by one of the nasty Nåså\'s.\nYou tell him where you found his friend Hansi, and tell him to wait for you there.\n",
    "When you come through a clearing in the forest you see a Nisse who\'s tied up against a tree. He looks pretty beaten up. \nYou ask him if he\'s alright. After muttering for a bit, he manages to inform you that he\'s a 'spikker' so he\'s more than alright. \nJust as you finish untying him, you realize that you are not alone...\n"   
    ],
    "ending": '\nWhen the fight ends, you take Gunther and help him back to his friends. In the evening you drink beer and dance støveldæns.\n',
    "specialitem" : {'type':'sword', 'hitbonus':2, 'dmgbonus': 1, 'ability': 'powerattack'},
    "maxStorylocIndex": 1,
}
#
# Scenario 2. town
#

town = {
    "intro": 'Intro Town: You wake up with a thundering headache. The nisse\'s are no where to be seen.\nWhile sorting out your business you realize that you are in the edge of the forest, which is scarser here.\nYou can see rooftops in the distance to the south east...\n',
    "description": [
        [
            '00: You are in the edge of the forest, you see that the trees are more scarse here than in the thick forest you were in earlier.\nTo the south east you can see rooftops of the nearby village.\n',
            '01: You are between the forest and the edge of the village on a small meadow. close by you can see a building, you are guessing it might be the village stable.\n',
            '02: You are on a road that leads to the village to the south, there are a few buildings nearby.\n',
            '03: You are in a light forested area north east of the village. A man who\'s chopping some firewood looks suspiciously at you..\n',
            '04: Around you are a few trees and a small stream. To the south there\'s a bridge, and beyond that some fields.\nYou see the rooftops of the village to the south west.\n',
        ],
        [
            '05: You are in the edge of the forest, you see that the trees are more scarse here than in the thick forest you were in earlier.\nTo the east you can see rooftops of the nearby village.\n',
            '06: You walk along a small road that opens up to the village to the east. There are a few houses here. The villagers does not look that friendly. They might be suspicious of outsiders.\n ',
            '07: You are in the middle of the northern part of the village, there are several buildings, they look partially abandoned.\nThere are still people walking around though. To the south there\'s a ridge leading down to the southern part of the village\n',
            '08: You enter the north eastern part of the village. There are a few buildings there, including a sawmill.\nFurther out there\'s a patch of grass leading into the north eastern forest.\n',
            '09: You are on the road leading into the village to the west. To the south there are a few fields.\nThere\'s a stream to the east flowing from north to south\n',
        ],
        [
            '10: You are on the western edge of the forest. You see the village to the east. Nearby is a cottage with a small pig pen, it looks abandoned\n',
            '11: You are at the edge of the southern part of the village. There\'s a ridge to the north, leading up to the northern part of the village.\nTo the south you see a barn, with fields nearby.\n',
            '12: You arrive at the southern part of the village, theres several buildings that look mostly abandoned.\nThere are some villagers eyeing you up and down.\n',
            '13: You are at the western edge of the southern part of the village. There\'s a stable here, with a fenced pen for the horses. There are also a field nearby\n',
            '14: You are standing in some fields by a stream that\'s going south, to the south you see a bridge going over the stream\n',
        ],
        [
            '15: You come to an open area with a road leading east to the village.\nTheres a fenced area here, it seems like it\'s been used for cattle, but now it looks in a state of disrepair\n',
            '16: You\'re standing by a barn next to some fields. The fields look like they\'ve had better days.\n To the south there are more fields. You see the village to the east.\n',
            '17: You are in the southern part of the village, there\'s a bit fewer buildings here. To the south you see some fields.\n',
            '18: You\'re standing in a field. There are several fields around you, with some buildings to the north',
            '19: test',
        ],
        [
            '20: test',
            '06: test',
            '07: test',
            '08: test',
            '24: test',
        ],
    ],
    
    "startlocationagain":'',
    "examination": ['Examination 1', 'Examination 2', 'Examination 3'],
    "failedexamine": [
    'You look around the nearby bushes and realise that there\'s nothing here.\n',
    'The area does not seem to contain anything of interest.\n',
    'You find nothing.\n'
    ],
    "notexaminable": ['You take a quick sweep over the area and decide that there\'s not much to find here.\n'],
    "alreadyexamined": ['You have already examined this location. You look around, but there\'s nothing of interest.\n'],
    "storylocation": ['storylocation 1', 'storylocation 2', 'storylocation 3', 'Storylocation 4'],
    "ending": '',
    "maxStorylocIndex": 3,
    "startinglocation": [0, 0],
    "storylocations": [[0,1],[0,2],[0,3], [0,4]],
}

itemsAndAbilities = {
    "rest": '* Rest *: Player rests and restores his hp. Can only be used while traveling.',
    "examine": '* Examine *: Attempt to search for items in the location you are in. There\'s a random chance to find items.\nNot all locations are examinable.',
    "hit": '* Hit *: Player tries to hit the enemy, hit is modified by player strenght and weapon bonus.\nIf hit roll + bonus(es) is equal to enemy armor, you score a hit.\n',
    "parry": '* Parry * : Player enter parry mode. In this mode you skip your attack, but get more armor value until the next round.\nIf enemy misses his hit when you are in parry mode, you can counterattack. Counterattack is not modified by hit bonuses, and can not crit.\n',
    "healing potion": '* Healing potion *: Heals the player for x hp. You can only use this item while in combat.\nYou spend your round using a healing potion.',
    "powerattack": '* Power attack *: Attempt to strike the enemy. You get a slight reduction to your hit bonus, but you get +2 dmg if you hit.'

}

SCENARIOS = [forest, town] # List of scenario dictionaries. used for initializing scenarios. New scenarios should be added to this list. 

VICTORY = '''
   :::     ::: ::::::::::: :::::::: ::::::::::: ::::::::  :::::::::  :::   :::  ::: 
  :+:     :+:     :+:    :+:    :+:    :+:    :+:    :+: :+:    :+: :+:   :+:  :+:  
 +:+     +:+     +:+    +:+           +:+    +:+    +:+ +:+    +:+  +:+ +:+   +:+   
+#+     +:+     +#+    +#+           +#+    +#+    +:+ +#++:++#:    +#++:    +#+    
+#+   +#+      +#+    +#+           +#+    +#+    +#+ +#+    +#+    +#+     +#+     
#+#+#+#       #+#    #+#    #+#    #+#    #+#    #+# #+#    #+#    #+#             
 ###     ########### ########     ###     ########  ###    ###    ###     ###       '''

ENDING_MSG = 'You have completed the initial story, feel free to roam around.'


def gameOver():
    # Print game over text and ask if player want to start a new game.
    print('''
                       ::::::::      :::       :::   :::   ::::::::::          ::::::::  :::     ::: :::::::::: :::::::::   ::: 
                     :+:    :+:   :+: :+:    :+:+: :+:+:  :+:                :+:    :+: :+:     :+: :+:        :+:    :+:  :+:  
                    +:+         +:+   +:+  +:+ +:+:+ +:+ +:+                +:+    +:+ +:+     +:+ +:+        +:+    +:+  +:+   
                   :#:        +#++:++#++: +#+  +:+  +#+ +#++:++#           +#+    +:+ +#+     +:+ +#++:++#   +#++:++#:   +#+    
                  +#+   +#+# +#+     +#+ +#+       +#+ +#+                +#+    +#+  +#+   +#+  +#+        +#+    +#+  +#+     
                 #+#    #+# #+#     #+# #+#       #+# #+#                #+#    #+#   #+#+#+#   #+#        #+#    #+#          
                 ########  ###     ### ###       ### ##########          ########      ###     ########## ###    ###  ###       ''')
    import time
    time.sleep(2)
    print()
    print('Do you want to play again? (yes or no)')
    if not input().lower().startswith('y'):
        import sys
        sys.exit()
    else:
        import os
        import gm_charstats
        os.system('cls')
        gm_charstats.main()