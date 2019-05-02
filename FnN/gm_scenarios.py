


# Scenario file. Contains map data. Thought is that you can generate a new map/scenario after completing first scenario based on data in this file. 

# Scenario 1 / starting scenario

### Flavor text based on terrain location, e.g Forest, Lake, Beach, etc.

# Forest data
forest = {
    "intro": ['\nYou wake up lying on the ground, you are confused and wondering where you are, around you are a lush forest.\nBirds are chirping, and the noonday sun shines above you.\n'],
    "description": ['Forest Description 1\n', 'Forest Description 2\n', 'Forest Description 3\n'],
    "examination": ['Forest Examination 1\n', 'Forest Examination 2\n', 'Forest Examination 3\n'],
    "failedexamine": ['nothing found\n', 'lardy dardy no stuff\n', 'på den på den\n'],
    "alreadyexamined": ['You have already examined this location. You look around, but there\'s nothing of interest.\n'],
    "notexaminable": ['You take a quick sweep over the area and decide that there\'s not much to find here.\n'],
}

# example lake
lake = {
    "Description": ['Description 1', 'Description 2', 'Description 3'],
    "Examination": ['Examination 1', 'Examination 2', 'Examination 3']
}

from random import randint
#print(forest["Description"][randint(0, len(forest["Description"]))])