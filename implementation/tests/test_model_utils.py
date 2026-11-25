"""
Unit tests for model_utils.py
"""

import numpy as np
from PIL import Image
from model_utils import preprocess_image, predict_crop_disease, get_model_file_path

def test_preprocess_image():
    img = Image.new("RGB", (300, 300), color="green")
    processed = preprocess_image(img, target_size=(224, 224))
    
    assert isinstance(processed, np.ndarray)
    assert processed.shape == (1, 224, 224, 3)
    assert processed.max() <= 255.0
    assert processed.min() >= 0.0

def test_predict_crop_disease_handles_missing_model():
    img = Image.new("RGB", (100, 100), color="red")
    res = predict_crop_disease(img)
    
    assert "is_model_loaded" in res
    if not res["is_model_loaded"]:
        assert res["predicted_class"] is None
        assert res["confidence"] == 0.0
