import math
import heapq
import random


# Priority Queue based on heapq
class PriorityQueue:
    def __init__(self):
        self.elements = []

    def isEmpty(self):
        return len(self.elements) == 0

    def add(self, item, priority):
        heapq.heappush(self.elements,(priority,item))

    def remove(self):
        return heapq.heappop(self.elements)[1]


def search(map, start, goal, type, heuristic, info):
    frontier = PriorityQueue()
    frontier.add(start, 0)
    size_x = map.shape[1]
    size_y = map.shape[0]

    # Store information about visited cells, add information about obstacles
    closed = [[0 for row in range(size_x)] for col in range(size_y)]
    for x in range(size_x):
        for y in range(size_y):
            if map[y][x] == -1:
                closed[y][x] = -1

    # path taken, it is up to each cell to store this information as parents
    path = []

    # init. starting node
    start.parent = None

    while not frontier.isEmpty():
        current_cell = frontier.remove()

        # check if the goal is reached
        if current_cell == goal:
            while current_cell.parent != None:
                path.append(current_cell)
                current_cell = current_cell.parent
            break

        # for each neighbour of the current cell
        for next in get_neighbors(current_cell, goal, map, closed, type):

            # Update values for cell
            next.g = next.parent.g + 1
            next.h = get_heuristic(start, next, goal, info, heuristic)
            next.f = next.g + next.f
            prio = get_prio(next, goal, type)
            frontier.add(next, prio)

    return path, closed


# Returns a list of neighbors belonging to current_cell
def get_neighbors(current_cell, goal, map, closed, type):
    size_x = map.shape[1] - 1
    size_y = map.shape[0] - 1
    x = int(current_cell.position[1])
    y = int(current_cell.position[0])

    # Mark current cell as visited
    closed[y][x] = 1
    neighbors = []
    if y != 0:
        if closed[y-1][x] == 0:
            cell = Cell((y-1, x))
            cell.parent = current_cell
            neighbors.append(cell)
            closed[y-1][x] = 1
    if y != size_y:
        if closed[y+1][x] == 0:
            cell = Cell((y+1, x))
            cell.parent = current_cell
            neighbors.append(cell)
            closed[y+1][x] = 1
    if x != size_x:
        if closed[y][x+1] == 0:
            cell = Cell((y, x+1))
            cell.parent = current_cell
            neighbors.append(cell)
            closed[y][x+1] = 1
    if x != 0:
        if closed[y][x-1] == 0:
            cell = Cell((y, x-1))
            cell.parent = current_cell
            neighbors.append(cell)
            closed[y][x-1] = 1
    return neighbors


# Returns manhattan distance from start to goal
def manhattan_distance(start, goal):
    manhattan_distance = 2*(abs(int(goal.position[1]) - int(start.position[1])) + abs(int(goal.position[0]) - int(start.position[0])))
    return manhattan_distance


# Returns euclidean distance from start to goal
def euclidean_distance(start, goal):
    x_distance = abs(int(goal.position[1]) - int(start.position[1]))
    y_distance = abs(int(goal.position[0]) - int(start.position[0]))
    distance = math.sqrt(x_distance**2+y_distance**2)
    return distance


# Custom heuristic value based on the knowledge of the map pattern
def get_heuristic(start, next, goal, info, heuristic):
    y_top = info[0]
    y_bot = info[1]
    mid = info[2]
    scalar = 5
    y_cell = int(next.position[0])
    x_cell = int(next.position[1])
    y_start = int(start.position[0])
    if heuristic == "EUCLIDEAN":
        return scalar*euclidean_distance(next, goal)
    elif heuristic == "MANHATTAN":
        return scalar*manhattan_distance(next, goal)
    # Custom heuristic based on knowledge of the map
    elif heuristic == "H-SHAPE":
        if x_cell < mid:
            # Start closer to bottom of obstacle?
            if abs(y_bot - y_start) < abs(y_top - y_start):
                if y_cell > y_start:
                    return 1000
                else:
                    if y_cell > y_bot - 1:
                        return abs((y_bot-1) - y_cell)
                    return manhattan_distance(next, goal)
            # Start is closer to the top
            else:
                if y_cell < y_start:
                    return 1000
                if y_cell < y_top + 1:
                    return abs((y_top+1) - y_cell)
                return manhattan_distance(next, goal)
        else:
            return manhattan_distance(next, goal)


def get_prio(next, goal, type):
    # Based on type, add neighbor to frontier with respective priority
    if type == "DFS":
        return -next.g
    elif type == "BFS":
        return next.g
    elif type == "RANDOM":
        return random.randint(0, 100)
    elif type == "ASTAR":
        return next.f
    elif type == "GREEDY":
        return next.h


class Cell:

    # Structure for a cell in the map
    def __init__(self, position):
        self.position = position
        self.parent = None
        self.g = 0  # Distance from start
        self.h = 0  # Heuristic
        self.f = 0  # g+h

    def __eq__(self, other):
        if other is not None:
            if self.position[0] == other.position[0] and self.position[1] == other.position[1]:
                return True
            else:
                return False
        else:
            return False
