import tensorflow as tf
import numpy as np
from PIL import Image
import json

# Load trained model
model = tf.keras.models.load_model(
    "model/plant_disease_model.keras"
)

# Load class names
with open("class_names.json", "r") as file:
    class_names = json.load(file)


def predict_image(image_path):

    # Open image
    image = Image.open(image_path).convert("RGB")

    # Resize image
    image = image.resize((224, 224))

    # Convert image to NumPy array
    image_array = np.array(image, dtype=np.float32)

    # MobileNetV2 preprocessing
    image_array = tf.keras.applications.mobilenet_v2.preprocess_input(
        image_array
    )

    # Add batch dimension
    image_array = np.expand_dims(image_array, axis=0)

    # Make prediction
    predictions = model.predict(
        image_array,
        verbose=0
    )

    # Find highest probability
    predicted_index = np.argmax(predictions[0])

    predicted_class = class_names[predicted_index]

    confidence = float(
        predictions[0][predicted_index]
    ) * 100

    # Low-confidence result
    if confidence < 60:
        predicted_class = "Uncertain"

    return predicted_class, confidence