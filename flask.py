# -*- coding: utf-8 -*-
import os
import sys
import subprocess
from naoqi import ALProxy
import time
from PIL import Image  # del módulo PIL de Python 2: `pip install PIL` si no lo tienes


ROBOT_IP = "169.254.206.34"
ROBOT_PORT = 9559
temp_path = "temp.jpg"

# Capturar imagen desde la cámara del NAO
try:
    video = ALProxy("ALVideoDevice", ROBOT_IP, ROBOT_PORT)
    name_id = video.subscribeCamera("python_client", 0, 2, 11, 30)
    nao_image = video.getImageRemote(name_id)
    video.unsubscribe(name_id)


    if nao_image is None:
        print("Error: no se pudo capturar imagen desde NAO")
        sys.exit(1)

    width = nao_image[0]
    height = nao_image[1]
    array = nao_image[6]

    # Convertir la imagen a formato RGB y guardar como JPEG
    image = Image.frombytes("RGB", (width, height), array)
    image.save(temp_path, "JPEG")
    print("Imagen guardada en", temp_path)

except Exception as e:
    print("Error capturando imagen desde NAO:", e)
    sys.exit(1)

# Ejecutar el script que detecta dedos
try:
    result = subprocess.check_output(["C:/Python312/python.exe", "detectnumber.py", temp_path])
    result = result.strip()
except Exception as e:
    print("Error ejecutando detectnumber.py:", e)
    sys.exit(1)

# Comunicación con NAO
tts = ALProxy("ALTextToSpeech", ROBOT_IP, ROBOT_PORT)

# Aviso al usuario
tts.say("Prepárate para mostrar los dedos. Tomaré la foto en 3 segundos.")
time.sleep(3)  # Espera 3 segundos para que pongas la mano

# Ahora captura la imagen
video = ALProxy("ALVideoDevice", ROBOT_IP, ROBOT_PORT)
name_id = video.subscribeCamera("python_client", 0, 2, 11, 30)
nao_image = video.getImageRemote(name_id)
video.unsubscribe(name_id)

if nao_image is None:
    print("Error: no se pudo capturar imagen desde NAO")
    tts.say("Error tomando la foto")
    sys.exit(1)

# Guarda la imagen
width = nao_image[0]
height = nao_image[1]
array = nao_image[6]
image = Image.frombytes("RGB", (width, height), array)
image.save(temp_path, "JPEG")
print("Imagen guardada en", temp_path)
tts.say("Foto tomada. Procesando.")
# Ejecutar el script que detecta dedos
try:
    result = subprocess.check_output(["C:/Python312/python.exe", "detectnumber.py", temp_path])
    result = result.strip()
except Exception as e:
    print("Error ejecutando detectnumber.py:", e)
    tts.say("Error ejecutando el análisis de dedos.")
    sys.exit(1)

# Decir el resultado
if result.isdigit():
    fingers_up = int(result)
    print("Estas mostrando {} deditos.".format(fingers_up))
    tts.say("Estas mostrando {} deditos.".format(fingers_up))
else:
    print("No se pudieron detectar los dedos.")
    tts.say("No se pudieron detectar los dedos.")


