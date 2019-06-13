# Scenario file. Contains map data. Thought is that you can generate a new map/scenario after completing first scenario based on data in this file. 

#
# Scenario 1. Forest data
#
forest = {
    "intro": '\nYou wake up lying on the ground, you are confused and wondering where you are, around you are a lush forest.\nBirds are chirping, and the noonday sun shines above you.\n',

    "description": [
    [
    'You come through to a clearing in the forest, there\'s traces of a firepit next to some rocks. From the looks of it, someone camped here perhaps a week ago.\n',
    'Cursing after getting stung by a thorn bush, you turn back to the direction you were traveling in and see what you have already been seeing for a while... Trees.\n',
    'You come out from the trees and see a small stream of water. The sun has just moved behind some clouds, you\'re wondering if you should take a break.\n',
    'The terrain is going uphill, you hear a stream somewhere, you aren\'t sure of the direction cause you can\'t see the sun.\n',
    'Just as you climb over a fallen tree, you see a fox that rushes away from you.\n',
    ],
    [
    'You almost fall when you hear what you might think is a scream, it sounded like it was wery far away.\n',
    'It\'s getting darker as you get further and further into the forest, you are thinking about HEY! What was that!?! oh.... a dead mouse...\n',
    'You reach a high stone ridge. You can not climb up. You think that you might have to go around it.\n',
    'As you walk down a path you are wondering about why people don\'t spikk as much as they used to.\n',
    'Thousands of vendings kvern around in your head as you wander further into the forest.\n',
    ],
    [
    'Tired, you wander along the path in front of you, if you only had some juløl.\n',
    'Humming to the song "knuckle pokel man" you gaze further into the deep forest. You can only hear some rustling in the bushes nearby\n',
    'There\'s many problems in this world, and to you it seems that trees ain\'t one of them, or is it?\n', 
    'You wander further into the forest, thinking about what good old gammel nok told you in your younger days.\nFor example he said if you sleep in telt, make sure that it is raintett.\n',
    'The forest clears up in sort of a circle, looks like someone have cleared this area and put up a sick rock in the middle.\n',
    ],
    [
    'You get distracted by a squirrel that is seemingly trying to eat a rock. Strange...\n',
    'Haven\'t you been here before? Everything looks the same in the forest.\n',
    'What was that? A strange noise startles you. But it turns out that it\'s just the branch you just stepped on.\n',
    'You are already tired of this forest, you start to daydream about spikking a large propel for a flying machine.\n',
    'Man, if you only had a spilldåse, then you would not need to be so bored of walking on into this dark and god forsaken forest.\n',
    ],
    [
    'Your back is killing you, you think you might need a chiropractor chair.\n',
    'You pass a stream, you see a dead rabbit in it. No water for you it seems.\n',
    'Gosh darn, you just missed a rabbit that you could have had for dinner.\n',
    'Don\'t forget, The one who first comes to the mill, is him who first gets painted.\n',
    'You tear your shirt on a branch.\nThat\'s it simpelthen overhead not nå to do with\n',
    ]
    ],

    "startlocationagain": ['After a while of struggling through a shrubbery you finally get into a clearing in the forest, you look around and find out that this is the place that you woke up earlier.\nYou immidiately find out that you have to move on.\n'],
    
    "examination": [
    'You find a tree with a hole in it, you put your hand inside.... Hey, what\'s this? \n', 
    'You almost fall over a tree stump, after regaining your balance you see something shining on the ground.\n', 
    'You look around the nearby bushes, you look in a birds nest...\n',
    'You search through the rubble and...\n',
    'Hey, this was lying right in front of you the whole time.\n',
    ],
    
    "failedexamine": [
    'You look around the nearby bushes and realise that there\'s nothing here.\n',
    'The area does not seem to contain anything of interest.\n',
    'You find nothing.\n',
    'You rummage through an rock outcropping. Finding nothing but a rock\n',
    ],
    
    "alreadyexamined": ['You have already examined this location. You look around, but there\'s nothing of interest.\n'],
    
    "notexaminable": ['You take a quick sweep over the area and decide that there\'s not much to find here.\n'],
    
    "storylocation": [
    "You traverse through some bushes and come out into a clearing. In front of you stands a Nissemann, he tells you that 'it's hard to be a nissemann'.\nHe asks you if you can find his friends 'Frits' and 'Gunther'.\nHe doesn't know where to find them, so you decide to just continue on your journey.\n",
    "You hear some screaming close by, after you pass some rocks you see a Nisse who\'s lying on the ground. He seems badly injured. You ask him if he\'s feeling under the weather.\nThe response you get is 'that is a good vending, maybe we should use that in another episode', so you guess he\'s not as badly hurt as you first thought.\nAfter talking for a while you hear from him that his friend Gunther is missing, and that he might have been taken by one of the nasty Nåså\'s.\nYou tell him where you found his friend Hansi, and tell him to wait for you there.\n",
    "When you come through a clearing in the forest you see a Nisse who\'s tied up against a tree. He looks pretty beaten up. \nYou ask him if he\'s alright. After muttering for a bit, he manages to inform you that he\'s a 'spikker' so he\'s more than alright. \nJust as you finish untying him, you realize that you are not alone...\n"   
    ],
    "ending": '\nWhen the fight ends, you take Gunther and help him back to his friends. In the evening you drink juløl and dance støveldæns.\n',
    "maxStorylocIndex": 2,
}


