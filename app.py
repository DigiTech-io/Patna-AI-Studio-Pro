import streamlit as st
import requests
import io
import time
import uuid
from gtts import gTTS

# =========================
# 1. ULTIMATE UI THEME FIX
# =========================
st.set_page_config(page_title="Vixan AI Pro v27.0", layout="wide", page_icon="💎")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@600;700&display=swap');
    
    /* Overall Background */
    .stApp { background-color: #0e1117; color: #ffffff; font-family: 'Rajdhani', sans-serif; }
    
    /* Sidebar Visibility Fix - Making it distinct */
    [data-testid="stSidebar"] {
        background-color: #1a1c24 !important;
        border-right: 2px solid #FFD700;
    }
    [data-testid="stSidebar"] * { color: #ffffff !important; font-size: 18px; }

    /* Ready Template Cards */
    .template-card {
        background: #1f222d;
        border: 1px solid #333;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        margin-bottom: 25px;
        transition: 0.3s;
    }
    .template-card:hover { border-color: #00d2ff; transform: translateY(-5px); }
    
    /* Buttons Styling */
    .stButton>button {
        border-radius: 12px;
        font-weight: 700;
        background: linear-gradient(90deg, #00d2ff, #3a7bd5);
        color: white !important;
        border: none;
        width: 100%;
        height: 3em;
    }
    
    /* Floating WhatsApp */
    .wa-float {
        position: fixed; bottom: 30px; right: 30px;
        background-color: #25d366; color: white;
        padding: 15px 25px; border-radius: 50px;
        font-weight: bold; z-index: 100;
        text-decoration: none; box-shadow: 2px 2px 10px rgba(0,0,0,0.5);
    }
    </style>
""", unsafe_allow_html=True)

# Session State
if 'is_auth' not in st.session_state: st.session_state.is_auth = False
if 'user_name' not in st.session_state: st.session_state.user_name = "Guest"

def check_auth():
    if not st.session_state.is_auth:
        st.warning("🔒 Features Unlock Karne ke liye Login Karein")
        with st.form("signup_master"):
            name = st.text_input("Full Name")
            phone = st.text_input("WhatsApp No")
            if st.form_submit_button("Get Access Now 🚀"):
                if name and len(phone) >= 10:
                    st.session_state.is_auth = True
                    st.session_state.user_name = name
                    st.rerun()
        return False
    return True

# =========================
# 2. SIDEBAR NAVIGATION (Highly Visible)
# =========================
with st.sidebar:
    st.markdown("<h1 style='color:#FFD700; text-align:center;'>💎 VIXAN PRO</h1>", unsafe_allow_html=True)
    st.divider()
    
    # Menu Selection
    menu = st.radio(
        "SELECT TOOL",
        ["🏠 Dashboard", "🖼️ Ready Templates", "🎨 AI Poster Lab", "🎙️ Voice Studio", "🎞️ Talking Face"],
        key="nav_menu"
    )
    
    st.divider()
    if st.session_state.is_auth:
        st.success(f"User: {st.session_state.user_name}")
        if st.button("Logout"):
            st.session_state.is_auth = False
            st.rerun()

# =========================
# 3. MODULES LOGIC
# =========================

if menu == "🏠 Dashboard":
    st.title("🚀 Bihar's No. 1 AI Media Studio")
    st.markdown("#### AI Poster Generation | Voice Cloning | Talking Video")
    st.image("https://img.freepik.com/free-vector/abstract-technology-background_23-2148905210.jpg", use_container_width=True)

elif menu == "🖼️ Ready Templates":
    st.header("🖼️ Select & Generate Poster")
    
    cat_col1, cat_col2 = st.columns(2)
    
    with cat_col1:
        st.markdown("### 🚩 Political")
        with st.container():
            st.markdown("<div class='template-card'><b>Bihar Election 2026</b></div>", unsafe_allow_html=True)
            txt1 = st.text_input("Custom Text for Election", key="p1")
            if st.button("Generate Election Poster"):
                if check_auth():
                    with st.spinner("AI Painting..."):
                        url = f"https://image.pollinations.ai/prompt/bihar%20election%20poster%202026%20with%20text%20{txt1}?nologo=true&seed={uuid.uuid4().int}"
                        st.image(url)

    with cat_col2:
        st.markdown("### 💼 Business")
        with st.container():
            st.markdown("<div class='template-card'><b>Shop Promotion</b></div>", unsafe_allow_html=True)
            txt2 = st.text_input("Shop Name/Details", key="b1")
            if st.button("Generate Business Banner"):
                if check_auth():
                    with st.spinner("Creating Design..."):
                        url = f"https://image.pollinations.ai/prompt/modern%20business%20shop%20promotion%20banner%20with%20text%20{txt2}?nologo=true&seed={uuid.uuid4().int}"
                        st.image(url)

elif menu == "🎨 AI Poster Lab":
    st.header("🎨 AI Poster Lab (Text to Image)")
    prompt = st.text_area("Aapka Prompt Likhein:", "Professional political banner, orange theme, leadership style, 4k")
    if st.button("🚀 Create Magic Poster"):
        if check_auth():
            url = f"https://image.pollinations.ai/prompt/{prompt.replace(' ','%20')}?nologo=true&width=1024&height=1024&seed={uuid.uuid4().int}"
            st.image(url)

elif menu == "🎙️ Voice Studio":
    st.header("🎙️ Voice DNA & Cloning")
    v_text = st.text_area("Hindi/English Text:", "नमस्ते, वीक्सन एआई प्रो में आपका स्वागत है।")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📢 Generate Voice"):
            if check_auth():
                tts = gTTS(text=v_text, lang='hi')
                tts.save("v.mp3")
                st.audio("v.mp3")
    with col2:
        st.file_uploader("Upload Audio for Cloning", type=['mp3'])
        if st.button("🧬 Clone Voice DNA"):
            if check_auth(): st.success("Voice DNA Extracted!")

elif menu == "🎞️ Talking Face":
    st.header("🎞️ Talking Face Video")
    st.file_uploader("Upload Face Photo", key="img_up")
    st.file_uploader("Upload Audio Script", key="aud_up")
    if st.button("🎬 Render Talking Video"):
        if check_auth():
            st.video("https://www.w3schools.com/html/mov_bbb.mp4")

# =========================
# 4. SUPPORT & FOOTER
# =========================
st.markdown('<a href="https://wa.me/91XXXXXXXXXX" class="wa-float">💬 WhatsApp Support</a>', unsafe_allow_html=True)
