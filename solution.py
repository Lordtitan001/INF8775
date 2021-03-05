#!/usr/bin/env python3

# bellow is the link to the reference code used to implement the divide and conquer algotithm
# https://www.learnbay.io/the-skyline-problem/
import time, os, argparse


class Solution:
    def getBuildings(self, filename: str): 
        # name_split = filename.split(":")
        # if len(name_split) == 2:
        #     filename = filename.split(":")[1]
        #     print(filename)
        f = open(filename)
        size = int(f.readline())
        array = []
        for i in range(size):
            line = f.readline().split(" ")
            array.append((int(line[0]), int(line[1]), int(line[2])))
        f.close()
        return array

    def findCriticalPoints(self, skyLineArray):
        array = []
        for buildingPoints in skyLineArray:       
            array.append([buildingPoints[0], buildingPoints[2]])
            array.append([buildingPoints[1], 0])
        return array

    def setElevatedCriticalPoints(self, cirticalsPoints, buildings):
        index = 0
        for point in cirticalsPoints:
            for building in buildings:
                if (self.shouldElevate(point, building)):
                    if (cirticalsPoints[index][1] <  building[2]):
                        cirticalsPoints[index] = [point[0], building[2]]
                    
            index = index + 1

    def sortPoints(self, cirticalsPoints):
        cirticalsPoints.sort(key=lambda tup: tup[0])
        return

    def removeRedundants(self, cirticalsPoints):
        finalPoints = [cirticalsPoints[0]]
        for i in range(1, len(cirticalsPoints) - 1):
            if (cirticalsPoints[i][1] != cirticalsPoints[i - 1][1]) :
                finalPoints.append(cirticalsPoints[i])

        finalPoints.append(cirticalsPoints[len(cirticalsPoints) - 1])
        return finalPoints

    def shouldElevate(self, point, building):
        if (point[0] >= building[0] and point[0] < building[1] and point[1] < building[2]):
            return True
        return False

    def divideAndCombine(self, buildings, ceil: int = 1):
        size = len(buildings)
        if size == 0:
            return []
        if size == 1:
            left, right, h = buildings[0]
            return [[left, h], [right, 0]] 
        if (size < ceil):
            return self.brutForce(buildings)
        else:
            left_side = self.divideAndCombine(buildings[: size // 2], ceil)
            right_side = self.divideAndCombine(buildings[size // 2 :], ceil)
            return self.merge(left_side, right_side)

    def update_output(self, x, y, output):
            if not output or output[-1][0] != x:
                output.append([x, y])
            else:
                output[-1][1] = y
        
    def append(self, p, lst, n, y, curr_y, output):
        while p < n: 
            x, y = lst[p]
            p += 1
            if curr_y != y:
                self.update_output(x, y, output)
                curr_y = y

    def merge(self, left, right):
        
        leftSize = len(left)
        rigthSize = len(right)
        pointLeft = pointRight = 0
        curr_y  = left_y = right_y = 0
        output = []

        while pointLeft < leftSize and pointRight < rigthSize:
            point_l, point_r = left[pointLeft], right[pointRight]
            if point_l[0] < point_r[0]: 
                x, left_y = point_l
                pointLeft += 1
            else: 
                x, right_y = point_r 
                pointRight += 1
            max_y = max(left_y, right_y)
            if curr_y != max_y:
                self.update_output(x, max_y, output)
                curr_y = max_y

        self.append(pointLeft, left, leftSize, left_y, curr_y, output)
        self.append(pointRight, right, rigthSize, right_y, curr_y, output)

        return output
    
    def brutForce(self, buildings):
        cirticalsPoints = self.findCriticalPoints(buildings)
        self.setElevatedCriticalPoints(cirticalsPoints, buildings)
        self.sortPoints(cirticalsPoints)
        return self.removeRedundants(cirticalsPoints)

    def divideAndConquer(self, buildings):
        return self.divideAndCombine(buildings) 

    def divideAndConquerWithCeil(self, buildings, ceil):
        return self.divideAndCombine(buildings, ceil) 


def averageTimeForBruteForce(listOfFiles):
    timeExecuted = []
    for n in listOfFiles:
        sol1 = Solution()
        buildings = sol1.getBuildings(n)
        starting = time.time()
        sol1.brutForce(buildings)
        end = time.time()
        timeExecuted.append( (end- starting) *1000)
    allTime= 0
    for element in timeExecuted :
        allTime+= element
    return allTime/5

def averageTimedivideAndConquer(listOfFiles):
    timeExecuted = []
    for n in listOfFiles:
        sol1 = Solution()
        buildings = sol1.getBuildings(n)
        starting = time.time()
        sol1.divideAndConquer(buildings)
        end = time.time()
        timeExecuted.append( (end- starting) *1000)
    allTime= 0
    for element in timeExecuted :
        allTime+= element
    return allTime/5
    
def averageTimeForDiviceAndConquerWithCeil(listOfFiles):
    timeExecuted = []
    for n in listOfFiles:
        sol1 = Solution()
        buildings = sol1.getBuildings(n)
        starting = time.time()
        sol1.divideAndConquerWithCeil(buildings, 500)
        end = time.time()
        timeExecuted.append( (end- starting) *1000)
    allTime= 0
    for element in timeExecuted :
        allTime+= element
    return allTime/5
    
def main(): 
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--algorithm", type=str)
    parser.add_argument("-e", "--path", type=str)
    parser.add_argument("-p", "--d_couple", type=str)
    parser.add_argument("-t", "--d_time", type=str)
    args = parser.parse_args()

    sol = Solution()
    result = []
    buildings = sol.getBuildings(args.path)
    starting = time.time()

    if (args.algorithm == "brute"):
        result = sol.brutForce(buildings)

    if (args.algorithm == "recursif"):
        result = sol.divideAndConquer(buildings)

    if (args.algorithm == "seuil"):
        result = sol.divideAndConquerWithCeil(buildings, 100)

    ending = time.time()

    if (args.d_couple != None):
        for point in result:
            print(str(point[0]) + "," + str(point[1]))

    if (args.d_time != None):
        print((ending - starting) * 1000)

if __name__ == "__main__":
    # main()
    # fichiers de 1000
    averageBruteForce = averageTimedivideAndConquer(["N1000_0", "N1000_1", "N1000_2", "N1000_3", "N1000_4"])
    print('N1000 - ' + str(averageBruteForce))

    averageBruteForce = averageTimedivideAndConquer( ["N5000_0", "N5000_1", "N5000_2", "N5000_3", "N5000_4"])
    print('N5000 - ' + str(averageBruteForce))

    averageBruteForce = averageTimedivideAndConquer( ["N10000_0", "N10000_1", "N10000_2", "N10000_3", "N10000_4"])
    print('N10000 - ' + str(averageBruteForce))

    averageBruteForce = averageTimedivideAndConquer( ["N50000_0", "N50000_1", "N50000_2", "N50000_3", "N50000_4"])
    print('N50000 - ' + str(averageBruteForce))

    averageBruteForce = averageTimedivideAndConquer( {"N100000_0", "N100000_1", "N100000_2", "N100000_3", "N100000_4"})
    print('N100000 - ' + str(averageBruteForce))

    averageBruteForce = averageTimedivideAndConquer( {"N500000_0", "N500000_1", "N500000_2", "N500000_3", "N500000_4"})
    print('N500000 - ' + str(averageBruteForce))

