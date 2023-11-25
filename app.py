from flask import Flask, request, jsonify
import numpy
from flask_cors import CORS, cross_origin

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
	message = data.get('message', 'No message provided')
	response = {'status': 'success', "result_text": message}
	return jsonify(response)

# main driver function
if __name__ == '__main__':
	# app.run()
	app.run(debug=True, host='0.0.0.0', port=5000)
