import sys
from copy import deepcopy

class RideController:

    def __init__(self, rideList, rows, cols, vehicles, numRides, bonus, steps):
        self.bonus = bonus
        self.rideList = sorted(self.convertToRides(rideList))
        self.rows = rows
        self.cols = cols
        self.numRides = numRides
        self.steps = steps
        self.vehicles = [Car() for i in range(vehicles)]

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
            breakout = False
            while copiedRideList and not breakout:
                copiedRideList = self.sortRidesByLucrativity(car, copiedRideList)
                ride_ids = []
                for i,ride in enumerate(copiedRideList):
                    # print(ride)
                    # print ride.lucrativity
                    if car.attemptToAssignRide(ride):
                        # print('Assigned {}!'.format(ride.id))
                        ride_ids.append(ride.id)
                        break
                    #if i == 2:
                    #    breakout = True
                    if ride == copiedRideList[-1]:
                        breakout = True
                copiedRideList = self.removeRidesFromList(ride_ids, copiedRideList)
            #print('*******')
            #break
        return self.vehicles

    def sortRidesByLucrativity(self,car,unsortedRideList):
        for ride in unsortedRideList:
            ride.lucrativity = ride.calcLucrativity(car)
        return sorted(unsortedRideList, reverse=True)

    @staticmethod
    def removeRidesFromList(ride_ids, rideList):
        return [ride for ride in rideList if ride.id not in ride_ids]


    def convertToRides(self, rideList):
        newRideList = []
        id = 0
        for ride in rideList:
            newRide = Ride(
                Point(ride[0], ride[1]),
                Point(ride[2], ride[3]),
                ride[4],
                ride[5],
                id,
                self.bonus
            )
            id += 1
            newRideList.append(newRide)
        return newRideList

class Car: # should have id
    def __init__(self):
        self.position = Point(0, 0)
        self.time = 0
        self.assignedRides = []
        self.inUse = False

    def attemptToAssignBonusRide(self, ride):
        if self.time + ride.rideLength > ride.earliestTime:
            #ride will not get bonus
            #TODO check this logic
            return False
        time = ride.earliestTime + ride.rideLength
        position = ride.endPoint
        if time >= ride.latestTime:
         return False
        self.assignedRides.append(ride)
        self.time = time
        self.position = position
        return True

    def attemptToAssignRide(self, ride):
        #endtime = max(ride.earliestTime + ride.rideLength, self.time + ride.rideLength + (self.position - ride.startPoint))
        dist = self.position - ride.startPoint
        timeatstart = self.time + dist #this is the time we will get to the start point
        starttime = max(timeatstart,ride.earliestTime) #this is the time we will start the journey
        endtime = starttime + ride.rideLength
        position = ride.endPoint
        # print('I am at {}'.format(self.time))
        if endtime > ride.latestTime:
            #this should ensure we don't take rides we won't get paid for
            return False
        self.assignedRides.append(ride)
        self.time = endtime
        # print('I am now at {}'.format(self.time))
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
    def __init__(self, startPoint, endPoint, earliestTime, latestTime, id, bonus):
        self.bonus = bonus
        self.startPoint = startPoint
        self.endPoint = endPoint
        self.earliestTime = earliestTime
        self.latestTime = latestTime
        self.rideLength = self.lengthOfRide()
        self.latestStartTime = self.latestTime - self.rideLength - 1
        self.earliestArrivalTime = self.earliestTime + self.rideLength + 1
        self.id = id
        self.lucrativity = self.calcLucrativity(Car())

    def __str__(self):
        return "id: {}, start: {}, end: {}, earliestTime: {}, latestTime: {}, rideLength: {}, latestStartTime: {}, earliestArrivalTime: {}".format(
            self.id,
            self.startPoint,
            self.endPoint,
            self.earliestTime,
            self.latestTime,
            self.rideLength,
            self.latestStartTime,
            self.earliestArrivalTime
        )

    def calcLucrativity(self,car):
        lucrativity = 0
        dist = car.position - self.startPoint
        if car.time + dist <= self.earliestTime:
            lucrativity += self.bonus
            deadtime = self.earliestTime - car.time
        else:
            deadtime = dist
        lucrativity += self.rideLength
        #lucrativity -= deadtime*0.1
        return lucrativity

    def lengthOfRide(self):
        return self.endPoint - self.startPoint

    def __gt__(self, other):
        return self.lucrativity >= other.lucrativity

    def __lt__(self, other):
        return self.lucrativity < other.lucrativity



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
