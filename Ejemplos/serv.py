from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
from PIL import Image
import io

app = Flask(__name__)
model = tf.keras.applications.MobileNetV2(weights='imagenet')

def prepare_image(image_bytes):
    image = Image.open(io.BytesIO(image_bytes)).resize((224, 224))
    img_array = tf.keras.preprocessing.image.img_to_array(image)
    img_array = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)
    return np.expand_dims(img_array, axis=0)

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    image = request.files['image'].read()
    img = prepare_image(image)
    preds = model.predict(img)
    decoded = tf.keras.applications.mobilenet_v2.decode_predictions(preds, top=1)[0][0]
    return jsonify({'label': decoded[1], 'confidence': float(decoded[2])})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
