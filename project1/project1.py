# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 00:42:53 2021

@author: ithari42
"""

import math
import time


class Node():
    

    def __init__(self,id=-1,x=-1,y=-1):
        self.id = id
        self.x_grid = x
        self.y_grid = y
        self.edges = dict()
    def __str__(self):
        output = ""
        output += "id: " + str(self.id) + ", x: " + str(self.x_grid) + ", y: " + str(self.y_grid) +"\n"
        output += "Edges: " + str(len(self.edges)) + "\n"
        for id in self.edges:
            output += "\tid: " + str(id) + ", weight: " + str(self.edges[id]) + "\n" 
        return output
        
    def add_edge(self,id,weight):
        self.edges[id] = weight
        
    def has_edge_to(self,node):
        return node.id in self.edges.keys()
        
    def distance_to(self,node):
        if(self.has_edge_to(node)):
            return self.edges[node.id]
        else:
            return math.sqrt(((self.x_grid-node.x_grid)*1000)**2 + (((self.y_grid-node.y_grid)*1000)**2))

def square_to_coord(square_id):
    x = square_id % 10
    y = int(square_id / 10)
    return x,y

def load_nodes(filename="p1_graph.txt"):
    nodes = dict()
    source = -1
    dest = -1
    
    file = open(filename)
    line = file.readline()
    if("Vertices" in line):
        file.readline()
        line = file.readline()
        while ("#" not in line):
            words = line.split(",")
            if(len(words) == 2):
                id = int(words[0])
                x,y = square_to_coord(int(words[1]))
                nodes[id] = Node(id,x,y)
            line = file.readline()
            
    if "Edges" in line:
        file.readline()
        line = file.readline()
        while ("#" not in line):
            words = line.split(",")
            if(len(words) == 3):
                sc = int(words[0])
                dst = int(words[1])
                wgt = int(words[2])
                nodes[sc].add_edge(dst,wgt)
                nodes[dst].add_edge(sc,wgt)
            line = file.readline()
            
    if "Source" in line:
        for i in range(2):
            line = file.readline()
            words = line.split(",")
            if "S" in words[0]:
                source = int(words[1])
            elif "D" in words[0]:
                dest = int(words[1])

    return source,dest,nodes

def djikstra(start_id,end_id,nodes, complete=True):
    dist = dict()
    prev = dict()
    unsearched = []
    
    for node in nodes:
        dist[node] = -1
        prev[node] = -1
        unsearched.append(node)
    dist[start_id] = 0
    
    unfinished = True
    
    while(len(unsearched) > 0) and unfinished:
        shortest_id = -1
        shortest_distance = -1
        for node_id in unsearched:
            if shortest_distance == -1 and dist[node_id] != -1:
                shortest_distance == dist[node_id]
                shortest_id = node_id
            elif shortest_distance != -1 and dist[node_id] != -1:
                if dist[node_id] < shortest_distance:
                    shortest_distance == dist[node_id]
                    shortest_id = node_id
        
        unsearched.remove(shortest_id)
        
        for node_id in nodes[shortest_id].edges:
            if node_id in unsearched:
                alt_dist = dist[shortest_id] + nodes[shortest_id].edges[node_id]
                if node_id == dest and not complete: # not working currently
                    unfinished = False 
                 
                if alt_dist < dist[node_id] or dist[node_id] == -1:
                    dist[node_id] = alt_dist
                    prev[node_id] = shortest_id
                
                    
    return dist,prev


def astar(source,dest,nodes,weight=1):
    dist = dict()
    prev = dict()
    unsearched = []
    
    for node in nodes:
        dist[node] = -1
        prev[node] = -1
        unsearched.append(node)
    dist[source] = 0
    
    unfinished = True
    
    while(len(unsearched) > 0) and unfinished:
        shortest_id = -1
        shortest_distance = -1
        for node_id in unsearched:
            if shortest_distance == -1 and dist[node_id] != -1:
                shortest_distance == dist[node_id] + nodes[node_id].distance_to(nodes[dest])*weight
                shortest_id = node_id
            elif shortest_distance != -1 and dist[node_id] != -1:
                if dist[node_id] + nodes[node_id].distance_to(nodes[dest])*weight < shortest_distance:
                    shortest_distance == dist[node_id]
                    shortest_id = node_id
        
        unsearched.remove(shortest_id)
        
        for node_id in nodes[shortest_id].edges:
            if node_id == dest:
                # alt_dist = dist[shortest_id] + nodes[shortest_id].edges[node_id]
                # dist[node_id] = alt_dist
                # prev[node_id] = shortest_id
                unfinished = False
                # break
            
            if node_id in unsearched:
                alt_dist = dist[shortest_id] + nodes[shortest_id].edges[node_id]
                if alt_dist < dist[node_id] or dist[node_id] == -1:
                    dist[node_id] = alt_dist
                    prev[node_id] = shortest_id
                    
    return dist,prev


source,dest,nodes = load_nodes("p1_graph.txt")

        
for id in nodes:
    print(nodes[id])
print("\nSource:",source)
print("Destination:",dest)

source = 0
dest = 99





djikstra_c_total = 0
djikstra_i_total = 0
astar_total = 0

djikstra_c_min = -1
djikstra_i_min = -1
astar_min = -1

djikstra_c_max = 0
djikstra_i_max = 0
astar_max = 0

count = 0
for source in range(0,100):
    for dest in range(source+1,100):

        count += 1
        print("Processing:",count,source,dest)
        
        #djikstras complete
        start_time = time.time()
        dist,prev = djikstra(source, dest, nodes)
        end_time = time.time()
        
        djikstra_c_total += end_time-start_time    
        
        if djikstra_c_min == -1 or (end_time-start_time) < djikstra_c_min:
            djikstra_c_min = end_time-start_time
        if djikstra_c_max < (end_time-start_time):
            djikstra_c_max = end_time-start_time
        
        
        #djisktras incomplete
        start_time = time.time()
        dist,prev = djikstra(source, dest, nodes,complete=False)
        end_time = time.time()
        
        djikstra_i_total += end_time-start_time  
        
        if djikstra_i_min == -1 or (end_time-start_time) < djikstra_i_min:
            djikstra_i_min = end_time-start_time
        if djikstra_i_max < (end_time-start_time):
            djikstra_i_max = end_time-start_time
        
        
        #astar
        
        start_time = time.time()
        dist,prev = astar(source, dest, nodes)
        end_time = time.time()
        

        astar_total += end_time-start_time 
        
        if astar_min == -1 or (end_time-start_time) < astar_min:
            astar_min = end_time-start_time
        if astar_max < (end_time-start_time):
            astar_max = end_time-start_time
        
djisktra_c_average = djikstra_c_total*1000/(count) 
djisktra_i_average = djikstra_i_total*1000/(count) 
astar_average = astar_total*1000/(count)          
print("\nDjikstra complete")
print("Total Time(ms)  :",djikstra_c_total)
print("Average Time(us):",djisktra_c_average)
print("Min:",djikstra_c_min*1000)
print("Max:",djikstra_c_max*1000)

print("\nDjikstra incomplete")
print("Total Time(ms)  :",djikstra_i_total)
print("Average Time(us):",djisktra_i_average)
print("Min:",djikstra_i_min*1000)
print("Max:",djikstra_i_max*1000)

print("\nA*")
print("Total Time(ms)  :",astar_total)
print("Average Time(us):",astar_average)
print("Min:",astar_min*1000)
print("Max:",astar_max*1000)

print()
print("A* vs djikstra complete  :",djisktra_c_average/astar_average)
print("djikstra incomplete vs A*:",astar_average/djisktra_i_average)
        

# source = 2
# dest = 99


# #djikstras complete

# start_time = time.time_ns()
# dist,prev = djikstra(source, dest, nodes)
# end_time = time.time_ns()

# path = []
# length = dist[dest]
# current = dest

# while(current != source):
#     path.insert(0,current)
#     current = prev[current]
# path.insert(0,current)

# print("\ndjikstra's complete")
# print("distance:",length)
# print("path:",path)
# print("duration",end_time-start_time)

# #djikstras incomplete

# start_time = time.time_ns()
# dist,prev = djikstra(source, dest, nodes)
# end_time = time.time_ns()

# path = []
# length = dist[dest]
# current = dest

# while(current != source):
#     path.insert(0,current)
#     current = prev[current]
# path.insert(0,current)

# print("\ndjikstra's incomplete")
# print("distance:",length)
# print("path:",path)
# print("duration",end_time-start_time)
    

# #astar

# start_time = time.time_ns()
# dist,prev = astar(source, dest, nodes)
# end_time = time.time_ns()

# path = []
# length = dist[dest]
# current = dest

# while(current != source):
#     path.insert(0,current)
#     current = prev[current]
# path.insert(0,current)

# print("\nA*")
# print("distance:",length)
# print("path:",path)
# print("duration",end_time-start_time)
        
