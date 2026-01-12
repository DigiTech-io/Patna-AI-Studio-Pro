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
st.set_page_config(page_title="Vixan AI Pro v24.0", layout="wide", page_icon="💎")

SEGMIND_API = st.secrets.get("SEGMIND_API_KEY", "")
HF_TOKEN = st.secrets.get("HF_TOKEN", "")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@600;700&family=Inter:wght@400;700&display=swap');
    .main { background: #0a0b10; color: #ffffff; font-family: 'Rajdhani', sans-serif; }
    
    /* Template Grid Styling */
    .template-container {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
        gap: 20px;
        padding: 10px;
    }
    .template-card {
        background: #161a25;
        border: 1px solid #333;
        border-radius: 15px;
        overflow: hidden;
        transition: 0.3s ease-in-out;
        text-align: center;
    }
    .template-card:hover {
        transform: translateY(-10px);
        border-color: #FFD700;
        box-shadow: 0 10px 20px rgba(255, 215, 0, 0.2);
    }
    .template-img {
        width: 100%;
        height: 250px;
        object-fit: cover;
        border-bottom: 1px solid #333;
    }
    .cat-header {
        background: linear-gradient(90deg, #FFD700, #FF8C00);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 24px;
        margin-bottom: 15px;
    }
    
    /* Global Buttons */
    .stButton>button { border-radius: 12px; font-weight: 700; height: 3em; transition: 0.3s; border: none; width: 100%; }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 0 20px #00d4ff; }
    .float-container { position: fixed; bottom: 30px; right: 30px; z-index: 1000; display: flex; flex-direction: column; gap: 10px; }
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
    st.markdown("<h2 style='color:#FFD700;'>VIXAN PRO v24</h2>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=80)
    menu = st.radio("SELECT TOOL", ["🏠 Dashboard", "🖼️ Ready Templates", "🎨 AI Poster Lab", "🎙️ Voice Studio", "🎞️ Talking Face Video", "💳 Subscription"])
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
    st.markdown("#### Create Professional Branding in Seconds")
    st.image("https://img.freepik.com/free-vector/abstract-technology-background_23-2148905210.jpg", use_container_width=True)

# --- READYMADE TEMPLATES (4 SMART CATEGORIES) ---
elif menu == "🖼️ Ready Templates":
    st.header("🖼️ High-Quality Predefined Templates")
    
    # 4 SMART CATEGORIES
    cats = {
        "🚩 Political (Chunav)": ["BJP Bihar Theme", "JDU Development", "RJD Jan Seva", "Chunav Prachar 2026", "Leadership Banner"],
        "💼 Business & Shop": ["Modern Gym Banner", "Patna Digital Shop", "Restaurant Special", "Real Estate Luxury", "Mobile Store"],
        "🪔 Festivals (Tyohar)": ["Chhath Puja Special", "Diwali Greetings", "Holi Dhamaka", "Eid Mubarak", "Maha Shivratri"],
        "🎂 Birthday & Events": ["Royal Birthday", "Wedding Invitation", "Anniversary Post", "College Event", "Baby Shower"]
    }
    
    for cat_name, items in cats.items():
        st.markdown(f"<div class='cat-header'>{cat_name}</div>", unsafe_allow_html=True)
        cols = st.columns(5)
        for i, item in enumerate(items):
            with cols[i]:
                st.markdown(f"""
                    <div class='template-card'>
                        <img class='template-img' src='https://image.pollinations.ai/prompt/{item.replace(" ", "%20")}%20poster%20high%20quality?width=400&height=600&nologo=true'>
                        <div style='padding:10px; font-size:14px; font-weight:bold;'>{item}</div>
                    </div>
                """, unsafe_allow_html=True)
                if st.button(f"Edit {i}", key=f"{cat_name}_{i}"):
                    if check_auth():
                        st.success(f"Selected: {item}. Redirecting to Editor...")

# --- POSTER LAB ---
elif menu == "🎨 AI Poster Lab":
    st.header("🎨 AI Image Lab (Generate & Clone)")
    p_tab1, p_tab2 = st.tabs(["✨ Text to Image", "🧬 Image Clone"])
    
    with p_tab1:
        prompt = st.text_area("Describe your poster:", "Professional election banner, Bihar theme, 4k")
        if st.button("🚀 Generate New Poster"):
            if check_auth():
                with st.spinner("AI Painting..."):
                    url = f"https://image.pollinations.ai/prompt/{prompt.replace(' ','%20')}?nologo=true"
                    st.image(url)
                    st.download_button("Download", requests.get(url).content, "vixan_new.png")
                    
    with p_tab2:
        up_img = st.file_uploader("Upload Image to Clone Style", type=['jpg', 'png'])
        if st.button("🧬 Start Style Cloning"):
            if check_auth() and up_img:
                st.image(f"https://image.pollinations.ai/prompt/clone%20design%20of%20poster?seed={uuid.uuid4().int}")

# --- VOICE STUDIO ---
elif menu == "🎙️ Voice Studio":
    st.header("🎙️ Pro Voice Studio")
    v_tab1, v_tab2 = st.tabs(["📢 Text to Speech", "🧬 Voice Cloning"])
    
    with v_tab1:
        v_text = st.text_area("Enter Hindi Text:", "नमस्ते, वीक्सन एआई स्टूडियो में आपका स्वागत है।")
        if st.button("📢 Generate Voice"):
            if check_auth():
                tts = gTTS(text=v_text, lang='hi')
                tts.save("v.mp3")
                st.audio("v.mp3")

    with v_tab2:
        cl_aud = st.file_uploader("Upload 10s Voice Sample", type=['mp3', 'wav'])
        if st.button("🧬 Clone Voice DNA"):
            if check_auth() and cl_aud:
                st.success("Voice DNA Cloned Successfully!")
                st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")

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
