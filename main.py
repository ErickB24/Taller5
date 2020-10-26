"""#-----------------------------TALLER 5: camara y calibracion---------------------------------------------------------
                              Erick Steven Badillo Vargas
                                Ingenieria Electronica
                           Procesamiento de imagenes y vision
                                    Julian Quiroga
                                         2020
#----------------------------------------------------------------------------------------------------------------------#"""

import numpy as np
import cv2
import glob
import os
import json

# Criterio de iteraciones
criterio = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Preparar puntos
objp = np.zeros((7 * 7, 3), np.float32)
objp[:, :2] = np.mgrid[0:7, 0:7].T.reshape(-1, 2)

# Arreglos para guardar los puntos del objeto
objpoints = []  # 3d point in real world space
imgpoints = []  # 2d points in image plane.

# Ubicacion de las imagenes (tablero de ajedrez)
path = "/Users/Erick/Desktop/OCTAVO SEMESTRE/PROC DE IMAGENES/Camara y Calibracion/Tablero"

# Camara Celular
path_file = os.path.join(path, 'IGM*.PNG')  # Elegir archivos que contengan IGM
# Camara Web
# path_file = os.path.join(path, 'WIN*.jpg')  # Elegir archivos que contengan WIN (camara de Windows)

images = glob.glob(path_file)       # Glob de Imagenes

for fname in images:                                                # Para cada una de las imagenes :

    img = cv2.imread(fname)                                         # Leer Imagen
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)                # Imagen en Grises

    # Encontrar las esquinas del tablero de Ajedrez
    ret, corners = cv2.findChessboardCorners(img_gray, (7, 7), None)

    # Si se encuentran las imagenes:
    if ret == True:
        objpoints.append(objp)

        # encontrar pixel con precision sub-pixel
        corners2 = cv2.cornerSubPix(img_gray, corners, (11, 11), (-1, -1), criterio)
        imgpoints.append(corners2)  # Acumular

        # Dibujar esquinas sobre la imagen original
        img = cv2.drawChessboardCorners(img, (7, 7), corners2, ret)
        cv2.imshow('img', img)  # mostrar la imagen
        cv2.waitKey(400)        # Esperar 400 ms

cv2.destroyAllWindows()

#Calibrar camara
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, img_gray.shape[::-1], None, None)

print(mtx)
print(dist)

file_name = 'calibration.json'                  # nombre del archivo de calibracion
# file_name = 'calibrationweb.json'               # nombre del archivo de calibracion camara web
json_file = os.path.join(path, file_name)
d = [3.0]
tilt = [30.0]
pan = [0]
h = [2.0]

# convertir a lista para exportar a JSON
data = {

    'K': mtx.tolist(),              # Matriz K
    'distortion': dist.tolist(),    # Vector distorcion
    'd' : d,                        # Distancia
    'tilt' : tilt,                  # Angulo Tilt
    'pan' : pan,                    # Angulo Pan
    'h' : h                         # altura H
}

# Exportar a JSON
with open(json_file, 'w') as fp:
    json.dump(data, fp, sort_keys=True, indent=1, ensure_ascii=False)



