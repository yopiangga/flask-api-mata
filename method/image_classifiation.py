from keras.models import load_model
from keras.preprocessing.image import img_to_array, load_img
import numpy as np

model = load_model('./dataset/model.h5')

def process_image(image):
    # Load the image file, targeting a size compatible with your model
    img = load_img(image, target_size=(224, 224))
    # Convert the image data to an array and expand dimensions
    img = np.expand_dims(img_to_array(img), axis=0)
    
    return img
