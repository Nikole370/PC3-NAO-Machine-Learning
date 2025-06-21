from naoqi import ALProxy
import requests
import time

NAO_IP = "127.0.0.1"
NAO_PORT = 50748
SERVER_URL = "http://192.168.1.34:5000/predict" 

camProxy = ALProxy("ALVideoDevice", NAO_IP, NAO_PORT)
tts = ALProxy("ALTextToSpeech", NAO_IP, NAO_PORT)

resolution = 2    
colorSpace = 11  
fps = 5
nameId = camProxy.subscribeCamera("objectRecognition", 0, resolution, colorSpace, fps)

time.sleep(1)

image = camProxy.getImageRemote(nameId)
camProxy.unsubscribe(nameId)

width = image[0]
height = image[1]
array = image[6]
image_string = bytearray(array)

with open("/tmp/image.png", "wb") as f:
    f.write(image_string)

with open("/tmp/image.png", "rb") as f:
    response = requests.post(SERVER_URL, files={"image": f})

if response.status_code == 200:
    data = response.json()
    label = data["label"]
    confidence = data["confidence"]
    tts.say("Creo que veo un " + label + " con " + str(int(confidence * 100)) + " por ciento de certeza.")
else:
    tts.say("No pude reconocer el objeto.")
