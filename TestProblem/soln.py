import sys
from copy import deepcopy
from random import randint


class Pizza():

    ITERATION_LIMIT = 1000

    def __init__(self, grid, maxSliceSize, minIngredients):
        self.grid = grid
        self.initialGrid = deepcopy(grid)
        self.maxSliceSize = maxSliceSize
        self.minIngredients = minIngredients
        self.slices = []
        self.available_shapes = self.generate_shapes()
        self.possibleLocations = []

    def reset(self):
        self.grid = deepcopy(self.initialGrid)
        self.slices = []
        self.possibleLocations = []

    def generate_shapes(self):
        shapes = []
        for i in range(1, self.maxSliceSize + 1):
            for j in range(1, self.maxSliceSize + 1):
                if i*j <= self.maxSliceSize:
                    shapes.append((i, j))
        return shapes

    def findBest(self):
        possibleSlicesSolution = []
        return

    def get_random_shape(self):
        return self.available_shapes[randint(0, len(self.available_shapes) - 1)]

    def get_possible_locations(self):
        possible = []
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                if self.grid[i][j] != 'X':
                    possible.append((i, j))
        return possible

    def get_random_available_location(self):
        possible = self.get_possible_locations()       
        return possible[randint(0, len(possible) - 1)]

    def possible_to_slice(self):
        return len(self.get_possible_locations()) > 0

    def greedyApproach(self):
        for i in range(self.ITERATION_LIMIT):
            location = self.get_random_available_location()
            shape = self.get_random_shape()
            slice = Slice(location[0], location[1], location[0] + (shape[0] - 1), location[1] + (shape[1] - 1))
            if slice.isValidSlice(self.grid, self.minIngredients):
                self.slices.append(slice)
                self.cutSlice(slice)           

            if not self.possible_to_slice():
                break


    def cutSlice(self, slice):
        for row in range(slice.coords[0], slice.coords[2] + 1):
            for col in range(slice.coords[1], slice.coords[3] + 1):
                self.grid[row][col] = 'X'

    def checkValidity(self, proposedSlices):
        areValidSlices = all(slice.isValidSlice(self.grid, self.minIngredients) for slice in proposedSlices)
        noOverlaps = True
        for slice in proposedSlices:
            for otherSlice in proposedSlices:
                if slice != otherSlice:
                    noOverlaps = noOverlaps and not slice.overlaps(otherSlice)
        return areValidSlices and noOverlaps

    def calculateScore(self):
        score = 0
        for slice in self.slices:
            score += slice.size()
        return score

class Slice():
    def __init__(self, rowStart, colStart, rowFinish, colFinish):
        self.coords = (rowStart, colStart, rowFinish, colFinish)

    def __str__(self):
        return "{} {} {} {}".format(
            self.coords[0],
            self.coords[1],
            self.coords[2],
            self.coords[3]
        )

    def isValidSlice(self, pizzaGrid, minIngredients):
        outOfBounds = self.coords[0] < 0 or self.coords[1] < 0 or self.coords[2] >= len(pizzaGrid) or self.coords[3] >= len(pizzaGrid[0])
        if outOfBounds:
            return False
        countT = 0
        countM = 0
        for row in range(self.coords[0], self.coords[2] + 1):
            for col in range(self.coords[1], self.coords[3] + 1):
                if pizzaGrid[row][col] == 'T':
                    countT += 1
                elif pizzaGrid[row][col] == 'M':
                    countM += 1
                elif pizzaGrid[row][col] == 'X':
                    return False
        return countT >= minIngredients and countM >= minIngredients

    def overlaps(self, anotherSlice):
        return (
            (self.coords[3] < anotherSlice.coords[1]) or
            (anotherSlice.coords[3] < self.coords[1]) or
            (self.coords[2] < anotherSlice.coords[0]) or
            (anotherSlice.coords[2] < self.coords[0])
        )

    def size(self):
        return (self.coords[2] + 1 - self.coords[0])*(self.coords[3] + 1 - self.coords[1]) 


def readFile(inputFilepath):
    with open(inputFilepath, 'r') as inputFile:  
        fullFile = inputFile.read().split('\n')

    data = [int(x) for x in fullFile[0].split(' ')]
    rows, cols, minIngredients, maxCells = data[0], data[1], data[2], data[3]
    grid = []
    for i in range(rows):
        grid.append(list(fullFile[i + 1]))

    return Pizza(grid, maxCells, minIngredients)


def writeFile(outputFilepath, slices):
    with open(outputFilepath, 'w') as outputFile:
        outputFile.write('{}\n'.format(len(slices)))
        for slice in slices:
            outputFile.write('{} '.format(slice))
            if slice != slices[-1]:
                outputFile.write('\n')


def main():
    pizza = readFile(sys.argv[1])
    soln = []
    currentScore = -1

    for i in range(3):
        pizza.greedyApproach()
        score = pizza.calculateScore()
        if score > currentScore:
            soln = deepcopy(pizza.slices)
            currentScore = score
        pizza.reset()

    writeFile(sys.argv[2], soln)


if __name__ == '__main__':
    main()