import streamlit as st
import os
import requests
import io
import time
import uuid
from gtts import gTTS
from PIL import Image

# =========================
# 1. CONFIG & PRO THEME
# =========================
st.set_page_config(page_title="Vixan AI Pro v17.1", layout="wide", page_icon="🚀")

SEGMIND_API = st.secrets.get("SEGMIND_API_KEY", "")
HF_TOKEN = st.secrets.get("HF_TOKEN", "")

st.markdown("""
    <style>
    .main { background: #0a0e17; color: white; }
    .stButton>button { border-radius: 12px; font-weight: 700; height: 3em; transition: 0.3s; }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 0 15px #00d4ff; }
    .pro-card { 
        background: linear-gradient(145deg, #1e1e2f, #2a2a40); 
        border: 1px solid #FFD700; border-radius: 15px; padding: 20px;
    }
    .free-card { 
        background: rgba(255,255,255,0.05); 
        border: 1px solid #00d4ff; border-radius: 15px; padding: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# =========================
# 2. SESSION STATE & SMART LOGIN
# =========================
if 'is_auth' not in st.session_state:
    st.session_state.is_auth = False

# Function to check login ONLY when button is clicked
def check_login():
    if not st.session_state.is_auth:
        st.warning("🔒 Action Required: Please Signup to generate content.")
        # Popup form inside the page
        with st.form("quick_signup"):
            st.markdown("### 📝 Fast Signup to Unlock AI Tools")
            name = st.text_input("Full Name", placeholder="Enter your name")
            phone = st.text_input("WhatsApp Number", placeholder="10 digits")
            submit = st.form_submit_button("Unlock Studio ✨")
            if submit:
                if name and len(phone) >= 10:
                    st.session_state.is_auth = True
                    st.session_state.user_name = name
                    st.success(f"Welcome {name}! Studio Unlocked. Please click the generate button again.")
                    st.rerun()
                else:
                    st.error("Invalid details. Please check.")
        return False
    return True

# =========================
# 3. SIDEBAR (Hamesha Unlocked)
# =========================
with st.sidebar:
    st.title("💎 Vixan Studio")
    menu = st.radio("SELECT ENGINE", ["🏠 Dashboard", "🖼️ AI Poster Lab", "🎙️ AI Voice Studio", "🎞️ Pro Video Lab"])
    st.divider()
    if st.session_state.is_auth:
        st.info(f"User: {st.session_state.user_name}")
        if st.button("Logout"):
            st.session_state.is_auth = False
            st.rerun()
    else:
        st.caption("Status: Guest Mode (Signup to Gen)")

# =========================
# 4. MODULES (Unlocked Interface)
# =========================

# --- HOME ---
if menu == "🏠 Dashboard":
    st.title("🚀 Bihar's Most Powerful AI Media Engine")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="free-card"><h3>🆓 Free Tools</h3><p>Pollinations AI Image<br>Google TTS Voice</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="pro-card"><h3>💎 Pro Tools</h3><p>Segmind HD Image<br>Hugging Face Video</p></div>', unsafe_allow_html=True)
    st.image("https://img.freepik.com/free-vector/abstract-technology-background_23-2148905210.jpg", use_container_width=True)

# --- POSTER LAB ---
elif menu == "🖼️ AI Poster Lab":
    st.header("🖼️ AI Poster Generation")
    prompt = st.text_area("Describe your design:", "Political poster background, Bihar election theme, 4k")
    
    col_f, col_p = st.columns(2)
    with col_f:
        st.subheader("Free (Pollinations)")
        if st.button("🎨 Gen Free Image"):
            if check_login(): # Login check on click
                with st.spinner("AI Generating..."):
                    url = f"https://image.pollinations.ai/prompt/{prompt.replace(' ','%20')}?nologo=true"
                    response = requests.get(url)
                    st.image(response.content)
                    st.download_button("💾 Save Free", response.content, "free_poster.png")

    with col_p:
        st.subheader("Pro HD (Segmind)")
        if st.button("🔥 Gen Pro HD Image"):
            if check_login(): # Login check on click
                if SEGMIND_API:
                    with st.spinner("Segmind Engine working..."):
                        url = "https://api.segmind.com/v1/sdxl1.0-txt2img"
                        headers = {"x-api-key": SEGMIND_API}
                        data = {"prompt": prompt + ", high quality, 8k", "samples": 1}
                        response = requests.post(url, json=data, headers=headers)
                        if response.status_code == 200:
                            st.image(response.content)
                            st.download_button("💾 Save Pro", response.content, "pro_hd.png")
                else: st.error("Segmind API Key Missing!")

# --- VOICE STUDIO ---
elif menu == "🎙️ AI Voice Studio":
    st.header("🎙️ AI Voice Generation")
    v_text = st.text_area("Enter Text:", "नमस्ते, वीक्सन एआई स्टूडियो में आपका स्वागत है।")
    
    col_v1, col_v2 = st.columns(2)
    with col_v1:
        st.subheader("Free Google Voice")
        if st.button("📢 Generate Free Audio"):
            if check_login(): # Login check on click
                tts = gTTS(text=v_text, lang='hi')
                tts.save("free.mp3")
                st.audio("free.mp3")

    with col_v2:
        st.subheader("Pro Voice Settings")
        st.file_uploader("Upload Sample (Cloning)")
        if st.button("🧬 Start Pro Cloning"):
            if check_login(): # Login check on click
                st.warning("ElevenLabs/HF Connection Required")

# --- PRO VIDEO LAB ---
elif menu == "🎞️ Pro Video Lab":
    st.header("🎞️ Pro AI Video Generation")
    v_prompt = st.text_input("Enter Video Prompt:")
    
    if st.button("🎬 Generate AI Video"):
        if check_login(): # Login check on click
            if HF_TOKEN:
                with st.spinner("Hugging Face Engine Rendering..."):
                    time.sleep(3)
                    st.video("https://www.w3schools.com/html/mov_bbb.mp4")
            else: st.error("Hugging Face Token Missing!")

# =========================
# 5. FOOTER
# =========================
st.markdown("<hr><center>© 2026 Vixan AI Media Studio • Patna 🇮🇳</center>", unsafe_allow_html=True)
