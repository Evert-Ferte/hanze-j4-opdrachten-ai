import matplotlib.pyplot as plt
import random
import time
import itertools
import math
from collections import namedtuple

# based on Peter Norvig's IPython Notebook on the TSP

City = namedtuple('City', 'x y')

def distance(A, B):
    return math.hypot(A.x - B.x, A.y - B.y)

def try_all_tours(cities):
    # generate and test all possible tours of the cities and choose the shortest tour
    tours = alltours(cities)
    return min(tours, key=tour_length)

def alltours(cities):
    # return a list of tours (a list of lists), each tour a permutation of cities,
    # and each one starting with the same city
    # note: cities is a set, sets don't support indexing
    start = next(iter(cities)) 
    return [[start] + list(rest) for rest in itertools.permutations(cities - {start})]

# region Nearest neighbour algorithm + 2-opt

def nearest_neighbour(cities):
    available = set(cities)
    cur = available.pop()
    route = [cur, ]

    while len(available) > 0:
        cur = get_closest_neighbouring_city(cur, available)
        route.append(cur)
        available.remove(cur)

    return route

def nearest_neighbour_2opt(cities):
    route = nearest_neighbour(cities)
    print(tour_length(route))

    def two_opt_swap(r, i, k):
        return r[:i] + list(reversed(r[i:k])) + r[k:]

    improved = True
    while improved:
        bestPathLength = tour_length(route)
        for i in range(len(route) - 1):
            for k in range(i+1, len(route)):
                newRoute = two_opt_swap(route, i, k)
                newPathLength = tour_length(newRoute)

                if newPathLength < bestPathLength:
                    print('new shorter path found, changed from length {} to {}'.format(bestPathLength, newPathLength))
                    bestPathLength = newPathLength
                    route = newRoute  # continue
                else:
                    improved = False  # stop, no improved found

    print(tour_length(route))
    return route

def get_closest_neighbouring_city(city, cities):
    return min(cities, key=lambda d: distance(city, d))

# endregion

def tour_length(tour):
    # the total of distances between each pair of consecutive cities in the tour
    return sum(distance(tour[i], tour[i-1]) for i in range(len(tour)))

def make_cities(n, width=1000, height=1000, seed=None):
    # make a set of n cities, each with random coordinates within a rectangle (width x height).
    random.seed(seed if seed is not None else time.time())
    return frozenset(City(random.randrange(width), random.randrange(height)) for c in range(n))

def plot_tour(tour): 
    # plot the cities as circles and the tour as lines between them
    points = list(tour) + [tour[0]]
    plt.plot([p.x for p in points], [p.y for p in points], 'bo-') # blue circle markers, solid line style
    plt.axis('scaled') # equal increments of x and y have the same length
    plt.axis('off')
    plt.show()

def plot_tsp(algorithm, cities):
    # apply a TSP algorithm to cities, print the time it took, and plot the resulting tour.
    t0 = time.process_time()
    tour = algorithm(cities)
    t1 = time.process_time()
    print("{} city tour with length {:.1f} in {:.3f} secs for {}"
          .format(len(tour), tour_length(tour), t1 - t0, algorithm.__name__))
    print("Start plotting ...")
    plot_tour(tour)

# give a demo with 10 cities using brute force
# plot_tsp(try_all_tours, make_cities(10))
# plot_tsp(nearest_neighbour, make_cities(100, seed=22))
# plot_tsp(nearest_neighbour_2opt, make_cities(100, seed=22))


tour = ['A', 'B', 'C', 'D']
n = len(tour)
for i in range(n - 1):
    for k in range(i + 1, n):
        print(tour[:i] + list(reversed(tour[i:k])) + tour[k:])

# wat hier staat is 1/2 n^2
# n = 4
# for i in range(n):
#     for k in range(i+1, n):
#         print(i, k)
