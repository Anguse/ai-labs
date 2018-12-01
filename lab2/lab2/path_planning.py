import random
import numpy as np
import matplotlib.pyplot as plt


sizeOfMap2D = [100, 50]
percentOfObstacle = 0.9  # 30% - 60%, random

# Generate 2d grid map of size x * y
# starting Point and Ending Point
def generateMap2d(size_):
    # Generates a random 2d map of size size_. You can choose your desired size but whatever solution you come up with has
    # to work independently of map size
    size_x, size_y = size_[0], size_[1]

    map2d = np.random.rand(size_y, size_x)
    perObstacles_ = percentOfObstacle
    map2d[map2d <= perObstacles_] = 0
    map2d[map2d > perObstacles_] = -1

    yloc, xloc = [np.random.random_integers(0, size_x-1, 2), np.random.random_integers(0, size_y-1, 2)]
    while (yloc[0] == yloc[1]) and (xloc[0] == xloc[1]):
        yloc, xloc = [np.random.random_integers(0, size_x-1,2), np.random.random_integers(0, size_y-1, 2)]

    map2d[xloc[0]][yloc[0]] = -2
    map2d[xloc[1]][yloc[1]] = -3

    return map2d


# Generate 2d grid map with rotated-H-shape object
def generateMap2d_obstacle(size_):
    # Generates a special map with the middle blocked and passing from left to right being possible at the top or bottom
    # part of the map. If for some reason the map fails to generate like that rerun it as it is not foolproof
    size_x, size_y = size_[0], size_[1]
    map2d = generateMap2d(size_)

    map2d[map2d==-2] = 0
    map2d[map2d==-3] = 0

    # add special obstacle
    xtop = [np.random.random_integers(5, 3*size_x//10-2), np.random.random_integers(7*size_x//10+3, size_x-5)]
    ytop = np.random.random_integers(7*size_y//10 + 3, size_y - 5)
    xbot = np.random.random_integers(3, 3*size_x//10-5), np.random.random_integers(7*size_x//10+3, size_x-5)
    ybot = np.random.random_integers(5, size_y//5 - 3)


    map2d[ybot, xbot[0]:xbot[1]+1] = -1
    map2d[ytop, xtop[0]:xtop[1]+1] = -1
    minx = (xbot[0]+xbot[1])//2
    maxx = (xtop[0]+xtop[1])//2
    if minx > maxx:
        tempx = minx
        minx = maxx
        maxx = tempx
    if maxx == minx:
        maxx = maxx+1

    map2d[ybot:ytop, minx:maxx] = -1
    startp = [np.random.random_integers(0, size_x//2 - 4), np.random.random_integers(ybot+1, ytop-1)]

    map2d[startp[1], startp[0]] = -2
    goalp = [np.random.random_integers(size_x//2 + 4, size_x - 3), np.random.random_integers(ybot+1, ytop-1)]

    map2d[goalp[1],goalp[0]] = -3
    #return map2d, [startp[1], startp[0]], [goalp[1], goalp[0]], [ytop, ybot]
    return map2d, [ytop, ybot, minx]

def getHeuristic(map2d_):
    goal_ = np.where(map == -3)
    size_x = map2d_.shape[0]
    size_y = map2d_.shape[1]
    goal_x = goal_[0]
    goal_y = goal_[1]

    for x in range(size_x):
        for y in range(size_y):
            if map2d_[x][y] == 0:
                map2d_[x][y] = abs(goal_x - x) + abs(goal_y - y)

    return map2d_

def plotMap(map2d_, path_, title_ =''):
    # Plots a map as described in lab2 description containing integer numbers. Each number has a specific meaning. You can check
    # the example provided at the end of the file for more information

    import matplotlib.cm as cm
    plt.interactive(False)

    greennumber = map2d_.max()
    #greennumber = len(np.unique(map2d_))
    #print(greennumber)
    colors = cm.winter(np.linspace(0, 1, greennumber))

    colorsMap2d = [[[] for x in xrange(map2d_.shape[1])] for y in range(map2d_.shape[0])]
    # Assign RGB Val for starting point and ending point
    locStart, locEnd = np.where(map2d_ == -2), np.where(map2d_ == -3)

    colorsMap2d[int(locStart[0])][int(locStart[1])] = [.0, .0, .0, 1.0]  # black
    colorsMap2d[int(locEnd[0])][int(locEnd[1])] = [.0, .0, .0, .0]  # white

    # Assign RGB Val for obstacle
    locObstacle = np.where(map2d_ == -1)
    for iposObstacle in range(len(locObstacle[0])):
        colorsMap2d[locObstacle[0][iposObstacle]][locObstacle[1][iposObstacle]] = [1.0, .0, .0, 1.0]
    # Assign 0
    locZero = np.where(map2d_ == 0)

    for iposZero in range(len(locZero[0])):
        colorsMap2d[locZero[0][iposZero]][locZero[1][iposZero]] = [1.0, 1.0, 1.0, 1.0]

    # Assign Expanded nodes
    locExpand = np.where(map2d_>0)

    for iposExpand in range(len(locExpand[0])):
        colorsMap2d[locExpand[0][iposExpand]][locExpand[1][iposExpand]] = colors[map2d_[locExpand[0][iposExpand]][locExpand[1][iposExpand]]-1]

    for irow in range(len(colorsMap2d)):
        for icol in range(len(colorsMap2d[irow])):
            if colorsMap2d[irow][icol] == []:
                colorsMap2d[irow][icol] = [1.0, 0.0, 0.0, 1.0]

    plt.figure()
    plt.title(title_)
    plt.imshow(colorsMap2d, interpolation='nearest')
    plt.colorbar()
    plt.plot(path_[:][0],path_[:][1], color='magenta',linewidth=2.5)
    plt.ylim(0,map2d_.shape[0])
    plt.xlim(0,map2d_.shape[1])
    plt.draw()
    #plt.savefig()
    plt.show()

## Example
## Map description
##   0 - Free cell
##   -1 - Obstacle
##   -2 - Start point
##   -3 - Goal point
##
#map = generateMap2d([60,60])
#map_h_object, info = generateMap2d_obstacle([60, 60])
#plotMap(map, "Path", "Title")

#plt.clf()
#plt.imshow(map_h_object)
#plt.show()


## Solve using your implemented A* algorithm
## solved_map description
##   0 - unexpanded cell
##   -1 - obstacle
##   -2 - start point
##   -3 - goal point
##   positive_number - one of the values described in lab2 description (heuristic cost, travel cost, cell total cost,...)
## plotMap(solved_tmap,solved_path)
