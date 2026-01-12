import streamlit as st
import os
import requests
import uuid
import io
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont

# =========================
# 1. INITIAL SETUP & THEME
# =========================
st.set_page_config(page_title="Vixan AI Pro v11.0", layout="wide", page_icon="🚀")

# Premium Neon Gradient Theme
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@500;700&display=swap');
    
    html, body, [class*="css"] { font-family: 'Rajdhani', sans-serif; }
    .main { background: linear-gradient(135deg, #020111 0%, #050625 100%); color: white; }
    
    /* Neon Glow Cards */
    .tool-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(0, 210, 255, 0.3);
        border-radius: 20px; padding: 20px; transition: 0.3s;
        text-align: center; box-shadow: 0 0 15px rgba(0, 210, 255, 0.1);
    }
    .tool-card:hover { transform: translateY(-5px); border-color: #00d2ff; box-shadow: 0 0 25px rgba(0, 210, 255, 0.3); }
    
    /* Premium Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%);
        color: white; border-radius: 12px; border: none; font-weight: bold;
        padding: 10px 25px; transition: 0.4s; width: 100%;
    }
    .stButton>button:hover { letter-spacing: 2px; box-shadow: 0 0 20px #00d2ff; }
    
    /* Support Floating Buttons */
    .support-float { position: fixed; bottom: 30px; left: 30px; z-index: 100; display: flex; flex-direction: column; gap: 15px; }
    </style>
    """, unsafe_allow_html=True)

# Session State for User Authentication
if 'is_authenticated' not in st.session_state:
    st.session_state.is_authenticated = False

# =========================
# 2. LOGIN MODAL FUNCTION
# =========================
def show_login_popup():
    st.warning("🔒 Action Required: Please Signup to continue.")
    with st.expander("📝 Sign Up / Login to Vixan AI", expanded=True):
        name = st.text_input("Enter Full Name")
        phone = st.text_input("Enter WhatsApp Number")
        if st.button("Unlock AI Features ✨"):
            if name and len(phone) >= 10:
                st.session_state.is_authenticated = True
                st.session_state.user_name = name
                st.success(f"Welcome {name}! Features Unlocked.")
                st.rerun()
            else:
                st.error("Please provide valid details.")

# =========================
# 3. SIDEBAR NAVIGATION
# =========================
with st.sidebar:
    st.markdown("<h2 style='color:#00d2ff;'>VIXAN STUDIO</h2>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=100)
    menu = st.radio("MAIN MENU", ["🏠 Home Dashboard", "🖼️ AI Poster Lab", "🎙️ Pro Voice Studio", "🎞️ Video Center", "ℹ️ About & Support"])
    st.divider()
    if st.session_state.is_authenticated:
        st.write(f"Logged in as: **{st.session_state.user_name}**")
        if st.button("Logout"):
            st.session_state.is_authenticated = False
            st.rerun()

# =========================
# 4. MODULES
# =========================

# --- HOME ---
if menu == "🏠 Home Dashboard":
    st.title("🚀 Bihar's Leading AI Media Engine")
    st.markdown("#### High-End Graphics & AI Voices for Leaders & Brands")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div class='tool-card'><h3>🖼️</h3><h4>Poster Lab</h4><p>HD AI Graphics in seconds</p></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='tool-card'><h3>🎙️</h3><h4>Voice Studio</h4><p>Professional Human-like AI</p></div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='tool-card'><h3>🎞️</h3><h4>Video Magic</h4><p>Talking Posters & Animation</p></div>", unsafe_allow_html=True)
    
    st.image("https://img.freepik.com/free-vector/abstract-technology-background_23-2148905210.jpg", use_container_width=True)

# --- POSTER LAB ---
elif menu == "🖼️ AI Poster Lab":
    st.header("🖼️ AI Poster Generation Lab")
    
    col_in, col_pre = st.columns([1, 1.2])
    with col_in:
        name = st.text_input("Leader/Brand Name", "आपका नाम यहाँ")
        slogan = st.text_input("Hindi Slogan", "नया बिहार, नई पहचान")
        font_dir = "fonts"
        fonts = [f for f in os.listdir(font_dir) if f.endswith(".ttf")] if os.path.exists(font_dir) else ["Default"]
        sel_font = st.selectbox("Select Premium Font", fonts)
        prompt = st.text_area("Background Style", "Professional political banner, orange and gold theme, 4k")
        
        # Generation Logic with Auth Check
        if st.button("🎨 Generate Design Now"):
            if not st.session_state.is_authenticated:
                show_login_popup()
            else:
                with st.spinner("AI Generating..."):
                    img_url = f"https://image.pollinations.ai/prompt/{prompt.replace(' ','%20')}?width=1024&height=1024&nologo=true"
                    img_data = requests.get(img_url).content
                    st.session_state.last_image = img_data
                    st.image(img_data, caption="Generated Preview", use_container_width=True)
                    st.download_button("📥 Download HD Poster", img_data, "vixan_poster.png")

# --- VOICE STUDIO ---
elif menu == "🎙️ Pro Voice Studio":
    st.header("🎙️ Advanced AI Voice Lab")
    text_in = st.text_area("Enter Text (Hindi/English)", "नमस्ते, वीक्सन डिजिटल स्टूडियो में आपका स्वागत है।")
    
    st.subheader("⚙️ Voice Tuning Settings")
    c1, c2, c3 = st.columns(3)
    with c1:
        v_speed = st.slider("Speech Rate (Speed)", 0.5, 2.0, 1.0)
    with c2:
        v_pitch = st.slider("Pitch Control", -10, 10, 0)
    with c3:
        v_stability = st.slider("Tone Stability", 0.0, 1.0, 0.7)

    if st.button("📢 Generate Professional Voice"):
        if not st.session_state.is_authenticated:
            show_login_popup()
        else:
            with st.spinner("Processing High Quality Voice..."):
                tts = gTTS(text=text_in, lang='hi', slow=(v_speed < 1.0))
                tts.save("voice_out.mp3")
                st.audio("voice_out.mp3")
                with open("voice_out.mp3", "rb") as f:
                    st.download_button("📥 Download MP3 Audio", f, "vixan_audio.mp3")

# --- VIDEO CENTER ---
elif menu == "🎞️ Video Center":
    st.header("🎞️ Talking Poster - Video Center")
    st.info("Coming Soon: AI Video Lip-Sync for Posters")
    st.video("https://www.w3schools.com/html/mov_bbb.mp4")

# =========================
# 5. FLOATING SUPPORT (Locked to User)
# =========================
st.markdown(f"""
    <div class="support-float">
        <a href="https://wa.me/91XXXXXXXXXX?text=VixanAI%20Support" target="_blank">
            <button style="background:#25d366; color:white; border-radius:30px; padding:12px; border:none; cursor:pointer; width:180px; font-weight:bold;">
                💬 WhatsApp Chat
            </button>
        </a>
        <a href="tel:+91XXXXXXXXXX">
            <button style="background:#00d2ff; color:white; border-radius:30px; padding:12px; border:none; cursor:pointer; width:180px; font-weight:bold;">
                📞 Call Developer
            </button>
        </a>
    </div>
    """, unsafe_allow_html=True)
