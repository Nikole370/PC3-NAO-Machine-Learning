# -*- coding: utf-8 -*-
# NAO + modelo IA

from naoqi import ALProxy
import joblib
import numpy as np

# Conectamos al robot
ROBOT_IP = "192.168.X.X"  # Cambia por el IP de tu NAO
PORT = 9559

tts = ALProxy("ALTextToSpeech", ROBOT_IP, PORT)
motion = ALProxy("ALMotion", ROBOT_IP, PORT)

# Cargamos el modelo entrenado
clf = joblib.load('modelo_senales.pkl')

# Simulamos un input (esto lo cambiarás por tus features reales)
input_features = np.random.rand(1, 64)  # Solo como ejemplo

# Hacemos la predicción
pred = clf.predict(input_features)[0]

# Mapear la predicción a la acción
if pred == 0:
    tts.say("Detecté PARE. Me detengo.")
    motion.stopMove()
elif pred == 1:
    tts.say("Detecté Cruce peatonal. Saludo.")
    motion.setAngles("LShoulderPitch", -0.5, 0.2)
elif pred == 2:
    tts.say("Semáforo rojo. Espero.")
elif pred == 3:
    tts.say("Semáforo verde. Camino.")
    motion.walkTo(0.5, 0, 0)
else:
    tts.say("No reconozco la señal.")
