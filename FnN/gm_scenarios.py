


# Scenario file. Contains map data. Thought is that you can generate a new map/scenario after completing first scenario based on data in this file. 

# Scenario 1 / starting scenario

### Flavor text based on terrain location, e.g Forest, Lake, Beach, etc.

# Forest data
forest = {
    "intro": ['\nYou wake up lying on the ground, you are confused and wondering where you are, around you are a lush forest.\nBirds are chirping, and the noonday sun shines above you.\n'],
    "description": [
    'You come through to a clearing in the forest, there\'s traces of a firepit next to some rocks. From the looks of it, someone camped here perhaps a week ago.\n',
    'Cursing after getting stung by a thorn bush, you turn back to the direction you were traveling in and see what you have already been seeing for a while... Trees.\n',
    'You come out from the trees and see a small stream of water. The sun has just moved behind some clouds, you\'re wondering if you should take a break.\n',
    'The terrain is going uphill, you hear a stream somewhere, you aren\'t sure of the direction cause you can\'t see the sun.\n',
    'Just as you climb over a fallen tree, you see a fox that rushes away from you.\n',
    'You almost fall when you hear what you might think is a scream, it sounded like it was wery far away.\n',
    'It\'s getting darker as you get further and further into the forest, you are thinking about HEY! What was that!?! oh.... a dead mouse...\n',
    ],
    
    "examination": [
    'You find a tree with a hole in it, you put your hand inside.... Hey, what\'s this? ', 
    'You almost fall over a treestump, after regaining your balance you see something shining on the ground.\n', 
    'You look around the nearby bushes, you look in a birds nest that you find...\n',
    ],
    
    "failedexamine": [
    'You look around the nearby bushes and realise that there\'s nothing here.\n',
    'The area does not seem to contain anything of interest.\n',
    'You find nothing.\n'
    ],
    
    "alreadyexamined": ['You have already examined this location. You look around, but there\'s nothing of interest.\n'],
    
    "notexaminable": ['You take a quick sweep over the area and decide that there\'s not much to find here.\n'],
    
    "storylocation": [''],
}

# example lake
lake = {
    "Description": ['Description 1', 'Description 2', 'Description 3'],
    "Examination": ['Examination 1', 'Examination 2', 'Examination 3']
}

from random import randint
#print(forest["Description"][randint(0, len(forest["Description"]))])





