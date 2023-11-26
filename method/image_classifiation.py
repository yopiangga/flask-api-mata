# Step 1: Import necessary libraries
from keras.datasets import cifar10
from keras.models import Sequential
from keras.layers import Dense, Flatten
from keras.utils import to_categorical
import tensorflow as tf

# Step 2: Load the dataset
(train_images, train_labels), (test_images, test_labels) = cifar10.load_data()

# Step 3: Preprocess the dataset
train_images = train_images / 255.0
test_images = test_images / 255.0
train_labels = to_categorical(train_labels)
test_labels = to_categorical(test_labels)

# Step 4: Define the model architecture
model = Sequential([
    Flatten(input_shape=(32, 32, 3)),
    Dense(64, activation='relu'),
    Dense(10, activation='softmax')
])

# Step 5: Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Step 6: Train the model with the dataset
model.fit(train_images, train_labels, epochs=10, batch_size=64)

# Step 7: Save the model in .h5 format
model.save('model.h5')