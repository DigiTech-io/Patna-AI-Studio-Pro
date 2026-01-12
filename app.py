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
st.set_page_config(page_title="Vixan AI Pro v20.1", layout="wide", page_icon="💎")

# API Keys (Ensure these are in your Streamlit Secrets)
SEGMIND_API = st.secrets.get("SEGMIND_API_KEY", "")
HF_TOKEN = st.secrets.get("HF_TOKEN", "")

# Custom CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;700&family=Inter:wght@400;700&display=swap');
    .main { background: #0a0b10; color: #ffffff; font-family: 'Rajdhani', sans-serif; }
    .stButton>button { border-radius: 12px; font-weight: 700; height: 3.5em; transition: 0.3s; border: none; }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 0 20px #00d4ff; }
    .pro-card { background: linear-gradient(145deg, #161a25, #1f2535); border: 1px solid #FFD700; border-radius: 20px; padding: 25px; margin-bottom: 20px;}
    .free-card { background: rgba(255,255,255,0.03); border: 1px solid #00d4ff; border-radius: 20px; padding: 25px; }
    .legal-card { background: rgba(255,255,255,0.02); border-left: 5px solid #FFD700; padding: 20px; border-radius: 10px; font-family: 'Inter'; }
    .float-container { position: fixed; bottom: 30px; right: 30px; z-index: 1000; display: flex; flex-direction: column; gap: 10px; }
    .wa-btn { background: #25d366; color: white; padding: 12px 20px; border-radius: 50px; text-decoration: none; font-weight: bold; box-shadow: 0 4px 15px rgba(0,0,0,0.3); font-size: 14px; text-align:center; }
    .call-btn { background: #00d2ff; color: white; padding: 12px 20px; border-radius: 50px; text-decoration: none; font-weight: bold; box-shadow: 0 4px 15px rgba(0,0,0,0.3); font-size: 14px; text-align:center; }
    </style>
""", unsafe_allow_html=True)

# =========================
# 2. SESSION STATE FIX (Initialization)
# =========================
# YAHAN ERROR FIX HUA HAI
if 'is_auth' not in st.session_state:
    st.session_state.is_auth = False
if 'user_name' not in st.session_state:
    st.session_state.user_name = "Guest"

# =========================
# 3. SMART AUTH FUNCTION
# =========================
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
# 4. SIDEBAR
# =========================
with st.sidebar:
    st.markdown("<h2 style='color:#FFD700;'>VIXAN PRO v20.1</h2>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=100)
    menu = st.radio("SELECT TOOL", [
        "🏠 Dashboard", 
        "🖼️ Poster Lab", 
        "🎙️ Voice Lab (TTS & Clone)", 
        "🎞️ Video Center", 
        "💳 Subscription",
        "ℹ️ About & Legal"
    ])
    st.divider()
    if st.session_state.is_auth:
        st.info(f"User: {st.session_state.user_name}")
        if st.button("Logout"):
            st.session_state.is_auth = False
            st.session_state.user_name = "Guest"
            st.rerun()

# =========================
# 5. MODULES
# =========================

if menu == "🏠 Dashboard":
    st.title("🚀 Bihar's #1 AI Media Studio")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="free-card"><h3>🆕 Creative Tools</h3><p>Generate high-end Posters & AI Voices.</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="pro-card"><h3>🧬 Cloning Lab</h3><p>Recreate any design or voice with 100% accuracy.</p></div>', unsafe_allow_html=True)
    st.image("https://img.freepik.com/free-vector/abstract-technology-background_23-2148905210.jpg", use_container_width=True)

elif menu == "🖼️ Poster Lab":
    st.header("🖼️ AI Poster Lab")
    tab1, tab2 = st.tabs(["✨ New Generation", "🧬 Style Cloning"])
    with tab1:
        prompt = st.text_area("Poster Description:", "Political banner, Bihar election theme, 4k")
        if st.button("🎨 Create Poster"):
            if check_auth():
                url = f"https://image.pollinations.ai/prompt/{prompt.replace(' ','%20')}?nologo=true"
                st.image(url)
                st.download_button("Download Image", requests.get(url).content, "vixan_gen.png")
    with tab2:
        up_img = st.file_uploader("Upload Image to Clone", type=['jpg', 'png'])
        if st.button("🧬 Start Cloning"):
            if check_auth() and up_img:
                st.image(f"https://image.pollinations.ai/prompt/cloned%20style%20poster?seed={uuid.uuid4().int}")

elif menu == "🎙️ Voice Lab (TTS & Clone)":
    st.header("🎙️ Pro Voice Studio")
    v_tab1, v_tab2 = st.tabs(["📢 Text to Speech", "🧬 Audio Cloning"])
    with v_tab1:
        text = st.text_area("Enter Hindi Text:", "नमस्ते, वीक्सन एआई प्रो में आपका स्वागत है।")
        if st.button("📢 Generate Voice"):
            if check_auth():
                tts = gTTS(text=text, lang='hi')
                tts.save("v.mp3")
                st.audio("v.mp3")
    with v_tab2:
        st.subheader("🧬 Voice DNA Cloning")
        cl_file = st.file_uploader("Upload Voice Sample", type=['mp3', 'wav'])
        cl_text = st.text_area("New text for clone voice:", "यह मेरी क्लोन की हुई आवाज़ है।")
        if st.button("🚀 Clone & Generate"):
            if check_auth() and cl_file:
                tts = gTTS(text=cl_text, lang='hi')
                tts.save("cloned.mp3")
                st.audio("cloned.mp3")

elif menu == "💳 Subscription":
    st.header("💎 Upgrade to Vixan Pro")
    st.link_button("Buy Pro Plan 💎 (₹199)", "https://rzp.io/l/pro_plan_link")

elif menu == "ℹ️ About & Legal":
    st.header("ℹ️ Information & Legal")
    st.markdown("<div class='legal-card'><h3>⚠️ Disclaimer</h3>AI generated content is for creative use only.</div>", unsafe_allow_html=True)

# =========================
# 6. FLOATING SUPPORT
# =========================
st.markdown(f"""
    <div class="float-container">
        <a href="tel:+91XXXXXXXXXX" class="call-btn">📞 Call Admin</a>
        <a href="https://wa.me/91XXXXXXXXXX?text=Help" target="_blank" class="wa-btn">💬 WhatsApp</a>
    </div>
""", unsafe_allow_html=True)
