#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script con varias funciones útiles para la conversión de ficheros y creación de
diccionario a partir de la información recogida en los archivos de landmarks
"""

import csv


"""
Función que a partir de una línea con el formato de un punto en un fichero .pp
extrae el nombre del landmark

    :param line: Línea que incluye la información del punto y el nombre del
                 landmark que se desea obtener
"""
def get_landmark_name(line):
    i = 0
    encontrado = False
    
    # Mientras no encontremos el nombre y la línea no se acabe
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
    

"""
    Función que a partir de un fichero .pp es capaz de almacenar en un
    diccionario todos los nombres de los landmarks que existen en el fichero
    
        :param lmk_path: Ruta al fichero del que se desea extraer la
                         información
"""
def get_predicted_landmarks(lmk_path):
    lmk_dict = {}

    file = open(lmk_path, "r")
    
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
            lmk_dict[cont] = lmk_name
            cont+=1
            
    file.close()
    return lmk_dict



"""
    Función que a partir de un diccionario con los landmarks de referencia (los predichos por los métodos),
    y una ruta al fichero que se desea filtrar a partir de los landmarks de     
    referencia es capaz de filtrar el fichero de tal manera que los landmarks 
    que aparezcan en el fichero a filtrar pero no en el de referencia son eliminados.
    
        :reference_lmks: Diccionario con los landmarks de referencia a usar
                         en el filtrado
        :file_to_freference_lmksilter: Ruta al fichero que se desea filtrar
        :filter_file: Ruta del fichero filtrado que se quiere crear
"""
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

"""
    Función que a partir de un diccionario con los landmarks de referencia (los ground truth),
    y una ruta al fichero que se desea filtrar a partir de los landmarks de     
    referencia es capaz de filtrar el fichero de tal manera que los landmarks 
    que aparezcan en el fichero a filtrar pero no en el de referencia son eliminados.
    
        :reference_lmks: Diccionario con los landmarks de referencia a usar
                         en el filtrado
        :file_to_freference_lmksilter: Ruta al fichero que se desea filtrar
        :filter_file: Ruta del fichero filtrado que se quiere crear
"""    
def filter_predicted_pp_file(reference_lmks, file_to_filter, filter_file):
    
    for key in reference_lmks:
        lmk_point = reference_lmks[key].replace("'", "")
        reference_lmks[key] = lmk_point
        
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

"""
    Función que a partir de una ruta al fichero que se quiere convertir, una cadena
    con la ruta del fichero nuevo a crear y un diccionario con los landmarks 
    que contiene el fichero es capaz de convertir el fichero con extensión .pp
    a un fichero con extensión .txt
    
        :file_to_open: Ruta al fichero que se desea convertir
        :file_to_create: Ruta al fichero que se desea crear
        :ground_truth_pp: Diccionario con los landmarks que tiene el fichero
                          a filtrar
"""
def pp_to_txt (file_to_open, file_to_create, ground_truth_pp):
    
    # Se abren los ficheros correspondientes
    f = open(file_to_open, 'r')
    fw = open(file_to_create, 'w')
    lista = [''] * (len(ground_truth_pp))
    keep_reading = True
    
    # Mientras no se llegue al final del fichero
    # seguimos leyendo
    while(keep_reading):
        x_coord = 0
        y_coord = 0
        z_coord = 0
        name = ""
        linea = f.readline()

        # Si llegamos al final del fichero paramos de leer
        if "</PickedPoints>" in linea:
            keep_reading = False
        
        # Si estamos leyendo un landmark
        if "point" in linea:
            # Sacamos el nombre del landmark
            name = get_landmark_name(linea)
            
            # Separamos la línea en palabras (separadas por espacios)
            words = linea.split()
            
            # Por cada palabra, miramos si es una coordenada y si lo es guardamos
            # el valor de la coordenada
            for i in words:
                if ('x=' in i):
                    x_coord = i.split('"')[1]
                
                if ('y=' in i):
                    y_coord = i.split('"')[1]
                
                if ('z=' in i):
                    z_coord = i.split('"')[1]
            
            # Si hemos almacenado las coordenadas de manera correcta
            if (x_coord != 0 and y_coord != 0 and z_coord != 0):
                pos_lmk = -1
                encontrado = False
                # Comprobamos que el landmarks esta en el diccionario y guardamos
                # la posición en la que se encuentra
                for key in ground_truth_pp:
                    if ground_truth_pp[key] == name:
                        pos_lmk = key
                        encontrado = True

                    if (encontrado):
                        break

                # Guardamos, en la posición correspondiente, la información
                # del landmark encontrado
                if (pos_lmk != -1):
                    lista[pos_lmk-1] = str(x_coord) + " " + str(y_coord) + " " + str(z_coord) + '\n'


    # Una vez leido todo el documento escribimos en el fichero
    # las coordenadas de los landmarks (ordenadas según el diccionario) en el 
    # fichero de escritura indicado
    for coord in lista:
        fw.write(coord)
        
    # Se cierran los ficheros de escritura y lectura
    f.close()
    fw.close()


"""
    Función que a partir de una ruta al fichero que se quiere convertir es capaz
    de convertir el fichero con extensión .pp a uno con extensión .csv
    
        :file_to_open: Ruta al fichero que se desea convertir
"""
def pp_to_csv(file):   
    # Creamos el nombre del fichero a crear     
    csv_to_create = file.replace('.pp','.csv')
    csv_to_create = csv_to_create.replace('filtered_', '')
    
    # Abrimos con permisos de escritura el fichero que se desea crear
    with open(csv_to_create, 'w', encoding='UTF8') as csv_file:
        # Creamos el writer de csv
        writer = csv.writer(csv_file)
        # Escribimos la cabecera
        header = ["lmk_name", "x_coord", "y_coord", "z_coord"]
        writer.writerow(header)
        
        # Abrimos el fichero del que vamos a leer la información
        f = open(file, "r")
        
        # Mientras que se pueda leer el fichero sacamos la información del punto
        # y la escribimos en el fichero correspondiente (no hace falta preservar
        # ningún orden porque ya se leen ordenados)
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


