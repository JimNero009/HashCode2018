import sys
from copy import deepcopy

class RideController:
    def __init__(self, rideList, rows, cols, vehicles, numRides, bonus, steps):
        self.rideList = sorted(self.convertToRides(rideList))
        self.rows = rows
        self.cols = cols
        self.numRides = numRides
        self.bonus = bonus
        self.steps = steps
        self.vehicles = [Car(i+1) for i in range(vehicles)]

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

    def assignCarsToRides(self):
        copiedRideList = deepcopy(self.rideList)
        for car in self.vehicles:
            ride_ids = []
            for ride in copiedRideList:
                if car.attemptToAssignRide(ride):
                    ride_ids.append(ride.id)
            copiedRideList = self.removeRidesFromList(ride_ids, copiedRideList)
            if not copiedRideList:
                break
        return self.vehicles

    @staticmethod
    def removeRidesFromList(ride_ids, rideList):
        return [ride for ride in rideList if ride.id not in ride_ids]


    @staticmethod
    def convertToRides(rideList):
        newRideList = []
        id = 0
        for ride in rideList:
            newRide = Ride(
                Point(ride[0], ride[2]),
                Point(ride[1], ride[3]),
                ride[4],
                ride[5],
                id
            )
            id += 1
            newRideList.append(newRide)
        return newRideList

class Car: # should have id
    def __init__(self, id):
        self.position = Point(0, 0)
        self.time = 0
        self.assignedRides = []
        self.inUse = False
        self.id = id

    def attemptToAssignRide(self, ride):
        time = max(ride.earliestTime + ride.rideLength,
            self.time + ride.rideLength + (self.position - ride.startPoint)
        )
        position = ride.endPoint
        if time >= ride.latestTime:
            return False
        self.assignedRides.append(ride)
        self.time = time
        self.position = position
        return True

    def isInUse(self):
        return self.inUse

    def switchInUse(self):
        self.inUse = not self.inUse


    


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return '({}, {})'.format(self.x, self.y)

    def __sub__(self, other):
        return abs(other.x - self.x) + abs(other.y - self.y)


class Ride:
    def __init__(self, startPoint, endPoint, earliestTime, latestTime, id):
        self.startPoint = startPoint
        self.endPoint = endPoint
        self.earliestTime = earliestTime
        self.latestTime = latestTime
        self.rideLength = self.lengthOfRide()
        self.latestStartTime = self.latestTime - self.rideLength - 1
        self.earliestArrivalTime = self.earliestTime + self.rideLength + 1
        self.id = id

    def __str__(self):
        return "start: {}, end: {}, earliestTime: {}, latestTime: {}, rideLength: {}, latestStartTime: {}, earliestArrivalTime: {}".format(
            self.startPoint,
            self.endPoint,
            self.earliestTime,
            self.latestTime,
            self.rideLength,
            self.latestStartTime,
            self.earliestArrivalTime
        )

    def lengthOfRide(self):
        return self.endPoint - self.startPoint

    def __gt__(self, other):
        return self.earliestTime >= other.earliestTime

    def __lt__(self, other):
        return self.earliestTime < other.earliestTime



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
        for vehicle in solution:
            rideString = str(len(vehicle.assignedRides))
            for ride in vehicle.assignedRides:
                rideString += ' {}'.format(ride.id)
            outputFile.write("{}\n".format(rideString))

def main():
    rideController = readInput()
    # for i in range(len(rideController.rideList)):
    #     print(rideController.rideList[i])
    vehicleList = rideController.assignCarsToRides()
    writeOutput(vehicleList)


if __name__ == '__main__':
    main()
