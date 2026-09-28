from flask import Flask, render_template, request, send_from_directory
import os

from model import predict_image
from database import create_database, save_scan, get_scans

app = Flask(__name__)
create_database()

UPLOAD_FOLDER = "uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# Disease information
DISEASE_INFO = {

    "Potato___Early_blight": {
        "name": "Potato Early Blight",
        "description": "A fungal disease that commonly affects potato leaves and can reduce plant growth and yield.",
        "symptoms": "Dark spots or brown lesions may appear on older leaves.",
        "prevention": "Remove affected leaves, maintain good airflow, avoid overhead watering, and keep the growing area clean."
    },

    "Potato___Late_blight": {
        "name": "Potato Late Blight",
        "description": "A serious disease that can spread quickly under cool and humid conditions.",
        "symptoms": "Dark irregular lesions can develop on leaves and stems.",
        "prevention": "Improve air circulation, avoid prolonged leaf wetness, remove infected plant material, and use appropriate disease management practices."
    },

    "Potato___healthy": {
        "name": "Healthy Potato Leaf",
        "description": "The AI did not detect the potato diseases included in this model.",
        "symptoms": "No major disease pattern from the trained classes was detected.",
        "prevention": "Continue regular watering, proper nutrition, good sunlight, and monitor the plant regularly."
    },

    "Tomato___Early_blight": {
        "name": "Tomato Early Blight",
        "description": "A fungal disease that commonly affects tomato leaves and may reduce plant health and yield.",
        "symptoms": "Brown spots with darker rings can appear on older leaves.",
        "prevention": "Remove affected leaves, improve airflow, avoid wetting leaves unnecessarily, and keep the growing area clean."
    },

    "Tomato___healthy": {
        "name": "Healthy Tomato Leaf",
        "description": "The AI did not detect the tomato diseases included in this model.",
        "symptoms": "No major disease pattern from the trained classes was detected.",
        "prevention": "Continue proper watering, sunlight, nutrition, and regular plant monitoring."
    },

        "Uncertain": {
        "name": "Unable to Identify",
        "description": "The AI could not confidently identify this image using the trained plant disease classes.",
        "symptoms": "The image may be unclear, unrelated to the trained classes, or have insufficient visual information.",
        "prevention": "Please upload a clear image of a potato or tomato leaf and try again."
    }
}


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/history")
def history():
    scans = get_scans()
    return render_template("history.html", scans=scans)


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(
        app.config["UPLOAD_FOLDER"],
        filename
    )


@app.route("/predict", methods=["POST"])
def predict():

    image = request.files.get("image")

    if not image:
        return "No image uploaded"

    image_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        image.filename
    )

    image.save(image_path)

    prediction, confidence = predict_image(image_path)

    information = DISEASE_INFO.get(
        prediction,
        {
            "name": prediction,
            "description": "Information is not available.",
            "symptoms": "Information is not available.",
            "prevention": "Please consult a plant health professional."
        }
    )

    # Save scan to database
    save_scan(
        prediction,
        information["name"],
        confidence
    )

    return render_template(
        "result.html",
        prediction=information["name"],
        confidence=f"{confidence:.2f}",
        image_name=image.filename,
        description=information["description"],
        symptoms=information["symptoms"],
        prevention=information["prevention"]
    )
if __name__ == "__main__":
    app.run(debug=True)