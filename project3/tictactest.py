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
        
    def __str__(self):
        output = ""
        output += "columns\n" + str(self.cols) + "\n"
        output += "rows\n" + str(self.rows) + "\n"
        output += "left Diagonal: " + str(self.left_diag) +"\n"
        output += "right Diagonal: " + str(self.right_diag) +"\n"
        return output
        

class Grid():
    def __init__(self,col_offset,row_offset,length):
        self.col_offset = -col_offset
        self.row_offset = -row_offset
        self.length = length
        self.grid = np.zeros((length,length))
        self.crd = CRD()
        self.update_CRD()
        
    def __str__(self):
        output = ""
        output += "grid x: " + str(self.col_offset) + "\n"
        output  += "grid y: " + str(self.row_offset) + "\n"
        output += str(self.grid) + "\n"
        output += str(self.crd) +"\n"
        output += "winner: " + str(self.check_win())
        return output
        
    def apply_move(self,row,col,piece):
        col_coord = col - self.col_offset
        row_coord = row - self.row_offset
        if col_coord < self.length and row_coord < self.length:
            self.grid[row_coord,col_coord] = piece
            self.update_CRD()
            
            
            
    def update_CRD(self):
      
        #check rows/columns
        for i in range(self.length):
            col_total = np.sum(self.grid,0)[i]
            row_total = np.sum(self.grid,1)[i]
            
            self.crd.cols[i] = col_total
            self.crd.rows[i] = row_total
        
        #check diagonals
        left_total = 0
        right_total = 0
        for i in range(self.length):
            left_total += self.grid[i,i]
            right_total += self.grid[i,self.length-i-1]
        
        self.crd.left_diag = left_total
        self.crd.right_diag = right_total
        
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
                
    def print_game(self,sub_grids=False):
        
        print(self.full_grid)
        print( "winner: " + str(self.check_win()))
        print()
        
        if(sub_grids):
            for grid in self.grids:
                print(grid)
                print()

    def apply_move(self,row,col,piece):
        
        self.full_grid.apply_move(row,col,piece)
        
        for grid in self.grids:
            grid.apply_move(row,col,piece)
            
    def check_win(self):

        for grid in self.grids:
            result = grid.check_win()
            if result != 0:
                return result
            
        return 0


class Player():
    
    def __init__(self,piece):
        self.piece = piece
        
    def make_move(self,game):
        col_choice = -1
        row_choice = -1
        s = self.piece #sign conversion
        
        # determine which row and column to move
        
        
        # col_totals = dict()
        # row_totals = dict()
        # diag_totals = dict()
        
        # # initialize total lookups
        # for i in range(0,game.target+1):
        #     col_totals[i] = []
        #     row_totals[i] = []
        #     diag_totals[i] = []
        
        
        spaces = dict()  

        for row in range(game.boardsize):
            for col in range(game.boardsize):
                
                if game.full_grid[row,col] == 0: # only consider empty spaces
                    n_values = dict()
                    
                    target_max = game.target-1
                    target_min = 0
                    
                    for n in range(target_max,target_min-1,-1):
                        n_values[n] = 0
                        n_values[-n] = 0
                        for grid in game.grids:
                            if grid.crd.cols[col] == n:
                                n_values[n] += 1
                            elif grid.crd.cols[col] == -n:
                                n_values[-n] += 1
                                
                            if grid.crd.rows[row] == n:
                                n_values[n] += 1
                            elif grid.crd.rows[row] == -n:
                                n_values[-n] += 1
                            
                            
                            if row+grid.row_offset == col+grid.col_offset: # consider left diagonal
                                pass
                                
                        
                    
                    spaces[(row,col)] = n_values

        
        
        return row_choice,col_choice,self.piece
        
    

game = Game(4,3)
#game.print_game()

game.apply_move(1,1,-1)
#game.print_game()
game.apply_move(3,1,-1)
game.apply_move(0,0,-1)
game.apply_move(2,2,-1)
game.apply_move(0,3,1)
game.apply_move(1,3,1)
game.apply_move(2,3,1)
game.print_game()

game = Game(3,3)
p1 = Player(1)
p2 = Player(-1)

game.print_game()
