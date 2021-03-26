# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 17:37:38 2021

@author: ithari42
"""


class CRD():
    
    def __init__(self):
        self.cols = dict()
        self.rows = dict()
        self.left_diag = 0
        self.right_diag = 0
        
        self.abs_cols = dict()
        self.abs_rows = dict()
        self.abs_left = dict()
        self.abs_right = dict()
        
        
    def __str__(self):
        output = ""
        output += "columns\n" + str(self.cols) + "\n" + str(self.abs_cols) + "\n"
        output += "rows\n" + str(self.rows) + "\n" + str(self.abs_rows) + "\n"
        output += "left Diagonal: " + str(self.left_diag) + " Abs: " + str(self.abs_left) + "\n"
        output += "right Diagonal: " + str(self.right_diag) + ", Abs: " + str(self.abs_right) + "\n"
        return output
        
