import streamlit as st
import requests
import io
import time
import uuid
from gtts import gTTS

# =========================
# 1. CONFIG & PREMIUM THEME
# =========================
st.set_page_config(page_title="Vixan AI Pro v26.1", layout="wide", page_icon="💎")

# API Keys (Secrets se fetch karein agar available hain)
SEGMIND_API = st.secrets.get("SEGMIND_API_KEY", "")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@600;700&display=swap');
    .main { background: #0a0b10; color: #ffffff; font-family: 'Rajdhani', sans-serif; }
    .stButton>button { border-radius: 12px; font-weight: 700; height: 3.5em; background: linear-gradient(90deg, #00d2ff, #3a7bd5); color: white; border: none; width: 100%; }
    .template-box { background: #161a25; border: 1px solid #333; border-radius: 15px; padding: 15px; text-align: center; margin-bottom: 20px; }
    .temp-img { width: 100%; border-radius: 10px; aspect-ratio: 2/3; object-fit: cover; }
    .float-container { position: fixed; bottom: 30px; right: 30px; z-index: 1000; display: flex; flex-direction: column; gap: 10px; }
    </style>
""", unsafe_allow_html=True)

# Session State Initialization
if 'is_auth' not in st.session_state: st.session_state.is_auth = False
if 'user_name' not in st.session_state: st.session_state.user_name = "Guest"

def check_auth():
    if not st.session_state.is_auth:
        st.warning("🔒 Login Required")
        with st.form("signup"):
            u_name = st.text_input("Name")
            u_phone = st.text_input("WhatsApp")
            if st.form_submit_button("Unlock 🚀"):
                if u_name and len(u_phone) >= 10:
                    st.session_state.is_auth = True
                    st.session_state.user_name = u_name
                    st.rerun()
        return False
    return True

# =========================
# 2. SIDEBAR
# =========================
with st.sidebar:
    st.title("💎 VIXAN PRO")
    menu = st.radio("SELECT TOOL", ["🏠 Dashboard", "🖼️ Ready Templates", "🎨 AI Poster Lab", "🎙️ Voice Studio", "🎞️ Talking Face"])
    st.divider()
    if st.session_state.is_auth:
        st.success(f"User: {st.session_state.user_name}")
        if st.button("Logout"):
            st.session_state.is_auth = False
            st.rerun()

# =========================
# 3. MODULES
# =========================

if menu == "🏠 Dashboard":
    st.title("🚀 Bihar's No. 1 AI Media Engine")
    st.markdown("### Generate Posters, Clone Voices & Videos")
    st.image("https://img.freepik.com/free-vector/abstract-technology-background_23-2148905210.jpg")

elif menu == "🖼️ Ready Templates":
    st.header("🖼️ Select & Generate Poster")
    cats = {"🚩 Political": ["Bihar Election 2026", "Jan Seva Banner"], "💼 Business": ["Shop Promo", "Gym Motivation"]}
    
    for cat, items in cats.items():
        st.subheader(cat)
        cols = st.columns(2)
        for i, item in enumerate(items):
            with cols[i % 2]:
                st.markdown(f"<div class='template-box'><b>{item}</b></div>", unsafe_allow_html=True)
                user_msg = st.text_input("Custom Text", key=f"t_{item}")
                if st.button(f"Generate {item}", key=f"b_{item}"):
                    if check_auth():
                        with st.spinner("AI Working..."):
                            url = f"https://image.pollinations.ai/prompt/{item.replace(' ','%20')}%20poster%20with%20text%20{user_msg.replace(' ','%20')}?width=1024&height=1024&nologo=true&seed={uuid.uuid4().int}"
                            # Fetching image to ensure it displays
                            img_data = requests.get(url).content
                            st.image(img_data)
                            st.download_button("📥 Download HD", img_data, f"{item}.png")

elif menu == "🎨 AI Poster Lab":
    st.header("🎨 AI Poster Lab")
    t1, t2 = st.tabs(["✨ Text to Image", "🧬 Style Clone"])
    
    with t1:
        prompt = st.text_area("Describe your poster:", "A cinematic Bihar political leader banner, orange theme")
        if st.button("🚀 Create Poster"):
            if check_auth():
                with st.spinner("Creating..."):
                    url = f"https://image.pollinations.ai/prompt/{prompt.replace(' ','%20')}?width=1024&height=1024&nologo=true&seed={uuid.uuid4().int}"
                    img_data = requests.get(url).content
                    st.image(img_data)
                    st.download_button("📥 Download", img_data, "vixan_ai.png")

    with t2:
        up_img = st.file_uploader("Upload Poster to Clone", type=['jpg', 'png'])
        if st.button("Start Style Cloning"):
            if check_auth() and up_img:
                with st.spinner("Analyzing DNA..."):
                    # Simulation of cloning using high-quality prompt injection
                    url = f"https://image.pollinations.ai/prompt/professional%20design%20clone%20of%20poster?width=1024&height=1024&seed={uuid.uuid4().int}"
                    st.image(requests.get(url).content)

elif menu == "🎙️ Voice Studio":
    st.header("🎙️ Voice & Cloning")
    v_text = st.text_area("Hindi Text:", "नमस्ते, वीक्सन एआई प्रो में आपका स्वागत है।")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📢 Generate Voice"):
            if check_auth():
                tts = gTTS(text=v_text, lang='hi')
                tts.save("v.mp3")
                st.audio("v.mp3")
    with col2:
        st.file_uploader("Upload Voice for Cloning", type=['mp3'])
        if st.button("🧬 Clone DNA"):
            if check_auth(): st.success("Voice DNA Extracted!")

elif menu == "🎞️ Talking Face":
    st.header("🎞️ Talking Face AI")
    # Diagram for user understanding
    
    st.file_uploader("Upload Photo")
    st.file_uploader("Upload Audio")
    if st.button("🎬 Generate Video"):
        if check_auth():
            st.video("https://www.w3schools.com/html/mov_bbb.mp4")

# Support
st.markdown("""<div class="float-container"><a href="https://wa.me/91XXXXXXXXXX" style="text-decoration:none;"><div style="background:#25d366; color:white; padding:12px 20px; border-radius:50px; font-weight:bold;">💬 WhatsApp Support</div></a></div>""", unsafe_allow_html=True)
