# coding:utf-8
#!/usr/bin/env python

"""
author: Qijie Pan
Date: 11.30.2015

"""


import random
import time
from tsp import City
from tsp import Greedy


# Now let's we implement the local search -- 2-opt algorithm
# The thought of 2-opt algorithm is that it will compare every valid combination of the swapping
# mechanism(Replace 2 edges), stop until there is no improvement for the
# minimun distance

class TwoOpt(object):
    """docstring for TwoOpt"""

    def __init__(self, cities, greedy):
        """
        type: cities list<City>
        type: improvement boolean
        type: existPath list<(City,City)>
        type: existDistance float
        """
        self.cities = cities
        self.improvement = True
        self.existPath = greedy[0]
        self.existDistance = greedy[1]

    def twoOptSwap(self, path, i, k):
        """
        The method is to change the edges for the path
        type: path list<(City,City)>
        type: i int
        type: k int
        rtype: list<(City,City)>
        """
        modifiedPath = [path[0][0]]
        for c in path:
            modifiedPath.append(c[1])
        start = modifiedPath[0:i]
        middle = modifiedPath[i:k]
        middle = middle[::-1]
        end = modifiedPath[k:]
        modifiedPath = start + middle + end

        finalPath = []
        for j in xrange(len(modifiedPath) - 1):
            finalPath.append((modifiedPath[j], modifiedPath[j + 1]))
        return finalPath

    def calculateDistance(self, path):
        """
        This method is to calculate the distance between two nodes using Eucilidean Distance
        type: path list<(City,City)>
        """

        totalDistance = 0
        for i in path:
            totalDistance += ((float(i[0].x) - float(i[1].x))
                              ** 2 + (float(i[0].y) - float(i[1].y))**2)**0.5
        return totalDistance

    def twoOptSolution(self):
        """
        generate a random path. For here, we can use the result we got from
        the greedy.

        rtype: path list<(City,City)>, distance float
        """

        while self.improvement:
            #self.improvement = False
            for i in xrange(1, len(self.existPath) - 2):
                for k in xrange(i + 2, len(self.existPath)):
                    newPath = self.twoOptSwap(self.existPath, i, k)
                    newDistance = self.calculateDistance(newPath)
                    if newDistance < self.existDistance:
                        self.existDistance = newDistance
                        self.existPath = newPath
                        self.improvement = False

        return self.existPath, self.existDistance


if __name__ == '__main__':

    start = time.clock()
    # use a array to store all the city instance in the file
    cities = []

    # open the file
    with open('gr666.tsp', 'r') as f:
        for line in f:
            if line[0] == '0':
                cityInfo = line.split(' ')  # use ; to split the name, x and y
                city = City(cityInfo[0], cityInfo[1], cityInfo[2])
                cities.append(city)

    # we use the greedy result as the initial algorithm. So it will be better
    # to get the result
    greedy = Greedy(cities).greedySolution(0, 'L1')

    # print the result
    print "*** This is the 2-opt Solution with the Eucilidean Distance ***"
    tOptSolution = TwoOpt(cities, greedy).twoOptSolution()
    print "** This is the Path **"
    pathName = []
    for p in tOptSolution[0]:
        pathName.append((p[0].name, p[1].name))
    print pathName
    print "** This is the Distance for Eucilidean Distance **"
    print tOptSolution[1]
    elapsed = (time.clock() - start)
    print "Time Used:", elapsed

