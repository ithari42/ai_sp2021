# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 17:37:38 2021

@author: ithari42
"""

import numpy as np

from crd import CRD
from grid import Grid
from game import Game


class Player():
    
    def __init__(self,team_id,piece,mode="simple"):
        self.team_id = team_id
        self.piece = piece
        self.mode = mode
        
    def make_move(self,game):
        if self.mode == "simple":
            return self.simple(game)
        else:
            return self.aggressive(game)
        
        
    def simple(self,game):
        
        col_choice = -1
        row_choice = -1
        s = self.piece #sign conversion
        
        # determine which row and column to claim
        
        space_values = game.space_values
        target = game.target-1
        
        
        best_value_space = dict()
        best_value = dict()
        
        for value in range(target,-1,-1):
            best_value_space[value] = (-1,-1)
            best_value[value] = 0
            best_value_space[-value] = (-1,-1)
            best_value[-value] = 0
            for space in space_values:
                if space_values[space][value] > best_value[value]:
                    best_value_space[value] = space
                    best_value[value] = space_values[space][value]
                    
                if space_values[space][-value] > best_value[-value]:
                    best_value_space[-value] = space
                    best_value[-value] = space_values[space][-value]
                    
        for value in range(target,-1,-1):
            if best_value[s*value] > 0:
                row_choice = best_value_space[s*value][0]
                col_choice = best_value_space[s*value][1]
                break
            elif best_value[-s*value] > 0:
                row_choice = best_value_space[-s*value][0]
                col_choice = best_value_space[-s*value][1]
                break
                
                    
        if row_choice == -1 or col_choice == -1: # game will be tied, so pick any empty space
            for row in range(game.boardsize):
                for col in range(game.boardsize):
                    if game.full_grid.grid[row,col] == 0:
                        row_choice = row
                        col_choice = col
        
        return row_choice,col_choice,self.piece
        
        
    # choosing a space to claim in an aggressive manner, prioritizing
    # creating oppurtunities to win over preventing the opponent from winning
    def aggressive(self,game):
        
        col_choice = -1
        row_choice = -1
        s = self.piece #sign conversion
        
        # determine which row and column to claim
        
        space_values = game.space_values
        target = game.target-1
        
        
        best_space = dict()
        best_value = dict()
        
        for value in range(target,-1,-1):
            
            for space in space_values:
                
                if value == target and space[s*value] > 0: #if the player has an oppurtunity to win take it
                    return space[0],space[1],self.piece
                elif value == target-1 and space[s*value] > 1: #if the player can put the opponent in checkmate, do so
                    return space[0],space[1],self.piece
            

        
        return row_choice,col_choice,self.piece