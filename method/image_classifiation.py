from keras.models import load_model
from keras.preprocessing.image import img_to_array, load_img
import numpy as np

# Load the pre-trained h5 model
model = load_model('model.h5')

def process_image(image_path):
    # Load the image file, targeting a size compatible with your model
    img = load_img(image_path, target_size=(150, 150))
    # Convert the image data to an array and expand dimensions
    img = np.expand_dims(img_to_array(img), axis=0)
    return img

def predict_image_class(image_path):
    # Preprocess the image
    processed_image = process_image(image_path)

    # Use the model to classify the image
    predictions = model.predict(processed_image)
    return predictions

# Now, you can use `predict_image_class()` to classify an image
image_path = "./test_image.jpg"
predictions = predict_image_class(image_path)
print(predictions)
