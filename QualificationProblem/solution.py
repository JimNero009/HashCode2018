import sys


class RideController:
    def __init__(self, rideList, rows, cols, vehicles, numRides, bonus, steps):
        self.rideList = rideList
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

class Car:
    pass


class Route:
    pass


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
    print(rideController)
    # Magic here...
    solution = 'Hooray!'
    writeOutput(solution)


if __name__ == '__main__':
    main()
