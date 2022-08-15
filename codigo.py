#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 12:20:20 2022

@author: angel
"""

import numpy as np
import pandas as pd
import os
import glob
import matplotlib.pyplot as plt
import seaborn as sns
import filter_gt_landmarks
import sys


def compute_rigid_alignment(grundtruth_landmark_points, predicted_mesh_landmark_points, landmarks_transformation):
    """
    Computes the rigid alignment between the 
    :param grundtruth_landmark_points: A N x 3 list with annotations of the ground truth scan.
    :param predicted_mesh_landmark_points: A N x 3 list containing the annotated 3D point locations in the predicted mesh.
    """

    grundtruth_landmark_points = np.array(grundtruth_landmark_points)
    predicted_mesh_landmark_points = np.array(predicted_mesh_landmark_points)
    
    d, Z, tform = procrustes(grundtruth_landmark_points, landmarks_transformation, scaling=True, reflection='best')
    
    
    # Use tform to transform all vertices in predicted_mesh_vertices to the ground truth reference space:
    predicted_mesh_landmarks_aligned = tform['scale']*(tform['rotation'].T.dot(predicted_mesh_landmark_points.T).T) + tform['translation']
    
    return predicted_mesh_landmarks_aligned

def procrustes(X, Y, scaling=True, reflection='best'):
    """
    Taken from https://github.com/patrikhuber/fg2018-competition

    A port of MATLAB's `procrustes` function to Numpy.
    Code from: https://stackoverflow.com/a/18927641.

    Procrustes analysis determines a linear transformation (translation,
    reflection, orthogonal rotation and scaling) of the points in Y to best
    conform them to the points in matrix X, using the sum of squared errors
    as the goodness of fit criterion.

        d, Z, [tform] = procrustes(X, Y)

    Inputs:
    ------------
    X, Y
        matrices of target and input coordinates. they must have equal
        numbers of  points (rows), but Y may have fewer dimensions
        (columns) than X.

    scaling
        if False, the scaling component of the transformation is forced
        to 1

    reflection
        if 'best' (default), the transformation solution may or may not
        include a reflection component, depending on which fits the data
        best. setting reflection to True or False forces a solution with
        reflection or no reflection respectively.

    Outputs
    ------------
    d
        the residual sum of squared errors, normalized according to a
        measure of the scale of X, ((X - X.mean(0))**2).sum()

    Z
        the matrix of transformed Y-values

    tform
        a dict specifying the rotation, translation and scaling that
        maps X --> Y

    """

    n, m = X.shape
    ny, my = Y.shape

    muX = X.mean(0)
    muY = Y.mean(0)

    X0 = X - muX
    Y0 = Y - muY

    ssX = (X0 ** 2.).sum()
    ssY = (Y0 ** 2.).sum()

    # centred Frobenius norm
    normX = np.sqrt(ssX)
    normY = np.sqrt(ssY)

    # scale to equal (unit) norm
    X0 /= normX
    Y0 /= normY

    if my < m:
        Y0 = np.concatenate((Y0, np.zeros(n, m - my)), 0)

    # optimum rotation matrix of Y
    A = np.dot(X0.T, Y0)
    U, s, Vt = np.linalg.svd(A, full_matrices=False)
    V = Vt.T
    T = np.dot(V, U.T)

    if reflection is not 'best':

        # does the current solution use a reflection?
        have_reflection = np.linalg.det(T) < 0

        # if that's not what was specified, force another reflection
        if reflection != have_reflection:
            V[:, -1] *= -1
            s[-1] *= -1
            T = np.dot(V, U.T)

    traceTA = s.sum()

    if scaling:

        # optimum scaling of Y
        b = traceTA * normX / normY

        # standarised distance between X and b*Y*T + c
        d = 1 - traceTA ** 2

        # transformed coords
        Z = normX * traceTA * np.dot(Y0, T) + muX

    else:
        b = 1
        d = 1 + ssY / ssX - 2 * traceTA * normY / normX
        Z = normY * np.dot(Y0, T) + muX

    # transformation matrix
    if my < m:
        T = T[:my, :]
    c = muX - b * np.dot(muY, T)

    # transformation values
    tform = {'rotation': T, 'scale': b, 'translation': c}

    return d, Z, tform


    
def create_dict_name():
    dic = {}
    dic['Fernando'] = 'DID1'
    dic['Manuel'] = 'DID2'
    dic['Jose'] = 'DID3'
    dic['Migue'] = 'DID4'
    dic['Alejandro'] = 'DID6'
    dic['Javier'] = 'DID9'
    dic['Aila'] = 'DID11'
    dic['Lydia'] = 'DID12'
    dic['Arnaut'] = 'DID13'
    dic['Veronica'] = 'DID14'
    dic['Juan'] = 'DID15'
    dic['Rosa'] = 'DID16'
    dic['Inma'] = 'DID17'
    dic['Sergio'] = 'DID18'
    dic['Enrique'] = 'DID19'
    
    return dic

def read_GT_PP_from_csv(dic, path):
    #csv_path = "/home/angel/Escritorio/NowDatasetExp2/lmk_truth_vrn"
    df_list = []
    
    for lmk_file in os.listdir(path):
        
        if lmk_file[-3:] == "csv":
            df = pd.read_csv(path + "/" + lmk_file)
            df = df[['lmk_name', 'x_coord', 'y_coord', 'z_coord']]
            df.insert(4, 'Modelo', dic[lmk_file[:-4]])
            df = df.set_index('Modelo')
            df_list.append(df)
        
    df_all_lmks = pd.concat(df_list)

    return df_all_lmks

def read_predicted_lmk_from_csv(dic, csv_path, GT_DF):
    df_list = []
    lista_landmarks = ["AlareL","AlareR", "CheilionR", "CheilionL",
                       "EndocanthionL", "EndocanthionR", "FrontotemporaleL",
                       "FrontotemporaleR", "Glabella", "Gnathion", 
                       "LabialeInferius", "LabialeSuperius", "Nasion",
                       "OtobasionInferiusL", "OtobasionInferiusR",
                       "Stomion","Subnasale", "Supramentale","TragionL",
                       "TragionR", "ZygionL", "ZygionR"]
    
    for lmk_file in os.listdir(csv_path):
        
        if lmk_file[-3:] == "csv":
            df = pd.read_csv(csv_path + "/" + lmk_file)
            df = df[['lmk_name', 'x_coord', 'y_coord', 'z_coord']]
            
            # Align predicted_landmarks in the space of ground truth landmarks
            landmarks_transformation = df[['lmk_name','x_coord','y_coord', 'z_coord']].to_numpy()
            gt_df_modelo = GT_DF.loc[dic[lmk_file[:-4]]]
            ground_truth_landmarks = gt_df_modelo[['lmk_name','x_coord','y_coord', 'z_coord']].to_numpy()
            
            landmarks_transformation = landmarks_transformation.tolist()
            ground_truth_landmarks = ground_truth_landmarks.tolist()
            
            for element in landmarks_transformation:
                a = element[0].replace("'", "")
                a = a.replace(" ", "")

                if (lista_landmarks.count(a) <= 0):
                    landmarks_transformation.remove(element)
                    
            for element in ground_truth_landmarks:
                a = element[0].replace("'", "")
                a = a.replace(" ", "")

                if (lista_landmarks.count(a) <= 0):
                    ground_truth_landmarks.remove(element)
                    
            
            landmarks_transformation_1 = []
            for element in landmarks_transformation:
                landmarks_transformation_1.append(element[1:])
                
            ground_truth_landmarks_1 = []
            for element in ground_truth_landmarks:
                ground_truth_landmarks_1.append(element[1:])
                
            landmarks_transformation = np.array(landmarks_transformation_1)
            predicted_landmarks = df[['x_coord','y_coord', 'z_coord']].to_numpy()
            predicted_landmarks = compute_rigid_alignment(ground_truth_landmarks_1, predicted_landmarks,landmarks_transformation)
            df.iloc[:,1:4] = predicted_landmarks
            
            df.insert(0, 'Modelo', dic[lmk_file[:-4]])
            df = df.set_index('Modelo')
            df_list.append(df)
        
    df_all_lmks = pd.concat(df_list)
    
    
    return df_all_lmks

def get_error_dataframe(gt_df, predicted_df):
    distance_df = predicted_df.iloc[:, :1]
    pre_df_dist = predicted_df.iloc[:, -3:]
    gt_df_dist = gt_df.iloc[:, -3:]
    
    tmp = ((pre_df_dist['x_coord'] - gt_df_dist['x_coord'])**2 + (pre_df_dist['y_coord'] - gt_df_dist['y_coord'])**2 + (pre_df_dist['z_coord'] - gt_df_dist['z_coord'])**2)**(1/2)
    
    distance_df = pd.concat([distance_df, tmp], axis=1)
    distance_df.columns=['lmk_name', 'dst_euclidea']

    return distance_df


def estadisitcos_modelo(error_df):
    data = error_df.groupby('Modelo')
    
    return data.describe()


def estadisticos_landmark_modelo(error_df):
    df = error_df[['lmk_name','dst_euclidea']]
    
    data = df.groupby('lmk_name')
    return data.describe()


def estadisticos_todos_lmks_todos_modelos(error_df):
    
    return error_df['dst_euclidea'].describe()


def need_preparation(method, folder_path, lmk_type):
    num_csv_files = len(glob.glob1(folder_path,"*.csv"))
    
    folder_preparation = True
    
    if (num_csv_files == 15):
        print("Saltando la preparación y conversión de los landmarks {}\
              del método {}".format(lmk_type, method))
        folder_preparation = False
    elif (num_csv_files != 0):
        print("Borrando los archivos csv existentes para iniciar la preparación\
              de los landmarks desde 0 del método {}".format(method))
    
        files = os.listdir(folder_path)
        for item in files:
            if item.endswith(".csv"):
                os.remove(os.path.join(folder_path, item))
                
    return folder_preparation
    
    

def folder_preparation(folder_path, predicted_lmks_path):
    for file in os.listdir(folder_path):
        if "filtered_" in file:
            os.remove(os.path.join(folder_path, file))
    
    for file in os.listdir(folder_path):
        if file.endswith('.pp'):
            predicted_lmk_path = predicted_lmks_path + '/' + file
            predicted_lmks_dict = filter_gt_landmarks.get_predicted_landmarks(predicted_lmk_path)
            
            created_file = folder_path + '/' + 'filtered_' + file
            filter_gt_landmarks.filter_pp_file(predicted_lmks_dict, folder_path + '/' + file, created_file)
    
    for file in os.listdir(folder_path):
        if "filtered" in file:
            created_file = folder_path + '/' + file
            filter_gt_landmarks.pp_to_csv(created_file)


def predicted_landmark_preparation(folder_path, gt_lmks_path):
    for file in os.listdir(folder_path):
        if file.endswith('.pp'):
            gt_lmk_path = gt_lmks_path + '/' + file
            gt_lmks_dict = filter_gt_landmarks.get_predicted_landmarks(gt_lmk_path)
            
            created_file = folder_path + '/' + 'filtered_' + file
            
            filter_gt_landmarks.filter_predicted_pp_file(gt_lmks_dict, folder_path + '/' + file, created_file)
            
    for file in os.listdir(folder_path):
        if "filtered" in file:
            filter_gt_landmarks.pp_to_csv(folder_path + '/' + file)
    
if __name__ == '__main__':
    #convert_pp_to_csv('/home/angel/Escritorio/NowDatasetExp2/lmk_truth')
    
    ##########################################################################
    #
    # Bloque de código para la preparación automática de la estructura de carpetas
    # necesaria y la transformación de formato de los landmarks de cada método
    #
    ##########################################################################  
    os.chdir('/home/angel/Escritorio/Informatica/TFG/Evaluacion 2')
    
    if not os.path.isdir('./lmk_truth_vrn'):
        sys.exit("Debe existir un fichero llamado lmk_truth_vrn con los landmarks\
              verdaderos del modelo VRN")
    elif not os.path.isdir('./lmk_truth_deca'):
        sys.exit("Debe existir un fichero llamado lmk_truth_deca con los landmarks\
              verdaderos del modelo DECA")
    elif not os.path.isdir('./lmk_truth_mvfnet'):
        sys.exit("Debe existir un fichero llamado lmk_truth_mvfnet con los landmarks\
              verdaderos del modelo MVFNET")
    elif not os.path.isdir('./lmk_truth_p2v'):
        sys.exit("Debe existir un fichero llamado lmk_truth_p2v con los landmarks\
              verdaderos del modelo P2V")
    
        
    folder_preparation_deca = need_preparation('DECA', './gt_lmks/DECA', "ground truth")
    folder_preparation_mvfnet = need_preparation('MVFNET', './gt_lmks/MVFNET', "ground truth")
    folder_preparation_p2v = need_preparation('P2V', './gt_lmks/P2V', "ground truth")
    folder_preparation_vrn = need_preparation('VRN', './gt_lmks/VRN', "ground truth")
    
    if folder_preparation_deca:
        folder_preparation('./gt_lmks/DECA', "./predicted_lmks/DECA")
    
    if folder_preparation_mvfnet:
        folder_preparation('./gt_lmks/MVFNET', "./predicted_lmks/MVFNET")   
        
    if folder_preparation_p2v:
        folder_preparation('./gt_lmks/P2V', "./predicted_lmks/P2V")   
        
    if folder_preparation_vrn:
        folder_preparation('./gt_lmks/VRN', "./predicted_lmks/VRN")   
        
    
    folder_predicted_preparation_deca = need_preparation('DECA', "./predicted_lmks/DECA", "predicted")
    folder_predicted_preparation_mvfnet = need_preparation('MVFNET', "./predicted_lmks/MVFNET", "predicted")
    folder_predicted_preparation_p2v = need_preparation('P2V', "./predicted_lmks/P2V", "predicted")
    folder_predicted_preparation_vrn = need_preparation('VRN', "./predicted_lmks/VRN", "predicted")
    
    if folder_predicted_preparation_deca:
        predicted_landmark_preparation("./predicted_lmks/DECA", './lmk_truth_deca')
        
    if folder_predicted_preparation_mvfnet:
        predicted_landmark_preparation("./predicted_lmks/MVFNET", './lmk_truth_mvfnet')
        
    if folder_predicted_preparation_p2v:
        predicted_landmark_preparation("./predicted_lmks/P2V", './lmk_truth_p2v')
        
    if folder_predicted_preparation_vrn:
        predicted_landmark_preparation("./predicted_lmks/VRN", './lmk_truth_vrn')
        
    
    ##########################################################################
    #
    # Lectura de los landmarks ground truth y predichos de cada modelo para
    # calcular estadísticos a partir de estos.
    #
    ##########################################################################
    dic = create_dict_name()

    GT_df_VRN = read_GT_PP_from_csv(dic, './gt_lmks/VRN')
    PREDICTED_df_VRN = read_predicted_lmk_from_csv(dic, "./predicted_lmks/VRN", GT_df_VRN)
    GT_df_DECA = read_GT_PP_from_csv(dic, './gt_lmks/DECA')
    PREDICTED_df_DECA = read_predicted_lmk_from_csv(dic, "./predicted_lmks/DECA", GT_df_DECA)
    GT_df_P2V = read_GT_PP_from_csv(dic, './gt_lmks/P2V')
    PREDICTED_df_P2V = read_predicted_lmk_from_csv(dic, "./predicted_lmks/P2V", GT_df_P2V)
    GT_df_MVFNET = read_GT_PP_from_csv(dic, './gt_lmks/MVFNET')
    PREDICTED_df_MVFNET = read_predicted_lmk_from_csv(dic, "./predicted_lmks/MVFNET", GT_df_MVFNET)

    ##########################################################################
    #
    # Cálculo de los estadísticos de cada modelo con la ayuda de la biblioteca
    # pandas
    #
    ##########################################################################
    error_df_VRN = get_error_dataframe(GT_df_VRN, PREDICTED_df_VRN)
    error_df_DECA = get_error_dataframe(GT_df_DECA, PREDICTED_df_DECA)
    error_df_P2V = get_error_dataframe(GT_df_P2V, PREDICTED_df_P2V)
    error_df_MVFNET = get_error_dataframe(GT_df_MVFNET, PREDICTED_df_MVFNET)
    
    est_error_VRN = estadisitcos_modelo(error_df_VRN)
    est_lmk_VRN = estadisticos_landmark_modelo(error_df_VRN)
    tmp_VRN = estadisticos_todos_lmks_todos_modelos(error_df_VRN)
    
    est_error_DECA = estadisitcos_modelo(error_df_DECA)
    est_lmk_DECA = estadisticos_landmark_modelo(error_df_DECA)
    tmp_DECA = estadisticos_todos_lmks_todos_modelos(error_df_DECA)
    
    est_error_P2V = estadisitcos_modelo(error_df_P2V)
    est_lmk_P2V = estadisticos_landmark_modelo(error_df_P2V)
    tmp_P2V = estadisticos_todos_lmks_todos_modelos(error_df_P2V)
    
    est_error_MVFNET = estadisitcos_modelo(error_df_MVFNET)
    est_lmk_MVFNET = estadisticos_landmark_modelo(error_df_MVFNET)
    tmp_MVFNET = estadisticos_todos_lmks_todos_modelos(error_df_MVFNET)
    
    
    
    print("Mediana VRN: "     , error_df_VRN[['dst_euclidea']].median())
    print("Mediana DECA: "    , error_df_DECA[['dst_euclidea']].median())
    print("Mediana mvfnet: "  , error_df_MVFNET[['dst_euclidea']].median())
    print("Mediana P2V: "     , error_df_P2V[['dst_euclidea']].median())

    
    
    ##########################################################################
    # Creación de un diagrama de cajas para la visualización de los estadísticos
    # calculados
    ##########################################################################
    error_df_VRN['Metodo']='VRN'
    error_df_DECA['Metodo'] = 'DECA'
    error_df_MVFNET['Metodo'] = "MVF-Net"
    error_df_P2V['Metodo'] = "P2V"
    
    old_values_vrn= ["Alare' L", "Alare' R", "Cheilion' L", "Cheilion' R",
                     "Endocanthion' L","Endocanthion' R", "Exocanthion' L",
                     "Exocanthion' R","Frontotemporale' L","Frontotemporale' R",
                     "Frontozygomaticus' L", "Frontozygomaticus' R", "Glabella",
                     "Gnathion'", "Gonion' L","Gonion' R", "Labiale Inferius'",
                     "Labiale Superius'","Menton","Midsupraorbital' L","Midsupraorbital' R",
                     "Nasion'","Otobasion Inferius' L","Otobasion Inferius' R","Pogonion",
                     "Pronasale'","Stomion'","Subnasale'","Supramentale'","Tragion L",
                     "Tragion R", "Zygion' L","Zygion' R",]
    
    new_values = ["AlL", "AlR", "ChL", "ChR", "EnL", "EnR", "ExL", "ExR", "FtL",
                  "FtR", "FzgyL", "FzgyR", "Gl", "Gn", "GoL", "GoR", "Li",
                  "Ls", "Me", "MsoL", "MsoR", "Na", "OL", "OR", "Po", "Prn",
                  "St", "Sbn", "Sm", "TrL", "TrR", "ZygL", "ZygR"]
    
    error_df_VRN['lmk_name'] = error_df_VRN['lmk_name'].replace(old_values_vrn,new_values)
    error_df_DECA['lmk_name'] = error_df_DECA['lmk_name'].replace(old_values_vrn,new_values)
    error_df_MVFNET['lmk_name'] = error_df_MVFNET['lmk_name'].replace(old_values_vrn,new_values)
    error_df_P2V['lmk_name'] = error_df_P2V['lmk_name'].replace(old_values_vrn,new_values)
    
    cdf = pd.concat([error_df_VRN, error_df_DECA, error_df_MVFNET, error_df_P2V]) 
    
    cdf.rename(columns = {'lmk_name':'Landmarks', 'dst_euclidea':'Dst. Eucl.'}, inplace = True)
    cdf = cdf.sort_values("Landmarks")
    ax = sns.boxplot(x="Landmarks", y="Dst. Eucl.", hue="Metodo", data=cdf)
    
    ax.set_title("Distribución de error de cada método por landmark")
    ax.set_xticklabels(ax.get_xticklabels(),rotation=90)
    ax.tick_params(labelsize=10)
    plt.show()
    
    
    methods = ["DECA", "MVFNET", "P2V", "VRN"]
    
    for method in methods:
        folder = "./results/" + method + "/"
        for file in os.listdir(folder):
            os.remove(os.path.join(folder, file))
    
    est_error_DECA.to_csv('./results/DECA/est_error_DECA.csv', sep='\t')
    est_error_DECA.to_excel('./results/DECA/est_error_DECA.xlsx')
    est_error_MVFNET.to_csv('./results/MVFNET/est_error_MVFNET.csv', sep='\t')
    est_error_MVFNET.to_excel('./results/MVFNET/est_error_MVFNET.xlsx')
    est_error_P2V.to_csv('./results/P2V/est_error_P2V.csv', sep='\t')
    est_error_P2V.to_excel('./results/P2V/est_error_P2V.xlsx')
    est_error_VRN.to_csv('./results/VRN/est_error_VRN.csv', sep='\t')
    est_error_VRN.to_excel('./results/VRN/est_error_VRN.xlsx')
    
    est_lmk_DECA.to_excel('./results/DECA/est_lmk_DECA.xlsx')
    est_lmk_MVFNET.to_excel('./results/MVFNET/est_lmk_MVFNET.xlsx')
    est_lmk_P2V.to_excel('./results/P2V/est_lmk_P2V.xlsx')
    est_lmk_VRN.to_excel('./results/VRN/est_lmk_VRN.xlsx')

    tmp_DECA.to_csv('./results/DECA/est_generales_DECA', sep='\t')
    tmp_MVFNET.to_csv('./results/MVFNET/est_generales_MVFNET', sep='\t')
    tmp_P2V.to_csv('./results/P2V/est_generales_P2V', sep='\t')
    tmp_VRN.to_csv('./results/VRN/est_generales_VRN', sep='\t')
    
    error_df_DECA.to_excel('./results/DECA/error_exp2.xlsx')
    error_df_DECA.to_csv('./results/DECA/error_exp2.csv', sep='\t')
    error_df_MVFNET.to_excel('./results/MVFNET/error_exp2.xlsx')
    error_df_MVFNET.to_csv('./results/MVFNET/error_exp2.csv', sep='\t')
    error_df_P2V.to_excel('./results/P2V/error_exp2.xlsx')
    error_df_P2V.to_csv('./results/P2V/error_exp2.csv', sep='\t')
    error_df_VRN.to_excel('./results/VRN/error_exp2.xlsx')
    error_df_VRN.to_csv('./results/VRN/error_exp2.csv', sep='\t')

# =============================================================================
#     print("Landmarks con dist > 5: ", error_df[error_df.dst_euclidea > 5].shape)
#     print("Landmarks con dist < 5: ", error_df[error_df.dst_euclidea < 5].shape)
#     
#     print("% de landmarks > 5: ", (error_df[error_df.dst_euclidea > 5].shape[0]*100)/483)
#     print("% de landmarks < 5: ", (error_df[error_df.dst_euclidea < 5].shape[0]*100)/483)
#     
#     print("% de landmarks > 6: ", (error_df[error_df.dst_euclidea > 6].shape[0]*100)/483)
#     print("% de landmarks < 6: ", (error_df[error_df.dst_euclidea < 6].shape[0]*100)/483)
#     
#     print("% de landmarks > 7: ", (error_df[error_df.dst_euclidea > 7].shape[0]*100)/483)
#     print("% de landmarks < 7: ", (error_df[error_df.dst_euclidea < 7].shape[0]*100)/483)
#     
#     print("% de landmarks > 10: ", (error_df[error_df.dst_euclidea > 10].shape[0]*100)/483)
#     print("% de landmarks < 10: ", (error_df[error_df.dst_euclidea < 10].shape[0]*100)/483)
#     
#     print("% de landmarks > 13: ", (error_df[error_df.dst_euclidea > 13].shape[0]*100)/483)
#     print("% de landmarks < 13: ", (error_df[error_df.dst_euclidea < 13].shape[0]*100)/483)
#     
#     #print("% de landmarks > 15: ", (error_df[error_df.dst_euclidea > 15].shape[0]*100)/483)
#     #print("% de landmarks < 15: ", (error_df[error_df.dst_euclidea < 15].shape[0]*100)/483)
#     
#     #print("% de landmarks > 20: ", (error_df[error_df.dst_euclidea > 20].shape[0]*100)/483)
#     #print("% de landmarks < 20: ", (error_df[error_df.dst_euclidea < 20].shape[0]*100)/483)
#     
#     error_df[error_df.dst_euclidea > 13].to_csv("./lmk_error>13")
#     
#     error_df.loc[(error_df['dst_euclidea']>=10) & (error_df['dst_euclidea']<=13)].to_csv("./lmk_errorEntre10y13")
#     
#     #print(error_df[error_df.dst_euclidea < 5].to_string())
#     
#     #occur = error_df[error_df.dst_euclidea < 5].groupby(['lmk_name']).size()
#     #display(occur)
#     error_df.to_csv('./error_exp2.csv')
# =============================================================================
