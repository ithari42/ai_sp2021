# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 17:37:38 2021

@author: ithari42
"""

import numpy as np

from crd import CRD


class Grid():
    def __init__(self,col_offset,row_offset,length,is_full_grid=False):
        self.col_offset = -col_offset
        self.row_offset = -row_offset
        self.length = length
        self.grid = np.zeros((length,length))
        self._is_full_grid = is_full_grid
        self.crd = CRD()
        self.update_CRD()
        
    def __str__(self):
        output = ""
        if( not self._is_full_grid):
            output += "grid x: " + str(self.col_offset) + "\n"
            output  += "grid y: " + str(self.row_offset) + "\n"
            output += str(self.grid) + "\n"
            #output += str(self.crd) +"\n"
            output += "winner: " + str(self.check_win())
        else:
            output += str(self.grid) + "\n"
            #output += str(self.crd) +"\n"
        return output
        
    def translate_rc(self,row,col):
        t_row = row + self.row_offset
        t_col = col + self.col_offset
        # print("\nx-o","y-o")
        # print(self.row_offset,self.col_offset)
        # print("row","t_row")
        # print(row,t_row)
        # print("col","t_col")
        # print(col,t_col)
        if (t_row >= self.length or t_col >= self.length):
            return -1,-1
        elif(t_row < 0 or t_col < 0):
            return -1,-1
        else:
            return t_row,t_col
    
    
    def apply_move(self,row,col,piece):
        col_coord = col + self.col_offset
        row_coord = row + self.row_offset
        if col_coord < self.length and row_coord < self.length and col_coord >= 0 and row_coord >= 0:
            self.grid[row_coord,col_coord] = piece
            self.update_CRD()
            
            
            
    def update_CRD(self):
      
        #check rows/columns
        
        col_sum = np.sum(self.grid,0)
        row_sum = np.sum(self.grid,1)
        
        abs_grid = np.abs(self.grid)
        abs_col_sum = np.sum(abs_grid,0)
        abs_row_sum = np.sum(abs_grid,1)
        
        for i in range(self.length):
            
            self.crd.cols[i] = col_sum[i]
            self.crd.rows[i] = row_sum[i]
            
            self.crd.abs_cols[i] = abs_col_sum[i]
            self.crd.abs_rows[i] = abs_row_sum[i]
        
        #check diagonals
        left_sum = 0
        right_sum = 0
        abs_left_sum = 0
        abs_right_sum = 0
        
        for i in range(self.length):
            left_sum += self.grid[i,i]
            right_sum += self.grid[i,self.length-i-1]
            
            abs_left_sum += abs_grid[i,i]
            abs_right_sum += abs_grid[i,self.length-i-1]
        
        self.crd.left_diag = left_sum
        self.crd.right_diag = right_sum
        
        self.crd.abs_left = abs_left_sum
        self.crd.abs_right = abs_right_sum
        
    def check_win(self):
        

        for row_sum in self.crd.rows.values():
            if row_sum == self.length:
                return 1
            elif row_sum == -self.length:
                return -1
        for col_sum in self.crd.cols.values():
            if col_sum == self.length:
                return 1
            elif col_sum == -self.length:
                return -1
        if self.crd.left_diag == self.length:
            return 1
        elif self.crd.left_diag == -self.length:
            return -1
        
        if self.crd.right_diag == self.length:
            return 1
        elif self.crd.right_diag == -self.length:
            return -1
        
        return 0

