import sys


class Pizza():
    def __init__(self, grid, maxSliceSize, minIngredients):
        self.grid = grid
        self.maxSliceSize = maxSliceSize
        self.minIngredients = minIngredients
        self.slices = []

    def findBest(self):
        possibleSlicesSolution = []


    def cutSlice(self, rowStart, colStart, rowFinish, colFinish):
        return Slice(rowStart, colStart, rowFinish, colFinish)

    def checkValidity(self, proposedSlices):
        areValidSlices = all(slice.isValidSlice(self.grid, self.minIngredients) for slice in proposedSlices)
        noOverlaps = True
        for slice in proposedSlices:
            for otherSlice in proposedSlices:
                if slice != otherSlice:
                    noOverlaps = noOverlaps and not slice.overlaps(otherSlice)
        return areValidSlices and noOverlaps

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
        countT = 0
        countM = 0
        for row in range(self.coords[0], self.coords[2] + 1):
            for col in range(self.coords[1], self.coords[3] + 1):
                if pizzaGrid[row][col] == 'T':
                    countT += 1
                elif pizzaGrid[row][col] == 'M':
                    countM += 1
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

    # Some awesome algorithm here
    pizza.slices = [Slice(0, 0, 2, 1)]
    print(pizza.slices[0].isValidSlice(pizza.grid, pizza.minIngredients)) 

    writeFile(sys.argv[2], pizza.slices)


if __name__ == '__main__':
    main()