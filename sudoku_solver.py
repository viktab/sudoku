#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 14:17:22 2020

@author: vik
"""

import math

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
    
    
        
game = Sudoku([[2, 0, 0, 0, 8, 0, 0, 0, 3], 
              [0, 9, 0, 0, 0, 0, 5, 0, 8],
              [0, 0, 0, 0, 0, 0, 0, 6, 0],
              [4, 0, 2, 0, 9, 7, 0, 0, 0],
              [0, 6, 0, 0, 0, 0, 8, 0, 0],
              [3, 0, 0, 0, 0, 0, 0, 5, 0],
              [6, 4, 7, 0, 0, 0, 0, 3, 0],
              [0, 0, 3, 0, 0, 0, 0, 0, 7],
              [0, 5, 0, 0, 6, 0, 2, 8, 0]])