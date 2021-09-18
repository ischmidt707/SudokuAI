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


class ConstraintSolver:
    def __init__(self, puzzle):
        self.operations = 0
        # create copy of puzzle object with new pointer to ensure puzzle from main not changed
        self.puzzle = copy.deepcopy(puzzle)

    # count number of operations to provide hardware independent evaluation of algorithm efficiency
    def addOp(self):
        self.operations += 1

    # solve method will be overridden in all subclasses
    def solve(self):
        print("Solve needs to be overridden.")

    # check if puzzle is solved (i.e, no zeros remain on board)
    def isSolved(self):
        return np.all(self.puzzle.board)

    # check if all constraints of the puzzle are met with new value added
    def constraintCheck(self, x, y, val):
        # check if there are duplicates in row
        for i in range(0, 9):
            if (self.puzzle.board[x, i] == val):
                return False
        # check if there are duplicates in column
        for i in range(0, 9):
            if (self.puzzle.board[i, y] == val):
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


# all specific solvers have constraintsolver as superclass

# simple backtracking
class BacktrackSimple(ConstraintSolver):
    def __init__(self, puzzle):
        super().__init__(puzzle)

    # actual backtracking portion
    def backtrack(self):
        if self.isSolved():
            return True
        pass
    # solve method overridden
    def solve(self):
        return self.backtrack(self)

# backtracking with forward checking
class BacktrackFWCheck(ConstraintSolver):
    def __init__(self, puzzle):
        super().__init__(puzzle)


# backtracking with arc consistentcy
class BacktrackArcCons(ConstraintSolver):
    def __init__(self, puzzle):
        super().__init__(puzzle)


# simulated annealing with miinum conflict heuristic
class LocalSearchSAMC(ConstraintSolver):
    def __init__(self, puzzle):
        super().__init__(puzzle)


# genetic algorithm w/ penalty function and tournament selection
class LocalSearchGenetic(ConstraintSolver):
    def __init__(self, puzzle):
        super().__init__(puzzle)


# puzzle class used to input and store the puzzles being solved
class Puzzle:
    def __init__(self, filename):
        # domain of possible values for solution
        self.domain = np.zeros((9, 9), dtype=np.ndarray)
        # values currently on board
        self.board = np.zeros((9, 9), dtype=int)
        self.importPuzzle(filename)

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
                        self.domain[line][i] = [1,2,3,4,5,6,7,8,9]
                line += 1

    # print puzzle into console
    def printPuzzle(self):
        print(self.board)
        print(self.domain)


test = Puzzle("puzzles/Easy-P1.csv")
test.printPuzzle()


class Main:

    def __init__(self):
        pass

    def main(self):
        pass
