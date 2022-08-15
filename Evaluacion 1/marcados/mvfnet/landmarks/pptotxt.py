#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 27 18:52:12 2022

@author: angel
"""

import os
import shutil

folder = "/home/angel/Escritorio/marcados/mvfnet/landmarks"


for file in os.listdir(folder):
    file_open = folder + '/' + file
    
    file_to_create = folder + '/' + file
    file_to_create = file_to_create.replace('.pp', '.txt', 1)
    
    print("ABRO ARCHIVO: ", file_open)
    print("CREO: ", file_to_create)
    
    if '.pp' in file_open:
        f = open(file_open, 'r')
        fw = open(file_to_create, 'w')
        while(True):
            x_coord = 0
            y_coord = 0
            z_coord = 0
            linea = f.readline()
            
            print("Linea:" ,linea)
            if not linea:
                break
        
            words = linea.split()
            
            for i in words:
                if ('x=' in i):
                    x_coord = i.split('"')[1]
                    #print("x: ", x_coord)
                    
                if ('y=' in i):
                    y_coord = i.split('"')[1]
                    #print("y: ", y_coord)
                    
                if ('z=' in i):
                    z_coord = i.split('"')[1]
                    #print("z: ", z_coord)
                
            if (x_coord != 0 and y_coord != 0 and z_coord != 0):
                line = str(x_coord) + " " + str(y_coord) + " " + str(z_coord) + '\n'
                print("Escribo: ", line)
                fw.write(line)
 

        f.close()
        fw.close()
