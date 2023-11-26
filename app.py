from flask import Flask, request, jsonify
import numpy
from flask_cors import CORS, cross_origin
import audio_to_text as at
import base64

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
def hello_world():
	return 'Hello Team Mata Netra | Auto Deploy follow Branch Master 2'

@app.route('/message', methods=['POST'])
@cross_origin()
def post_example():
	data = request.get_json()
	message = data.get('message', 'No message provided',)
	response = {'status': 'success', "result_text": message}
	return jsonify(response)

@app.route('/audio', methods=['POST'])
def upload_file():
    try:
        # Check if the request contains a file
        if 'audio' not in request.files:
            return jsonify({'status': 'error', 'message': 'No file part'}), 400

        file = request.files['audio']

        # Check if the file is present and has a allowed file extension
        if file.filename == '':
            return jsonify({'status': 'error', 'message': 'No selected file'}), 400

        # You can customize the allowed file extensions
        allowed_extensions = {'wav', 'mp3'}
        if '.' not in file.filename or file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
            return jsonify({'status': 'error', 'message': 'Invalid file extension'}), 400
		
        audio_binary = file.read()

        # Encode the binary content to base64
        base64_audio = base64.b64encode(audio_binary).decode('utf-8')
        
        result = at.base64_to_text(base64_audio)

        if result == "Failed to translate audio":
            return jsonify({'status': 'error', 'message': 'Failed to translate audio'}), 400
        if result == "Cannot requst Google API":
            return jsonify({'status': 'error', 'message': 'Cannot requst Google API'}), 500

        return jsonify({'status': 'succes', 'message': result}), 200

		# # Process other form data
        # form_data = request.form.to_dict()
        # print(f"Form Data: {form_data}")

        # # Handle the file as needed, for example, save it to a server or process it
        # # In this example, we just print the file name
        # print(f"Received file: {file.filename}")

        # return jsonify({'status': 'success', 'message': 'File uploaded successfully'}), 200

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

# main driver function
if __name__ == '__main__':
	# app.run()
	app.run(debug=True, host='0.0.0.0', port=5000)
