import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
import sys
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from src.predict import load_model, predict

# Page config
st.set_page_config(
    page_title="Apple Orchard AI — Himachal Pradesh",
    page_icon="🍎",
    layout="centered"
)

# Custom CSS - Himalayan theme, no emojis, clean
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,wght@0,600;0,700;1,600;1,700&family=Inter:wght@400;500;600&display=swap');

    * { font-family: 'Inter', sans-serif; }

    .stApp {
        background: #FAF3EB;
    }

    .header {
        padding: 3rem 0 2rem 0;
        border-bottom: 1px solid #E5D5C0;
        margin-bottom: 2.5rem;
    }

    .header-label {
        font-size: 0.7rem;
        font-weight: 600;
        letter-spacing: 3px;
        text-transform: uppercase;
        color: #BB5B36;
        margin-bottom: 0.5rem;
    }

    .header-title {
        font-family: 'Fraunces', serif;
        font-size: 2.8rem;
        font-weight: 700;
        color: #2A2118;
        line-height: 1.1;
        margin: 0;
    }

    .header-sub {
        font-size: 0.9rem;
        color: #7A6C5D;
        margin-top: 0.6rem;
        font-weight: 400;
    }

    .result-card {
        background: #FFFFFF;
        border-radius: 12px;
        padding: 2rem;
        margin-top: 1.5rem;
        border: 1px solid #E5D5C0;
    }

    .result-status {
        font-size: 0.7rem;
        font-weight: 600;
        letter-spacing: 3px;
        text-transform: uppercase;
        margin-bottom: 0.4rem;
    }

    .result-status.disease {
        color: #BB5B36;
    }

    .result-status.healthy {
        color: #6B7A4F;
    }

    .result-disease {
        font-family: 'Fraunces', serif;
        font-size: 2rem;
        font-weight: 700;
        color: #2A2118;
        margin: 0;
    }

    .result-confidence {
        font-size: 0.8rem;
        color: #7A6C5D;
        margin-top: 0.3rem;
    }

    .result-description {
        font-size: 0.9rem;
        color: #7A6C5D;
        margin-top: 1rem;
        line-height: 1.6;
        padding-bottom: 1rem;
        border-bottom: 1px solid #E5D5C0;
    }

    .warning-card {
        background: #FFFFFF;
        border-radius: 12px;
        padding: 2rem;
        margin-top: 1.5rem;
        border: 1px solid rgba(184,134,46,0.35);
    }

    .warning-status {
        font-size: 0.7rem;
        font-weight: 600;
        letter-spacing: 3px;
        text-transform: uppercase;
        color: #B8862E;
        margin-bottom: 0.4rem;
    }

    .warning-message {
        font-size: 0.9rem;
        color: #7A6C5D;
        line-height: 1.6;
    }

    .section-label {
        font-size: 0.65rem;
        font-weight: 600;
        letter-spacing: 2.5px;
        text-transform: uppercase;
        color: #BB5B36;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }

    .item {
        font-size: 0.88rem;
        color: #7A6C5D;
        line-height: 1.6;
        margin-bottom: 0.5rem;
        padding-left: 1.1rem;
        position: relative;
    }

    .item:last-child {
        margin-bottom: 0;
    }

    .item::before {
        content: "•";
        position: absolute;
        left: 0;
        color: #BB5B36;
        font-weight: 700;
    }

    .season-tag {
        display: block;
        width: 100%;
        box-sizing: border-box;
        margin-top: 1.2rem;
        background: rgba(187,91,54,0.1);
        border: 1px solid rgba(187,91,54,0.25);
        color: #BB5B36;
        font-size: 0.72rem;
        line-height: 1.5;
        padding: 0.55rem 0.9rem;
        border-radius: 10px;
        letter-spacing: 0.5px;
    }

    .divider {
        border: none;
        border-top: 1px solid #E5D5C0;
        margin: 2rem 0;
    }

    .footer {
        text-align: center;
        color: #7A6C5D;
        font-size: 0.72rem;
        letter-spacing: 1px;
        margin-top: 3rem;
        padding-top: 1.5rem;
        border-top: 1px solid #E5D5C0;
    }

    /* Hide streamlit defaults */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* File uploader styling - warm minimal theme */
    .stFileUploader label {
        color: #2A2118 !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
    }

    [data-testid="stFileUploaderDropzone"] {
        background: #FFFFFF;
        border: 1px dashed #E5D5C0;
        border-radius: 12px;
    }

    [data-testid="stFileUploaderDropzoneInstructions"] {
        color: #2A2118;
    }

    [data-testid="stFileUploader"] [data-testid="stBaseButton-secondary"] {
        background: #BB5B36;
        color: #FFFFFF;
        border: none;
        border-radius: 8px;
    }

    [data-testid="stFileUploader"] [data-testid="stBaseButton-secondary"]:hover {
        background: #96431F;
        color: #FFFFFF;
    }

    /* Uploaded-photo preview thumbnail (left column of the results area) */
    .st-key-preview-image img {
        max-width: 100%;
        height: auto;
        object-fit: contain;
        border-radius: 12px;
        border: 1px solid #E5D5C0;
    }

    /* "About this project" -- manual toggle + plain scrollable div,
       replacing st.expander entirely. A plain div with a fixed height
       and overflow-y: auto has no competing internal Streamlit CSS to
       fight, unlike stExpander/stExpanderDetails. */
    .st-key-about-toggle button {
        background: transparent;
        border: none;
        color: #2A2118;
        font-size: 0.85rem;
        font-weight: 500;
        padding: 0.4rem 0;
        box-shadow: none;
    }

    .st-key-about-toggle button:hover {
        background: transparent;
        color: #BB5B36;
        border: none;
    }

    .st-key-about-toggle button:focus:not(:active) {
        color: #2A2118;
        border: none;
        box-shadow: none;
    }

    .about-box {
        height: auto;
        padding: 12px 16px;
        box-sizing: border-box;
        background: #FFFFFF;
        border: 1px solid #E5D5C0;
        border-radius: 10px;
        color: #7A6C5D;
        font-size: 0.85rem;
        line-height: 1.5;
    }
</style>
""", unsafe_allow_html=True)

# Header
header_col, image_col = st.columns([3, 2])
with header_col:
    st.markdown("""
    <div class="header">
        <div class="header-label">Leaf Health Scanner</div>
        <div class="header-title">Apple Leaf<br>Disease Detection</div>
        <div class="header-sub">Upload a photo for an instant diagnosis.</div>
    </div>
    """, unsafe_allow_html=True)
with image_col:
    # width=1094 matches the resolution assets/apple_tree_display.png was
    # regenerated at (measured cssWidth * devicePixelRatio * 2). Streamlit
    # re-encodes st.image() sources to exactly this many raster pixels, so
    # passing a smaller width here would silently throw away sharpness --
    # the browser still shrinks the *displayed* size to fit the column.
    st.image(str(BASE_DIR / "assets" / "apple_tree_display.png"), width=1094)

# "About this project" + Orchard Digest ticker, side by side
about_col, ticker_col = st.columns(2)

with about_col:
    if "show_about" not in st.session_state:
        st.session_state.show_about = False

    with st.container(key="about-toggle"):
        chevron = "▾" if st.session_state.show_about else "▸"
        if st.button(f"{chevron}  About this project", key="about-toggle-btn"):
            st.session_state.show_about = not st.session_state.show_about

    if st.session_state.show_about:
        st.markdown(
            '<div class="about-box">Trained on the PlantVillage dataset using '
            "EfficientNet-B0 transfer learning. Inspired by apple orchards in "
            "Himachal Pradesh, India.</div>",
            unsafe_allow_html=True,
        )

with ticker_col:
    with open(BASE_DIR / "src" / "apple_facts.json", "r", encoding="utf-8") as f:
        apple_facts = json.load(f)

    # A plain <script> inside st.markdown() gets torn down and rebuilt on
    # every Streamlit rerun (e.g. each time a file is uploaded), which
    # resets/stutters any running animation. st.components.v1.html() renders
    # into its own iframe instead; as long as the HTML string is identical
    # across reruns, Streamlit doesn't recreate the iframe, so the interval
    # timer inside it just keeps running undisturbed. The random start index
    # is chosen in the embedded JS (at iframe load) rather than in Python,
    # so the generated HTML stays byte-for-byte the same every rerun.
    ticker_html = f"""
    <div id="ticker-root">
        <div class="ticker-label">Orchard Digest</div>
        <div id="ticker-text" class="ticker-text"></div>
    </div>
    <style>
        html, body {{ margin: 0; padding: 0; }}
        #ticker-root {{
            font-family: 'Inter', sans-serif;
            box-sizing: border-box;
            width: 100%;
            height: 148px;
            background: #FFFFFF;
            border: 1px solid #E5D5C0;
            border-radius: 12px;
            padding: 1.1rem 1.3rem;
            display: flex;
            flex-direction: column;
            justify-content: center;
            overflow: hidden;
        }}
        .ticker-label {{
            font-size: 0.65rem;
            font-weight: 600;
            letter-spacing: 2.5px;
            text-transform: uppercase;
            color: #BB5B36;
            margin-bottom: 0.5rem;
            flex-shrink: 0;
        }}
        .ticker-text {{
            font-size: 0.85rem;
            line-height: 1.5;
            color: #2A2118;
            opacity: 1;
            transition: opacity 400ms ease;
        }}
        .ticker-text.fade {{
            opacity: 0;
        }}
    </style>
    <script>
        const facts = {json.dumps(apple_facts)};
        let idx = Math.floor(Math.random() * facts.length);
        const textEl = document.getElementById('ticker-text');
        textEl.textContent = facts[idx];

        setInterval(function () {{
            textEl.classList.add('fade');
            setTimeout(function () {{
                idx = (idx + 1) % facts.length;
                textEl.textContent = facts[idx];
                textEl.classList.remove('fade');
            }}, 400);
        }}, 4500);
    </script>
    """
    components.html(ticker_html, height=168)

@st.cache_resource
def get_model():
    return load_model(BASE_DIR / "data" / "apple_disease_model_v2.pth")

model = get_model()

# Upload
uploaded_file = st.file_uploader(
    "Select a leaf photograph — JPG or PNG",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")

    preview_col, result_col = st.columns([0.42, 0.58])

    with preview_col:
        with st.container(key="preview-image"):
            st.image(image, caption="Uploaded photograph", width="stretch")

    with result_col:
        with st.spinner("Analyzing..."):
            try:
                result = predict(image, model)
                confidence_value = float(result["confidence"].rstrip("%"))

                if confidence_value < 60:
                    st.markdown("""
                        <div class="warning-card">
                        <div class="warning-status">Low Confidence</div>
                        <div class="warning-message">Unclear image — please retry with a clearer photo of the leaf</div>
                        </div>
                    """, unsafe_allow_html=True)
                else:
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

            except Exception:
                st.error("Could not analyze this image. Please try a different photo.")

st.markdown("""
<div class="footer">
    Apple Orchard Intelligence — Built for Himalayan Farmers
</div>
""", unsafe_allow_html=True)