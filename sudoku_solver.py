#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 14:17:22 2020

@author: vik
"""

import math
from copy import deepcopy

med = [[0, 4, 0, 6, 0, 1, 0, 0, 0],
       [3, 0, 7, 9, 4, 8, 0, 5, 6],
       [0, 0, 8, 7, 5, 0, 0, 4, 0],
       [0, 0, 0, 1, 8, 6, 3, 0, 0],
       [9, 0, 5, 0, 3, 0, 0, 0, 0],
       [8, 0, 6, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 8, 0, 0, 0, 6, 0],
       [0, 0, 0, 0, 0, 9, 4, 0, 8],
       [6, 0, 0, 4, 0, 0, 0, 1, 2]]

hard = [[0, 0, 3, 0, 0, 0, 0, 0, 0],
        [2, 0, 0, 0, 0, 8, 3, 0, 7],
        [0, 0, 0, 1, 5, 0, 0, 0, 4],
        [0, 0, 1, 0, 0, 0, 0, 0, 0],
        [0, 2, 0, 7, 0, 0, 0, 0, 6],
        [0, 0, 5, 8, 0, 6, 0, 1, 3],
        [8, 3, 7, 0, 0, 0, 0, 0, 2],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 6, 0 ,0, 0, 2, 7, 0, 8]]

hard2 = [[0, 0, 1, 5, 9, 0, 6, 0, 0],
         [0, 6, 0, 2, 3, 0, 4, 5, 0],
         [9, 0, 0, 0, 0, 0, 0, 0, 0],
         [4, 0, 0, 0, 0, 0, 1, 6, 0],
         [0, 3, 0, 0, 0, 0, 0, 7, 0],
         [0, 0, 0, 7, 0, 0, 0, 9, 3],
         [0, 0, 4, 0, 0, 0, 0, 0, 0],
         [3, 7, 2, 4, 0, 0, 0, 1, 5],
         [1, 0, 0, 0, 0, 0, 0, 0, 0]]

expert = [[0, 1, 0, 0, 7, 0, 0, 0, 0],
          [5, 0, 2, 4, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 4, 0, 0],
          [3, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 7, 0, 0, 5, 3, 0, 8],
          [0, 0, 8, 0, 0, 0, 9, 0, 0],
          [0, 8, 0, 0, 1, 7, 5, 0, 3],
          [0, 2, 0, 5, 0, 9, 0, 8, 0],
          [1, 7, 0, 0, 0, 8, 0, 4, 0]]

expert2 = [[4, 0, 7, 0, 0, 0, 0, 8, 0],
           [0, 8, 0, 0, 0, 0, 3, 4, 0],
           [0, 0, 0, 8, 5, 0, 0, 0, 7],
           [0, 2, 0, 0, 9, 0, 0, 3, 0],
           [5, 3, 0, 0, 0, 0, 2, 0, 0],
           [0, 0, 9 ,0, 6, 0, 5, 0, 0],
           [0, 0, 0, 0, 0, 0, 6, 2, 0],
           [7, 9, 0, 0, 0, 2, 0, 0, 0],
           [3, 0, 0, 0, 0, 0, 0, 0, 9]]

steps = 0
backtracks = 0

class Sudoku:
    def __init__(self, array):
        """
        rows: each list is a row (0 means empty)
        cols: each list is a column
        squares: each list is a square (squares read left to right then down
                    but within a square indeces read top to bottom then right)
        allowed: dict mapping each position to a set of numbers that can 
                    still be placed there without breaking any rules. Empty set means 
                    a number has been assigned to that position
        """
        self.rows = array
        self.cols = [[],[],[],[],[],[],[],[],[]]
        for i in range(9):
            for j in range(9):
                self.cols[j].append(array[i][j])
        self.squares = [[],[],[],[],[],[],[],[],[]]
        for i in range(9):
            for j in range(9):
                n = math.floor(j/3)
                m = math.floor(i/3)
                index = n*3+m
                self.squares[index].append(self.rows[j][i])
        self.allowed = {}
        for i in range(9):
            for j in range(9):
                if self.rows[j][i] != 0:
                    self.allowed[(i, j)] = set()
                else:
                    self.allowed[(i, j)] = {1,2,3,4,5,6,7,8,9}
                    
    def copy(self):
        """
        Return a copy of itself
        """
        new_game = Sudoku(deepcopy(self.rows))
        return new_game
                    
    def pos_from_square(self, square, index):
        """
        square: which 3x3 square you're in
        index: index within the square
        returns: regular position coordinates (x, y)
        """
        min_row = math.floor(square/3)*3
        min_col = (square%3)*3
        add_col = math.floor(index/3)
        add_row = index%3
        return (min_col + add_col, min_row + add_row)
    
    def square_from_pos(self, pos):
        """
        pos: position you're in
        returns
        a: which 3x3 square the position is in
        b: index of the position in said 3x3 square
        """
        (i, j) = pos
        n = math.floor(j/3)
        m = math.floor(i/3)
        a = n*3+m
        b = (i%3)*3 + (j%3)
        return a, b
                    
    def place_number(self, spot, num):
        """ 
        Updates the sudoku object so that the given number num is assigned to the given spot
        """
        global steps 
        steps += 1
        (i, j) = spot
        self.rows[j][i] = num
        self.cols[i][j] = num
        a, b = self.square_from_pos(spot)
        self.squares[a][b] = num
        
    def unsolvable(self):
        for pos in self.allowed:
            i, j = pos
            if len(self.allowed[pos]) == 0 and self.rows[j][i] == 0:
                return True
        return False
    
    def assign_domains(self):
        """
        Assign each spot in the game a set of numbers that it can be without breaking the 
        rules of the game, given the current state of the board. If any domain is reduced to 
        len 1, assign the remaining possible number to that spot
        """
        for i in range(9):
            for j in range(9):
                if self.rows[j][i] == 0:
                    row = self.rows[j]
                    col = self.cols[i]
                    n = math.floor(j/3)
                    m = math.floor(i/3)
                    a = n*3+m
                    square = self.squares[a]
                    remove = set([value for value in row if value != 0]).union([value for value in col if value != 0]).union([value for value in square if value != 0])
                    new_allowed = self.allowed[(i, j)].difference(remove)
                    if len(new_allowed) == 1:
                        self.place_number((i, j), list(new_allowed)[0])
                        self.allowed[(i, j)] = set()
                    else:
                        self.allowed[(i, j)] = new_allowed
                        
    def check_squares(self):
        """
        For each 3x3 square in the game, check if any numbers only has 1 possible spot
        that they can go in that square
        """
        for a in range(9):
            for num in range(1, 10):
                if num not in self.squares[a]:
                    spots = 0
                    for b in range(9):
                        pos = self.pos_from_square(a, b)
                        if num in self.allowed[pos]:
                            spots += 1
                            spot = pos
                    if spots == 1:
                        self.place_number(spot, num)
                        self.allowed[spot] = set()
                        
    def check_rows(self):
        """
        Same functionality as check_squares, but check each row
        """
        for j in range(9):
            for num in range(1, 10):
                if num not in self.rows[j]:
                    spots = 0
                    for i in range(9):
                        if num in self.allowed[(i, j)]:
                            spots += 1
                            spot = (i, j)
                    if spots == 1:
                        self.place_number(spot, num)
                        self.allowed[spot] = set()
        
    def check_cols(self):
        """
        Same functionality as check_squares, but check each column
        """
        for i in range(9):
            for num in range(1, 10):
                if num not in self.cols[i]:
                    spots = 0
                    for j in range(9):
                        if num in self.allowed[(i, j)]:
                            spots += 1
                            spot = (i, j)
                    if spots == 1:
                        self.place_number(spot, num)
                        self.allowed[spot] = set()
                        
    def check_blocked_cols(self):
        """
        For each square, checks if there are any unassigned numbers that can
        only possibly go in one column. If there are, removes that number from 
        the remaining empty spots in that column in the other 3x3 squares
        """
        for a in range(9):
            missing_numbers = list({1,2,3,4,5,6,7,8,9}.difference(set(self.squares[a])))
            for missing in missing_numbers:
                cols_allowed = set()
                for b in range(9):
                    pos = self.pos_from_square(a, b)
                    if missing in self.allowed[pos]:
                        cols_allowed.add(pos[1])
                if len(cols_allowed) == 1:
                    j = list(cols_allowed)[0]
                    for i in range(9):
                        square, z = self.square_from_pos((i, j))
                        if square != a and missing in self.allowed[(i, j)]:
                            self.allowed[(i, j)].remove(missing)
    
    def check_blocked_rows(self):
        """
        Similar functionality to check_blocked_cols, but checks for rows
        """
        for a in range(9):
            missing_numbers = list({1,2,3,4,5,6,7,8,9}.difference(set(self.squares[a])))
            for missing in missing_numbers:
                rows_allowed = set()
                for b in range(9):
                    pos = self.pos_from_square(a, b)
                    if missing in self.allowed[pos]:
                        rows_allowed.add(pos[0])
                if len(rows_allowed) == 1:
                    i = list(rows_allowed)[0]
                    for j in range(9):
                        square, z = self.square_from_pos((i, j))
                        if square != a and missing in self.allowed[(i, j)]:
                            self.allowed[(i, j)].remove(missing)
                
    def solve(self, backtracked = True):
        """
        Main recursion function to solve the sudoku puzzle!
        """
        
        global backtracks
        if backtracked:
            backtracks += 1
        
        # base case - unsolvable
        if self.unsolvable():
            return None
        
        # check for rules 
        prev = deepcopy(self.rows)
        finding = True
        i = 0
        while finding:
            self.assign_domains()
            self.check_squares()
            self.check_rows()
            self.check_cols()
            self.check_blocked_cols()
            self.check_blocked_rows()
            if prev == self.rows:
                finding = False
            prev = deepcopy(self.rows)
            i += 1
            
        # return if solved
        if not any(0 in x for x in self.rows):
            return self.rows
        
        # try to make a guess between two places in a square for one number
        new_game = self.copy()
        found = False
        for square in range(9):
            for num in range(1, 10):
                if num not in self.squares[square]:
                    possibilities = []
                    for b in range(9):
                        pos = self.pos_from_square(square, b)
                        if num in self.allowed[pos]:
                            possibilities.append(pos)
                    if len(possibilities) == 2:
                        p1 = possibilities[0]
                        p2 = possibilities[1]
                        number = num
                        new_game.place_number(p1, number)
                        found = True
                        break
            if found:
                break
            
        if found: 
            # recurse on the guess 
            ans = new_game.solve()
            
            # if didn't work, try the other option
            if ans is None:
                new_game = self.copy()
                new_game.place_number(p2, number)
                ans = new_game.solve()
            return ans
        
        # if couldn't make a guess between two places, try to make one between three
        else:
            new_game = self.copy()
            found = False
            for square in range(9):
                for num in range(1, 10):
                    if num not in self.squares[square]:
                        possibilities = []
                        for b in range(9):
                            pos = self.pos_from_square(square, b)
                            if num in self.allowed[pos]:
                                possibilities.append(pos)
                        if len(possibilities) == 3:
                            p1 = possibilities[0]
                            p2 = possibilities[1]
                            p3 = possibilities[2]
                            number = num
                            new_game.place_number(p1, number)
                            found = True
                            break
                if found:
                    break
                
            if found: 
                # recurse on the guess 
                ans = new_game.solve()
                
                # if didn't work, try the second option
                if ans is None:
                    new_game = self.copy()
                    new_game.place_number(p2, number)
                    ans = new_game.solve()
                    
                # if didn't work, try the third option
                if ans is None:
                    new_game = self.copy()
                    new_game.place_number(p3, number)
                    ans = new_game.solve()
                return ans
            
            # if still couldn't make a guess between three places, keep
            # picking a random number for the spot with the smallest domain
            # until you make a guess that works
            else:
                # find the position with the smallest domain
                smallest_domain = 9
                guess_pos = None
                for pos in new_game.allowed:
                    if len(new_game.allowed[pos]) < smallest_domain:
                        smallest_domain = len(new_game.allowed[pos])
                        guess_pos = pos
                # keep making guesses until got the right one
                guesses = list(new_game.allowed[pos])
                ans = None
                while ans is None:
                    if len(guesses) == 0:
                        return None
                    num = guesses.pop(0)
                    new_game = self.copy()
                    new_game.place_number(guess_pos, num)
                    ans = new_game.solve()
                return ans
        
game = Sudoku(expert2)
print(game.solve(False))
print("Solved with " + str(steps) + " insertions and " + str(backtracks) + " backtracks!")