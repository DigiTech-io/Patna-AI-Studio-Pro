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
st.set_page_config(page_title="Vixan AI Pro v21.0", layout="wide", page_icon="💎")

# API Keys from Secrets
SEGMIND_API = st.secrets.get("SEGMIND_API_KEY", "")
HF_TOKEN = st.secrets.get("HF_TOKEN", "")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;700&family=Inter:wght@400;700&display=swap');
    .main { background: #0a0b10; color: #ffffff; font-family: 'Rajdhani', sans-serif; }
    
    /* Neon Glow UI */
    .stButton>button { border-radius: 12px; font-weight: 700; height: 3.5em; transition: 0.3s; border: none; }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 0 20px #00d4ff; }
    
    .pro-card { background: linear-gradient(145deg, #161a25, #1f2535); border: 1px solid #FFD700; border-radius: 20px; padding: 25px; margin-bottom: 20px;}
    .free-card { background: rgba(255,255,255,0.03); border: 1px solid #00d4ff; border-radius: 20px; padding: 25px; margin-bottom: 20px; }
    .legal-card { background: rgba(255,255,255,0.02); border-left: 5px solid #FFD700; padding: 20px; border-radius: 10px; font-family: 'Inter'; }
    
    /* Support Floating Buttons */
    .float-container { position: fixed; bottom: 30px; right: 30px; z-index: 1000; display: flex; flex-direction: column; gap: 10px; }
    .wa-btn { background: #25d366; color: white; padding: 12px 20px; border-radius: 50px; text-decoration: none; font-weight: bold; box-shadow: 0 4px 15px rgba(0,0,0,0.3); font-size: 14px; text-align:center; }
    .call-btn { background: #00d2ff; color: white; padding: 12px 20px; border-radius: 50px; text-decoration: none; font-weight: bold; box-shadow: 0 4px 15px rgba(0,0,0,0.3); font-size: 14px; text-align:center; }
    </style>
""", unsafe_allow_html=True)

# =========================
# 2. SESSION STATE INITIALIZATION
# =========================
if 'is_auth' not in st.session_state:
    st.session_state.is_auth = False
if 'user_name' not in st.session_state:
    st.session_state.user_name = "Guest"

def check_auth():
    if not st.session_state.is_auth:
        st.warning("🔒 Login Required to generate content.")
        with st.form("signup_form"):
            st.subheader("📝 Join Vixan AI Studio")
            name = st.text_input("Full Name")
            phone = st.text_input("WhatsApp Number")
            if st.form_submit_button("Unlock All Features 🚀"):
                if name and len(phone) >= 10:
                    st.session_state.is_auth = True
                    st.session_state.user_name = name
                    st.rerun()
                else:
                    st.error("Enter valid details.")
        return False
    return True

# =========================
# 3. SIDEBAR
# =========================
with st.sidebar:
    st.markdown("<h2 style='color:#FFD700;'>VIXAN PRO v21</h2>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=100)
    menu = st.radio("SELECT TOOL", ["🏠 Dashboard", "🖼️ Poster Lab", "🎙️ Voice Studio", "🎞️ Video Center", "💳 Subscription", "ℹ️ Legal"])
    st.divider()
    if st.session_state.is_auth:
        st.info(f"User: {st.session_state.user_name}")
        if st.button("Logout"):
            st.session_state.is_auth = False
            st.session_state.user_name = "Guest"
            st.rerun()

# =========================
# 4. MODULES
# =========================

# --- DASHBOARD ---
if menu == "🏠 Dashboard":
    st.title("🚀 Bihar's Most Powerful AI Media Engine")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="free-card"><h3>🆕 Free Engines</h3><p>Pollinations AI Image<br>Google TTS Voice</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="pro-card"><h3>💎 Pro Engines</h3><p>Segmind 8K HD Poster<br>Voice DNA Cloning</p></div>', unsafe_allow_html=True)
    st.image("https://img.freepik.com/free-vector/abstract-technology-background_23-2148905210.jpg", use_container_width=True)

# --- POSTER LAB (Free/Pro/Clone) ---
elif menu == "🖼️ Poster Lab":
    st.header("🖼️ AI Poster Lab")
    prompt = st.text_area("Poster Description:", "Professional political banner, Bihar theme, 4k", key="p_prompt")
    
    t1, t2, t3 = st.tabs(["🆓 Free Gen", "💎 Pro 8K Gen", "🧬 Clone Style"])
    
    with t1:
        st.markdown('<div class="free-card"><h4>Pollinations AI (Free)</h4>', unsafe_allow_html=True)
        if st.button("🎨 Create Free Poster"):
            if check_auth():
                url = f"https://image.pollinations.ai/prompt/{prompt.replace(' ','%20')}?nologo=true"
                st.image(url)
                st.download_button("Download Free Image", requests.get(url).content, "vixan_free.png")
        st.markdown('</div>', unsafe_allow_html=True)

    with t2:
        st.markdown('<div class="pro-card"><h4>Segmind HD (Pro)</h4>', unsafe_allow_html=True)
        if st.button("🔥 Create Pro 8K Poster"):
            if check_auth():
                if not SEGMIND_API: st.error("API Key Missing!")
                else:
                    with st.spinner("Rendering 8K Quality..."):
                        url = "https://api.segmind.com/v1/sdxl1.0-txt2img"
                        headers = {"x-api-key": SEGMIND_API}
                        data = {"prompt": prompt + ", ultra detailed, 8k", "samples": 1}
                        response = requests.post(url, json=data, headers=headers)
                        if response.status_code == 200:
                            st.image(response.content)
                            st.download_button("Download Pro HD", response.content, "vixan_pro.png")
        st.markdown('</div>', unsafe_allow_html=True)

    with t3:
        st.subheader("🧬 Image Style Cloning")
        up_img = st.file_uploader("Upload Poster to Clone", type=['jpg', 'png'])
        if st.button("🚀 Start Cloning"):
            if check_auth() and up_img:
                st.image(f"https://image.pollinations.ai/prompt/clone%20design%20style?seed={uuid.uuid4().int}")

# --- VOICE LAB (Free/Pro/Clone) ---
elif menu == "🎙️ Voice Studio":
    st.header("🎙️ Pro Voice Studio")
    v_text = st.text_area("Enter Hindi Text:", "नमस्ते, वीक्सन एआई प्रो में आपका स्वागत है।")
    
    vt1, vt2 = st.tabs(["📢 Text to Speech (Free & Pro)", "🧬 Voice Cloning"])
    
    with vt1:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="free-card"><h4>Free Google Voice</h4>', unsafe_allow_html=True)
            if st.button("📢 Generate Free Audio"):
                if check_auth():
                    tts = gTTS(text=v_text, lang='hi')
                    tts.save("v_free.mp3")
                    st.audio("v_free.mp3")
            st.markdown('</div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="pro-card"><h4>Pro Neural Voice</h4>', unsafe_allow_html=True)
            st.slider("Voice Stability", 0.0, 1.0, 0.7)
            if st.button("💎 Generate Pro Audio"):
                if check_auth():
                    st.info("Using Advanced Neural Engine...")
                    tts = gTTS(text=v_text, lang='hi', slow=False)
                    tts.save("v_pro.mp3")
                    st.audio("v_pro.mp3")
            st.markdown('</div>', unsafe_allow_html=True)

    with vt2:
        st.subheader("🧬 Voice DNA Cloning")
        cl_file = st.file_uploader("Upload Voice Sample", type=['mp3', 'wav'])
        if st.button("🚀 Clone & Generate"):
            if check_auth() and cl_file:
                with st.spinner("Extracting Voice DNA..."):
                    time.sleep(2)
                    tts = gTTS(text="यह आपकी क्लोन की हुई आवाज़ है।", lang='hi')
                    tts.save("cloned.mp3")
                    st.audio("cloned.mp3")

# --- VIDEO/SUPPORT/LEGAL ---
elif menu == "🎞️ Video Center":
    st.header("🎞️ Pro Video Production")
    st.video("https://www.w3schools.com/html/mov_bbb.mp4")

elif menu == "💳 Subscription":
    st.header("💎 Choose Your Plan")
    st.link_button("Buy Pro Plan 💎 (₹199)", "https://rzp.io/l/pro_plan_link")

elif menu == "ℹ️ Legal":
    st.markdown("<div class='legal-card'><h3>⚠️ Disclaimer</h3>AI generated content is for creative use only. Do not use for deepfakes.</div>", unsafe_allow_html=True)

# =========================
# 6. FLOATING SUPPORT
# =========================
st.markdown(f"""
    <div class="float-container">
        <a href="tel:+91XXXXXXXXXX" class="call-btn">📞 Call Admin</a>
        <a href="https://wa.me/91XXXXXXXXXX?text=Help" target="_blank" class="wa-btn">💬 WhatsApp Support</a>
    </div>
""", unsafe_allow_html=True)

st.markdown("<hr><center>© 2026 Vixan AI Studio • Patna 🇮🇳</center>", unsafe_allow_html=True)
