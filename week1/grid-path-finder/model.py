import random
import heapq
import math
import config as cf

# global var
grid = [[0 for x in range(cf.SIZE)] for y in range(cf.SIZE)]
visitedNodes = set()

class PriorityQueue:
    # a wrapper around heapq (aka priority queue), a binary min-heap on top of a list
    def __init__(self):
        # create a min heap (as a list)
        self.elements = []
    
    def empty(self):
        return len(self.elements) == 0
    
    # heap elements are tuples (priority, item)
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    # pop returns the smallest item from the heap
    # i.e. the root element = element (priority, item) with highest priority
    def get(self):
        return heapq.heappop(self.elements)[1]

def bernoulli_trial(app):
    return 1 if random.random() < int(app.prob.get())/10 else 0

def get_grid_value(node):
    # node is a tuple (x, y), grid is a 2D-list [x][y]
    return grid[node[0]][node[1]]

def set_grid_value(node, value): 
    # node is a tuple (x, y), grid is a 2D-list [x][y]
    grid[node[0]][node[1]] = value

def search(app, start, goal):
    prioQ = PriorityQueue()
    useAStar = app.alg.get() == 'A*'
    pathVal = 1                         # The value of a path between each node
    heuristicIntensity = 5              # Indicates how intense the heuristic value will be counted towards the priority
    path = {}

    print('\nInfo about run:')
    print('prioQ.empty()', prioQ.empty())
    print('path', path)
    print('visitedNodes', visitedNodes)

    prioQ.put(start, 0)
    while True:
        if prioQ.empty(): break

        # Get the current node, visit it, and get all of its neighbours
        cur = prioQ.get()
        if cur == goal: break

        visit(cur)
        neighbours = get_neighbouring_nodes(cur)

        # Loop through all the neighbours
        for nb in neighbours:
            # Calculate the potential new value
            newVal = get_grid_value(cur) + pathVal
            # Compare the new value with the old (existing) value
            if newSmallerThanOld(newVal, get_grid_value(nb)):
                set_grid_value(nb, newVal)
                prioQ.put(nb, newVal if not useAStar else newVal + dist(nb, goal) * heuristicIntensity)  # Use A* if selected
                path[nb] = cur  # Set where we came from, so we can traverse the path later on

                # Color the nodes we check
                app.plot_node(nb, color=cf.PATH_C)
            app.pause()
    visitedNodes.clear()

    # When finished, and if we reached our goal, traverse the path
    if goal in path:
        app.draw_path(path)

def get_neighbouring_nodes(node):
    n = []
    for i in range(4):
        addX = (i % 2) * (1 if i < 2 else -1)
        addY = ((i + 1) % 2) * (1 if i < 2 else -1)
        if 0 <= node[0] + addX < cf.SIZE and 0 <= node[1] + addY < cf.SIZE:
            if get_grid_value((node[0] + addX, node[1] + addY)) != 'b':
                if not visited((node[0] + addX, node[1] + addY)):
                    n.append((node[0] + addX, node[1] + addY))
    return n

def visited(node):
    return node in visitedNodes

def visit(node):
    visitedNodes.add(node)

def newSmallerThanOld(new: int, old: int):
    if old != -1: return new < old
    return True

def dist(a, b):
    return math.sqrt(math.pow((b[0] - a[0]), 2) + math.pow((b[1] - a[1]), 2))
