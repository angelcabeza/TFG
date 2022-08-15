#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 15 13:01:05 2022

@author: angel
"""


import os
import shutil
import filter_gt_landmarks


os.chdir('./Evaluacion 2/gt_lmks')

for folder in os.listdir('.'):
    path = './' + folder
    
    for file in os.listdir(path):
        if "filtered_" in file:
            file_path = path + '/' + file
            new_filename = file.replace("filtered_", "")
            new_path = '/home/angel/Escritorio/Informatica/TFG/Evaluacion 2/lmk_truth_deca/' + new_filename
            
            if (folder == "MVFNET"):
                new_path = '/home/angel/Escritorio/Informatica/TFG/Evaluacion 2/lmk_truth_mvfnet/' + new_filename
            elif folder == "P2V":
                new_path = '/home/angel/Escritorio/Informatica/TFG/Evaluacion 2/lmk_truth_p2v/' + new_filename
            elif folder == "VRN":
                new_path = '/home/angel/Escritorio/Informatica/TFG/Evaluacion 2/lmk_truth_vrn/' + new_filename
            
        
            os.rename(file_path, new_path)


os.chdir('/home/angel/Escritorio/Informatica/TFG/Evaluacion 2/predicted_lmks')

for folder in os.listdir('.'):
    path = "./" + folder
    
    for file in os.listdir(path):
        if "filtered_" in file:
            file_path = path + '/' + file
            new_name_gt = file.replace("filtered_", "")
            new_name = new_name_gt.replace(".pp", ".txt")
            new_file = path + '/' + new_name
            
            gt_pp = '/home/angel/Escritorio/Informatica/TFG/Evaluacion 2/lmk_truth_deca/' + new_name_gt
            
            if (folder == "MVFNET"):
                gt_pp = '/home/angel/Escritorio/Informatica/TFG/Evaluacion 2/lmk_truth_mvfnet/' + new_name_gt
            elif folder == "P2V":
                gt_pp = '/home/angel/Escritorio/Informatica/TFG/Evaluacion 2/lmk_truth_p2v/' + new_name_gt
            elif folder == "VRN":
                gt_pp = '/home/angel/Escritorio/Informatica/TFG/Evaluacion 2/lmk_truth_vrn/' + new_name_gt
            
            gt_dict = filter_gt_landmarks.get_predicted_landmarks(gt_pp)
            filter_gt_landmarks.pp_to_txt(file_path, new_file, gt_dict)
    
    for file in os.listdir(path):
        if ".txt" in file:
            file_path = path + '/' + file
            folder_name = file.replace(".txt", "")
            
            dst_folder = "/home/angel/Escritorio/Informatica/TFG/Evaluacion 2/predicted_mesh/DECA/" + folder_name + '/' + file
            
            if (folder == "MVFNET"):
                dst_folder = "/home/angel/Escritorio/Informatica/TFG/Evaluacion 2/predicted_mesh/MVFNET/" + folder_name + '/' + file
            elif folder == "P2V":
                dst_folder = "/home/angel/Escritorio/Informatica/TFG/Evaluacion 2/predicted_mesh/P2V/" + folder_name + '/' + file
            elif folder == "VRN":
                dst_folder = "/home/angel/Escritorio/Informatica/TFG/Evaluacion 2/predicted_mesh/VRN/" + folder_name + '/' + file
                
            
            os.replace(file_path, dst_folder)
