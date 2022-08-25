# TFG

Generación de modelos faciales 3D a partir de fotografías: Estudio de viabilidad en el ámbito forense.

Este repositorio contiene todos los ficheros necesarios para realizar las dos evaluaciones realizadas en este trabajo:

  1. Análiss denso: realizado a partir de la evaluación NoW: https://github.com/soubhiksanyal/now_evaluation
  2. Análisis a nivel de landmark: evaluación a nivel de landmark de todos los modelos.



# Métodos escogidos
El código de los métodos escogidos y sus respectivas guías de instalación se encuentran en los siguientes enlaces:
  * DECA: https://github.com/YadiraF/DECA
  * MVFNET: https://github.com/whwu95/MVFNet
  * Pix2Vertex: https://github.com/eladrich/pix2vertex.pytorch
  * VRN: https://github.com/AaronJackson/vrn
  
  
# Guía de uso 
Ambas evaluaciones están totalmente automatizadas. Para ejecutar la evaluación 2 hay que utilizar el siguiente comando:

    python ./codigo.py
                                                     
Una vez ejecutada la evaluación 2 se puede proceder con el análisis denso, para ello hay que realizar los siguientes pasos

    python ./analisis_denso_eval2.py
                                                     
Y por últimos solo habría que realizar los dos análisis densos con las siguientes instrucciones:

   - método -> parámetro que puede contener los siguientes valores: `DECA | MVFNET | P2V | VRN`
   - dataset -> parámetro que puede contener los siguientes valores: `NoW | DID`

   - Análisis denso dataset 2: `python compute_error.py ../Evaluacion\ 2 ../Evaluacion\ 2/predicted_mesh/<método>/ <dataset> <método> val`
   - Análisis denso dataset 1: `python compute_error.py ../Evaluacion\ 1 ../Evaluacion\ 1/marcados/<método>/ <dataset> <método> val`
   
   
 # Requisitos
 Para ejecutar los siguientes códigos no se requiere ningún tipo de requisito mas allá de:
 
  - Numpy
  - Python version: 3.x (en mi caso he utilzado la versión 3.7.6)
  - Pandas
  - Seaborn
