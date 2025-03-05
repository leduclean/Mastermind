# -*- coding: utf-8 -*-
"""
Created on Wed Mar  5 12:46:54 2025

@author: Simon
"""
# On utilise un import relatif (`from . import common`)  
# pour s'assurer que le module est bien importé,  
# peu importe comment l'application est exécutée avec Flask.  
# Cela évite les erreurs liées aux imports absolus.  
from . import common

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


        