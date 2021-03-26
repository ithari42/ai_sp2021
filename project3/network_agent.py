# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 01:01:12 2021

@author: ithari42
"""

TEAM_ID = '1282'
API_KEY = '2b88caa0b3073664be7d'
USER_ID = '1080'
URL1 = 'www.notexponential.com'
URL2 = '/aip2pgaming/api/index.php'
TEAM_ID2 = '1283'


import http.client
import mimetypes
from codecs import encode
import json

class Network_Agent():
    def __init__(self,api_key,user_id):
        self.api_key = api_key
        self.user_id = user_id
        pass
    
    def get_my_games(self,team_id):
        #url = URL+"teamId="+TEAM_ID+"&type=myGames"
        conn = http.client.HTTPSConnection(URL1)
        boundary = ''
        payload = ''
        headers = {
          'userid': self.user_id,
          'x-api-key': self.api_key,
          'Content-type': 'multipart/form-data; boundary={}'.format(boundary)
        }
        conn.request("GET", URL2
                     +"?type=myGames"
                     +"&teamId="+team_id, payload, headers)
        res = conn.getresponse()
        #data = res.read().decode()
        data=json.loads(res.read().decode('utf-8'))
        print(data)

    
    def create_game(self,team_id1,team_id2,board_size='20',target='10'):
        conn = http.client.HTTPSConnection(URL1)
        dataList = []
        boundary = 'wL36Yn8afVp8Ag7AmP8qZ0SA4n1v9T'
        dataList.append(encode('--' + boundary))
        dataList.append(encode('Content-Disposition: form-data; name=type;'))
        
        dataList.append(encode('Content-Type: {}'.format('text/plain')))
        dataList.append(encode(''))
        
        dataList.append(encode("game"))
        dataList.append(encode('--' + boundary))
        dataList.append(encode('Content-Disposition: form-data; name=teamId1;'))
        
        dataList.append(encode('Content-Type: {}'.format('text/plain')))
        dataList.append(encode(''))
        
        dataList.append(encode(team_id1))
        dataList.append(encode('--' + boundary))
        dataList.append(encode('Content-Disposition: form-data; name=teamId2;'))
        
        dataList.append(encode('Content-Type: {}'.format('text/plain')))
        dataList.append(encode(''))
        
        dataList.append(encode(team_id2))
        dataList.append(encode('--' + boundary))
        dataList.append(encode('Content-Disposition: form-data; name=gameType;'))
        
        dataList.append(encode('Content-Type: {}'.format('text/plain')))
        dataList.append(encode(''))
        
        dataList.append(encode("TTT"))
        dataList.append(encode('--' + boundary))
        dataList.append(encode('Content-Disposition: form-data; name=boardSize;'))
        
        dataList.append(encode('Content-Type: {}'.format('text/plain')))
        dataList.append(encode(''))
        
        dataList.append(encode(board_size))
        dataList.append(encode('--' + boundary))
        dataList.append(encode('Content-Disposition: form-data; name=target;'))
        
        dataList.append(encode('Content-Type: {}'.format('text/plain')))
        dataList.append(encode(''))
        
        dataList.append(encode(target))
        dataList.append(encode('--'+boundary+'--'))
        dataList.append(encode(''))
        body = b'\r\n'.join(dataList)
        payload = body
        headers = {
          'userid': self.user_id,
          'x-api-key': self.api_key,
          'Content-type': 'multipart/form-data; boundary={}'.format(boundary)
        }
        conn.request("POST", URL2, payload, headers)       
        
        res = conn.getresponse()
        data=json.loads(res.read().decode('utf-8'))
        print(data)
        
        if "gameId" in data:
            return data['gameId']
        else:
            return ""
        
        
        game_id = '' #parse this from data
        return game_id
        
    def make_move(self,team_id,game_id,x,y):
        conn = http.client.HTTPSConnection(URL1)
        dataList = []
        boundary = 'wL36Yn8afVp8Ag7AmP8qZ0SA4n1v9T'
        dataList.append(encode('--' + boundary))
        dataList.append(encode('Content-Disposition: form-data; name=type;'))
        
        dataList.append(encode('Content-Type: {}'.format('text/plain')))
        dataList.append(encode(''))
        
        dataList.append(encode("move"))
        dataList.append(encode('--' + boundary))
        dataList.append(encode('Content-Disposition: form-data; name=teamId;'))
        
        dataList.append(encode('Content-Type: {}'.format('text/plain')))
        dataList.append(encode(''))
        
        dataList.append(encode(team_id))
        dataList.append(encode('--' + boundary))
        dataList.append(encode('Content-Disposition: form-data; name=gameId;'))
        
        dataList.append(encode('Content-Type: {}'.format('text/plain')))
        dataList.append(encode(''))
        
        dataList.append(encode(game_id))
        dataList.append(encode('--' + boundary))
        dataList.append(encode('Content-Disposition: form-data; name=move;'))
        
        dataList.append(encode('Content-Type: {}'.format('text/plain')))
        dataList.append(encode(''))
        
        dataList.append(encode(str(x)+","+str(y)))
        dataList.append(encode('--'+boundary+'--'))
        dataList.append(encode(''))
        body = b'\r\n'.join(dataList)
        payload = body
        headers = {
          'userid': self.user_id,
          'x-api-key': self.api_key,
          'Content-type': 'multipart/form-data; boundary={}'.format(boundary)
        }
        conn.request("POST", URL2, payload, headers)
        
        res = conn.getresponse()
        data=json.loads(res.read().decode('utf-8'))
        print(data)
        
        if "moveId" in data:
            return data['moveId']
        else:
            return ""
        
    def get_moves(self,game_id,turn_count):
        conn = http.client.HTTPSConnection(URL1)
        boundary = ''
        payload = ''
        headers = {
          'userid': self.user_id,
          'x-api-key': self.api_key,
          'Content-type': 'multipart/form-data; boundary={}'.format(boundary)
        }
        conn.request("GET", URL2
                     +"?type=moves"
                     +"&gameId="+game_id
                     +"&count="+str(turn_count), payload, headers)
        res = conn.getresponse()
        data=json.loads(res.read().decode('utf-8'))
        print(data)
        
        if "moves" in data:
            return data['moves']
        else:
            return ""
            
    
    
# agent = Network_Agent(API_KEY,USER_ID)
# agent.get_my_games("1282")
# moves = agent.get_moves("2325",10)
# print(moves[0]['moveId'])

# move_id = agent.make_move("1283","2325",2,1)
# print(move_id)





