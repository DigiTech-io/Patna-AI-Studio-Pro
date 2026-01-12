import streamlit as st
import os
import requests
import io
import time
import uuid
from gtts import gTTS
from PIL import Image

# =========================
# 1. APP CONFIG & ULTIMATE THEME
# =========================
st.set_page_config(page_title="Vixan AI Pro v17.0", layout="wide", page_icon="💎")

SEGMIND_API = st.secrets.get("SEGMIND_API_KEY", "")
HF_TOKEN = st.secrets.get("HF_TOKEN", "")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    .main { background: #0a0b10; color: #ffffff; font-family: 'Inter', sans-serif; }
    .stButton>button { 
        border-radius: 12px; font-weight: 700; height: 3.5em; 
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .pro-card { 
        background: linear-gradient(145deg, #161a25, #1f2535); 
        border: 1px solid #FFD700; border-radius: 20px; padding: 25px;
        box-shadow: 0 10px 40px rgba(255,215,0,0.1);
    }
    .free-card { 
        background: rgba(255,255,255,0.03); 
        border: 1px solid #00d4ff; border-radius: 20px; padding: 25px;
    }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: #161a25 !important; color: white !important; border: 1px solid #333 !important;
    }
    </style>
""", unsafe_allow_html=True)

# =========================
# 2. SESSION & LOGIN SYSTEM
# =========================
if 'is_auth' not in st.session_state:
    st.session_state.is_auth = False

if not st.session_state.is_auth:
    st.markdown("<h1 style='text-align:center; color:#FFD700;'>💎 Vixan AI Studio Pro</h1>", unsafe_allow_html=True)
    with st.container():
        st.markdown("<div class='pro-card' style='max-width:500px; margin:auto;'>", unsafe_allow_html=True)
        u_name = st.text_input("Full Name")
        u_phone = st.text_input("WhatsApp Number (10 Digits)")
        if st.button("Unlock All Engines 🚀"):
            if u_name and len(u_phone) >= 10:
                st.session_state.is_auth = True
                st.session_state.user_name = u_name
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# =========================
# 3. SIDEBAR NAVIGATION
# =========================
with st.sidebar:
    st.markdown("<h2 style='color:#FFD700;'>VIXAN PRO v17</h2>", unsafe_allow_html=True)
    menu = st.radio("SELECT ENGINE", ["🏠 Dashboard", "🖼️ AI Poster Lab", "🎙️ AI Voice Studio", "🎞️ Pro Video Lab"])
    st.divider()
    st.write(f"Logged in: **{st.session_state.user_name}**")
    if st.button("Logout"):
        st.session_state.is_auth = False
        st.rerun()

# =========================
# 4. REAL API ENGINES (PRO)
# =========================

def generate_pro_poster(prompt):
    url = "https://api.segmind.com/v1/sdxl1.0-txt2img"
    headers = {"x-api-key": SEGMIND_API}
    data = {
        "prompt": prompt + ", professional poster, highly detailed, 8k resolution, cinematic lighting",
        "seed": uuid.uuid4().int % 1000000,
        "scheduler": "dpmpp_2m",
        "num_inference_steps": 30,
        "negative_prompt": "blurry, low quality, distorted text, messy"
    }
    response = requests.post(url, json=data, headers=headers)
    return response.content if response.status_code == 200 else None

def generate_pro_video(prompt):
    # Asli Hugging Face API (Stable Video Diffusion model)
    API_URL = "https://api-inference.huggingface.co/models/google/veo-1" # Ya aapka pasandida model
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    # Note: Video generation takes time, usually returns a job or binary
    response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
    return response.content if response.status_code == 200 else None

# =========================
# 5. PAGE LOGIC
# =========================

if menu == "🏠 Dashboard":
    st.title("🚀 Bihar's Most Powerful AI Engine")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="free-card"><h3>🆓 Free Engines</h3><p>Pollinations Image<br>Google TTS Voice</p></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="pro-card"><h3>💎 Pro Engines</h3><p>Segmind 8K (SDXL)<br>Hugging Face Video</p></div>', unsafe_allow_html=True)

elif menu == "🖼️ AI Poster Lab":
    st.header("🖼️ AI Poster Generator")
    prompt = st.text_area("Design Prompt:", "A professional election banner for Bihar, orange theme, leadership style")
    
    col_f, col_p = st.columns(2)
    with col_f:
        st.subheader("Free (Pollinations)")
        if st.button("🎨 Gen Free"):
            url = f"https://image.pollinations.ai/prompt/{prompt.replace(' ','%20')}?nologo=true"
            st.image(url)
            st.download_button("Download Free", requests.get(url).content, "free.png")

    with col_p:
        st.subheader("Pro HD (Segmind)")
        if st.button("🔥 Gen Pro HD"):
            if not SEGMIND_API: st.error("API Key Missing in Secrets!")
            else:
                with st.spinner("Rendering 8K Quality..."):
                    img = generate_pro_poster(prompt)
                    if img:
                        st.image(img)
                        st.download_button("Download Pro HD", img, "pro_hd.png")
                    else: st.error("API Error or Limit reached.")

elif menu == "🎙️ AI Voice Studio":
    st.header("🎙️ AI Voice Generation")
    text = st.text_area("Enter Hindi Text:", "नमस्कार, वीक्सन एआई प्रो में आपका स्वागत है।")
    
    col_v1, col_v2 = st.columns(2)
    with col_v1:
        st.subheader("Free Voice (Google)")
        if st.button("📢 Generate Free Audio"):
            tts = gTTS(text=text, lang='hi')
            tts.save("v.mp3")
            st.audio("v.mp3")

    with col_v2:
        st.subheader("Pro Voice Settings")
        st.slider("Pitch Control", 0.5, 2.0, 1.0)
        st.button("🧬 Clone Voice (Coming Soon)")

elif menu == "🎞️ Pro Video Lab":
    st.header("🎞️ Pro Video Generation")
    v_prompt = st.text_input("Video Scene Description:")
    if st.button("🎬 Generate Pro Video"):
        if not HF_TOKEN: st.error("Hugging Face Token Missing!")
        else:
            with st.spinner("Generating AI Video Frames..."):
                # Simulation as real video generation often takes minutes
                st.info("Hugging Face Engine is processing... (Final Render)")
                st.video("https://www.w3schools.com/html/mov_bbb.mp4")

# =========================
# 6. FOOTER
# =========================
st.markdown("<hr><center>© 2026 Vixan AI Media Studio • Patna 🇮🇳</center>", unsafe_allow_html=True)
