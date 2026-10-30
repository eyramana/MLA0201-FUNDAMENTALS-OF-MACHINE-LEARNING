"""
CropGuard AI - Web Application
Interactive Streamlit UI for Plant Disease Detection, Advisory, & Orchard Diagnostics.
"""

import os
import streamlit as st
from PIL import Image
from model_utils import (
    CLASS_NAMES,
    get_model_file_path,
    load_crop_guard_model,
    predict_crop_disease,
)
from recommendations import get_recommendations

# Streamlit Page Config
st.set_page_config(
    page_title="CropGuard AI — Plant Disease Diagnostic Platform",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.3rem;
        color: #1b4332;
        font-weight: 700;
        margin-bottom: 0px;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #40916c;
        margin-bottom: 25px;
    }
    .card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        border-left: 5px solid #2d6a4f;
        margin-bottom: 15px;
    }
    .metric-container {
        background-color: #d8f3dc;
        padding: 15px;
        border-radius: 8px;
        text-align: center;
    }
    .badge-healthy {
        background-color: #2b9348;
        color: white;
        padding: 4px 12px;
        border-radius: 12px;
        font-weight: bold;
    }
    .badge-disease {
        background-color: #d90429;
        color: white;
        padding: 4px 12px;
        border-radius: 12px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">🌱 CropGuard AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">AI-Powered Agricultural Diagnostics & Crop Protection Advisory</div>', unsafe_allow_html=True)

# Sidebar
st.sidebar.image("https://img.icons8.com/color/96/plant-under-sun.png", width=70)
st.sidebar.title("CropGuard Navigation")
nav_choice = st.sidebar.radio("Go to:", ["🔬 Leaf Diagnostics", "📚 Disease Knowledgebase", "⚙️ Model Status & Guide"])

model_path = get_model_file_path()
if model_path:
    st.sidebar.success(f"✅ Model Ready ({os.path.basename(model_path)})")
else:
    st.sidebar.warning("⚠️ Model file missing in model/")
    st.sidebar.info("Place the trained `crop_disease_model.keras` inside `model/`")

model, model_message = load_crop_guard_model()
if model is None:
    st.sidebar.error(model_message)

# Navigation: Leaf Diagnostics
if nav_choice == "🔬 Leaf Diagnostics":
    st.subheader("Upload or Capture Leaf Image for Analysis")
    
    col_input, col_display = st.columns([1, 1])

    with col_input:
        input_mode = st.radio("Select Input Method:", ["Upload Image File", "Use Camera"], horizontal=True)
        uploaded_file = None
        
        if input_mode == "Upload Image File":
            uploaded_file = st.file_uploader("Choose a leaf image...", type=["jpg", "jpeg", "png"])
        else:
            uploaded_file = st.camera_input("Take a photo of the affected plant leaf")

    if uploaded_file is not None:
        try:
            image = Image.open(uploaded_file)
            image.load()
        except (OSError, ValueError) as error:
            st.error(f"Unable to read the uploaded image: {error}")
            st.stop()
        
        with col_display:
            st.image(image, caption="Uploaded Crop Leaf", use_container_width=True)

        st.markdown("---")
        st.subheader("Diagnostic Results")
        
        with st.spinner("Analyzing leaf patterns using Deep Neural Network..."):
            res = predict_crop_disease(image)

        if not res["is_model_loaded"]:
            st.error(f"Unable to analyze the image: {res['message']}")
            st.info("Verify that the model and class mapping files exist and are compatible with the installed TensorFlow/Keras version.")
        else:
            predicted_class = res["predicted_class"]
            confidence = res["confidence"]
            if predicted_class is None:
                st.error(res["message"])
                st.stop()
            rec = get_recommendations(predicted_class)
            
            c1, c2, c3 = st.columns(3)
            with c1:
                st.metric(label="Diagnosed Condition", value=rec["disease_name"])
            with c2:
                st.metric(label="Target Crop", value=rec["crop"])
            with c3:
                st.metric(label="Model Confidence", value=f"{confidence * 100:.1f}%")

            st.markdown(f"**Description:** {rec['description']}")
            st.markdown("### Top Predictions")
            for class_name, score in res["top_predictions"]:
                st.write(f"- {class_name}: {score * 100:.1f}%")
            
            if "healthy" in predicted_class.lower():
                st.success("🎉 The leaf appears healthy! Continue standard crop management.")
            else:
                st.warning("⚠️ Pathogen detected. Follow the treatment plan below.")

            st.markdown("### 📋 Recommended Action Plan")
            tab1, tab2, tab3 = st.tabs(["🍃 Organic Solutions", "💊 Chemical Treatments", "🧱 Cultural & Irrigation Controls"])
            
            with tab1:
                for idx, org in enumerate(rec["organic_control"], 1):
                    st.markdown(f"**{idx}.** {org}")
            with tab2:
                for idx, chem in enumerate(rec["chemical_control"], 1):
                    st.markdown(f"**{idx}.** {chem}")
            with tab3:
                st.markdown("#### Preventive Practices")
                for idx, prev in enumerate(rec["preventive_measures"], 1):
                    st.markdown(f"**{idx}.** {prev}")
                st.markdown("#### Soil & Irrigation Guidance")
                st.info(rec["soil_irrigation_advice"])

# Navigation: Knowledgebase
elif nav_choice == "📚 Disease Knowledgebase":
    st.subheader("Crop Health & Pathogen Directory")
    st.write("Browse details and treatments for supported crop diseases.")
    
    selected_class = st.selectbox("Select Plant Class:", CLASS_NAMES)
    rec = get_recommendations(selected_class)
    
    st.markdown(f"### {rec['disease_name']} (*{rec['crop']}*)")
    st.write(rec["description"])
    
    st.markdown("#### Organic Control")
    for item in rec["organic_control"]:
        st.write(f"- {item}")
        
    st.markdown("#### Chemical Control")
    for item in rec["chemical_control"]:
        st.write(f"- {item}")
        
    st.markdown("#### Prevention & Care")
    for item in rec["preventive_measures"]:
        st.write(f"- {item}")

# Navigation: Model Status & Guide
else:
    st.subheader("Model Status & Integration Guide")
    
    st.markdown("""
    ### 🚀 Training & Integrating the Real Model
    
    1. **Google Colab Training Notebook:**
       - Open `notebooks/CropGuard_Training.ipynb` in [Google Colab](https://colab.research.google.com).
       - Enable GPU Accelerator (`Runtime > Change runtime type > T4 GPU`).
       - Run all cells to train MobileNetV2 on the PlantVillage dataset.
    
    2. **Model Download & Placement:**
       - Export the trained model as `crop_guard_model.h5` or `crop_guard_model.keras`.
       - Copy the model file into the project directory:
         `Desktop/CropGuard_AI/model/crop_guard_model.h5`
    
    3. **Supported Disease Classes:**
    """)
    for name in CLASS_NAMES:
        st.markdown(f"- `{name}`")
