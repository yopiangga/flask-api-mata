from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import base64

import method.audio_to_text as at
import method.distance as distance
import method.azimuth as azimuth
import method.image_classifiation as image_classifiation
import method.similarity as similarity
import config.app as config

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
def hello_world():
	return 'Mata Netra v ' + config.version

@app.route('/get-routes', methods=['GET'])
def get_routes():
    return jsonify({'routes': distance.data})

@app.route('/shortest_path', methods=['POST'])
# @cross_origin()
def shortest_path():
    data = request.get_json()
    source = data['source']
    target = data['target']
    return distance.get_distance(source, target)

@app.route('/azimuth', methods=['POST'])
# @cross_origin()
def get_azimuth():
    data = request.get_json()
    source = data['source']
    target = data['target']
    return jsonify({'azimuth': azimuth.calculate_azimuth(source['lat'], source['lng'], target['lat'], target['lng'])})

@app.route('/audio-to-text', methods=['POST'])
@cross_origin()
def audio_to_text():
    try:
        if 'audio' not in request.files:
            return jsonify({'status': 'error', 'message': 'No file part'}), 400

        file = request.files['audio']

        if file.filename == '':
            return jsonify({'status': 'error', 'message': 'No selected file'}), 400

        allowed_extensions = {'wav', 'mp3'}
        if '.' not in file.filename or file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
            return jsonify({'status': 'error', 'message': 'Invalid file extension'}), 400
		
        audio_binary = file.read()

        base64_audio = base64.b64encode(audio_binary).decode('utf-8')

        result = at.base64_to_text(base64_audio)

        if result == "Failed to translate audio":
            return jsonify({'status': 'error', 'message': 'Failed to translate audio'}), 400
        if result == "Cannot requst Google API":
            return jsonify({'status': 'error', 'message': 'Cannot requst Google API'}), 500

        return jsonify({'status': 'succes', 'message': result}), 200

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/image-classification', methods=['POST'])  
# @cross_origin()
def classify_image():
    imagefile = request.files['image']
    img = imagefile.read()
    img_base64 = base64.b64encode(img).decode('utf-8')

    # predictions, probabilities = prediction.classifyImage(img)
    # Load and preprocess the image
    processed_image = process_image(img)

    # Use the model to classify the image
    predictions = model.predict(processed_image)

    result = {
        'base64': img_base64,
        'predictions': "predictions"
    }
    return jsonify(result)

@app.route('/speech-to-route', methods=['POST'])
# @cross_origin()
def speech_to_route():
    data = request.get_json()
    speech = data['speech']

    temp = similarity.speech_to_route(speech)
    return jsonify({'status': 'succes', 'route': temp}), 200

if __name__ == '__main__':
	# app.run()
	app.run(debug=True, host='0.0.0.0', port=5000)
    #  app.run(debug=True, host='0.0.0.0', port=5000)
