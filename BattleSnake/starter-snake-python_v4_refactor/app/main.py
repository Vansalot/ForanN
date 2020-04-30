import json, os, random, bottle, math, copy, time

import pathfinder as pf
import classes

from pprint import pprint as pp
from api import ping_response, start_response, move_response, end_response

GAMEBOARD = None
BOARD = []
FOODCOORD = '' # Coordinate set for food when starving. 

@bottle.route('/')
def index():
    return '''
    Battlesnake documentation can be found at
       <a href="https://docs.battlesnake.io">https://docs.battlesnake.io</a>.
    '''

@bottle.route('/static/<path:path>')
def static(path):
    """
    Given a path, return the static file located relative
    to the static folder.

    This can be used to return the snake head URL in an API response.
    """
    return bottle.static_file(path, root='static/')

@bottle.post('/ping')
def ping():
    """
    A keep-alive endpoint used to prevent cloud application platforms,
    such as Heroku, from sleeping the application instance.
    """
    return ping_response()

@bottle.post('/start')
def start():
    data = bottle.request.json
    
    """
    TODO: If you intend to have a stateful snake AI,
            initialize your snake state here using the
            request's data if necessary.
    """
    global GAMEBOARD
    GAMEBOARD = classes.Gameboard(data)

    # Find size of the board and create the board matrix
    boardSize = [data["board"]["height"],data["board"]["width"]]
    



    print(json.dumps(data))
    snakeApperance = {"color": '#00FF00',
             "headType": 'bendr',
             "tailType": 'hook',
             }

    return start_response(snakeApperance)


@bottle.post('/move')
def move():
    global GAMEBOARD
    start_time = time.time()

    data = bottle.request.json

    """
    TODO: Using the data from the endpoint request object, your
            snake AI must choose a direction to move in.
    """

    costMatrix = {
    "ownhead": 0,
	"empty": 1,
	"food": 5,
	"edge": 200,
	"corner": 300,
	"snakeheadclose": 799,
	"snakehead": 9999,
	"snakebody": 9999,
    "snaketail": 699,
    }

    print(json.dumps(data))
    # update the cost of the different nodes on the board
    gridCost = {} # contains the cost value of all the nodes on the board.
    gridCost = pf.updateGridCost(costMatrix, data)

    # set up the matrix of what goes where on the board.
    grid = {}

    # If you have eaten food, clear the foodcoord variable.
    if data["you"]["health"] == 100:
        global FOODCOORD
        FOODCOORD = ''

    boardSize = [data["board"]["height"],data["board"]["width"]]
    ownloc = str(data["you"]["body"][0]["x"]) + ', ' + str(data["you"]["body"][0]["y"])
    
    goal = getGoal(ownloc, data, boardSize, gridCost)

    while True:
        try: 
            targetCord = pf.dijkstra(pf.createGrid(boardSize, gridCost), ownloc, goal, gridCost)
            break
        except:
            if targetCord == None:
                goal = getGoal(ownloc, data, boardSize, gridCost, nextSafeSector=True)
                break

    rsp = move_response(findDir(ownloc, targetCord))

    end_time = time.time()
    delta_time = end_time - start_time
    print('*** Time spent by move():', delta_time)

    
    return rsp

def findDir(ownloc, targetCord):
    1, 0 - 0, 0
    intOwnLoC = intUpStr(ownloc)
    intTargetCord = intUpStr(targetCord)
    direction = ''

    if intOwnLoC[0] < intTargetCord[0]:
        direction = 'right'

    if intOwnLoC[0] > intTargetCord[0]:
        direction = 'left'

    if intOwnLoC[1] < intTargetCord[1]:
        direction = 'down'
    
    if intOwnLoC[1] > intTargetCord[1]:
        direction = 'up'
    
    return direction

def getGoal(ownloc, data, boardSize, gridCost, nextSafeSector=False):
    # to fix: when too big and potentially can not reach the desired location. Find new location. 

    pos = ownloc
    goalPos = ownloc
    safestSectors = pf.getSafeSector(gridCost["sectors"])
    safestSector = safestSectors[0]

    if nextSafeSector == True:
        safestSector = safestSectors[1]

    # If you have low health, get food.
    global FOODCOORD
    if data["you"]["health"] < 30 and FOODCOORD:
        if gridCost[FOODCOORD] == 5:
            goalPos = FOODCOORD
            print('# 3 Hunger!! to reach: ', goalPos)    
            return goalPos
        else:
            pass
    
    if data["you"]["health"] < 30 and not FOODCOORD:
        index = random.randint(1, len(data["board"]["food"]) - 1)
        goalPos = str(data["board"]["food"][index]["x"]) + ', ' + str(data["board"]["food"][index]["y"])
        FOODCOORD = goalPos
        print('# 3 Hunger!! NEW FOOD to reach: ', goalPos)
        return goalPos


    # Select random coord in the safest sector
    while ownloc == goalPos or gridCost[goalPos] > 999:
        safex = random.randint(gridCost["sectors"][safestSector]["coords"][0][0], gridCost["sectors"][safestSector]["coords"][0][1])
        safey = random.randint(gridCost["sectors"][safestSector]["coords"][1][0], gridCost["sectors"][safestSector]["coords"][1][1])
        if safey == 10:
            safey -= 1
        if safex == 10:
            safex -= 1
        goalPos = pf.getBoardLocation(safex, safey)

    print("# Goal is ", goalPos)
    return goalPos

def intUpStr(string):
    '''
    input string coordinates, returns list of the string coords. 
    ex: input '0, 5', output: [0, 5](int)
    '''
    returnList = []

    for x in string.split(', '):
        returnList.append(int(x))
    return returnList

def getListfromlistedDicts(listedDicts):
    # return list of food coordinates from nested dict input
    newList = []
    for dictionary in listedDicts:
        coordinate = [dictionary["x"], dictionary["y"]]
        newList.append(coordinate)
    return newList


@bottle.post('/end')
def end():
    data = bottle.request.json

    """
    TODO: If your snake AI was stateful,
        clean up any stateful objects here.
    """
    #print(json.dumps(data))

    return end_response()

# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug=os.getenv('DEBUG', True)
    )
