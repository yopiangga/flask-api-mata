# Flask API untuk konversi gambar ke base64
from flask import Flask, request, jsonify
import base64

app = Flask(__name__)

@app.route('/image', methods=['POST'])
def convert_image():
    imagefile = request.files['image'] 
    img = imagefile.read()

    img_base64 = base64.b64encode(img).decode('utf-8')

    response = {
        'base64': img_base64
    }

    return jsonify(response)

# Klasifikasi gambar menggunakan ImageAI

from imageai.Classification import ImageClassification

prediction = ImageClassification()
prediction.setModelTypeAsMobileNetV2()
prediction.setModelPath("model/mobilenet_v2.h5")
prediction.loadModel()

# Gabungkan kedua kode

@app.route('/image', methods=['POST'])  
def convert_and_classify_image():
    
    # Ambil gambar dan ubah ke base64
    imagefile = request.files['image']
    img = imagefile.read()
    img_base64 = base64.b64encode(img).decode('utf-8')

    # Klasifikasi gambar
    predictions, probabilities = prediction.classifyImage(img)

    # Kembalikan hasil klasifikasi dan base64
    result = {
        'base64': img_base64,
        'predictions': predictions
    }

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)