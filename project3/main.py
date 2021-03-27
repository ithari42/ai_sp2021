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
from network_agent import Network_Agent

import json
import time


TEAM_ID1 = '1282'
TEAM_ID2 = '1283'
API_KEY = '2b88caa0b3073664be7d'
USER_ID = '1080'
DELAY=1

def create_game(agent,team_id1,team_id2,boardsize,target,player=1,old_game_id=''):
    game_id = old_game_id
    if(old_game_id == ""):
        game_id = agent.create_game(team_id1,team_id2,str(boardsize),str(target))

    if(game_id != ""):
        game = Game(game_id,boardsize,target)
        
        if(player == 1):
            p1 = Player(team_id1,1,"simple")
        else:
            p1 = Player(team_id2,-1,"simple")
        return game,p1
    else:
        return -1,-1
    
def create_2p_game(agent,team_id1,team_id2,boardsize,target,old_game_id=''):
    
    game_id = old_game_id
    if(old_game_id == ""):
        game_id = agent.create_game(team_id1,team_id2,str(boardsize),str(target))
    if(game_id != ""):
        game = Game(game_id,boardsize,target)
        
        p1 = Player(team_id1,1,"simple")
        p2 = Player(team_id2,-1,"simple")
        
        return game,p1,p2
    else:
        return -1,-1,-1
    
    
def reset_game(agent,game):
    moves = agent.get_moves(game.game_id, int(game.boardsize ** 2))
    new_game = Game(game.game_id,game.boardsize,game.target)
    
    if moves == "":
        return ""
    
    for i in range(len(moves)):
        
        symbol = moves[i]['symbol']
        moveId = moves[i]['moveId']
        col = int(moves[i]["moveX"])
        row = int(moves[i]["moveY"])
        if symbol == 'O':
            new_game.apply_move(row,col,1)
            new_game.last_move = moveId
        elif symbol == 'X':
            new_game.apply_move(row,col,-1)
            new_game.last_move = moveId
        else:
            return ""
    return new_game
        
    
def make_move(agent,game,player):
    
        
    row,col,piece = player.make_move(game)
    move_res = agent.make_move(player.team_id,game.game_id,str(col),str(row))
    
    if move_res != "":
        game.apply_move(row,col,player.piece)
        game.last_move = move_res
        return True
    return False
        
        
                
def play_game_1ai(team_id1=TEAM_ID1,team_id2=TEAM_ID2,boardsize=20,target=10,player_num=1,old_game_id=""):
    agent = Network_Agent(API_KEY,USER_ID)
    game,p1 = create_game(agent,team_id1,team_id2,boardsize,target,player_num,player_num,old_game_id)
    if game != -1:
        
        while(True):
            
            ngame = reset_game(agent,game)
        
            if(ngame != ""):
                game = ngame
            
            
            game.print_game()
            time.sleep(DELAY)
            
            if(game.check_win() == 0):
                print("player 1 making move")
                make_move(agent,game,p1)
            else:
                break
        
    else:
        print("ERROR: Game Creation Failed!!")
        

def play_game_2ai(team_id1=TEAM_ID1,team_id2=TEAM_ID2,boardsize=20,target=10,old_game_id=""):
    agent = Network_Agent(API_KEY,USER_ID)
    game,p1,p2 = create_2p_game(agent,team_id1,team_id2,boardsize,target,old_game_id)
    if game != -1:
        
        while(True):
            
            ngame = reset_game(agent,game)
        
            if(ngame != ""):
                game = ngame
            
            
            game.print_game()
            time.sleep(DELAY)
            
            if(game.check_win() == 0):
                success = make_move(agent,game,p1)
                if( not success):
                    make_move(agent,game,p2)
            else:
                break
        
        
    else:
        print("ERROR: Game Creation Failed!!")




    
    
    
    

