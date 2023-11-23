from flask import Flask
import numpy

app = Flask(__name__)

@app.route('/')
def hello_world():
	return 'Hello World action'

# main driver function
if __name__ == '__main__':
	app.run()
