


# Scenario file. Contains map data. Thought is that you can generate a new map/scenario after completing first scenario based on data in this file. 

# Scenario 1 / starting scenario

### Flavor text based on terrain location, e.g Forest, Lake, Beach, etc.

# Forest data
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
    'As you walk down a path you are wondering about why people don\'t spikk as much as they used to.\n'
    ],
    
    "examination": [
    'You find a tree with a hole in it, you put your hand inside.... Hey, what\'s this? \n', 
    'You almost fall over a treestump, after regaining your balance you see something shining on the ground.\n', 
    'You look around the nearby bushes, you look in a birds nest...\n'
    ],
    
    "failedexamine": [
    'You look around the nearby bushes and realise that there\'s nothing here.\n',
    'The area does not seem to contain anything of interest.\n',
    'You find nothing.\n'
    ],
    
    "alreadyexamined": ['You have already examined this location. You look around, but there\'s nothing of interest.\n'],
    
    "notexaminable": ['You take a quick sweep over the area and decide that there\'s not much to find here.\n'],
    
    "storylocation": [
    "You traverse through some bushes and come out into a clearing. In front of you stand a Nissemann, he tells you that 'it's hard to be a nissemann'.\nHe asks you if you can find his friends 'Frits' and 'Gunther'.\nHe doesn't know where to find them, so you just have to start somewhere.\n",
    "You hear some screaming close by, after you pass some rocks you see a Nisse who\'s lying on the ground. He is badly injured. You ask him if he\'s feeling under the weather.\nThe response you get is 'that is a good vending, maybe we should use that in another episode', so you guess he\'s not as badly hurt as you first thought.\nAfter talking for a while you hear from him that his friend Gunther is missing, and that he might have been taken by one of the nasty Nåså\'s.\nYou tell him where you found his friend Hansi, and tell him to wait for you there.\n",
    "When you come through a clearing in the forest you see a Nisse who\'s tied up against a tree. He looks pretty beaten up. \nYou ask him if he\'s alright. After muttering for a bit, he manages to inform you that he\'s a 'spikker' so he\'s more than alright. \nJust as you finish untying him, you realize that you are not alone...\n"   
    ],
    "Ending": 'When the fight ends, you take Gunther and help him back to his friends. In the evening you drink beer and dance støveldæns.'
}

# example lake
lake = {
    "Description": ['Description 1', 'Description 2', 'Description 3'],
    "Examination": ['Examination 1', 'Examination 2', 'Examination 3']
}

from random import randint
#print(forest["Description"][randint(0, len(forest["Description"]))])





