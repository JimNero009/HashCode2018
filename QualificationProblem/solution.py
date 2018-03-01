import sys

class RideController:
    def __init__(self, rideList, rows, cols, vehicles, numRides, bonus, steps):
        self.rideList = self.convertToRides(rideList)
        self.rows = rows
        self.cols = cols
        self.numRides = numRides
        self.bonus = bonus
        self.steps = steps
        self.vehicles = vehicles

    def __str__(self):
        output = '''
            rows: {}
            cols: {}
            vehicles: {}
            numRides: {}
            bonus: {}
            steps: {}
            rideList: {}
        '''.format(self.rows, self.cols, self.vehicles, self.numRides, self.bonus, self.steps, self.rideList)
        return output

    @staticmethod
    def convertToRides(rideList):
        newRideList = []
        for ride in rideList:
            newRide = Ride(
                Point(ride[0], ride[2]),
                Point(ride[1], ride[3]),
                ride[4],
                ride[5]
            )
            newRideList.append(newRide)
        return newRideList

class Car:
    def __init__(self):
        self.assignedRides = []

    def assignRide(self, ride):
        self.assignedRides.append(ride)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return '({}, {})'.format(self.x, self.y)

    def __sub__(self, other):
        return abs(other.x - self.x) + abs(other.y - self.y)


class Ride:
    def __init__(self, startPoint, endPoint, earliestTime, latestTime):
        self.startPoint = startPoint
        self.endPoint = endPoint
        self.earliestTime = earliestTime
        self.latestTime = latestTime
        self.rideLength = self.lengthOfRide()

    def __str__(self):
        return "start: {}, end: {}, earliestTime: {}, latestTime: {}, rideLength: {}".format(
            self.startPoint,
            self.endPoint,
            self.earliestTime,
            self.latestTime,
            self.rideLength
        )

    def lengthOfRide(self):
        return self.endPoint - self.startPoint


def readInput():
    '''
    Read input and parse according to structure
    '''
    with open(sys.argv[1], 'r') as inputFile:  
        fullFile = inputFile.read().split('\n')

    rows, cols, vehicles, numRides, bonus, steps = [int(x) for x in fullFile[0].split(' ')]
    rideList = []
    for i in range(1, 1 + numRides):
        rideList.append([int(x) for x in fullFile[i].split(' ')])
    rc = RideController(rideList, rows, cols, vehicles, numRides, bonus, steps)
    return rc


def writeOutput(solution):
    '''
    Write output in required form
    '''
    with open(sys.argv[2], 'w') as outputFile:
        outputFile.write(solution)


def main():
    rideController = readInput()
    for i in range(len(rideController.rideList)):
        print(rideController.rideList[i])
    # Magic here...
    solution = 'Hooray!'
    writeOutput(solution)


if __name__ == '__main__':
    main()
