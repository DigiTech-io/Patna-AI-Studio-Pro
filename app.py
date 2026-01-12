import streamlit as st
import os
import requests
import uuid
import io
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont

# =========================
# 1. THEME & APP CONFIG
# =========================
st.set_page_config(page_title="Vixan AI Pro v13.0", layout="wide", page_icon="🚀")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;700&display=swap');
    html, body, [class*="css"] { font-family: 'Rajdhani', sans-serif; }
    .main { background: linear-gradient(135deg, #020111 0%, #050625 100%); color: white; }
    
    /* Neon Cards */
    .feature-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(0, 210, 255, 0.3);
        border-radius: 20px; padding: 20px; margin-bottom: 20px;
    }
    
    /* Global Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%);
        color: white; border-radius: 12px; border: none; font-weight: bold; width: 100%; transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 0 20px #00d2ff; }
    
    .support-float { position: fixed; bottom: 30px; left: 30px; z-index: 100; display: flex; flex-direction: column; gap: 10px; }
    </style>
    """, unsafe_allow_html=True)

# Session Management
if 'is_authenticated' not in st.session_state:
    st.session_state.is_authenticated = False

# =========================
# 2. LOGIN POPUP
# =========================
def check_auth():
    if not st.session_state.is_authenticated:
        st.warning("🔒 Login Required to Generate Content")
        with st.expander("📝 Fast Signup / Login", expanded=True):
            u_name = st.text_input("Name")
            u_phone = st.text_input("WhatsApp Number")
            if st.button("Unlock All Features ✨"):
                if u_name and len(u_phone) >= 10:
                    st.session_state.is_authenticated = True
                    st.session_state.user_name = u_name
                    st.rerun()
        return False
    return True

# =========================
# 3. SIDEBAR
# =========================
with st.sidebar:
    st.markdown("<h2 style='color:#00d2ff;'>VIXAN STUDIO</h2>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=100)
    menu = st.radio("MAIN MENU", ["🏠 Home Dashboard", "🖼️ AI Poster Lab", "🎙️ AI Voice Studio", "🎞️ Video Center"])
    st.divider()
    if st.session_state.is_authenticated:
        st.success(f"User: {st.session_state.user_name}")
        if st.button("Logout"):
            st.session_state.is_authenticated = False
            st.rerun()

# =========================
# 4. MODULES
# =========================

# --- HOME ---
if menu == "🏠 Home Dashboard":
    st.title("🚀 Vixan AI Master Studio")
    st.markdown("#### The Ultimate AI Media Engine: Create, Clone & Innovate")
    
    
    
    c1, c2, c3 = st.columns(3)
    with c1: st.info("🖼️ **AI Poster Lab**: Text-to-Poster & Image-to-Image Clone.")
    with c2: st.success("🎙️ **AI Voice Studio**: Text-to-Speech & Voice Cloning.")
    with c3: st.warning("🎞️ **Video Center**: Talking Posters & Animation.")
    
    st.image("https://img.freepik.com/free-vector/abstract-technology-background_23-2148905210.jpg", use_container_width=True)

# --- POSTER LAB (Creation + Clone) ---
elif menu == "🖼️ AI Poster Lab":
    st.header("🖼️ AI Poster Lab (Create & Clone)")
    
    tab1, tab2 = st.tabs(["✨ Create New (Text)", "🧬 Clone Existing (Upload)"])
    
    with tab1:
        st.subheader("Text to AI Poster")
        p_text = st.text_area("Describe your poster:", "Professional political banner, orange theme, 4k")
        if st.button("🚀 Generate New Poster"):
            if check_auth():
                with st.spinner("AI Painting..."):
                    url = f"https://image.pollinations.ai/prompt/{p_text.replace(' ','%20')}?width=1024&height=1024&nologo=true"
                    data = requests.get(url).content
                    st.image(data)
                    st.download_button("📥 Download", data, "new_vixan.png")

    with tab2:
        st.subheader("Image-to-Image Clone")
        up_img = st.file_uploader("Upload Poster to Clone", type=['jpg','png'])
        clone_name = st.text_input("New Name for Clone", "Vixan AI")
        if st.button("🧬 Start Poster Cloning"):
            if check_auth():
                if up_img:
                    with st.spinner("Analyzing & Cloning..."):
                        url = f"https://image.pollinations.ai/prompt/clone%20design%20of%20poster%20for%20{clone_name.replace(' ','%20')}?width=1024&height=1024&nologo=true"
                        data = requests.get(url).content
                        st.image(data)
                        st.download_button("📥 Download Clone", data, "cloned_vixan.png")
                else: st.error("Please upload an image!")

# --- VOICE STUDIO (TTS + Clone) ---
elif menu == "🎙️ AI Voice Studio":
    st.header("🎙️ AI Voice Lab (TTS & Clone)")
    
    tab_v1, tab_v2 = st.tabs(["📢 Text to Speech", "🧬 Voice Cloning"])
    
    with tab_v1:
        v_text = st.text_area("Enter Text:", "नमस्ते, वीक्सन एआई स्टूडियो में आपका स्वागत है।")
        v_speed = st.slider("Speed", 0.5, 2.0, 1.0)
        if st.button("📢 Generate Free Voice"):
            if check_auth():
                tts = gTTS(text=v_text, lang='hi', slow=(v_speed < 1.0))
                tts.save("v.mp3")
                st.audio("v.mp3")
                with open("v.mp3", "rb") as f: st.download_button("📥 Download MP3", f, "voice.mp3")

    with tab_v2:
        st.subheader("Voice DNA Cloning")
        up_aud = st.file_uploader("Upload Voice Sample", type=['mp3','wav'])
        cl_text = st.text_area("Text to Speak in Cloned Voice:", "यह मेरी क्लोन की हुई आवाज़ है।")
        if st.button("🧬 Clone & Speak"):
            if check_auth():
                if up_aud:
                    with st.spinner("Cloning Voice..."):
                        tts = gTTS(text=cl_text, lang='hi')
                        tts.save("cl.mp3")
                        st.audio("cl.mp3")
                else: st.error("Upload voice sample first!")

# --- VIDEO CENTER ---
elif menu == "🎞️ Video Center":
    st.header("🎞️ AI Video Production")
    st.info("Coming Soon: Real-time Lip Sync & Face Swap")
    st.video("https://www.w3schools.com/html/mov_bbb.mp4")

# =========================
# 5. SUPPORT
# =========================
st.markdown(f"""
    <div class="support-float">
        <a href="https://wa.me/91XXXXXXXXXX" target="_blank"><button style="background:#25d366; color:white; border-radius:30px; border:none; padding:10px; font-weight:bold;">💬 WhatsApp</button></a>
        <a href="tel:+91XXXXXXXXXX"><button style="background:#00d2ff; color:white; border-radius:30px; border:none; padding:10px; font-weight:bold;">📞 Call Now</button></a>
    </div>
    """, unsafe_allow_html=True)
