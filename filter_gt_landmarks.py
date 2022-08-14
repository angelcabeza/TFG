#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para filtrar los landmarks ground_truth de la segunda evaluación de
manera que tanto los landmarks ground_truth como los predichos sean los mismos.
"""

import csv

def get_landmark_name(line):
    i = 0
    encontrado = False
    while (i < (len(line) - 5) and not encontrado):
        
        # Comprobamos si estamos leyendo el nombre del punto
        # y lo guardamos en una lista caracter por caracter
        if (line[i:i+5] == "name="):
            lmk_name = []
            cont = i+6
            j = 0
            while j < 100 and not encontrado:
                if (line[cont] != '"'):
                    lmk_name.append(line[cont])
                    cont += 1
                else:
                    encontrado = True
        
        i+=1
            
    # Convertimos la lista a string y la almacenamos en
    # el diccionario
    lmk_name_string = ''.join(lmk_name)
    
    return lmk_name_string
    

def get_predicted_landmarks(predicted_lmk_path):
    predicted_lmk_dict = {}

    file = open(predicted_lmk_path, "r")
    
    keep_reading = True
    cont = 1
    
    while(keep_reading):
        line = file.readline()
        
        # Si llegamos al final del fichero paramos de leer
        if "</PickedPoints>" in line:
            keep_reading = False
        
        # Miramos si estamos en la parte del fichero correspondiente 
        # a los landmarks
        if (keep_reading and "point" in line):
            lmk_name = get_landmark_name(line)
                    
            # Convertimos la lista a string y la almacenamos en
            # el diccionario
            predicted_lmk_dict[cont] = lmk_name
            cont+=1
            
    file.close()
    return predicted_lmk_dict


def filter_pp_file(reference_lmks, file_to_filter, filter_file):  
    for key in reference_lmks:
        lmk_point = reference_lmks[key].replace("'", "")
        reference_lmks[key] = lmk_point
        
    reading_file = open(file_to_filter, "r")
    writing_file = open(filter_file, "w")
    
    
    keep_reading = True    
    while(keep_reading):
        line = reading_file.readline()
        
        # Si llegamos al final del fichero paramos de leer
        # y escribimos la ultima linea
        if "</PickedPoints>" in line:
            keep_reading = False
        
        # Miramos si estamos en la parte del fichero correspondiente 
        # a los landmarks
        if (keep_reading and "point" in line):
            lmk_name = get_landmark_name(line)
            
            lmk_name = lmk_name.replace("'", "")
            
            if (lmk_name in reference_lmks.values()):
                writing_file.write(line)
                
        else:
            writing_file.write(line)
            
    writing_file.close()
    reading_file.close()
    
def filter_predicted_pp_file(reference_lmks, file_to_filter, filter_file):
    
    for key in reference_lmks:
        lmk_point = reference_lmks[key].replace("'", "")
        reference_lmks[key] = lmk_point
        
    if "Enrique" in file_to_filter:
        print(reference_lmks)
        
    reading_file = open(file_to_filter, "r")
    writing_file = open(filter_file, "w")
    
    lista = [''] * (len(reference_lmks))
    
    keep_reading = True    
    while(keep_reading):
        line = reading_file.readline()
        
        # Si llegamos al final del fichero paramos de leer
        # y escribimos la ultima linea
        if "</PickedPoints>" in line:
            keep_reading = False
        
        # Miramos si estamos en la parte del fichero correspondiente 
        # a los landmarks
        if (keep_reading and "point" in line):
            lmk_name = get_landmark_name(line)
            
            lmk_name = lmk_name.replace("'", "")
            
            if (lmk_name in reference_lmks.values()):
                keys = [k for k, v in reference_lmks.items() if v == lmk_name]
                lista[keys[0] - 1] = line
                
        else:
            if "</PickedPoints>" in line:
                for i in lista:
                    writing_file.write(i)
                    
            writing_file.write(line)
            
    writing_file.close()
    reading_file.close()

def pp_to_txt (file_to_open, file_to_create, ground_truth_pp):
    f = open(file_to_open, 'r')
    fw = open(file_to_create, 'w')
    lista = [''] * (len(ground_truth_pp))
    keep_reading = True
    
    while(keep_reading):
        x_coord = 0
        y_coord = 0
        z_coord = 0
        name = ""
        linea = f.readline()

        if "</PickedPoints>" in linea:
            keep_reading = False
            
        if "point" in linea:
            name = get_landmark_name(linea)
                    
            words = linea.split()

        
            for i in words:
                if ('x=' in i):
                    x_coord = i.split('"')[1]
                
                if ('y=' in i):
                    y_coord = i.split('"')[1]
                
                if ('z=' in i):
                    z_coord = i.split('"')[1]
            
            if (x_coord != 0 and y_coord != 0 and z_coord != 0):
                pos_lmk = -1
                encontrado = False
                for key in ground_truth_pp:
                    if ground_truth_pp[key] == name:
                        pos_lmk = key
                        encontrado = True

                    if (encontrado):
                        break


                if (pos_lmk != -1):
                    lista[pos_lmk-1] = str(x_coord) + " " + str(y_coord) + " " + str(z_coord) + '\n'


    for coord in lista:
        fw.write(coord)

    f.close()
    fw.close()


def pp_to_csv(file):        
    csv_to_create = file.replace('.pp','.csv')
    csv_to_create = csv_to_create.replace('filtered_', '')
    
    with open(csv_to_create, 'w', encoding='UTF8') as csv_file:
        writer = csv.writer(csv_file)
        header = ["lmk_name", "x_coord", "y_coord", "z_coord"]
        writer.writerow(header)
        
        f = open(file, "r")
        
        while(True):
            line = f.readline()
            if not line:
                f.close()
                break
    
            if '<point' in line:
                lmk_name = get_landmark_name(line)
                words = line.split()
    
            
                for i in words:
                    if ('x=' in i):
                        x_coord = i.split('"')[1]
                    
                    if ('y=' in i):
                        y_coord = i.split('"')[1]
                    
                    if ('z=' in i):
                        z_coord = i.split('"')[1]
                        
                
                row = [lmk_name, x_coord, y_coord, z_coord]
                writer.writerow(row)
    
        f.close()


