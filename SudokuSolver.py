"""
Project 1 for CSCI 446

Isaac Schmidt and Nic Dzomba

Description: Testing implementations of 5 different AI algorithms for
solving sudoku puzzles of a range of difficulties, and evaluating performance
based on number of operations to solve.
"""

import numpy as np
import csv
import copy
import random
from queue import Queue


class ConstraintSolver:
    def __init__(self, puzzle):
        self.operations = 0
        # create copy of puzzle object with new pointer to ensure puzzle from main not changed
        self.puzzle = copy.deepcopy(puzzle)

    # count number of operations to provide hardware independent evaluation of algorithm efficiency
    def addOp(self):
        self.operations += 1

    def printBoard(self):
        print(self.puzzle.board)

    # solve method will be overridden in all subclasses
    def solve(self):
        print("Solve needs to be overridden.")

    # check if puzzle is solved (i.e, no zeros remain on board)
    # may need to be overridden in local search algs
    def isSolved(self):
        return np.all(self.puzzle.board)

    # find next location without assigned value
    def find_loc(self):
        for i in range(0, 9):
            for j in range(0, 9):
                if (self.puzzle.board[i][j] == 0):
                    return [i, j]

    # check if all constraints of the puzzle are met with new value added
    def constraintCheck(self, x, y, val):
        # check if there are duplicates in row
        for i in range(0, 9):
            if (self.puzzle.board[x][i] == val):
                return False
        # check if there are duplicates in column
        for i in range(0, 9):
            if (self.puzzle.board[i][y] == val):
                return False
        # check if there are duplicates in box
        xb = x - x % 3
        yb = y - y % 3
        for i in range(0, 3):
            for j in range(0, 3):
                if (self.puzzle.board[xb + i][yb + j] == val):
                    return False
        # all constraints pass
        return True

    #Calculating fitness of a potential solution; low scores better
    def updateFitness(self, genome):
        #We count the cell as a duplicate with itself in each check,
        # so to account for this we simply start at -(81*3)=-243 for the 3
        # false positive duplicates each cell will get.
        fit = -243
        for x in range(9):
            for y in range(9):
                # count duplicates in row
                for i in range(0, 9):
                    if (genome.board[x][i] == genome.board[x][y]):
                        fit += 1
                # count duplicates in column
                for i in range(0, 9):
                    if (genome.board[i][y] == genome.board[x][y]):
                        fit += 1
                # count duplicates in box
                xb = x - x % 3
                yb = y - y % 3
                for i in range(0, 3):
                    for j in range(0, 3):
                        if (genome.board[xb + i][yb + j] == genome.board[x][y]):
                            fit += 1
        #fitness is calculated as the sum of all constraint violations.
        genome.fitness = fit



# all specific solvers have constraintsolver as superclass

# simple backtracking
class BacktrackSimple(ConstraintSolver):
    def __init__(self, puzzle):
        super().__init__(puzzle)

    # solve method overridden
    def solve(self):
        if self.isSolved():
            return True
        var = self.find_loc()
        x = var[0]
        y = var[1]
        for val in self.puzzle.domain[x][y]:
            self.addOp()
            if self.constraintCheck(x, y, val):
                self.puzzle.board[x][y] = val
                result = self.solve()
                if result:
                    return True
                self.puzzle.board[x][y] = 0
        return False


# backtracking with forward checking
class BacktrackFWCheck(ConstraintSolver):
    def __init__(self, puzzle):
        super().__init__(puzzle)

    # removes any values at (x,y) that make in inconsistent at (a,b)
    def removeInconsistent(self, x, y, a, b):
        removed = True
        for i in self.puzzle.domain[x][y]:
            for j in self.puzzle.domain[a][b]:
                if i != j:
                    removed = False
            if removed:
                self.puzzle.domain[x][y].remove(i)
            else:
                removed = True

    # forward checking function, to be done after once each variable is chosen
    def forwardCheck(self, x, y):
        for i in range(0, 9):
            self.removeInconsistent(x, y, i, y)
        for i in range(0, 9):
            self.removeInconsistent(x, y, x, i)
        xb = x - x % 3
        yb = y - y % 3
        for i in range(0, 3):
            for j in range(0, 3):
                self.removeInconsistent(x, y, xb + i, yb + j)

    # solve method overridden
    def solve(self):
        if self.isSolved():
            return True
        var = self.find_loc()
        x = var[0]
        y = var[1]
        self.forwardCheck(x, y)
        for val in self.puzzle.domain[x][y]:
            self.addOp()
            if self.constraintCheck(x, y, val):
                self.puzzle.board[x][y] = val
                result = self.solve()
                if result:
                    return True
                self.puzzle.board[x][y] = 0
        return False


# backtracking with arc consistency
class BacktrackArcCons(ConstraintSolver):
    def __init__(self, puzzle):
        super().__init__(puzzle)

    # removes any values at (x,y) that make in inconsistent at (a,b)
    def removeInconsistent(self, x, y, a, b):
        removed = True
        for i in self.puzzle.domain[x][y]:
            for j in self.puzzle.domain[a][b]:
                if i != j:
                    removed = False
            if removed:
                self.puzzle.domain[x][y].remove(i)
            else:
                removed = True
        return removed

    def arccons(self):
        queue = Queue()

        while not queue.empty():
            pass
    # solve method overridden
    def solve(self):
        if self.isSolved():
            return True
        var = self.find_loc()
        x = var[0]
        y = var[1]
        for val in self.puzzle.domain[x][y]:
            self.addOp()
            if self.constraintCheck(x, y, val):
                self.puzzle.board[x][y] = val
                result = self.solve()
                if result:
                    return True
                self.puzzle.board[x][y] = 0
        return False


