"""Flask entry point for the CropGuard AI web experience."""

import io
import re
from typing import Any

from flask import Flask, jsonify, render_template, request
from PIL import Image, UnidentifiedImageError

from model_utils import predict_crop_disease
from recommendations import get_recommendations

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}


def _is_allowed_file(filename: str) -> bool:
    has_extension = bool(re.fullmatch(r".+\.([a-zA-Z0-9]+)", filename))
    return has_extension and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def _serialise_prediction(result: dict[str, Any]) -> dict[str, Any]:
    predicted_class = result.get("predicted_class")
    return {
        "predicted_class": predicted_class,
        "confidence": result.get("confidence", 0.0),
        "top_predictions": [
            {"class_name": name, "confidence": score}
            for name, score in result.get("top_predictions", [])
        ],
        "recommendations": get_recommendations(predicted_class) if predicted_class else None,
    }


@app.errorhandler(413)
def request_entity_too_large(_error: Any):
    return jsonify({"error": "The image is larger than the 5 MB upload limit."}), 413


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/predict")
def predict():
    uploaded_file = request.files.get("image")
    if uploaded_file is None or not uploaded_file.filename:
        return jsonify({"error": "Choose a leaf image before analyzing it."}), 400
    if not _is_allowed_file(uploaded_file.filename):
        return jsonify({"error": "Only JPG, JPEG, and PNG images are supported."}), 400

    try:
        image = Image.open(io.BytesIO(uploaded_file.read()))
        image.load()
    except (UnidentifiedImageError, OSError):
        return jsonify({"error": "The uploaded file is not a readable image."}), 400

    result = predict_crop_disease(image)
    if not result.get("is_model_loaded"):
        return jsonify({"error": "The trained model is unavailable. Check the model files and try again."}), 503
    if not result.get("predicted_class"):
        return jsonify({"error": "The model could not produce a prediction."}), 500
    return jsonify(_serialise_prediction(result))


if __name__ == "__main__":
    app.run(debug=False)
