"""#-----------------------------TALLER 5: camara y calibracion---------------------------------------------------------
                              Erick Steven Badillo Vargas
                                Ingenieria Electronica
                           Procesamiento de imagenes y vision
                                    Julian Quiroga
                                         2020
#----------------------------------------------------------------------------------------------------------------------#"""
import numpy as np
import cv2
import json
from Clases import projective_camera
from Clases import set_rotation
from Clases import projective_camera_project
import os

path = "/Users/Erick/Desktop/OCTAVO SEMESTRE/PROC DE IMAGENES/Camara y Calibracion/Tablero"  # Ubicacion archivo
file_name = 'calibration.json'                  # Nombre del JSON para camara celular
# file_name = 'calibrationweb.json'                  # Nombre del JSON para camara Web
json_file = os.path.join(path, file_name)       # Abrir archivo
with open(json_file) as fp:
    json_data = json.load(fp)                   # leer archivo

# Importar del archivo JSON
K = json_data['K']                      # Importar K
d = json_data['d'][0]                   # Importar d
tilt = json_data['tilt'][0]             # Importar tilt
pan = json_data['pan'][0]               # Importar pan
h = json_data['h'][0]                   # Importar h


# Tamaño de la imagen
width = 1920                            # Ancho de la imagen
height = 1080                           # Alto de la imagen


# Parametros Extrinsecos
R = set_rotation(tilt, pan, 0)          # Matriz de Rotacion R
t = np.array([0, -d, h])                # Matriz de traslacion t

# Crear Modelo de Camara a partir de la calibracion
camera = projective_camera(K, width, height, R, t)


# Puntos para el Cubo 3D
square_3D = np.array([[0.5, -0.5,0.5], [0.5, -0.5, -0.5], [-0.5, -0.5, -0.5], [-0.5, -0.5, 0.5]])
square_2D = projective_camera_project(square_3D, camera)        # Crear Proyeccion
square_3D_2 = np.array([[0.5, 0.5, 0.5], [0.5, 0.5, -0.5], [-0.5, 0.5, -0.5], [-0.5, 0.5, 0.5]])
square_2D_2 = projective_camera_project(square_3D_2, camera)    # Crear Proyeccion

# Crear imagen sobre la que se va a escribir
image_projective = 255 * np.ones(shape=[camera.height, camera.width, 3], dtype=np.uint8)

# lineas para unir cuadrados
cv2.line(image_projective, (square_2D[3][0], square_2D[3][1]), (square_2D_2[3][0], square_2D_2[3][1]), (255, 255, 0), 3)
cv2.line(image_projective, (square_2D[0][0], square_2D[0][1]), (square_2D_2[0][0], square_2D_2[0][1]), (255, 255, 0), 3)
cv2.line(image_projective, (square_2D[1][0], square_2D[1][1]), (square_2D_2[1][0], square_2D_2[1][1]), (255, 255, 0), 3)

# Crear lineas cuadrado 2 2D
cv2.line(image_projective, (square_2D_2[0][0], square_2D_2[0][1]), (square_2D_2[1][0], square_2D_2[1][1]), (0, 255, 0), 3)
cv2.line(image_projective, (square_2D_2[1][0], square_2D_2[1][1]), (square_2D_2[2][0], square_2D_2[2][1]), (0, 255, 0), 3)
cv2.line(image_projective, (square_2D_2[2][0], square_2D_2[2][1]), (square_2D_2[3][0], square_2D_2[3][1]), (0, 255, 0), 3)
cv2.line(image_projective, (square_2D_2[3][0], square_2D_2[3][1]), (square_2D_2[0][0], square_2D_2[0][1]), (0, 255, 0), 3)

# Crear linea cuadrado 1
cv2.line(image_projective, (square_2D[0][0], square_2D[0][1]), (square_2D[1][0], square_2D[1][1]), (200, 0, 0), 3)
cv2.line(image_projective, (square_2D[1][0], square_2D[1][1]), (square_2D[2][0], square_2D[2][1]), (200, 1, 0), 3)
cv2.line(image_projective, (square_2D[2][0], square_2D[2][1]), (square_2D[3][0], square_2D[3][1]), (200, 1, 0), 3)
cv2.line(image_projective, (square_2D[3][0], square_2D[3][1]), (square_2D[0][0], square_2D[0][1]), (200, 1, 0), 3)
cv2.line(image_projective, (square_2D[2][0], square_2D[2][1]), (square_2D_2[2][0], square_2D_2[2][1]), (255, 255, 0), 3)

cv2.imshow("Image", image_projective)       # Mostrar cubo
cv2.waitKey(0)
