# 🌱 CropGuard AI — Intelligent Plant Disease Detection System

CropGuard AI is a computer vision and deep learning application designed to identify plant leaf diseases from images and provide actionable organic, chemical, and preventive treatment recommendations.

---

## 📁 Project Structure

```
CropGuard_AI/
├── app.py                   # Existing Streamlit web application
├── flask_app.py             # Flask web application and prediction API
├── model_utils.py           # TensorFlow model interface & image pre-processor
├── recommendations.py       # Disease recommendation database & treatment logic
├── requirements.txt         # Project dependencies
├── README.md                # Documentation
├── .gitignore               # Git ignore rules
├── model/                   # Location for trained TensorFlow model (.h5 or .keras)
├── templates/index.html     # Flask dashboard page
├── static/                  # Flask CSS and browser JavaScript
├── data/                    # Sample images and dataset placeholders
├── assets/                  # UI assets and stylesheets
├── notebooks/               # Google Colab notebook for GPU training
└── tests/                   # Unit test suite
```

---

## ⚡ Quick Start Guide

### 1. Installation
Clone or navigate to the project directory and install dependencies:

```bash
cd "C:\Users\EY Ramana\Desktop\CropGuard_AI"
pip install -r requirements.txt
```

### 2. Running the Flask Web Application
Launch the premium browser interface:

```bash
.venv_deploy\Scripts\python.exe flask_app.py
```

Open `http://127.0.0.1:5000` in a browser. The prediction endpoint accepts
`multipart/form-data` uploads under the `image` field at `POST /predict`.

The supplied `.keras` model was saved with Keras 3.13.2. The tested
compatibility baseline is TensorFlow 2.21.0 with Keras 3.12.4. Use the project
environment rather than a system Python installation with TensorFlow 2.12.

For a clean deployment environment on Windows:

```powershell
py -3.10 -m venv .venv_deploy
.venv_deploy\Scripts\python.exe -m pip install -r requirements-deploy.txt
.venv_deploy\Scripts\python.exe -m pip check
```

Activate it for an interactive session with:

```powershell
.venv_deploy\Scripts\Activate.ps1
```

The original Streamlit interface remains available:

```bash
.venv\Scripts\streamlit.exe run app.py
```

---

## 🤖 Training the TensorFlow Model

The model training pipeline is configured in `notebooks/CropGuard_Training.ipynb`.

1. Upload `notebooks/CropGuard_Training.ipynb` to [Google Colab](https://colab.research.google.com).
2. Connect to a GPU runtime (`Runtime > Change runtime type > T4 GPU`).
3. Run all cells to train a **MobileNetV2** transfer learning model.
4. Download the resulting `crop_guard_model.h5` or `crop_guard_model.keras`.
5. Move the model file to the local `model/` folder:
   `Desktop/CropGuard_AI/model/crop_guard_model.h5`

---

## 🧪 Running Unit Tests

Run the test suite using `pytest`:

```bash
pytest tests/
```

---

## 🛡️ License
Licensed under the [MIT License](LICENSE).
