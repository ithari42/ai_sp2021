# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 11:54:09 2021

@author: ithari42
"""

import numpy as np
import os


misses = 0
debug = False

class Node():

    def __init__(self,n_id=-1,color=-1):
        self.n_id = n_id
        self.edges = dict()
        self.color = color
        self.a_colors = []
        
    def __str__(self):
        output = ""
        output += "n_id: " + str(self.n_id) + "\n"
        output += "color: " + str(self.color) +"\n"
        output += "Edges: " + str(len(self.edges)) + "\n"
        for n_id in self.edges:
            output += "\tn_id: " + str(n_id) + "\n" 
        return output
        
    def reset_available_colors(self,colors):
        self.a_colors = colors.copy()
        
    def add_edge(self,n_id,node):
        self.edges[n_id] = node
        
    def has_edge_to(self,node):
        return node.n_id in self.edges
    
    def num_edges(self):
        return len(self.edges)

    
    def color_node(self,color=-1):
        self.color = color
        if color != -1:
            for edge in self.edges.values():
                if color in edge.a_colors and edge.color == -1:
                    edge.a_colors.remove(color) 
    

def load_nodes(filen_id="test.txt"):
    global debug
    
    nodes = dict()
    colors = []
    
    file = open(filen_id)
    line = file.readline()
    line = file.readline()
    if("Colors" in line):
        #file.readline()
        line = file.readline()
        
        words = line.split(" ")
        num_colors = int(words[2])
        for i in range(num_colors):
            colors.append(i)
        line = file.readline()
    
    
    if "Graph" in line:
        line = file.readline()
        while (line != ""):
            words = line.split(",")
            if(len(words) == 2):
                node0 = int(words[0])
                node1 = int(words[1])
                if node0 not in nodes:
                    node = Node(node0)
                    node.reset_available_colors(colors)
                    nodes[node0] = node
                if node1 not in nodes:
                    node = Node(node1)
                    node.reset_available_colors(colors)
                    nodes[node1] = node
                nodes[node0].add_edge(node1,nodes[node1])
                nodes[node1].add_edge(node0,nodes[node0])
                
            line = file.readline()

            
    file.close()
    
    return nodes, colors

    
def reset_a_colors(nodes,colors):
    
    for node in nodes.values():
        node.a_colors = colors.copy()

def apply_colors(order,nodes,colors):
    global debug
    reset_a_colors(nodes,colors)
    for n_id in order:
        node = nodes[n_id]
        node.color_node(node.color)
    

def try_colors(index,order,nodes,colors):
    global misses
    global debug
    if index >= len(order): # found solution 
        if debug: print("SUCCESS: Solution found!")
        return True
    elif index < 0: # something bad happened
        if debug: print("ERROR: order index < 0")
        return False 
        
        
        
    n_id = order[index]
    node = nodes[n_id]
    possible_colors = node.a_colors.copy()
    for color in possible_colors:
        node.color_node(color)
        if debug: print(n_id,": color =",color)
        
        # early detection of bad colors
        good = True
        for i in range(len(order)-1,index,-1):
            if len(nodes[i].a_colors) == 0:
                good = False
                
        success = False
        if good:
            success = try_colors(index+1,order,nodes,colors) # continue coloring recursively
        
        if success: # coloring succesfull so return true
            return True
        else: # reset coloring to previous state for next run
            node.color_node(-1) 
            apply_colors(order,nodes,colors)
    
    
    #if this point is reached, no coloring exists for the graph
    if debug: print(n_id,": no valid colors")
    misses += 1
    return False
    
def solve_csp(filename="data.txt"):
    global misses
    misses = 0
    global debug
    
    nodes,colors = load_nodes(filename)
    
    for node in nodes:
        if debug: print(nodes[node])
    if debug: print("colors =",colors)
    
    
    
    
    # determine an order to color nodes in
    order = []
    while(len(order) < len(nodes)): # n nodes
        
        most_n = -1
        most_node = -1
        
        for n_id in nodes: # O(n to 1) nodes
            if n_id not in order:
                n = 0
                for edge in nodes[n_id].edges: # O(n to 1)
                    if edge not in order:
                        n += 1
                #n = len(nodes[n_id].edges) # O(1)
                if n > most_n:
                    most_n = nodes[n_id].num_edges()
                    most_node = n_id
                    
        order.append(most_node)
    if debug: print("order = ",order)
    
    success = try_colors(0,order,nodes,colors)
    
    if debug: print(success)
    
    if debug: print("Misses:",misses)
    
    print("\n------------------------")
    print("File:",filename)
    print("Vertices:",len(nodes))
    print("Colors:",colors)
    print("Solvable:",success)
    print("Backtraces =",misses)
    if success:
        for node in nodes.values():
            print("vertex =",node.n_id,": color =",node.color)
    print("------------------------\n")        
    

    
# main program
    
f_count = 0
for file in os.listdir("data"):
    if file.endswith(".txt"):
        solve_csp("data/"+file)
        f_count += 1

if f_count == 0:
    print("ERROR: No .txt files found in data directory")
    
    
    
    