#
# Scenario 2. town
#

town = {
    "intro": 'You wake up with a thundering headache. The nisse\'s are nowhere to be seen.\nWhile sorting out your business you realize that you are in the edge of the forest, which is scarser here.\nYou can see rooftops in the distance to the south east...\n',
    "description": [
        [
            'You are in the edge of the forest, you see that the trees are more scarse here than in the thick forest you were in earlier.\nTo the south east you can see rooftops of the nearby village.\n',
            'You are between the forest and the edge of the village on a small meadow. close by you can see a building, you are guessing it might be the village stable.\n',
            'You are on a road that leads to the village to the south, there are a few buildings nearby.\n',
            'You are in a light forested area north east of the village. A man who\'s chopping some firewood looks suspiciously at you..\n',
            'Around you are a few trees and a small stream. To the south there\'s a bridge, and beyond that some fields.\nYou see the rooftops of the village to the south west.\n',
        ],
        [
            'You are in the edge of the forest, you see that the trees are more scarse here than in the thick forest you were in earlier.\nTo the east you can see rooftops of the nearby village.\n',
            'You walk along a small road that opens up to the village to the east. There are a few houses here. The villagers does not look that friendly. They might be suspicious of outsiders.\n ',
            'You are in the middle of the northern part of the village, there are several buildings, they look partially abandoned.\nThere are still people walking around though. To the south there\'s a ridge leading down to the southern part of the village\n',
            'You enter the north eastern part of the village. There are a few buildings there, including a sawmill.\nFurther out there\'s a patch of grass leading into the north eastern forest.\n',
            'You are on the road leading into the village to the west. To the south there are a few fields.\nThere\'s a stream to the east flowing from north to south\n',
        ],
        [
            'You are on the western edge of the forest. You see the village to the east. Nearby is a cottage with a small pig pen, it looks abandoned\n',
            'You are at the edge of the southern part of the village. There\'s a ridge to the north, leading up to the northern part of the village.\nTo the south you see a barn, with fields nearby.\n',
            'You arrive at the southern part of the village, theres several buildings that look mostly abandoned.\nThere are some villagers eyeing you up and down.\n',
            'You are at the western edge of the southern part of the village. There\'s a stable here, with a fenced pen for the horses. There are also a field nearby\n',
            'You are standing in some fields by a stream that\'s going south, to the south you see a bridge going over the stream\n',
        ],
        [
            'You come to an open area with a road leading east to the village.\nTheres a fenced area here, it seems like it\'s been used for cattle, but now it looks in a state of disrepair.\n',
            'You\'re standing by a barn next to some fields. The fields look like they\'ve had better days.\nTo the south there are more fields. You see the village to the east.\n',
            'You are in the southern part of the village, there\'s a bit fewer buildings here. To the south you see some fields.\n',
            'You\'re standing in a field. There are several fields around you, with some buildings to the north\n',
            'You are standing on a small road leading into a deep forest. There\'s a stream between you and the village to the north west.\n',
        ],
        [
            'You are in the forest south west of the village that you saw earlier. For some reason there\'s squirrels everywhere.\n',
            'You are standing in a cornfield, it doesn\'t look well maintained. To the far north by north east you can see the village.\nNear you there are even more fields.\n',
            'You\'re standing in a field. There are several fields around you. To the east you can see what only can be the village cemetery. You aren\'t too keen on going over there\n.',
            'You are standing by the stream that runs east of the village.\nThe water looks dirty, probably because of the rain. Near you there are (more) fields.',
            'You are in the forest south west of the village that you saw earlier.\nThere are some not so happy noises coming from deep within the forest.\n',
        ],
    ],
    
    "startlocationagain":'You end up where you woke up this morning, your head is still banging...\n',
    "examination": [
    'You search around some junk on the ground and\n',
    'To your surprise you stumble over something.\n',
    'You see something glinting on the ground.\n',
    ],
    "failedexamine": [
    'You look around your near vicinity and realise that there\'s nothing here.\n',
    'The area does not seem to contain anything of interest.\n',
    'You find nothing.\n'
    ],
    "notexaminable": ['You take a quick sweep over the area and decide that there\'s not much to find here.\n'],
    "alreadyexamined": ['You have already examined this location. You look around, but there\'s nothing of interest.\n'],
    "storylocation": [
    'When you arrive at the edge of the village. You meet a nisse who looks very tired.\nAfter talking for a while you find out that they are having trouble with someone abducting their fjøsnisser.\nYou should investigate.\n',
    'You meet a nissemor with teary eyes, she\'s sad cause her fjøsnisse dissappeared the other day.\nShe also told you that when she went by the cemetary she think that she saw someone suspicious.\n', 
    'Upon arriving at the cemetary you see someone run away, he ran north east!\n',
    'Finally, just by the bridge leading out to the eastern area you catch him, he turn\'s around and...\n'],
    
    "ending": 'After kicking the ass of the supposed abductor. You go to the closest thing that can be called a tavern. Then you enjoy many juløl...\n',
    "maxStorylocIndex": 3,
    "startinglocation": [0, 0],
    "storylocations": [[1, 1],[3, 1],[2, 4], [4, 1]],
}

