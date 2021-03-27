# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 17:37:38 2021

@author: ithari42
"""

import numpy as np

from crd import CRD
from grid import Grid

class Game():
    def __init__(self,game_id,boardsize,target):
        self.game_id = game_id
        self.boardsize = boardsize
        self.target = target
        self.last_move = ""
        self.full_grid = Grid(0,0,boardsize,True)
        self.grids = []
        self.turncount = 0
        self.make_grids()
        self.space_values = dict()
        self.update_space_values()
        
    
    def make_grids(self):
        
        m = self.boardsize
        n = self.target
        
        for i in range(m-n+1):
            for j in range(m-n+1):
                self.grids.append(Grid(j,i,n))
                #print(j,i)
                
    def update_space_values(self):
        self.space_values = dict()
        
        for row in range(self.boardsize):
            for col in range(self.boardsize):
                space = self.full_grid.grid[row,col]
                #self.space_values[(row,col)] = dict()
                if space == 0:
                    
                    max_target = self.target-1
                    min_target = -max_target
                    
                    values = dict()
                    for i in range(max_target,min_target-1,-1):
                        values[i] = 0
                    
                                       
                    for grid in self.grids:

                        t_row,t_col = grid.translate_rc(row,col)
                        
                        # print(t_row,t_col)
                        if t_row == -1: # verify space falls within subgrid
                            continue
                        # determine what the row value for the space is in this subgrid
                        if abs(grid.crd.rows[t_row]) == grid.crd.abs_rows[t_row]:
                            value = grid.crd.rows[t_row]
                            values[value] += 1
                            
                        # determine what the col value for the space is in this subgrid  
                        if abs(grid.crd.cols[t_col]) == grid.crd.abs_cols[t_col]:
                            value = grid.crd.cols[t_col]
                            values[value] += 1

                        # determine what the leftd value for the space is in this subgrid
                        if t_row == t_col and abs(grid.crd.left_diag) == grid.crd.abs_left:
                        #if t_row == t_col:
                            value = grid.crd.left_diag
                            values[value] += 1
                        # determine what the rightd value for the space is in this subgrid
                        #if t_row == (grid.length-t_col-1) and abs(grid.crd.right_diag) == grid.crd.abs_right:
                        if t_row == (grid.length-t_col-1):
                            value = grid.crd.right_diag
                            values[value] += 1
                            
                    self.space_values[(row,col)] = values
                            
                        
                    
                
    def print_game(self,sub_grids=False):
        
        print("\n-------------------------\n")
        
        if(sub_grids):
            for grid in self.grids:
                print(grid)
                print()
                
        print(self.full_grid)
        # for space in self.space_values:
        #     print(space,self.space_values[space])
        print("Turn:",self.turncount)
        print( "winner: " + str(self.check_win()))
        print()
                
        
        print("\n-------------------------\n")

    def apply_move(self,row,col,piece):
        
        self.full_grid.apply_move(row,col,piece)
        
        for grid in self.grids:
            grid.apply_move(row,col,piece)
            
        self.update_space_values()
        self.turncount += 1
            
    def check_win(self):

        for grid in self.grids:
            result = grid.check_win()
            if result != 0:
                return result
            
        return 0
