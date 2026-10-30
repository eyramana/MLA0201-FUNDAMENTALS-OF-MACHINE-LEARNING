import json
import os
import zipfile
from typing import Any

import numpy as np
import tensorflow as tf
from PIL import Image


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "model")
MODEL_PATH = os.path.join(MODEL_DIR, "crop_disease_model.keras")
CLASS_INDICES_PATH = os.path.join(MODEL_DIR, "class_indices.json")

_loaded_model: Any = None
CLASS_NAMES: list[str] = []


def get_model_file_path() -> str | None:
    """Return the configured model path when the trained model is available."""
    if os.path.isfile(MODEL_PATH):
        return MODEL_PATH
    return None


def load_crop_guard_model() -> tuple[Any, str]:
    """Load the trained model and its class mapping once."""
    global _loaded_model

    if _loaded_model is not None:
        return _loaded_model, "Model loaded successfully."

    if not os.path.isfile(MODEL_PATH):
        return None, f"Model not found: {MODEL_PATH}"

    if not os.path.isfile(CLASS_INDICES_PATH):
        return None, f"Class mapping not found: {CLASS_INDICES_PATH}"

    try:
        with open(CLASS_INDICES_PATH, "r", encoding="utf-8") as file:
            class_indices = json.load(file)

        if not isinstance(class_indices, dict) or not class_indices:
            return None, "Class mapping is empty or invalid."

        indexed_classes = []
        for class_name, index in class_indices.items():
            if not isinstance(class_name, str) or not isinstance(index, int):
                return None, "Class mapping must contain string names and integer indices."
            indexed_classes.append((index, class_name))

        indexed_classes.sort()
        expected_indices = list(range(len(indexed_classes)))
        actual_indices = [index for index, _ in indexed_classes]
        if actual_indices != expected_indices:
            return None, "Class mapping indices must be contiguous and start at zero."

        class_names = [class_name for _, class_name in indexed_classes]
        if len(class_names) != 38:
            return None, f"Expected 38 classes in class mapping, found {len(class_names)}."

        CLASS_NAMES.clear()
        CLASS_NAMES.extend(class_names)

        try:
            model = tf.keras.models.load_model(MODEL_PATH)
        except Exception as standard_load_error:
            try:
                model = _load_keras_model_compatibility_fallback()
            except Exception as fallback_error:
                raise RuntimeError(
                    "Standard Keras loading failed: "
                    f"{standard_load_error}. Compatibility loading also failed: "
                    f"{fallback_error}"
                ) from fallback_error

        output_shape = model.output_shape
        output_classes = output_shape[-1] if output_shape else None
        if output_classes != len(class_names):
            return (
                None,
                "Model and class mapping do not match: "
                f"model has {output_classes} outputs, mapping has {len(class_names)} classes.",
            )

        _loaded_model = model
        return _loaded_model, "Trained MobileNetV2 model loaded successfully."
    except (OSError, json.JSONDecodeError) as error:
        return None, f"Error loading class mapping: {error}"
    except Exception as error:
        return None, f"Error loading model: {error}"


def _remove_unsupported_serialization_fields(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: _remove_unsupported_serialization_fields(item)
            for key, item in value.items()
            if key != "quantization_config"
        }
    if isinstance(value, list):
        return [_remove_unsupported_serialization_fields(item) for item in value]
    return value


def _load_keras_model_compatibility_fallback() -> Any:
    """Load models saved by newer Keras versions without changing the model file."""
    with zipfile.ZipFile(MODEL_PATH) as model_archive:
        config = json.loads(model_archive.read("config.json"))

    compatible_config = _remove_unsupported_serialization_fields(config)
    model = tf.keras.models.model_from_json(json.dumps(compatible_config))
    model.load_weights(MODEL_PATH)
    return model


def preprocess_image(
    pil_image: Image.Image, target_size: tuple[int, int] = (224, 224)
) -> np.ndarray:
    """Convert an uploaded image to a raw float32 model input batch."""
    if not isinstance(pil_image, Image.Image):
        raise TypeError("pil_image must be a PIL.Image.Image instance.")

    image = pil_image.convert("RGB").resize(target_size)
    image_array = np.asarray(image, dtype=np.float32)
    return np.expand_dims(image_array, axis=0)


def predict_crop_disease(pil_image: Image.Image) -> dict[str, Any]:
    """Return the predicted class, confidence, and three highest predictions."""
    model, message = load_crop_guard_model()

    if model is None:
        return {
            "is_model_loaded": False,
            "predicted_class": None,
            "confidence": 0.0,
            "top_predictions": [],
            "message": message,
        }

    try:
        predictions = np.asarray(model.predict(preprocess_image(pil_image), verbose=0))
        if predictions.ndim != 2 or predictions.shape[0] == 0:
            raise ValueError(f"Unexpected prediction shape: {predictions.shape}")

        scores = predictions[0]
        if len(scores) != len(CLASS_NAMES):
            raise ValueError(
                f"Prediction output has {len(scores)} classes; "
                f"class mapping has {len(CLASS_NAMES)}."
            )
        if not np.all(np.isfinite(scores)):
            raise ValueError("Prediction output contains non-finite scores.")

        top_indices = np.argsort(scores)[::-1][:3]
        predicted_index = int(top_indices[0])
        return {
            "is_model_loaded": True,
            "predicted_class": CLASS_NAMES[predicted_index],
            "confidence": float(scores[predicted_index]),
            "top_predictions": [
                (CLASS_NAMES[int(index)], float(scores[index])) for index in top_indices
            ],
            "message": "Prediction successful",
        }
    except Exception as error:
        return {
            "is_model_loaded": True,
            "predicted_class": None,
            "confidence": 0.0,
            "top_predictions": [],
            "message": f"Prediction error: {error}",
        }
