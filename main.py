import os
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.preprocessing import image
from PIL import Image
import base64
import json
import re
from io import BytesIO
from flask import Flask

# Set the path to the dataset
dataset_path = "C:\\Users\\maxza\\Desktop\\flagweb\\CountryFlags"

# Define image parameters
img_height, img_width = 64, 64
batch_size = 32

# Create data generators for training and validation
train_datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2
)

train_generator = train_datagen.flow_from_directory(
    dataset_path,
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='categorical',
    subset='training'
)

validation_generator = train_datagen.flow_from_directory(
    dataset_path,
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='categorical',
    subset='validation'
)

# Build the CNN model
model = models.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(img_height, img_width, 3)),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(128, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dense(len(train_generator.class_indices), activation='softmax')
])

# Compile the model
model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# Train the model
history = model.fit(
    train_generator,
    epochs= 75,
    validation_data=validation_generator
)
image_path = r"C:\Users\maxza\Desktop\flagweb\Flags\download.png"  # Replace with the path to your image
# @app.route('/hook', methods=['POST'])
# def save_canvas():
#     image_data = re.sub('^data:image/.+;base64,', '', request.form['imageBase64'])
#     im = Image.open(BytesIO(base64.b64decode(image_data)))
#     # im.save('canvas.png')
#     return json.dumps({'result': 'success'}), 200, {'ContentType': 'application/json'}
# Load and preprocess the input image
img = image.load_img(image_path, target_size=(64, 64))
img_array = image.img_to_array(img)
img_array = np.expand_dims(img_array, axis=0)
img_array /= 255.  # Normalize the image
predictions = model.predict(img_array)
predicted_class_index = np.argmax(predictions[0])
class_indices = train_generator.class_indices
inverse_class_indices = {v: k for k, v in class_indices.items()}
predicted_class = inverse_class_indices[predicted_class_index]

print("Predicted flag:", predicted_class)
# Save the model
model.save("flag_recognition_model.h5")
