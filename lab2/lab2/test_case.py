import search_algorithm as sa
import path_planning as pp
import numpy as np
import matplotlib.pyplot as plt
import copy
import time

# Generate Map and get start & goal
map, info = pp.generateMap2d_obstacle([40, 40])
start = sa.Cell(np.where(map == -2))
goal = sa.Cell(np.where(map == -3))
size_y = map.shape[0]
size_x = map.shape[1]

# Generate and time different paths
start_time = time.time()
dfs_path, dfs_closed = sa.search(map, start, goal, "DFS", "EUCLIDEAN", info)
end = time.time()
dfs_time = (end - start_time)
start_time = time.time()
bfs_path, bfs_closed = sa.search(map, start, goal, "BFS", "EUCLIDEAN", info)
end = time.time()
bfs_time = (end - start_time)
start_time = time.time()
random_path, random_closed = sa.search(map, start, goal, "RANDOM", "EUCLIDEAN", info)
end = time.time()
random_time = (end - start_time)
start_time = time.time()
greedy_path, greedy_closed = sa.search(map, start, goal, "GREEDY", "EUCLIDEAN", info)
end = time.time()
greedy_time = (end - start_time)
start_time = time.time()
astar_path_manhattan, astar_manhattan_closed = sa.search(map, start, goal, "ASTAR", "MANHATTAN", info)
end = time.time()
astar_manhattan_time = (end - start_time)
start_time = time.time()
astar_path_euclidean, astar_euclid_closed = sa.search(map, start, goal, "ASTAR", "EUCLIDEAN", info)
end = time.time()
astar_euclidean_time = (end - start_time)
start_time = time.time()
greedy_path_hshape, greedy_hshape_closed = sa.search(map, start, goal, "GREEDY", "H-SHAPE", info)
end = time.time()
greedy_hshape_time = (end - start_time)

# Maps
dfs_map = copy.deepcopy(map)
bfs_map = copy.deepcopy(map)
random_map = copy.deepcopy(map)
greedy_map = copy.deepcopy(map)
astar_man_map = copy.deepcopy(map)
astar_euclid_map = copy.deepcopy(map)
greedy_hshape_map = copy.deepcopy(map)

# Insert path to corresponding map
for cell in dfs_path:
    x = int(cell.position[0])
    y = int(cell.position[1])
    dfs_map[x][y] = -4
for x in range(size_x):
    for y in range(size_y):
        if dfs_closed[x][y] == 0:
            dfs_map[x][y] = 1
for cell in random_path:
    x = int(cell.position[0])
    y = int(cell.position[1])
    random_map[x][y] = -4
for x in range(size_x):
    for y in range(size_y):
        if random_closed[x][y] == 0:
            random_map[x][y] = 1
for cell in bfs_path:
    x = int(cell.position[0])
    y = int(cell.position[1])
    bfs_map[x][y] = -4
for x in range(size_x):
    for y in range(size_y):
        if bfs_closed[x][y] == 0:
            bfs_map[x][y] = 1
for cell in greedy_path:
    x = int(cell.position[0])
    y = int(cell.position[1])
    greedy_map[x][y] = -4
for x in range(size_x):
    for y in range(size_y):
        if greedy_closed[x][y] == 0:
            greedy_map[x][y] = 1
for cell in astar_path_euclidean:
    x = int(cell.position[0])
    y = int(cell.position[1])
    astar_euclid_map[x][y] = -4
for x in range(size_x):
    for y in range(size_y):
        if astar_euclid_closed[x][y] == 0:
            astar_euclid_map[x][y] = 1
for cell in astar_path_manhattan:
    x = int(cell.position[0])
    y = int(cell.position[1])
    astar_man_map[x][y] = -4
for x in range(size_x):
    for y in range(size_y):
        if astar_manhattan_closed[x][y] == 0:
            astar_man_map[x][y] = 1
for cell in greedy_path_hshape:
    x = int(cell.position[0])
    y = int(cell.position[1])
    greedy_hshape_map[x][y] = -4
for x in range(size_x):
    for y in range(size_y):
        if greedy_hshape_closed[x][y] == 0:
            greedy_hshape_map[x][y] = 1

# Print some tasty stats
print "############# STATS ############"
print "DFS: ", len(dfs_path), "steps, ", dfs_time, "seconds"
print "BFS: ", len(bfs_path), "steps, ", bfs_time, "seconds"
print "RANDOM: ", len(random_path), "steps, ", random_time, "seconds"
print "GREEDY: ", len(greedy_path), "steps, ", greedy_time, "seconds"
print "ASTAR MANHATTAN: ", len(astar_path_manhattan), "steps, ", astar_manhattan_time, "seconds"
print "ASTAR EUCLIDEAN: ", len(astar_path_euclidean), "steps, ", astar_euclidean_time, "seconds"
print "ASTAR H-SHAPE: ", len(greedy_path_hshape), "steps, ", greedy_hshape_time, "seconds"

# Plot
fig = plt.figure()
ax = fig.add_subplot(3,3,1)
ax.set_title("DFS")
ax.imshow(dfs_map)
ax = fig.add_subplot(3,3,2)
ax.set_title("BFS")
ax.imshow(bfs_map)
ax = fig.add_subplot(3,3,3)
ax.set_title("RANDOM")
ax.imshow(random_map)
ax = fig.add_subplot(3,3,4)
ax.set_title("GREEDY")
ax.imshow(greedy_map)
ax = fig.add_subplot(3,3,5)
ax.set_title("ASTAR MANHATTAN")
ax.imshow(astar_man_map)
ax = fig.add_subplot(3,3,6)
ax.set_title("ASTAR EUCLIDEAN")
ax.imshow(astar_euclid_map)
ax = fig.add_subplot(3,3,8)
ax.set_title("GREEDY H-SHAPE")
ax.imshow(greedy_hshape_map)
plt.show()

