# -*- coding: utf-8 -*-
# serv.py
from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import pandas as pd

app = Flask(__name__)

# 1) Carga el modelo pre-entrenado
model = tf.keras.models.load_model('gtsrb_model.h5', compile=False)


# 2) Carga el CSV de etiquetas (labels.csv en la misma carpeta)
df = pd.read_csv('labels.csv')
CLASS_MAP = dict(zip(df.ClassId, df.SignName))

def prepare_image(image_bytes):
    # 3) El modelo espera imágenes 32×32 y valores normalizados [0,1]
    image = Image.open(io.BytesIO(image_bytes)).resize((64, 64))  # Ajusta a lo que espera el modelo
    arr = tf.keras.preprocessing.image.img_to_array(image)
    arr = arr / 255.0
    return np.expand_dims(arr, axis=0)

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    # 4) Lee y preprocesa la imagen subida
    image_bytes = request.files['image'].read()
    img = prepare_image(image_bytes)

    # 5) Inferencia
    preds = model.predict(img)               # devuelve shape (1,43)
    cid   = int(np.argmax(preds, axis=1)[0])
    conf  = float(np.max(preds))

    # 6) Traduce el índice a nombre
    label = CLASS_MAP.get(cid, str(cid))
    return jsonify({
        'class_id':   cid,
        'label':      label,
        'confidence': conf
    })

if __name__ == '_main_':
    # Arranca en todas las interfaces, puerto 5000
    app.run(host='0.0.0.0', port=5000)