# -*- coding: utf-8 -*-
"""
Created on Thu Mar 11 20:03:27 2021

@author: Jonathan Pritchett
"""

import numpy as np

from crd import CRD
from grid import Grid
from game import Game
from player import Player




    

# game = Game(4,3)
# #game.print_game()

# game.apply_move(1,1,-1)
# #game.print_game()
# game.apply_move(3,1,-1)
# game.apply_move(0,0,-1)
# game.apply_move(2,2, 1)
# game.apply_move(0,3,1)
# game.apply_move(1,3,1)
# game.apply_move(2,1,1)
# #game.apply_move(2,3,1)
# game.print_game()

# game = Game(3,3)
# p1 = Player(1)
# p2 = Player(-1)

# game.print_game()
        
    
    
# game = Game(4,3)
# game.apply_move(0,0,1)
# game.apply_move(1,1,1)
# game.apply_move(2,1,-1)
# game.print_game(False)

p1 = Player(1)
p2 = Player(-1)
game = Game(3,2)

while(True):
    game.turn_count = 1
    row,col,piece = p1.make_move(game)
    print("Player:",piece,"Claimed",row,col)
    game.apply_move(row,col,piece)
    game.print_game()
    if(game.check_win() != 0 or row == -1 or col == -1):
        print("Tie Game!")
        break
    row,col,piece = p2.make_move(game)
    print("Player:",piece,"Claimed",row,col)
    game.apply_move(row,col,piece)
    game.print_game()
    if(game.check_win() != 0 or row == -1 or col == -1):
        print("Tie Game!")
        break