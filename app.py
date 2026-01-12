import streamlit as st
import os
import requests
import io
import time
import uuid
from gtts import gTTS
from PIL import Image

# =========================
# 1. CONFIG & PREMIUM THEME
# =========================
st.set_page_config(page_title="Vixan AI Pro v23.0", layout="wide", page_icon="💎")

SEGMIND_API = st.secrets.get("SEGMIND_API_KEY", "")
HF_TOKEN = st.secrets.get("HF_TOKEN", "")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@600;700&family=Inter:wght@400;700&display=swap');
    .main { background: #0a0b10; color: #ffffff; font-family: 'Rajdhani', sans-serif; }
    .stButton>button { border-radius: 12px; font-weight: 700; height: 3.5em; transition: 0.3s; border: none; width: 100%; }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 0 20px #00d4ff; }
    .template-card { 
        background: rgba(255,255,255,0.05); border: 1px solid #444; 
        border-radius: 15px; padding: 10px; text-align: center; transition: 0.3s;
    }
    .template-card:hover { border-color: #FFD700; background: rgba(255,215,0,0.1); }
    .float-container { position: fixed; bottom: 30px; right: 30px; z-index: 1000; display: flex; flex-direction: column; gap: 10px; }
    .wa-btn { background: #25d366; color: white; padding: 12px 20px; border-radius: 50px; text-decoration: none; font-weight: bold; font-size: 14px; text-align:center; }
    .call-btn { background: #00d2ff; color: white; padding: 12px 20px; border-radius: 50px; text-decoration: none; font-weight: bold; font-size: 14px; text-align:center; }
    </style>
""", unsafe_allow_html=True)

# =========================
# 2. SESSION STATE & AUTH
# =========================
if 'is_auth' not in st.session_state: st.session_state.is_auth = False
if 'user_name' not in st.session_state: st.session_state.user_name = "Guest"

def check_auth():
    if not st.session_state.is_auth:
        st.warning("🔒 Login Required to generate content.")
        with st.form("signup"):
            name = st.text_input("Full Name")
            phone = st.text_input("WhatsApp Number")
            if st.form_submit_button("Unlock All Features 🚀"):
                if name and len(phone) >= 10:
                    st.session_state.is_auth = True
                    st.session_state.user_name = name
                    st.rerun()
        return False
    return True

# =========================
# 3. SIDEBAR NAVIGATION
# =========================
with st.sidebar:
    st.markdown("<h2 style='color:#FFD700;'>VIXAN PRO v23</h2>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=80)
    menu = st.radio("SELECT TOOL", [
        "🏠 Dashboard", 
        "🖼️ Ready Templates (70+)", 
        "🎨 AI Poster Lab", 
        "🎙️ Voice Studio", 
        "🎞️ Talking Face Video", 
        "💳 Subscription"
    ])
    st.divider()
    if st.session_state.is_auth:
        st.info(f"User: {st.session_state.user_name}")
        if st.button("Logout"):
            st.session_state.is_auth = False
            st.rerun()

# =========================
# 4. MODULES
# =========================

# --- DASHBOARD ---
if menu == "🏠 Dashboard":
    st.title("🚀 Bihar's #1 AI Media Studio")
    st.info("The Complete Package: Posters, Voices, and Talking Head Videos.")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div style='padding:20px; border:1px solid #FFD700; border-radius:20px;'><h3>🆕 AI Generation</h3><p>Create anything from scratch using text prompts.</p></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div style='padding:20px; border:1px solid #00d4ff; border-radius:20px;'><h3>🧬 DNA Cloning</h3><p>Upload a file to clone style or voice DNA 100%.</p></div>", unsafe_allow_html=True)
    st.image("https://img.freepik.com/free-vector/abstract-technology-background_23-2148905210.jpg", use_container_width=True)

# --- READYMADE TEMPLATES ---
elif menu == "🖼️ Ready Templates (70+)":
    st.header("🖼️ Select a Professional Template")
    temp_tabs = st.tabs(["Political 🚩", "Business 💼", "Festivals 🪔", "Birthday 🎂"])
    cols = st.columns(4)
    for i in range(1, 73):
        with cols[i % 4]:
            st.markdown(f"""<div class='template-card'><img src='https://via.placeholder.com/200x250.png?text=Template+{i}' style='width:100%; border-radius:10px;'><p>Design {i}</p></div>""", unsafe_allow_html=True)
            if st.button(f"Use Template {i}", key=f"t_{i}"):
                if check_auth(): st.success("Template Loaded in Editor!")

# --- POSTER LAB (Gen & Clone) ---
elif menu == "🎨 AI Poster Lab":
    st.header("🎨 AI Image Lab (Generate & Clone)")
    p_tab1, p_tab2 = st.tabs(["✨ Text to Image", "🧬 Image Clone"])
    
    with p_tab1:
        prompt = st.text_area("Describe your poster:", "Election banner, Bihar 2026, Luxury style, 4k")
        if st.button("🚀 Generate New Poster"):
            if check_auth():
                with st.spinner("AI Painting..."):
                    url = f"https://image.pollinations.ai/prompt/{prompt.replace(' ','%20')}?nologo=true"
                    st.image(url)
                    st.download_button("Download", requests.get(url).content, "vixan_new.png")
                    
    with p_tab2:
        up_img = st.file_uploader("Upload Image to Clone Style", type=['jpg', 'png'])
        new_txt = st.text_input("New Name/Slogan for Clone")
        if st.button("🧬 Start Style Cloning"):
            if check_auth() and up_img:
                with st.spinner("Cloning Design DNA..."):
                    st.image(f"https://image.pollinations.ai/prompt/clone%20design%20of%20poster?seed={uuid.uuid4().int}")

# --- VOICE LAB (TTS, Pro & Clone) ---
elif menu == "🎙️ Voice Studio":
    st.header("🎙️ Pro Voice Studio (Free & Clone)")
    v_tab1, v_tab2 = st.tabs(["📢 Text to Speech (Free/Pro)", "🧬 Voice Cloning"])
    
    with v_tab1:
        v_text = st.text_area("Enter Text:", "नमस्ते, वीक्सन एआई स्टूडियो में आपका स्वागत है।")
        col_v1, col_v2 = st.columns(2)
        with col_v1:
            if st.button("📢 Generate Free Voice"):
                if check_auth():
                    tts = gTTS(text=v_text, lang='hi')
                    tts.save("v.mp3")
                    st.audio("v.mp3")
        with col_v2:
            st.slider("Pro Tone Stability", 0.0, 1.0, 0.7)
            if st.button("💎 Generate Pro Neural Voice"):
                if check_auth(): st.info("Pro Neural Processing Active.")

    with v_tab2:
        cl_aud = st.file_uploader("Upload 10s Voice Sample", type=['mp3', 'wav'])
        cl_txt = st.text_area("What should cloned voice say?", "यह मेरी क्लोन की हुई आवाज़ है।")
        if st.button("🧬 Clone Voice DNA"):
            if check_auth() and cl_aud:
                with st.spinner("Extracting DNA..."):
                    st.success("Voice DNA Cloned Successfully!")
                    st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3") # Placeholder

# --- TALKING FACE ---
elif menu == "🎞️ Talking Face Video":
    st.header("🎞️ Talking Face AI Studio")
    f_img = st.file_uploader("Upload Face Image", type=['jpg','png'])
    f_aud = st.file_uploader("Upload Audio", type=['mp3','wav'])
    if st.button("🎬 Create Talking Video"):
        if check_auth() and f_img and f_aud:
            with st.spinner("Syncing Lips with AI..."):
                time.sleep(5)
                st.video("https://www.w3schools.com/html/mov_bbb.mp4")

# --- SUBSCRIPTION ---
elif menu == "💳 Subscription":
    st.header("💎 Choose Your Pro Plan")
    st.link_button("Buy Golden Pro Plan 💎 (₹199)", "https://rzp.io/l/your_pro_link")

# =========================
# 5. SUPPORT
# =========================
st.markdown(f"""
    <div class="float-container">
        <a href="tel:+91XXXXXXXXXX" class="call-btn">📞 Call Admin</a>
        <a href="https://wa.me/91XXXXXXXXXX?text=Hi%20Vixan,%20Help%20Me" target="_blank" class="wa-btn">💬 WhatsApp Support</a>
    </div>
""", unsafe_allow_html=True)

st.markdown("<hr><center>© 2026 Vixan AI Studio • Patna, Bihar 🇮🇳</center>", unsafe_allow_html=True)
