# coding:utf-8
#!/usr/bin/env python
"""
author: Qijie Pan
Date: 11.30.2015

"""

import random
import time


# use a class to store the file, the key will be cities's name, and the value should be a tuple
# store the x and y coordinates.


class City(object):
    """docstring for City"""

    def __init__(self, name, xcoordinate, ycoordinate, visited=False):
        """
        type: name string
        type: x  int
        type: y  int
        type: visited boolean
        """
        self.name = name
        self.x = xcoordinate
        self.y = ycoordinate
        self.visited = visited


# Now let's implement the greedy algorithm.
# The thought of the greedy is at first we need to randomly pick a initial city, after that, go
# through all the cities which have not been visited and find the minimun distance. And then use
# the city we found as the start city, do the same process, until we go
# back to our initial city


# pro: it's pretty fast

# con: can not promise it's the best solution. Only best in local.


class Greedy(object):
    """docstring for Greedy"""

    def __init__(self, cities, path=[], totaldis=0.0):
        """
        type: cities  list<city>
        type: path list<(startCity,endCity)>
        type: numCities int
        type: totaldis float

        """
        self.cities = cities  # store all the cities' infomation
        self.path = path  # store the path of the solution
        # store the number of cities in this tsp question
        self.numCities = len(cities)
        self.totalDis = totaldis  # store the total distance of this tsp question

    def eucilideanDistance(self, (x1, y1), (x2, y2)):
        """
        The two points are located on coordinates (x1,y1) and (x2,y2),
        sent as parameters.

        rtype: float
        """
        xdiff = float(x2) - float(x1)
        ydiff = float(y2) - float(y1)
        return ((xdiff)**2 + (ydiff)**2)**0.5

    def manhatanDistance(self, (x1, y1), (x2, y2)):
        """
        The two points are located on coordinates (x1,y1) and (x2,y2),
        sent as parameters.

        rtype: float
        """
        return abs(float(x2) - float(x1)) + abs(float(y2) - float(y1))

    def __findNearst(self, bcity, cities, method):
        """
        type: bcity: City
        type: cities: list<City>
        type: method: string
        rtype: City
        """
        mindistance = 10000000  # which means infinity
        nearstCity = bcity
        if method == 'L1':
            for ecity in cities:
                if not ecity.visited:
                    distance = self.eucilideanDistance(
                        (bcity.x, bcity.y), (ecity.x, ecity.y))
                    if mindistance > distance:
                        mindistance = distance
                        nearstCity = ecity
            nearstCity.visited = True
            self.totalDis += mindistance
            return nearstCity

        elif method == 'L2':
            for ecity in cities:
                if not ecity.visited:
                    distance = self.manhatanDistance(
                        (bcity.x, bcity.y), (ecity.x, ecity.y))
                    if mindistance > distance:
                        mindistance = distance
                        nearstCity = ecity
            nearstCity.visited = True
            self.totalDis += mindistance
            return nearstCity

    def greedySolution(self, seed, method):
        # initialize the random seed which can let us to decide the initial
        # city
        """
        type: seed: int
        type: method: string
        rtype: list<path>, distance: float

        """
        random.seed(seed)
        initialCity = self.cities[int(random.random() * self.numCities)]
        initialCity.visited = True  # which means the city has been visited

        numVisted = 1
        beginCity = initialCity
        while numVisted < self.numCities:
            endCity = self.__findNearst(beginCity, self.cities, method)
            self.path.append((beginCity, endCity))
            beginCity = endCity
            numVisted += 1

        # for the last step, we need to calculate the begin's distance with the
        # initial city
        if method == 'L1':
            self.totalDis += self.eucilideanDistance(
                (beginCity.x, beginCity.y), (initialCity.x, initialCity.y))
            self.path.append((beginCity, initialCity))
        if method == 'L2':
            self.totalDis += self.manhatanDistance((beginCity.x,
                                                    beginCity.y), (initialCity.x, initialCity.y))
            self.path.append((beginCity, initialCity))

        return self.path, self.totalDis

if __name__ == '__main__':
    # We can define the seed and the method to calculate the distance.
    # For method, we can choose L1 stands EucilideanDistance and L2 stands
    # ManhatanDistance
    start = time.clock()

    # use a array to store all the city instance in the file
    cities = []

    # open the file
    with open('gr666.tsp', 'r') as f:
        for line in f:
            if line[0] == '0':
                cityInfo = line.split(' ')  # use " "to split the name, x and y
                city = City(cityInfo[0], cityInfo[1], cityInfo[2])
                cities.append(city)
                
    EuSolution = Greedy(cities)

    print "*** This is the Greedy Solution with the Eucilidean Distance ***"
    EuDistanceSolution = EuSolution.greedySolution(0, 'L1')  # seed = 0
    print "** This is the Path **"
    pathName = []
    for p in EuDistanceSolution[0]:
        pathName.append((p[0].name, p[1].name))
    print pathName
    print "** This is the Distance for Eucilidean Distance **"
    print EuDistanceSolution[1]
    elapsed = (time.clock() - start)
    print "Time Used:", elapsed

    start = time.clock()

    # use a array to store all the city instance in the file
    cities = []

    # open the file
    with open('gr666.tsp', 'r') as f:
        for line in f:
            if line[0] == '0':
                cityInfo = line.split(' ')  # use " " to split the name, x and y
                city = City(cityInfo[0], cityInfo[1], cityInfo[2])
                cities.append(city)

    MaSolution = Greedy(cities)

    print "*** This is the Greedy Solution with the Manhatan Distance ***"
    ManhatanSolution = MaSolution.greedySolution(0, 'L2')  # seed is 0
    print "** This is the Path **"
    pathName = []
    for p in ManhatanSolution[0]:
        pathName.append((p[0].name, p[1].name))
    print pathName
    print "** This is the Distance for Manhatan Distance **"
    print ManhatanSolution[1]
    elapsed = (time.clock() - start)
    print "Time Used:", elapsed
