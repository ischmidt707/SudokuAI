"""
Project 1 for CSCI 446

Isaac Schmidt and Nic Dzomba

Description: Testing implementations of 5 different AI algorithms for
solving sudoku puzzles of a range of difficulties.
"""

import numpy as np
import csv


class ConstraintSolver:
    def __init__(self):
        self.operations = 0

    def count(self):
        self.operations += 1

    def solve(self):
        pass


class BacktrackSimple(ConstraintSolver):
    def __init__(self):
        super().__init__()


class BacktrackFWCheck(ConstraintSolver):
    def __init__(self):
        super().__init__()


class BacktrackArcCons(ConstraintSolver):
    def __init__(self):
        super().__init__()


class LocalSearchSAMC(ConstraintSolver):
    def __init__(self):
        super().__init__()


class LocalSearchGenetic(ConstraintSolver):
    def __init__(self):
        super().__init__()


# puzzle class used to input and store the puzzles being solved
class Puzzle:
    def __init__(self, filename):
        self.board = self.importPuzzle(filename)

    # import puzzle from csv file into 2d int array, where 0's replace ? from input file
    def importPuzzle(self, filename):
        with open(filename) as pfile:
            puzzle = np.zeros((9, 9), dtype=int)
            puzzle_reader = csv.reader(pfile, delimiter=',')
            line = 0
            for row in puzzle_reader:
                for i in range(0, 9):
                    if row[i] in ("1", "2", "3", "4", "5", "6", "7", "8", "9"):
                        puzzle[line, i] = int(row[i])
                line += 1
        return puzzle

    def printPuzzle(self):
        print(self.board)


test = Puzzle("puzzles/Easy-P1.csv")
test.printPuzzle()


class Main:

    def __init__(self):
        pass

    def main(self):
        pass
