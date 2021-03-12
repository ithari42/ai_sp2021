# -*- coding: utf-8 -*-
"""
Created on Thu Mar 11 20:03:27 2021

@author: Jonathan Pritchett
"""

import numpy as np




class CRD():
    
    def __init__(self):
        self.cols = dict()
        self.rows = dict()
        self.left_diag = 0
        self.right_diag = 0
        
        

class Grid():
    def __init__(self,x_offset,y_offset,length):
        self.x_offset = -x_offset
        self.y_offset = -y_offset
        self.length = length
        self.grid = np.zeros((length,length))
        self.crd = CRD()
        
    def apply_move(self,x,y,piece):
        x_coord = x - self.x_offset
        y_coord = y - self.y_offset
        if x_coord < self.length and y_coord < self.length:
            self.grid[y_coord,x_coord] = piece
            self.update_CRD()
            
            
            
    def update_CRD():
      
        #check rows/columns
        for i in range(length):
            col_total = np.sum(self.grid,0)[i]
            row_total = np.sum(self.grid,1)[i]
            
            self.crd.rows[i] = col_total
            self.crd.cols[i] = row_total
        
        #check diagonals
        left_total = 0
        right_total = 0
        for i in range(length):
            left_total += self.grid[i,i]
            right_total += self.grid[i,length-i]
            
        self.crd.left_diag = left_total
        self.crd.right_diag = right_total
        
        return piece_wins


class Game():
    def __init__(self,boardsize,target):
        self.boardsize = boardsize
        self.target = target
        self.full_grid = Grid(0,0,boardsize)
        self.grids = []
        self.make_grids()
    
    def make_grids(self):
        
        m = self.boardsize
        n = self.target
        
        for i in range(m-n+1):
            for j in range(m-n+1):
                self.grids.append(Grid(j-1,i-1,n))
                
    def print_game(self):
        
        print(self.full_grid.grid)
        print()
        
        for grid in self.grids:
            print(grid.grid)
            print()

    def apply_move(self,x,y,piece):
        
        self.full_grid.apply_move(x,y,piece)
        
        for grid in self.grids:
            grid.apply_move(x,y,piece)
            
    def check_win(self):
        
        for grid in self.grids:
            result = grid.check_win()


game = Game(4,3)
game.print_game()

game.apply_move(1,1,1)
game.print_game()
game.apply_move(3,1,-1)
game.print_game()


