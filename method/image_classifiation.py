# Step 1: Import necessary libraries
import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.model_selection import train_test_split
import tensorflow as tf

# Step 2: Load the CSV file using pandas
df = pd.read_csv('data-d4-l1-v2 ')

# Step 3: Preprocess the dataset if necessary
# This step depends on your dataset. You might need to normalize numerical data, 
# encode categorical data, handle missing values, etc.

# Step 4: Split the dataset into features (X) and target (y)
X = df.drop('target_column', axis=1)
y = df['target_column']

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 5: Define the model architecture
model = Sequential([
    Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
    Dense(1, activation='sigmoid')
])

# Step 6: Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Step 7: Train the model with the dataset
model.fit(X_train, y_train, epochs=10, batch_size=32)

# Step 8: Save the model in .h5 format
model.save('model.h5')