# simulated annealing with minimum conflict heuristic
class LocalSearchSAMC(ConstraintSolver):
    def __init__(self, puzzle):
        super().__init__(puzzle)


# genetic algorithm w/ penalty function and tournament selection
class LocalSearchGenetic(ConstraintSolver):
    def __init__(self, puzzle):
        super().__init__(puzzle)
        self.population = []
        self.protected = []
        self.bestFitness = 1000000
        self.leader = None

    # creating a new potential solution from scratch
    def newGenome(self):
        genome = copy.deepcopy(self.puzzle)
        for x in range(9):
            for y in range(9):
                #fill up whole board randomly
                if [x,y] not in self.protected:
                    genome.board[x][y] = random.randint(0,8)
        # keeping track of how good our best solution is
        self.updateFitness(genome)
        if genome.fitness < self.bestFitness:
            self.bestFitness = genome.fitness
            self.leader = genome
        return genome

    def initPop(self, popSize):
        for i in range(popSize):
            self.population.append(self.newGenome())

    def crossMutate(self, mutation, parent1, parent2):
        # randomly select point for cross mutation, that doesn't include the ends
        crossPoint = random.randint(1,80)
        # first, delete mutation's board and replace with parent2's board
        mutation.board = parent2.board
        # then replace the first crossPoint number of cells with parent1's cells
        for point in range(crossPoint):
            x = point % 9
            y = (point - (point % 9)) // 9
            mutation.board[x][y] = parent1.board[x][y]

        # updating fitness and checking for new leader
        self.updateFitness(mutation)
        if mutation.fitness < self.bestFitness:
            self.bestFitness = mutation.fitness
            self.leader = mutation

    def mutate(self, mutation):
        # randomly change 3 cells
        for i in range(3):
            x = random.randint(0,8)
            y = random.randint(0,8)
            if [x,y] not in self.protected:
                mutation.board[x][y] = random.randint(1,9)

        # updating fitness and checking for new leader
        self.updateFitness(mutation)
        if mutation.fitness < self.bestFitness:
            self.bestFitness = mutation.fitness
            self.leader = mutation

    def solve(self, popSize, tourneySize, iterations):
        # popSize = total population size
        # tourneySize = how many solutions we select for each tournament
        # iterations = number of times we run an evolution tournament (steady-state replacement)

        # Identifying the given values that should never be changed
        for x in range(9):
            for y in range(9):
                if self.puzzle.board[x][y] != 0:
                    self.protected.append([x,y])

        # create the beginning population
        self.initPop(popSize)
        print("starting best fitness:")
        print(self.leader.fitness)

        # select and rank a tournament subset of the population, iter times.
        for iter in range(iterations):
            selection = random.sample(self.population, tourneySize)
            rankedTourney = []
            # determine rank position
            for s in selection:
                self.updateFitness(s)
                # put genome into first position if it's the first genome to be ranked
                if not rankedTourney:
                    rankedTourney.append(s)
                else:
                    position = 0
                    while position < len(rankedTourney) and rankedTourney[position].fitness < s.fitness:
                        position += 1
                    rankedTourney.insert(position, s)
            # replace the lowest ranked genome in tournament with a cross mutation of best 2 (currently decommissioned)
            #self.crossMutate(rankedTourney[-1], rankedTourney[0], rankedTourney[1])
            #self.addOp()

            # replace lowest ranked genome with a mutation of best ranked genome
            rankedTourney[-1].board = copy.deepcopy(rankedTourney[0].board)
            self.mutate(rankedTourney[-1])
            self.addOp()




# puzzle class used to input and store the puzzles being solved
class Puzzle:
    def __init__(self, filename):
        # domain of possible values for solution
        self.domain = np.zeros((9, 9), dtype=np.ndarray)
        # values currently on board
        self.board = np.zeros((9, 9), dtype=int)
        self.importPuzzle(filename)
        # initialize fitness as very bad, for possible use later
        self.fitness = 1000000

    # import puzzle from csv file into 2d int array, where 0's replace ? from input file
    def importPuzzle(self, filename):
        with open(filename) as pfile:
            puzzle_reader = csv.reader(pfile, delimiter=',')
            line = 0
            for row in puzzle_reader:
                for i in range(0, 9):
                    if row[i] in ("1", "2", "3", "4", "5", "6", "7", "8", "9"):
                        self.board[line][i] = int(row[i])
                        self.domain[line][i] = [int(row[i])]
                    else:
                        self.domain[line][i] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                line += 1

    # print puzzle into console
    def printPuzzle(self):
        print(self.board)


test = Puzzle("puzzles/Evil-P5.csv")

solvetest = BacktrackSimple(test)
solvefwtest = BacktrackFWCheck(test)
solvetest.solve()
solvefwtest.solve()
print(solvetest.operations)
solvetest.printBoard()
print(solvefwtest.operations)
solvefwtest.printBoard()

"""
tournamentTest = LocalSearchGenetic(test)
tournamentTest.solve(100, 10, 20000)
print(tournamentTest.operations)
print(tournamentTest.leader.fitness)
print(tournamentTest.leader.board)
"""

class Main:

    def __init__(self):
        pass

    def main(self):
        pass
