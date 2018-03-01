import sys


def readInput():
    '''
    Read input and parse according to structure
    '''
    with open(sys.argv[1], 'r') as inputFile:  
        fullFile = inputFile.read().split('\n')
    # Problem specific stuff here
    # ...


def writeOutput(solution):
    '''
    Write output in required form
    '''
    with open(sys.argv[2], 'w') as outputFile:
        outputFile.write(solution)


def main():
    readInput()
    # Magic here...
    solution = 'Hooray!'
    writeOutput(solution)


if __name__ == '__main__':
    main()
