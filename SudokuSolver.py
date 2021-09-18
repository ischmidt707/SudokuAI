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

    def count():
        operations += 1


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


class Puzzle:
    def __init__(self, filename):
        self.board = self.importPuzzle(filename)

    def importPuzzle(self, filename):
        with open(filename) as pfile:
            puzzle = np.zeros((9, 9), dtype=int)
            puzzle_reader = csv.reader(pfile, delimiter=',')
            line = 0
            for row in puzzle_reader:
                for i in range(0, 9):
                    print(i)
                    if row[i] in ("1", "2", "3", "4", "5", "6", "7", "8", "9"):
                        puzzle[line, i] = int(row[i])
                line += 1
                print(puzzle)
        return puzzle


test = Puzzle("puzzles/Easy-P1.csv")
print(test.board)


class Main:
    pass
