import streamlit as st
import os
import requests
import io
import time
from gtts import gTTS
from PIL import Image
import base64

# =========================
# 1. FIXED THEME & APP CONFIG v14.1 - ERROR FREE
# =========================
st.set_page_config(
    page_title="Vixan AI Pro v14.1", 
    layout="wide", 
    page_icon="✨",
    initial_sidebar_state="expanded"
)

# FIXED CSS - No complex selectors that break
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Safe Global Styles */
    .main { 
        background: linear-gradient(135deg, #0a0a23 0%, #1a1a3a 50%, #2a1a4a 100%);
        padding: 2rem;
        color: white;
    }
    
    /* Fixed Button Styles */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        border: none;
        border-radius: 16px;
        padding: 12px 24px;
        font-weight: 600;
        font-size: 14px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 14px rgba(102, 126, 234, 0.3);
        width: 100%;
        height: 48px;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }
    
    /* Primary Button */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #00d4ff 0%, #0099cc 100%) !important;
        box-shadow: 0 6px 20px rgba(0, 212, 255, 0.4) !important;
        height: 56px !important;
        font-size: 16px !important;
    }
    
    /* Card Style */
    .card {
        background: rgba(255,255,255,0.05);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(255,255,255,0.1);
        padding: 2rem;
        margin: 1rem 0;
    }
    
    /* Floating Support */
    .float-container {
        position: fixed;
        bottom: 30px;
        right: 30px;
        z-index: 1000;
    }
    
    .float-btn {
        background: linear-gradient(135deg, #25d366 0%, #128c7e 100%);
        color: white;
        border-radius: 50px;
        padding: 15px 20px;
        margin: 10px 0;
        box-shadow: 0 8px 25px rgba(37, 211, 102, 0.4);
        text-decoration: none;
        display: block;
        text-align: center;
        transition: all 0.3s ease;
    }
    </style>
""", unsafe_allow_html=True)

# =========================
# 2. FIXED SESSION STATE - NO KeyError
# =========================
def init_session_state():
    """Initialize all session state variables safely"""
    defaults = {
        'is_authenticated': False,
        'user_name': '',
        'generated_count': 0,
        'current_page': 'dashboard',
        'poster_prompt': '',
        'voice_text': ''
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# =========================
# 3. FIXED AUTH SYSTEM
# =========================
def show_login_overlay():
    """Safe login overlay without breaking layout"""
    if st.session_state.is_authenticated:
        return True
    
    st.markdown("## 🔐 Welcome to Vixan AI Pro v14.1")
    st.markdown("### Please Login to Unlock All Features")
    
    with st.form("login_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("👤 Full Name", key="input_name")
        with col2:
            phone = st.text_input("📱 WhatsApp Number", placeholder="10 digits", key="input_phone")
        
        submit = st.form_submit_button("🚀 Unlock Premium Features", use_container_width=True)
        
        if submit:
            if name.strip() and len(phone.strip()) >= 10 and phone.strip().isdigit():
                st.session_state.is_authenticated = True
                st.session_state.user_name = name.strip()
                st.success(f"🎉 Welcome {name}! All features unlocked!")
                st.balloons()
                time.sleep(1)
                st.rerun()
            else:
                st.error("❌ Please enter valid name & 10-digit phone number")
    
    st.stop()

# =========================
# 4. FIXED SIDEBAR
# =========================
with st.sidebar:
    st.markdown("""
        <div style='text-align: center; padding: 2rem 1rem;'>
            <h1 style='color: #00d4ff; font-size: 2rem; margin: 0;'>✨ VIXAN AI</h1>
            <p style='color: #a0a0ff; font-size: 0.9rem;'>Pro v14.1 Studio</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Safe menu selection
    menu_options = ["🏠 Dashboard", "🖼️ Poster Lab", "🎙️ Voice Studio", "🎞️ Video Center"]
    selected_menu = st.radio("🎛️ Quick Navigation", menu_options, index=0)
    
    st.divider()
    
    if st.session_state.is_authenticated:
        st.metric("👤 User", st.session_state.user_name)
        st.metric("✨ Generations", st.session_state.generated_count)
        if st.button("🔓 Logout", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    else:
        st.info("🔐 Login required for premium features")

# =========================
# 5. SAFE PAGE FUNCTIONS
# =========================
def dashboard_page():
    st.title("🚀 Vixan AI Master Studio v14.1")
    st.markdown("**The Ultimate AI Media Creation Suite**")
    
    # Stats cards - SAFE HTML
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="card"><h3 style="color: #00d4ff;">🖼️ 10K+</h3><p>Posters</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="card"><h3 style="color: #00c851;">🎙️ 5K+</h3><p>Voices</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="card"><h3 style="color: #ff6b6b;">🎞️ 2K+</h3><p>Videos</p></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="card"><h3 style="color: #ffd93d;">⭐ 4.9</h3><p>Rating</p></div>', unsafe_allow_html=True)
    
    # Quick actions
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🖼️ Quick Poster"):
            st.session_state.current_page = 'poster'
            st.rerun()
    with col2:
        if st.button("🎙️ Quick Voice"):
            st.session_state.current_page = 'voice'
            st.rerun()
    with col3:
        if st.button("🎞️ Video Demo"):
            st.session_state.current_page = 'video'
            st.rerun()

def poster_lab_page():
    if not st.session_state.is_authenticated:
        show_login_overlay()
    
    st.header("🖼️ AI Poster Lab Pro")
    tab1, tab2 = st.tabs(["✨ Text-to-Poster", "🧬 Clone"])
    
    with tab1:
        prompt = st.text_area("📝 Describe your poster", 
                            "professional political banner, orange theme, 4K", 
                            height=100)
        
        col1, col2 = st.columns([3,1])
        with col1:
            if st.button("🚀 Generate Poster", type="primary"):
                generate_poster(prompt)
        with col2:
            st.info("💡 Try political campaign posters!")
    
    with tab2:
        uploaded = st.file_uploader("📤 Upload to clone", type=['jpg','png'])
        if uploaded and st.button("🧬 Clone Design", type="primary"):
            generate_poster("professional clone of uploaded design")

def generate_poster(prompt):
    """Safe poster generation"""
    st.session_state.generated_count += 1
    
    with st.spinner("🎨 AI Generating..."):
        try:
            url = f"https://image.pollinations.ai/prompt/{prompt.replace(' ','%20')}?width=1024&height=1024&nologo=true"
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                st.image(response.content, use_container_width=True)
                st.download_button("💾 Download", response.content, "vixan_poster.png")
                st.success("✅ Poster ready!")
                st.balloons()
            else:
                st.error("❌ Try different prompt")
        except:
            st.error("❌ Network error. Try again.")

def voice_studio_page():
    if not st.session_state.is_authenticated:
        show_login_overlay()
    
    st.header("🎙️ AI Voice Studio Pro")
    
    text = st.text_area("✍️ Text to speak", 
                       "नमस्ते! वीक्सन एआई स्टूडियो में आपका स्वागत है।",
                       height=120)
    
    col1, col2 = st.columns(2)
    with col1:
        lang = st.selectbox("🌐 Language", ["hi", "en"])
    with col2:
        speed = st.slider("Speed", 0.5, 2.0, 1.0)
    
    if st.button("🎙️ Generate Voice", type="primary"):
        generate_voice(text, lang, speed)

def generate_voice(text, lang, speed):
    """Safe voice generation"""
    st.session_state.generated_count += 1
    
    with st.spinner("🎵 Creating voice..."):
        try:
            tts = gTTS(text=text[:300], lang=lang, slow=(speed < 1.0))
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            
            st.audio(fp.read())
            st.download_button("💾 Download MP3", fp.getvalue(), "vixan_voice.mp3")
            st.success("✅ Voice ready!")
        except Exception as e:
            st.error(f"❌ Voice error: {str(e)}")

def video_center_page():
    st.header("🎞️ AI Video Center")
    st.warning("🎬 Video generation coming in v14.2!")
    st.video("https://sample-videos.com/zip/10/mp4/SampleVideo_1280x720_1mb.mp4")

# =========================
# 6. FIXED MAIN ROUTING - NO KeyError
# =========================
page_functions = {
    "🏠 Dashboard": dashboard_page,
    "🖼️ Poster Lab": poster_lab_page,
    "🎙️ Voice Studio": voice_studio_page,
    "🎞️ Video Center": video_center_page
}

# Safe page rendering
if selected_menu in page_functions:
    page_functions[selected_menu]()
else:
    dashboard_page()  # Fallback

# =========================
# 7. SAFE FLOATING SUPPORT
# =========================
st.markdown("""
    <div class="float-container">
        <a href="https://wa.me/919876543210" class="float-btn">💬 WhatsApp Support</a>
    </div>
""", unsafe_allow_html=True)

# Safe footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #a0a0ff; padding: 2rem;'>
        ✨ **Vixan AI Pro v14.1** | Made in Patna, Bihar 🇮🇳 | © 2026
    </div>
""", unsafe_allow_html=True)