hills = {

}

#
# Helptext for items and abilities
#

itemsAndAbilities = {
    "rest": '* Rest * Player rests and restores his hp. Can only be used while traveling.\n',
    "examine": '* Examine * Attempt to search for items in the location you are in. There\'s a random chance to find items.\n  Not all locations are examinable.\n',
    "hit": '* Hit * Player tries to hit the enemy, hit is modified by player strenght, level, and weapon bonus.\n  If hit roll + bonus(es) are equal to enemy armor, you score a hit.\n',
    "parry": '* Parry * Player enter parry mode. In this mode you skip your attack, but get more armor value until the next round.\n  If enemy misses his hit when you are in parry mode, you can counterattack. Counterattack is not modified by hit bonuses.\n  Can not crit.\n',
    "healing potion": '* Healing potion * Heals the player for x hp. You can only use this item while in combat.\n  You spend your round using a healing potion.\n',
    "power attack": '* Power attack * Attempt to strike the enemy. You get a slight reduction to your hit bonus, but you get +2 dmg if you hit.\n',
    "sword": '* Sword * Adds +2 to hit rolls, and +1 to damage rolls. Also can give access to "power attack" ability.\n',
    "shield": '* Shield * Adds +1 to armor. Can also give access to "shield bash" ability.\n',
    "chainmail": '* Chainmail * Adds +2 to armor.\n',
    "helmet": '* Helmet * Adds +1 to armor.\n',
    "shield bash": '* Shield bash * Attempt to hit the enemy with your shield, hit and dmg are reduced by 2.\n  If Shield bash hits, there\'s a chance that the enemy will loose his round.\n',
}

# List of scenarios
SCENARIOS = [forest, town] # List of scenario dictionaries. used for initializing scenarios. New scenarios should be added to this list. 


#
# Combat flavor text strings
#
COMBAT_FLAVOR = {
    "combatintrostart": [
    'A raving madman who calls himself ',
    'Some dude named ',
    'As you were just minding your own business, ',
    'Oh snap! Shit has just hit the fan! ',
    '"Bob, bob, bob, ikke sant", you hear someone say behind you. You turn around and ',
    'Before you know it ',
    'Suddenly you notice that it get\'s really cold, you see that the puddle of water in front of you\nfreezes solid.' ,
    'You suddenly hear.... Is that "Eye of the tiger"..? Before you fathom what song it is ',
    'You suddenly hear.... Is that "Killing in the name"..? Before you fathom what song it is ',
    'You suddenly hear.... Is that "Møkkamann"..? Before you fathom what song it is ',
    ],
    "combatintroending": [
    ' lunges at you. He looks like he wants to introduce you to a can of whoop-ass! ',
    ' shows up and seems eager to wear you like a hat! ',
    ' sneaks up on you. He raises his hand in the air... ',
    ' tells you to respect his authority! ',
    ' slaps you around with a trout! ',
    ' starts ranting about irregularities in the pension fund.',
    ' stops you and start to explain why we need to increase the number of bomstasjoner in Oslo.',
    ' stops you, and then start\'s giving you a karaoke session of a life time.', 
    ' pats you on the back, raises a book up to your face and ask you if you have heard the good word of "Jehova".'
    ],   
    "combatwonstart": ['You whooped'],
    "combatwonending": ['ass, real goood.'],
}   


VICTORY = '''\n
   :::     ::: ::::::::::: :::::::: ::::::::::: ::::::::  :::::::::  :::   :::  ::: 
  :+:     :+:     :+:    :+:    :+:    :+:    :+:    :+: :+:    :+: :+:   :+:  :+:  
 +:+     +:+     +:+    +:+           +:+    +:+    +:+ +:+    +:+  +:+ +:+   +:+   
+#+     +:+     +#+    +#+           +#+    +#+    +:+ +#++:++#:    +#++:    +#+    
+#+   +#+      +#+    +#+           +#+    +#+    +#+ +#+    +#+    +#+     +#+     
#+#+#+#       #+#    #+#    #+#    #+#    #+#    #+# #+#    #+#    #+#             
 ###     ########### ########     ###     ########  ###    ###    ###     ###       \n'''

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