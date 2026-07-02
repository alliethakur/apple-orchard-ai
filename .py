import streamlit as st
import requests
from PIL import Image
import io

# Page config
st.set_page_config(
    page_title="Apple Orchard AI — Himachal Pradesh",
    page_icon="🍎",
    layout="centered"
)

# Custom CSS - Himalayan theme, no emojis, clean
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Inter:wght@300;400;500;600&display=swap');
    
    * { font-family: 'Inter', sans-serif; }
    
    .stApp {
        background: #0d1f1a;
    }

    .header {
        padding: 3rem 0 2rem 0;
        border-bottom: 1px solid rgba(255,255,255,0.08);
        margin-bottom: 2.5rem;
    }

    .header-label {
        font-size: 0.7rem;
        font-weight: 600;
        letter-spacing: 3px;
        text-transform: uppercase;
        color: #5a9e7a;
        margin-bottom: 0.5rem;
    }

    .header-title {
        font-family: 'Playfair Display', serif;
        font-size: 2.8rem;
        font-weight: 700;
        color: #f0ebe0;
        line-height: 1.1;
        margin: 0;
    }

    .header-sub {
        font-size: 0.9rem;
        color: rgba(255,255,255,0.35);
        margin-top: 0.6rem;
        font-weight: 300;
    }

    .upload-area {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 12px;
        padding: 2rem;
        margin-bottom: 2rem;
    }

    .result-card {
        background: rgba(255,255,255,0.04);
        border-radius: 12px;
        padding: 2rem;
        margin-top: 1.5rem;
        border: 1px solid rgba(255,255,255,0.08);
    }

    .result-status {
        font-size: 0.7rem;
        font-weight: 600;
        letter-spacing: 3px;
        text-transform: uppercase;
        margin-bottom: 0.4rem;
    }

    .result-status.disease {
        color: #e07070;
    }

    .result-status.healthy {
        color: #5a9e7a;
    }

    .result-disease {
        font-family: 'Playfair Display', serif;
        font-size: 2rem;
        font-weight: 700;
        color: #f0ebe0;
        margin: 0;
    }

    .result-confidence {
        font-size: 0.8rem;
        color: rgba(255,255,255,0.3);
        margin-top: 0.3rem;
    }

    .result-description {
        font-size: 0.9rem;
        color: rgba(255,255,255,0.55);
        margin-top: 1rem;
        line-height: 1.6;
        padding-bottom: 1rem;
        border-bottom: 1px solid rgba(255,255,255,0.06);
    }

    .section-label {
        font-size: 0.65rem;
        font-weight: 600;
        letter-spacing: 2.5px;
        text-transform: uppercase;
        color: #5a9e7a;
        margin-top: 1.2rem;
        margin-bottom: 0.6rem;
    }

    .item {
        font-size: 0.88rem;
        color: rgba(255,255,255,0.65);
        padding: 0.4rem 0;
        border-bottom: 1px solid rgba(255,255,255,0.04);
        line-height: 1.5;
    }

    .season-tag {
        display: inline-block;
        margin-top: 1.2rem;
        background: rgba(90,158,122,0.12);
        border: 1px solid rgba(90,158,122,0.25);
        color: #5a9e7a;
        font-size: 0.75rem;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        letter-spacing: 0.5px;
    }

    .divider {
        border: none;
        border-top: 1px solid rgba(255,255,255,0.06);
        margin: 2rem 0;
    }

    .footer {
        text-align: center;
        color: rgba(255,255,255,0.2);
        font-size: 0.72rem;
        letter-spacing: 1px;
        margin-top: 3rem;
        padding-top: 1.5rem;
        border-top: 1px solid rgba(255,255,255,0.06);
    }

    /* Hide streamlit defaults */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* File uploader styling */
    .stFileUploader label {
        color: rgba(255,255,255,0.5) !important;
        font-size: 0.85rem !important;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header">
    <div class="header-label">Himachal Pradesh — Disease Detection</div>
    <div class="header-title">Apple Orchard<br>Intelligence</div>
    <div class="header-sub">Upload a leaf photograph for instant disease diagnosis and treatment guidance</div>
</div>
""", unsafe_allow_html=True)

# Upload
st.markdown('<div class="upload-area">', unsafe_allow_html=True)
uploaded_file = st.file_uploader(
    "Select a leaf photograph — JPG or PNG",
    type=["jpg", "jpeg", "png"]
)
st.markdown('</div>', unsafe_allow_html=True)

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded photograph", use_column_width=True)

    with st.spinner("Analyzing..."):
        img_bytes = io.BytesIO()
        image.save(img_bytes, format="JPEG")
        img_bytes.seek(0)

        try:
            response = requests.post(
                "http://127.0.0.1:8000/predict",
                files={"file": ("leaf.jpg", img_bytes, "image/jpeg")}
            )
            result = response.json()

            is_healthy = "healthy" in result["disease"].lower()
            status_class = "healthy" if is_healthy else "disease"
            status_text = "No Disease Detected" if is_healthy else "Disease Detected"

        treatment_html = "".join([f'<div class="item">{t}</div>' for t in result["treatment"]])
        prevention_html = "".join([f'<div class="item">{p}</div>' for p in result["prevention"]])

        st.markdown(f"""
            <div class="result-card">
            <div class="result-status {status_class}">{status_text}</div>
            <div class="result-disease">{result["local_name"]}</div>
            <div class="result-confidence">Model confidence — {result["confidence"]}</div>
            <div class="result-description">{result["description"]}</div>
            <div class="section-label">Recommended Treatment</div>
            {treatment_html}
            <div class="section-label">Prevention</div>
            {prevention_html}
            <div class="season-tag">{result["season"]}</div>
        </div>
        """, unsafe_allow_html=True)

        except:
            st.error("Could not connect to prediction server. Make sure FastAPI is running.")

st.markdown("""
<div class="footer">
    Apple Orchard Intelligence — Built for Himalayan Farmers
</div>
""", unsafe_allow_html=True)