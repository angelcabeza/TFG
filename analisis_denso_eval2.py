#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Este script se encarga de convertir y mover los fichero .pp ya filtrados 
a las carpetas necesarias para poder realizar el análisis denso. Además
se encarga de la conversión de los fichero .pp a .txt según sea necesario.

"""

import os
import filter_gt_landmarks


# Recorremos la carpeta de los landmarks ground truth
for folder in os.listdir('./Evaluacion 2/gt_lmks'):
    path = './Evaluacion 2/gt_lmks/' + folder
    
    # Para cada método
    for file in os.listdir(path):
        
        # Cogemos los landmarks marcados como filtered (ya filtrados), los
        # renombramos y los movemos a la carpeta 
        # Evaluacion 2/lmk_truth_<metodo>/file.pp
        if "filtered_" in file:
            file_path = path + '/' + file
            new_filename = file.replace("filtered_", "")
            new_path = './Evaluacion 2/lmk_truth_deca/' + new_filename
            
            if (folder == "MVFNET"):
                new_path = '.Evaluacion 2/lmk_truth_mvfnet/' + new_filename
            elif folder == "P2V":
                new_path = './Evaluacion 2/lmk_truth_p2v/' + new_filename
            elif folder == "VRN":
                new_path = './Evaluacion 2/lmk_truth_vrn/' + new_filename
            
        
            os.rename(file_path, new_path)


# Recorremos la carpea de los landmarks predichos por los métodos
for folder in os.listdir('./Evaluacion 2/predicted_lmks'):
    path = "./Evaluacion 2/predicted_lmks/" + folder
    
    # Para cada método
    for file in os.listdir(path):
        # Cogemos los landmarks marcados como filtered (ya filtrados)
        if "filtered_" in file:
            file_path = path + '/' + file
            new_name_gt = file.replace("filtered_", "")
            new_name = new_name_gt.replace(".pp", ".txt")
            new_file = path + '/' + new_name
            
            gt_pp = './Evaluacion 2/lmk_truth_deca/' + new_name_gt
            
            if (folder == "MVFNET"):
                gt_pp = './Evaluacion 2/lmk_truth_mvfnet/' + new_name_gt
            elif folder == "P2V":
                gt_pp = './Evaluacion 2/lmk_truth_p2v/' + new_name_gt
            elif folder == "VRN":
                gt_pp = './Evaluacion 2/lmk_truth_vrn/' + new_name_gt
            
            # Sacamos los landmarks ground truth del fichero .pp correspondiente
            # y los almacenamos en un diccionario
            gt_dict = filter_gt_landmarks.get_predicted_landmarks(gt_pp)
            
            # Convertimos los ficheros .pp a .txt
            filter_gt_landmarks.pp_to_txt(file_path, new_file, gt_dict)
    
    # Almacenamos cada fichero .txt creado en el sitio correspondiente dentro
    # de la carpeta /Evaluacion 2/predicted_mesh/<metodo>/<nombre_modelo>
    # esto es necesario porque NoW requiere esta estructura de carpetas para 
    # realizar el análisis
    for file in os.listdir(path):
        if ".txt" in file:
            file_path = path + '/' + file
            folder_name = file.replace(".txt", "")
            
            dst_folder = "./Evaluacion 2/predicted_mesh/DECA/" + folder_name + '/' + file
            
            if (folder == "MVFNET"):
                dst_folder = "./Evaluacion 2/predicted_mesh/MVFNET/" + folder_name + '/' + file
            elif folder == "P2V":
                dst_folder = "./Evaluacion 2/predicted_mesh/P2V/" + folder_name + '/' + file
            elif folder == "VRN":
                dst_folder = "./Evaluacion 2/predicted_mesh/VRN/" + folder_name + '/' + file
                
            
            os.replace(file_path, dst_folder)
