import base64
from flask import Flask, request, Response, jsonify
import numpy as np
import networkx as nx
import json
from flask_cors import CORS, cross_origin

import method.distance as distance
import method.azimuth as azimuth
import method.image_classifiation as image_classifiation

app = Flask(__name__)

@app.route('/')
@cross_origin()
def get_home():
    return jsonify({'message': 'Welcome to Mata API'})

@app.route('/get-routes', methods=['GET'])
@cross_origin()
def get_routes():
    return jsonify({'routes': distance.data})

@app.route('/shortest_path', methods=['POST'])
@cross_origin()
def shortest_path():
    data = request.get_json()
    source = data['source']
    target = data['target']
    return distance.get_distance(source, target)

@app.route('/azimuth', methods=['POST'])
@cross_origin()
def get_azimuth():
    data = request.get_json()
    source = data['source']
    target = data['target']
    return jsonify({'azimuth': azimuth.calculate_azimuth(source['lat'], source['lng'], target['lat'], target['lng'])})

@app.route('/image-classification', methods=['POST'])  
@cross_origin()
def classify_image():
    imagefile = request.files['image']
    img = imagefile.read()
    img_base64 = base64.b64encode(img).decode('utf-8')

    # predictions, probabilities = prediction.classifyImage(img)

    result = {
        'base64': img_base64,
        'predictions': "predictions"
    }
    return jsonify(result)

if __name__ == '__main__':
	app.run(debug=False, host='0.0.0.0', port=5000)
	# app.run(debug=True, host='0.0.0.0', port=5000)
