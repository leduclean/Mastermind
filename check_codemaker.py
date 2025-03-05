# -*- coding: utf-8 -*-
"""
Created on Wed Mar  5 12:46:54 2025

@author: Simon
"""
import common

def check_codemaker(log_file):
    
    #Prend la solution donc l'avant derniere ligne
    #Et pour chaque pair de ligne regarde si l'evaluation du tried avec la solution est la meme que l'evaluation dans le document
    with open(log_file, 'r') as log :
        lines = log.readlines()
        
        solution = lines[-2]
        
        #Pas besoin de checker la derniere ligne donc len(lines)-1
        for i in range(0, len(lines)-1, 2):
            
            tried, ev = lines[i:i+2]
            if ev != common.evaluation(tried, solution):
                return False
    
    return True


        