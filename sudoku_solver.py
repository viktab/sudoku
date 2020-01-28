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

class Sudoku:
    def __init__(self, array):
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
                    
    def pos_from_square(self, square, index):
        min_row = math.floor(square/3)*3
        min_col = (square%3)*3
        add_col = math.floor(index/3)
        add_row = index%3
        return (min_col + add_col, min_row + add_row)
    
    def square_from_pos(self, pos):
        (i, j) = pos
        n = math.floor(j/3)
        m = math.floor(i/3)
        a = n*3+m
        b = (i%3)*3 + (j%3)
        return a, b
                    
    def place_number(self, spot, num):
        (i, j) = spot
        self.rows[j][i] = num
        self.cols[i][j] = num
        a, b = self.square_from_pos(spot)
        self.squares[a][b] = num
    
    def assign_domains(self):
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
#                    print((i, j))
#                    print(remove)
#                    print(new_allowed)
                    if len(new_allowed) == 1:
                        self.place_number((i, j), list(new_allowed)[0])
                        self.allowed[(i, j)] = set()
                    else:
                        self.allowed[(i, j)] = new_allowed
                        
    def check_squares(self):
        for a in range(8):
            print(a)
            print(self.squares[a])
            missing_numbers = list({1,2,3,4,5,6,7,8,9}.difference(set(self.squares[a])))
            for num in range(9):
                if num not in self.squares[a]:
                    # print("num: " + str(num))
                    spots = 0
                    for b in range(9):
                        # print(a, b)
                        pos = self.pos_from_square(a, b)
                        print(pos, self.allowed[pos])
                        if num in self.allowed[pos]:
                            print('plus 1')
                            spots += 1
                            spot = pos
                    print(num, spots)
                    if spots == 1:
                        print(a, b, num)
                        self.place_number(spot, num)
                        self.allowed[spot] = set()
                        
    def check_blocked_cols(self):
        for a in range(9):
            missing_numbers = list({1,2,3,4,5,6,7,8,9}.difference(set(self.squares[a])))
            for missing in missing_numbers:
                cols_allowed = set()
                for b in range(9):
                    pos = self.pos_from_square(a, b)
                    if missing in self.allowed[pos]:
                        cols_allowed.add(pos[1])
                if len(cols_allowed) == 1:
#                    print('yeet')
#                    print(a)
#                    print(missing)
#                    print(cols_allowed)
                    j = list(cols_allowed)[0]
                    for i in range(9):
                        square, z = self.square_from_pos((i, j))
                        if square != a and missing in self.allowed[(i, j)]:
                            self.allowed[(i, j)].remove(missing)
    
    def check_blocked_rows(self):
        for a in range(2):
            print('a: ' + str(a))
            missing_numbers = list({1,2,3,4,5,6,7,8,9}.difference(set(self.squares[a])))
            for missing in missing_numbers:
                print("num: " + str(missing))
                rows_allowed = set()
                for b in range(9):
                    pos = self.pos_from_square(a, b)
                    print(pos)
                    if missing in self.allowed[pos]:
                        print("in pos: " + str(pos))
                        rows_allowed.add(pos[0])
                if len(rows_allowed) == 1:
                    i = list(rows_allowed)[0]
                    for j in range(9):
                        square, z = self.square_from_pos((i, j))
                        if square != a and missing in self.allowed[(i, j)]:
                            self.allowed[(i, j)].remove(missing)
                            print((i, j))
                            print('allowed')
                            print(self.allowed[(i, j)])
                        
    def start(self):
        prev = deepcopy(self.rows)
        finding = True
        i = 0
        while finding:
            self.assign_domains()
            self.check_squares()
            if prev == self.rows:
                finding = False
            prev = deepcopy(self.rows)
            i += 1
        print(self.allowed)
        print(self.rows)
        print("after " + str(i) + " iteration(s) of checking for domains with only 1 number")
        # self.check_blocked_cols()
#        self.check_blocked_rows()
#        prev = deepcopy(self.rows)
#        finding = True
#        i = 0
#        while finding:
#            self.assign_domains()
#            self.check_squares()
#            if prev == self.rows:
#                finding = False
#            prev = deepcopy(self.rows)
#            i += 1
#        print(self.rows)
#        print(i)
#        print("after checking for blocked rows and columns")
        
        
game = Sudoku(hard2)
    
game.start()