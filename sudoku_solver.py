# -*- coding: utf-8 -*-
"""
Created on Tue May 12 18:03:46 2020

@author: andrew watterson
"""
import itertools as it
import numpy as np


def which_square(row, col):
    """Finds the 3x3 box of row, col position.
    boxes are left to right top to bottom of Sudoku"""
    return (row // 3)*3 + (col // 3)


def check_square(possible_solutions, output, row, col, square_dict):
    """Function will check sudoku box of the row, col cell, and remove any
    locked in numbers from that square from the possible_solutions for that cell"""
    square = which_square(row, col)
    conflicts = list()

    for row_compare, c_compare in square_dict[square]:
        if output[row_compare][c_compare] > 0:
            conflicts.append(output[row_compare][c_compare])
    for i in conflicts:
        if (i in possible_solutions[(row, col)]) & (len(possible_solutions[(row, col)]) > 1):
            possible_solutions[(row, col)].remove(i)
        #print(possible_solutions[(row,col)])
    #if (row==0) & (col==4):
    #    print(possible_solutions[(0,4)])
    return possible_solutions

def check_row(possible_solutions, output, row, col):
    """scan the row to see the locked in numbers of the row and remove these as possible solutions
    Function will also check Possible solutions with other cells in the row to decide if this is
    the only remaining position for that number"""
    conflicts = list()
    for c_compare in range(9):
        if output[row][c_compare] > 0:
            conflicts.append(output[row][c_compare])
    for i in conflicts:
        if (i in possible_solutions[(row, col)]) & (len(possible_solutions[(row, col)]) > 1):
            possible_solutions[(row, col)].remove(i)
        #Check if this is the only solution left in the row.
    for possible_solution in possible_solutions[(row, col)]:
        row_options = [possible_solutions[(row, key)] for key in \
                      it.chain(range(0, col), range(col+1, 9))] #flatten list within list
        row_options = [item for sublist in row_options for item in sublist]
        if possible_solution not in row_options:
            #print(row,col,possible_solution)
            possible_solutions[(row, col)] = [possible_solution]
    return possible_solutions

def check_col(possible_solutions, output, row, col):
    """scan the column to see the locked in numbers of the row and remove
    these as possible solutions.
    Function will also check Possible solutions with other cells in the column
    to decide if this is the only remaining position for that number."""
    conflicts = list()
    #print(possible_solutions[(row,col)])
    for r_compare in range(9):
        if output[r_compare][col] > 0:
            conflicts.append(output[r_compare][col])
    for i in conflicts:
        if (i in possible_solutions[(row, col)]) & (len(possible_solutions[(row, col)]) > 1):
            possible_solutions[(row, col)].remove(i)
        #print(possible_solutions[(row,col)])

    #Check if this is the only solution left in the col.
    for possible_solution in possible_solutions[(row, col)]:
        #find all the possible solutions in all the surrounding cells in this column
        col_options = [possible_solutions[(key, col)] for key in \
                       it.chain(range(0, row), range(row+1, 9))]
        #flatten list within list
        col_options = [item for sublist in col_options for item in sublist]
        # possible_solutions[(row,c_compare)])
        if possible_solution not in col_options:
            #print(row,col,possible_solution)
            possible_solutions[(row, col)] = [possible_solution]
    return possible_solutions


def extract_sudoku_problems():
    """"Extracts Sudoku puzzles and solutions from csv and reformats them as 9x9 squares"""
    quizzes_local = np.zeros((1000, 81), np.int32)
    solutions_local = np.zeros((1000, 81), np.int32)
    for i, line in enumerate(open('sudoku.csv', 'r').read().splitlines()[1:1001]):
        quiz_local, solution_local = line.split(",")
        for j, single_q_s in enumerate(zip(quiz_local, solution_local)):
            single_quiz_number, single_sudoku_number = single_q_s
            quizzes_local[i, j] = single_quiz_number
            solutions_local[i, j] = single_sudoku_number
    quizzes_local = quizzes_local.reshape((-1, 9, 9))
    solutions_local = solutions_local.reshape((-1, 9, 9))
    return quizzes_local, solutions_local

def initialise_square():
    """Tupules for every location on the sudoku with all the posible numbers for that location
    Initialised so that every number is possible at the start."""
    square_dict = dict()
    possible_solutions = {}
    for row in range(9):
        for col in range(9):
            #if row,
            #Square = 3
            #print(i)
            possible_solutions[(row, col)] = list(range(1, 10))
            square_num = which_square(row, col)
            #Square.update({s: (row,col)})
            #Square[s] = (row,col)
            if square_num in square_dict:
                # append the new number to the existing array at this slot
                square_dict[square_num].append((row, col))
            else:
                # create a new array in this slot
                square_dict[square_num] = [(row, col)]
    return square_dict, possible_solutions

def solve_puzzle(uanswered_puzzle):
    """"Solves Sudoku puzzle"""
    calculated_solution = uanswered_puzzle.copy()
    square_dict, possible_solutions = initialise_square()
    iteration = 0
    while np.count_nonzero(calculated_solution) < np.size(calculated_solution):
        iteration = iteration + 1
        for row in range(9):
            for col in range(9):
                if calculated_solution[row][col] == 0:
                    #Check internal square
                    possible_solutions = check_square(possible_solutions, calculated_solution, \
                                                    row, col, square_dict)
                    #Check Rows
                    possible_solutions = check_row(possible_solutions, calculated_solution, \
                                                   row, col)
                    #Check Column
                    possible_solutions = check_col(possible_solutions, calculated_solution, \
                                                   row, col)

                else:
                    possible_solutions[(row, col)] = []
                if len(possible_solutions[(row, col)]) == 1:
                    calculated_solution[row][col] = possible_solutions[(row, col)][0]
    return calculated_solution

if __name__ == '__main__':
    correctly_answered = 0
    QUIZZES, SOLUTIONS = extract_sudoku_problems()

    for Sd in range(len(QUIZZES)):
        quiz = QUIZZES[Sd, :, :].copy()

        solved_solution = solve_puzzle(quiz)

        if np.all(solved_solution == SOLUTIONS[Sd, :, :]):
            correctly_answered += 1

    print(f'Solved {correctly_answered}/{len(QUIZZES)} Sudoku Puzzles correctly')
          