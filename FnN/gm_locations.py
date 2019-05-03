import gm_scenarios
import random

class Locationforest():
    # Create an object of every location(coordinate) on the map
    def __init__(self, description):
        self.description = gm_scenarios.forest["description"][random.randint(0, len(gm_scenarios.forest["description"]) -1)] # Flavortext that is printed when entering a new location.
        self.encounterChance = random.randint(0, 9) # chance for encounter when entering the new area.
        self.visited = False # set if the location has been visited before.
        self.examineable = random.choice([True, False]) 
        self.examineChance = random.randint(1, 8) # Chance for successful examination.
        self.examineText = '' # Flavortext when you examine. 
        self.beenExamined = False # If the location has been examined before, it can not be examined again. 
        self.description = description
        self.mapTile = '#'
        self.setExamineText()

    def printstuff(self):
        # Made for testing the constructor, might be removed. 
        print(self.description, self.encounterChance, self.searchPossible)

    def setExamineText(self):
        # set flavortext if the location is examinable. 
        if self.examineable == True:
            self.examineText = gm_scenarios.forest["examination"][random.randint(0, len(gm_scenarios.forest["examination"]) -1)]

def setExamined(location):
    # Set self.examined to True when a player has examined location.
    location.beenExamined = True



'''#testing the constructor
locations = []

for i in range(5):
    templist = []
    for i in range(5):
        description = gm_scenarios.forest["description"][randint(0, len(gm_scenarios.forest["description"]) -1)]
        templist.append(Locationforest(description))
    locations.append(templist)


    
print(locations)


#maploc.printstuff()
'''