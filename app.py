import streamlit as st
from tensorflow.keras.models import load_model
import numpy as np
import cv2
from PIL import Image
import base64
import os
import requests
import io

# ---- API Key Gemini ----
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    st.error("🚨 Kunci API Gemini tidak ditemukan! Set environment variable `GEMINI_API_KEY`.")
    st.stop()

# ---- Fungsi Analisis AI Gemini ----
def analyze_image_with_gemini(image_data):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {'Content-Type': 'application/json'}

    buffered = io.BytesIO()
    image_data.save(buffered, format="JPEG")
    image_base64 = base64.b64encode(buffered.getvalue()).decode()

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": "Analisis gambar X-ray ini dan berikan penjelasan medis secara akurat."},
                    {"inline_data": {"mime_type": "image/jpeg", "data": image_base64}}
                ]
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        return response.json().get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "Analisis tidak tersedia.")
    except requests.exceptions.RequestException as e:
        return f"⚠️ Terjadi kesalahan saat mengambil analisis: {e}"

# ---- Fungsi Encode Gambar ke Base64 ----
def get_base64_of_bin_file(bin_file_path):
    try:
        with open(bin_file_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        st.error(f"🚨 Gambar background tidak ditemukan: {bin_file_path}")
        return None
    except Exception as e:
        st.error(f"⚠️ Error saat encode gambar {bin_file_path}: {e}")
        return None

# ---- Set Background & Custom CSS ----
main_bg = "mainimg1.jpg"
sidebar_bg = "sb2.jpg"

main_bg_base64 = get_base64_of_bin_file(main_bg) if os.path.exists(main_bg) else None
sidebar_bg_base64 = get_base64_of_bin_file(sidebar_bg) if os.path.exists(sidebar_bg) else None

st.markdown(f"""
<style>
/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Poppins:wght@400;700&display=swap');

/* General Styling */
[data-testid="stAppViewContainer"] {{
    background: {(f'url("data:image/jpeg;base64,{main_bg_base64}")' if main_bg_base64 else 'linear-gradient(45deg, #1a1a1a, #2c3e50, #1a1a1a)')};
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    background-blend-mode: overlay;
    background-color: rgba(20, 20, 20, 0.9);
    color: #ffffff;
    min-height: 100vh;
    animation: gradientMove 10s ease infinite;
}}
@keyframes gradientMove {{
    0% {{ background-position: 0% 50%; }}
    50% {{ background-position: 100% 50%; }}
    100% {{ background-position: 0% 50%; }}
}}

/* Sidebar Styling */
[data-testid="stSidebar"] {{
    background: {(f'url("data:image/jpeg;base64,{sidebar_bg_base64}")' if sidebar_bg_base64 else 'linear-gradient(45deg, #2c3e50, #1a1a1a, #2c3e50)')};
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    background-blend-mode: overlay;
    background-color: rgba(20, 20, 20, 0.75);
    color: #ffffff;
    border-right: 3px solid #00ffcc;
    box-shadow: 0 0 20px rgba(0, 255, 204, 0.5);
    animation: neonBorder 2s infinite alternate;
}}
@keyframes neonBorder {{
    0% {{ border-right-color: #00ffcc; box-shadow: 0 0 10px rgba(0, 255, 204, 0.5); }}
    100% {{ border-right-color: #00ccff; box-shadow: 0 0 20px rgba(0, 204, 255, 0.8); }}
}}

/* Title Styling */
.title {{
    font-family: 'Orbitron', sans-serif;
    font-size: 2.8em;
    text-align: center;
    color: #00ffcc;
    text-shadow: 2px 2px 10px rgba(0, 255, 204, 0.8), 0 0 20px rgba(0, 255, 204, 0.5);
    animation: glow 2s ease-in-out infinite alternate, fadeIn 1.5s ease-in-out;
}}
@keyframes glow {{
    from {{ text-shadow: 2px 2px 10px rgba(0, 255, 204, 0.8), 0 0 20px rgba(0, 255, 204, 0.5); }}
    to {{ text-shadow: 2px 2px 20px rgba(0, 255, 204, 1), 0 0 40px rgba(0, 255, 204, 0.8); }}
}}
@keyframes fadeIn {{
    0% {{ opacity: 0; transform: translateY(20px); }}
    100% {{ opacity: 1; transform: translateY(0); }}
}}

/* Subtitle Styling */
.subtitle {{
    font-family: 'Poppins', sans-serif;
    font-size: 1.2em;
    text-align: center;
    color: #ffffff;
    font-weight: bold;
    text-shadow: 1px 1px 5px rgba(0, 0, 0, 0.5);
    animation: fadeIn 2s ease-in-out;
}}

/* Button Styling */
.stButton>button {{
    background: linear-gradient(90deg, #ff416c, #ff4b2b);
    color: white;
    border-radius: 10px;
    font-size: 18px;
    padding: 10px 20px;
    box-shadow: 0 0 15px rgba(255, 65, 108, 0.5), 0 0 30px rgba(255, 75, 43, 0.3);
    transition: all 0.3s ease;
    animation: fadeIn 2.5s ease-in-out;
}}
.stButton>button:hover {{
    transform: scale(1.05);
    background: linear-gradient(90deg, #ff4b2b, #ff416c);
    box-shadow: 0 0 25px rgba(255, 65, 108, 0.8), 0 0 50px rgba(255, 75, 43, 0.5);
}}

/* Disclaimer Styling */
.disclaimer {{
    text-align: center;
    background: rgba(255, 165, 0, 0.3);
    padding: 15px;
    border-radius: 10px;
    border: 2px solid #ffcc00;
    color: #ffffff;
    font-weight: bold;
    text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.5);
    animation: fadeIn 2s ease-in-out;
}}

/* Sidebar Links Styling */
.sidebar-link {{
    display: inline-block;
    background: linear-gradient(90deg, #00ffcc, #00ccff);
    color: #1a1a1a;
    padding: 8px 15px;
    border-radius: 20px;
    text-decoration: none;
    font-family: 'Poppins', sans-serif;
    font-weight: bold;
    margin: 5px 0;
    transition: all 0.3s ease;
    animation: fadeIn 2.5s ease-in-out;
}}
.sidebar-link:hover {{
    transform: scale(1.05);
    background: linear-gradient(90deg, #00ccff, #00ffcc);
    box-shadow: 0 0 15px rgba(0, 255, 204, 0.5);
}}

/* Sidebar Text Styling */
.sidebar-text {{
    font-family: 'Poppins', sans-serif;
    color: #00ffcc;
    text-shadow: 0 0 10px rgba(0, 255, 204, 0.5);
    animation: fadeIn 2s ease-in-out;
}}

/* Result Card Styling */
.result-card {{
    background: rgba(20, 20, 20, 0.9);
    backdrop-filter: blur(10px);
    border-radius: 15px;
    padding: 20px;
    margin: 20px 0;
    border: 2px solid #00ffcc;
    box-shadow: 0 0 20px rgba(0, 255, 204, 0.5);
    color: #ffffff;
    text-align: center;
    animation: fadeIn 1s ease-in-out;
}}
.result-card h3 {{
    font-family: 'Orbitron', sans-serif;
    color: #00ffcc;
    text-shadow: 0 0 10px rgba(0, 255, 204, 0.5);
    margin-bottom: 10px;
}}
.result-card p {{
    font-family: 'Poppins', sans-serif;
    font-size: 1.1em;
    color: #ffffff;
    margin: 5px 0;
}}
.normal {{
    color: #00ff00;
    font-weight: bold;
    text-shadow: 0 0 10px rgba(0, 255, 0, 0.5);
}}
.pneumonia {{
    color: #ff4444;
    font-weight: bold;
    text-shadow: 0 0 10px rgba(255, 68, 68, 0.5);
}}

/* Expander Styling */
.stExpander {{
    background: rgba(20, 20, 20, 0.9);
    border-radius: 10px;
    border: 1px solid #00ffcc;
    color: #ffffff;
    animation: fadeIn 1.5s ease-in-out;
}}
.stExpander summary {{
    font-family: 'Poppins', sans-serif;
    font-size: 1.1rem;
    color: #00ffcc;
    text-shadow: 0 0 5px rgba(0, 255, 204, 0.5);
}}
.stExpander p {{
    font-family: 'Poppins', sans-serif;
    color: #ffffff;
}}
</style>
""", unsafe_allow_html=True)

# ---- Title ----
st.markdown('<p class="title">🔍 AI Pneumonia Detector</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">🚀 Deteksi Pneumonia dengan Deep Learning & Google Gemini</p>', unsafe_allow_html=True)

# ---- Load Model ----
model_path = "vgg19_model.h5"
if os.path.exists(model_path):
    model = load_model(model_path)
    st.sidebar.success("✅ Model berhasil dimuat!")
else:
    st.sidebar.error("❌ Model tidak ditemukan!")
    st.stop()

# ---- Sidebar Disclaimer ----
st.sidebar.markdown("""
<div class="disclaimer">
    ⚠️ <b>Disclaimer:</b><br>
    Hasil dari aplikasi ini bukan diagnosa medis.<br>
    Silakan konsultasi dengan dokter untuk kepastian lebih lanjut.
</div>
""", unsafe_allow_html=True)

# ---- Sidebar Developer Info ----
st.sidebar.markdown("""
---
<p class="sidebar-text">👨‍💻 <b>Developed by Farrel0xx</b></p>
<div style="text-align: center;">
    <a href="https://github.com/Farrel0xx" target="_blank" class="sidebar-link">
        <img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" width="20" style="vertical-align: middle; margin-right: 5px;"> GitHub
    </a><br>
    <a href="https://youtube.com/@Farrel0xx" target="_blank" class="sidebar-link">
        <img src="https://upload.wikimedia.org/wikipedia/commons/b/b8/YouTube_Logo_2017.svg" width="30" style="vertical-align: middle; margin-right: 5px;"> YouTube
    </a>
</div>
""", unsafe_allow_html=True)

# ---- Upload Image ----
uploaded_file = st.sidebar.file_uploader("📤 Pilih gambar X-ray", type=["jpg", "jpeg", "png"])

# ---- Prediksi ----
if uploaded_file is not None:
    img = Image.open(uploaded_file)
    st.image(img, caption="🩻 X-ray yang diupload", use_container_width=True)

    # Notifikasi sukses upload
    st.success("✅ Gambar berhasil diunggah!")

    if st.button("🔎 Prediksi"):
        with st.spinner("⏳ Menganalisis..."):
            img = img.convert("RGB")
            img_resized = cv2.resize(np.array(img), (224, 224))
            img_resized = img_resized / 255.0
            img_preprocessed = np.expand_dims(img_resized, axis=0)

            prediction = model.predict(img_preprocessed)
            prediction_class = np.argmax(prediction, axis=1)[0]
            confidence = prediction[0][prediction_class] * 100
            labels = ["✅ Normal", "⚠️ Pneumonia"]
            result = labels[prediction_class]
            result_class = "normal" if prediction_class == 0 else "pneumonia"

            # ---- Hasil Prediksi dalam Card ----
            st.markdown(f"""
            <div class="result-card">
                <h3>📊 Hasil Prediksi</h3>
                <p>Klasifikasi: <span class="{result_class}">{result}</span></p>
                <p>Kepercayaan: {confidence:.2f}%</p>
            </div>
            """, unsafe_allow_html=True)

            # ---- Panggil Gemini untuk Deskripsi ----
            st.markdown('<div class="result-card"><h3>📝 Penjelasan AI</h3>', unsafe_allow_html=True)
            uploaded_file.seek(0)
            desc = analyze_image_with_gemini(img)
            st.markdown(f"<p>{desc}</p>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # ---- Tampilkan Probabilitas ----
            with st.expander("📌 Lihat Probabilitas Detail"):
                st.write(f"✅ Normal: {prediction[0][0]:.4f}")
                st.write(f"⚠️ Pneumonia: {prediction[0][1]:.4f}")
