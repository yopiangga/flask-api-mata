
import tensorflow as tf
import keras
import cv2
import numpy as np
import base64
from PIL import Image
import io
from keras.preprocessing import image
from keras.applications import imagenet_utils
from keras.applications import MobileNet
from keras.applications.mobilenet import preprocess_input
from keras.models import load_model

# Load the pre-trained model
model = load_model('model.h5')
model._make_predict_function()
print('Model loaded. Start serving...')

# Load the pre-trained model
model = load_model('model.h5')
model._make_predict_function()
print('Model loaded. Check http://localhost:5000/')

# Initialize the Flask API
app = Flask(__name__)
# Route to predict
@app.route('/predict', methods=['POST'])
def predict():
    # Get the image from post request
    img = base64_to_pil(request.json)
    # Save the image to ./uploads
    img.save("./uploads/image.png")
    # Make prediction
    preds = model_predict("./uploads/image.png", model)
    # Process your result for human
    pred_class = decode_predictions(preds, top=1)
    result = str(pred_class[0][0][1])
    # Serialize the result, you can add additional fields
    return jsonify(result)

def base64_to_pil(string):
    imgdata = base64.b64decode(string)
    return Image.open(io.BytesIO(imgdata))

def model_predict(img_path, model):
    img = image.load_img(img_path, target_size=(224, 224))
    # Preprocessing the image
    x = image.img_to_array(img)
    # x = np.true_divide(x, 255)
    x = np.expand_dims(x, axis=0)
    # Be careful how your trained model deals with the input
    # otherwise, it won't make correct prediction!
    x = preprocess_input(x, mode='caffe')
    preds = model.predict(x)
    return preds
if __name__ == '__main__':

    app.run(debug=True)