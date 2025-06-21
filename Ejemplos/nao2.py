# obj_rec.py
# -- coding: utf-8 --
import time, io, requests
from PIL import Image
from naoqi import ALProxy

# 1) Configuración
NAO_IP     = "127.0.0.1"
NAO_PORT   = 50748
SERVER_URL = "http://localhost:5000/predict"

# 2) Proxies a los servicios NAOqi
camProxy = ALProxy("ALVideoDevice",  NAO_IP, NAO_PORT)
tts      = ALProxy("ALTextToSpeech", NAO_IP, NAO_PORT)
motion   = ALProxy("ALMotion",       NAO_IP, NAO_PORT)

# 3) Captura de un frame
resolution = 2    # 640×480
colorSpace = 11   # kYuvColorSpace
fps        = 5

#sub_id = camProxy.subscribe("objectRecog", resolution, colorSpace, fps)
sub_id = camProxy.subscribeCamera("objectRecog", 0, resolution, colorSpace, fps)

time.sleep(1)  # espera a llenar el buffer

img_tuple = camProxy.getImageRemote(sub_id)
camProxy.unsubscribe(sub_id)

# img_tuple = [width, height, nbLayers, colorSpace, timestamp, extraData, buffer]
width, height, array = img_tuple[0], img_tuple[1], img_tuple[6]

# Convertimos el buffer en PNG (formato YUV → RGB)
raw = bytearray(array)
img = Image.frombytes('YCbCr', (width, height), bytes(raw))
img = img.convert('RGB')

# 4) Serializamos la imagen en memoria
buf = io.BytesIO()
img.save(buf, format='PNG')
buf.seek(0)

# 5) Enviamos a la API Flask
files = {'image': ('img.png', buf, 'image/png')}
resp = requests.post(SERVER_URL, files=files)

# 6) Parseamos respuesta y decidimos acción
if resp.status_code != 200:
    tts.say("Error reconociendo señal.")
    motion.stopMove()
else:
    data  = resp.json()
    label = data["label"]
    conf  = data["confidence"]

    # 7) Mapeo de acciones según señal
    if "Stop" in label or "Pare" in label:
        tts.say("Señal de PARE. Me detengo.")
        motion.stopMove()

    elif "Ahead" in label or "Adelante" in label:
        tts.say("Sigo adelante.")
        motion.walkTo(0.5, 0, 0)

    elif "Right" in label or "Derecha" in label:
        tts.say("Giro a la derecha y avanzo.")
        motion.walkTo(0, 0, -1.0)
        motion.walkTo(0.5, 0, 0)

    elif "Left" in label or "Izquierda" in label:
        tts.say("Giro a la izquierda y avanzo.")
        motion.walkTo(0, 0, 1.0)
        motion.walkTo(0.5, 0, 0)

    else:
        # Para el resto de señales (velocidad, precaución, etc.)
        msg = "He visto {}. Continúo con precaución.".format(label)
        tts.say(msg)
        motion.walkTo(0.3, 0, 0)