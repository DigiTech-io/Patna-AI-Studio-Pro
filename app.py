import streamlit as st
import os
import requests
import uuid
import io
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont

# =========================
# 1. PAGE SETUP & PREMIUM THEME
# =========================
st.set_page_config(page_title="Vixan AI Pro v10.0", layout="wide", page_icon="🚀")

# Ultra-Smooth Neon UI
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;700&display=swap');
    html, body, [class*="css"] { font-family: 'Rajdhani', sans-serif; }
    .main { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); color: white; }
    .stButton>button {
        background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%);
        color: white; border-radius: 50px; border: none; font-weight: bold;
        transition: 0.3s; box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .stButton>button:hover { transform: scale(1.05); box-shadow: 0 6px 20px rgba(0,210,255,0.5); }
    .glass-card { background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); border-radius: 20px; padding: 25px; border: 1px solid rgba(255,255,255,0.1); }
    .support-float { position: fixed; bottom: 20px; right: 20px; z-index: 100; }
    </style>
    """, unsafe_allow_html=True)

# =========================
# 2. LOGIN SYSTEM (Session State)
# =========================
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    with st.container():
        st.markdown("<div class='glass-card' style='max-width:400px; margin:auto; margin-top:100px;'>", unsafe_allow_html=True)
        st.title("🔐 User Access")
        name = st.text_input("Full Name")
        phone = st.text_input("WhatsApp Number")
        if st.button("Start AI Magic ✨"):
            if name and len(phone) >= 10:
                st.session_state.logged_in = True
                st.session_state.user_name = name
                st.rerun()
            else:
                st.error("Please enter valid details")
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# =========================
# 3. SIDEBAR & MENU
# =========================
with st.sidebar:
    st.markdown(f"### Welcome, {st.session_state.user_name} 👋")
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=80)
    menu = st.radio("Explore Tools", ["🏠 Home", "🖼️ AI Poster Lab", "🎙️ Voice & Clone", "🎞️ Video Clone", "ℹ️ About & Legal"])
    st.divider()
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

# =========================
# 4. HOME DASHBOARD
# =========================
if menu == "🏠 Home":
    st.title(f"🚀 Vixan AI Media Studio Pro")
    st.markdown("#### Bihar's Most Powerful AI Engine for Digital Branding")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div class='glass-card'>🖼️ <b>Poster Lab</b><br>Create HD Designs in 10 sec</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='glass-card'>🎙️ <b>Voice Studio</b><br>Human-like AI Voices</div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='glass-card'>🎞️ <b>Video Clone</b><br>Talking AI Posters</div>", unsafe_allow_html=True)

    st.image("https://img.freepik.com/free-vector/abstract-technology-background_23-2148905210.jpg", use_container_width=True)

# =========================
# 5. POSTER LAB (Free/Pro + Font Selection)
# =========================
elif menu == "🖼️ AI Poster Lab":
    st.header("🖼️ Professional Poster Generator")
    mode = st.toggle("Switch to Pro (Segmind API Required)", value=False)
    
    col_in, col_pre = st.columns([1, 1.2])
    with col_in:
        l_name = st.text_input("Name on Poster", "आपका नाम यहाँ")
        l_slogan = st.text_input("Slogan", "नया बिहार, नई पहचान")
        
        font_dir = "fonts"
        fonts = [f for f in os.listdir(font_dir) if f.endswith(".ttf")] if os.path.exists(font_dir) else ["Default"]
        sel_font = st.selectbox("Select Font Style", fonts)
        
        prompt = st.text_area("Background Prompt", "Political banner background, luxury orange and gold theme, 4k")
        
        gen_btn = st.button("Generate & Process Design")

    with col_pre:
        if gen_btn:
            with st.spinner("AI Working..."):
                # FREE Image Generation (Pollinations)
                img_url = f"https://image.pollinations.ai/prompt/{prompt.replace(' ','%20')}?width=1024&height=1024&nologo=true"
                img_data = requests.get(img_url).content
                st.image(img_data, caption="Design Preview", use_container_width=True)
                st.download_button("📥 Download Design", img_data, "vixan_poster.png")

# =========================
# 6. VOICE CLONE & SETTINGS
# =========================
elif menu == "🎙️ Voice & Clone":
    st.header("🎙️ Advanced Voice Lab")
    text_in = st.text_area("Write Text", "नमस्ते, वीक्सन स्टूडियो में आपका स्वागत है।")
    
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Free Engine (Google)")
        v_speed = st.slider("Speech Speed", 0.5, 2.0, 1.0)
        if st.button("Generate Free Audio"):
            tts = gTTS(text=text_in, lang='hi', slow=(v_speed < 1.0))
            tts.save("v.mp3")
            st.audio("v.mp3")
    
    with c2:
        st.subheader("Clone Engine (Pro)")
        st.file_uploader("Upload Voice for Cloning (10s sample)")
        st.button("🧬 Start Cloning")

# =========================
# 7. ABOUT & DISCLAIMER
# =========================
elif menu == "ℹ️ About & Legal":
    st.title("ℹ️ Information Center")
    st.markdown("""
    ### 👨‍💻 About Me
    Vixan AI is developed by **Patna AI Studio**, Bihar's leader in generative AI technology. Our mission is to empower local businesses and leaders with world-class branding tools.
    
    ### ⚠️ Disclaimer
    * This AI tool is for creative branding only.
    * Do not use for creating fake news or deepfakes of political figures.
    * The developer is not responsible for misused content.
    """)

# =========================
# 8. FLOATING SUPPORT
# =========================
st.markdown(f"""
    <div class="support-float">
        <a href="https://wa.me/91XXXXXXXXXX?text=Hi%20Vixan%20Support,%20I%20need%20help." target="_blank">
            <button style="background:#25d366; color:white; border-radius:50px; padding:10px 20px; border:none; font-weight:bold;">
                💬 WhatsApp Support
            </button>
        </a>
        <br><br>
        <a href="tel:+91XXXXXXXXXX">
            <button style="background:#007bff; color:white; border-radius:50px; padding:10px 20px; border:none; font-weight:bold;">
                📞 Call Developer
            </button>
        </a>
    </div>
    """, unsafe_allow_html=True)
