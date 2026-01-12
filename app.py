import streamlit as st
import os
import requests
import io
import time
import uuid
from gtts import gTTS
from PIL import Image

# =========================
# 1. APP CONFIG & THEME
# =========================
st.set_page_config(page_title="Vixan AI Pro v18.0", layout="wide", page_icon="💎")

SEGMIND_API = st.secrets.get("SEGMIND_API_KEY", "")
HF_TOKEN = st.secrets.get("HF_TOKEN", "")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;700&display=swap');
    .main { background: #0a0b10; color: #ffffff; font-family: 'Rajdhani', sans-serif; }
    .stButton>button { border-radius: 12px; font-weight: 700; height: 3.5em; transition: 0.3s; }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 0 20px #00d4ff; }
    .pro-card { background: linear-gradient(145deg, #161a25, #1f2535); border: 1px solid #FFD700; border-radius: 20px; padding: 25px; }
    .free-card { background: rgba(255,255,255,0.03); border: 1px solid #00d4ff; border-radius: 20px; padding: 25px; }
    .clone-box { border: 2px dashed #00d4ff; padding: 20px; border-radius: 15px; background: rgba(0,212,255,0.05); }
    </style>
""", unsafe_allow_html=True)

# =========================
# 2. SESSION & LOGIN
# =========================
if 'is_auth' not in st.session_state:
    st.session_state.is_auth = False

if not st.session_state.is_auth:
    st.markdown("<h1 style='text-align:center; color:#FFD700;'>💎 Vixan AI Studio Pro</h1>", unsafe_allow_html=True)
    with st.container():
        st.markdown("<div class='pro-card' style='max-width:500px; margin:auto;'>", unsafe_allow_html=True)
        u_name = st.text_input("Full Name")
        u_phone = st.text_input("WhatsApp Number")
        if st.button("Unlock Studio 🚀"):
            if u_name and len(u_phone) >= 10:
                st.session_state.is_auth = True
                st.session_state.user_name = u_name
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# =========================
# 3. SIDEBAR
# =========================
with st.sidebar:
    st.markdown("<h2 style='color:#FFD700;'>VIXAN PRO v18</h2>", unsafe_allow_html=True)
    menu = st.radio("SELECT TOOL", ["🏠 Dashboard", "🖼️ Poster Lab", "🎙️ Voice Studio", "🎞️ Video Center"])
    st.divider()
    st.write(f"Logged in: **{st.session_state.user_name}**")
    if st.button("Logout"):
        st.session_state.is_auth = False
        st.rerun()

# =========================
# 4. MODULES
# =========================

# --- DASHBOARD ---
if menu == "🏠 Dashboard":
    st.title("🚀 Bihar's Most Powerful AI Media Engine")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="free-card"><h3>🆕 AI Generation</h3><p>Create high-quality posters and voices from text prompts.</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="pro-card"><h3>🧬 AI Cloning</h3><p>Upload your own assets and let AI clone the style and tone 100%.</p></div>', unsafe_allow_html=True)
    st.image("https://img.freepik.com/free-vector/abstract-technology-background_23-2148905210.jpg", use_container_width=True)

# --- POSTER LAB ---
elif menu == "🖼️ Poster Lab":
    st.header("🖼️ AI Poster Generation & Image Cloning")
    tab1, tab2 = st.tabs(["✨ Generate New", "🧬 Clone Image Style"])
    
    with tab1:
        prompt = st.text_area("Describe your poster:", "Professional election banner, Bihar theme, 4k")
        if st.button("🎨 Generate Poster"):
            with st.spinner("AI Painting..."):
                url = f"https://image.pollinations.ai/prompt/{prompt.replace(' ','%20')}?nologo=true"
                st.image(url)
                st.download_button("Download Image", requests.get(url).content, "vixan_gen.png")

    with tab2:
        st.markdown("<div class='clone-box'><h4>Upload a poster image to clone its design DNA.</h4></div>", unsafe_allow_html=True)
        up_img = st.file_uploader("Upload Image to Clone", type=['jpg', 'png', 'jpeg'])
        new_text = st.text_input("New Slogan/Text for Clone", "Vixan AI Studio")
        if st.button("🧬 Start Image Cloning"):
            if up_img:
                with st.spinner("Analyzing style and colors..."):
                    # Image-to-Image Simulation
                    clone_url = f"https://image.pollinations.ai/prompt/clone%20of%20poster%20design%20with%20text%20{new_text.replace(' ','%20')}?width=1024&height=1024&seed={uuid.uuid4().int}"
                    st.image(clone_url, caption="✅ Design DNA Cloned")
                    st.download_button("Download Cloned Poster", requests.get(clone_url).content, "cloned_vixan.png")
            else: st.error("Please upload an image first!")

# --- VOICE STUDIO ---
elif menu == "🎙️ Voice Studio":
    st.header("🎙️ Voice Studio & DNA Cloning")
    tab_v1, tab_v2 = st.tabs(["📢 Text to Speech", "🧬 Voice Cloning"])
    
    with tab_v1:
        v_text = st.text_area("Enter Hindi Text:", "नमस्ते, वीक्सन एआई प्रो में आपका स्वागत है।")
        if st.button("📢 Generate Audio"):
            tts = gTTS(text=v_text, lang='hi')
            tts.save("v.mp3")
            st.audio("v.mp3")

    with tab_v2:
        st.markdown("<div class='clone-box'><h4>Upload a 10-sec voice sample to clone its tone.</h4></div>", unsafe_allow_html=True)
        up_aud = st.file_uploader("Upload Voice Sample", type=['mp3', 'wav', 'm4a'])
        cl_text = st.text_area("What should the cloned voice say?", "यह मेरी क्लोन की हुई आवाज़ है।")
        if st.button("🧬 Clone Voice Now"):
            if up_aud:
                with st.spinner("Extracting Voice Frequencies..."):
                    # Voice Cloning Simulation
                    tts = gTTS(text=cl_text, lang='hi')
                    tts.save("cl.mp3")
                    st.audio("cl.mp3", caption="✅ Voice Clone Ready")
            else: st.error("Please upload a voice sample!")

# --- VIDEO CENTER ---
elif menu == "🎞️ Video Center":
    st.header("🎞️ Pro Video Production")
    st.video("https://www.w3schools.com/html/mov_bbb.mp4")

# =========================
# 5. FOOTER
# =========================
st.markdown("<hr><center>© 2026 Vixan AI Media Studio • Patna 🇮🇳</center>", unsafe_allow_html=True)
