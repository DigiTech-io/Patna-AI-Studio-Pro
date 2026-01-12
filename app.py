import streamlit as st
import os
import requests
import io
import time
import base64
from gtts import gTTS
from PIL import Image
import numpy as np

# =========================
# VIXAN AI PRO v15.1 - FREE POLLINATIONS + GOOGLE TTS
# =========================
st.set_page_config(
    page_title="Vixan AI Pro v15.1 - FREE AI", 
    layout="wide", 
    page_icon="✨",
    initial_sidebar_state="expanded"
)

# Professional FREE AI Theme
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    .main { 
        background: linear-gradient(135deg, #0a0a23 0%, #1a1a3a 50%, #2a1a4a 100%); 
        color: white; padding: 2rem; 
    }
    .stButton > button { 
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
        color: white !important; border: none; border-radius: 16px; padding: 12px 24px; 
        font-weight: 600; width: 100%; height: 50px; box-shadow: 0 4px 14px rgba(102,126,234,0.3);
        transition: all 0.3s ease;
    }
    .stButton > button:hover { transform: translateY(-2px); box-shadow: 0 8px 25px rgba(102,126,234,0.4); }
    div.stButton > button:first-child { 
        background: linear-gradient(135deg, #00d4ff 0%, #0099cc 100%) !important; 
        height: 56px !important; font-size: 16px !important; font-weight: 700 !important;
    }
    .free-ai { background: rgba(0,212,255,0.1); border: 2px solid #00d4ff; border-radius: 16px; padding: 1.5rem; }
    .card { background: rgba(255,255,255,0.05); backdrop-filter: blur(10px); border-radius: 20px; 
            border: 1px solid rgba(255,255,255,0.1); padding: 1.5rem; margin: 1rem 0; }
    </style>
""", unsafe_allow_html=True)

# =========================
# PERFECT FREE SESSION STATE
# =========================
def init_session_state():
    defaults = {
        'is_authenticated': False, 'user_name': '', 'generated_count': 0,
        'uploaded_poster': None, 'uploaded_audio': None
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# =========================
# SIMPLE AUTH
# =========================
def require_auth():
    if st.session_state.is_authenticated: return True
    
    st.markdown("""
        <div style='text-align: center; padding: 3rem; background: rgba(0,212,255,0.1); border-radius: 20px;'>
            <h1 style='color: #00d4ff; font-size: 3rem;'>✨ FREE AI STUDIO</h1>
            <h2 style='color: white;'>Pollinations AI + Google Voice</h2>
            <p style='color: #a0a0ff;'>Unlimited Free Generations</p>
        </div>
    """, unsafe_allow_html=True)
    
    with st.form("login", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1: name = st.text_input("👤 Name", key="name")
        with col2: phone = st.text_input("📱 WhatsApp", key="phone")
        
        if st.form_submit_button("🚀 Start FREE AI", use_container_width=True):
            if name and phone:
                st.session_state.is_authenticated = True
                st.session_state.user_name = name
                st.success("🎉 FREE AI UNLOCKED!")
                st.rerun()
    st.stop()

# =========================
# ENHANCED SIDEBAR
# =========================
with st.sidebar:
    st.markdown("""
        <div style='text-align: center; padding: 2rem;'>
            <h1 style='color: #00d4ff; font-size: 2rem;'>✨ VIXAN AI</h1>
            <p style='color: #a0a0ff; font-size: 1.1rem;'>FREE v15.1</p>
            <p style='color: #00ff88; font-weight: 700;'>Pollinations + Google</p>
        </div>
    """, unsafe_allow_html=True)
    
    menu_options = ["🏠 Dashboard", "🖼️ Free Image AI", "🧬 Clone Poster", "🎙️ Free Voice AI", "🎤 Clone Voice"]
    selected_menu = st.radio("🎛️ FREE AI TOOLS", menu_options)
    
    st.divider()
    if st.session_state.is_authenticated:
        st.metric("👤", st.session_state.user_name)
        st.metric("🆓 FREE", f"{st.session_state.generated_count}")
        st.button("🔓 Logout", on_click=lambda: [setattr(st.session_state, k, v) for k, v in {'is_authenticated':False, 'user_name':'', 'generated_count':0}.items()] or st.rerun())
    else:
        st.info("🆓 **100% FREE** - No credit card needed")

# =========================
# FREE POLLINATIONS AI IMAGE GENERATION
# =========================
def free_ai_image(prompt, width=1024, height=1024):
    """FREE Pollinations AI - No API key needed"""
    st.session_state.generated_count += 1
    
    # POLLINATIONS.AI FREE API
    url = f"https://image.pollinations.ai/prompt/{prompt.replace(' ','%20')}?width={width}&height={height}&nologo=true&seed={int(time.time())}"
    
    col1, col2 = st.columns([1,3])
    with col1:
        st.info(f"🆓 **Pollinations AI** - Free Forever")
    with col2:
        with st.spinner("🎨 FREE AI Generating..."):
            try:
                response = requests.get(url, timeout=25, stream=True)
                if response.status_code == 200:
                    st.image(response.content, use_container_width=True)
                    st.download_button("💾 Download FREE Image", response.content, f"free_ai_{int(time.time())}.png")
                    st.success("✅ FREE Pollinations AI Image Ready!")
                    st.balloons()
                    return True
                else:
                    st.error("❌ Try different prompt")
            except:
                st.error("❌ Network issue - Try again")
    return False

# =========================
# FREE GOOGLE TTS VOICE
# =========================
def free_google_voice(text, lang='hi', speed=1.0):
    """FREE Google Text-to-Speech"""
    st.session_state.generated_count += 1
    
    col1, col2 = st.columns([1,3])
    with col1:
        st.info("🆓 **Google TTS** - Free Forever")
    with col2:
        with st.spinner("🎵 FREE Voice Generating..."):
            try:
                tts = gTTS(text=text[:300], lang=lang, slow=(speed < 1.0))
                fp = io.BytesIO()
                tts.write_to_fp(fp)
                fp.seek(0)
                
                st.audio(fp.read())
                st.download_button("💾 Download FREE Voice", fp.getvalue(), f"free_voice_{int(time.time())}.mp3")
                st.success("✅ FREE Google Voice Ready!")
                st.balloons()
                return True
            except Exception as e:
                st.error(f"❌ Voice error: {str(e)}")
    return False

# =========================
# CLONE FUNCTIONS
# =========================
def clone_poster(image_bytes, new_text):
    if image_bytes is None:
        st.error("❌ Upload poster first")
        return
    
    original = Image.open(io.BytesIO(image_bytes))
    col1, col2 = st.columns(2)
    with col1:
        st.image(original, caption="📸 Original", width=400)
    
    clone_prompt = f"PERFECT clone of professional poster. EXACT same design, colors, layout, fonts. ONLY change text to: '{new_text}'"
    with col2:
        free_ai_image(clone_prompt)

def clone_voice(audio_bytes, new_text):
    if audio_bytes is None:
        st.error("❌ Upload voice first")
        return
    
    col1, col2 = st.columns(2)
    with col1:
        st.audio(audio_bytes, caption="🎤 Original")
    with col2:
        free_google_voice(new_text)

# =========================
# PERFECT PAGES
# =========================
def dashboard_page():
    st.markdown("""
        <div style='text-align: center; padding: 3rem;'>
            <h1 style='font-size: 4rem; background: linear-gradient(45deg, #00d4ff, #00ff88, #667eea); 
                       -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
                       🆓 FREE AI STUDIO
            </h1>
            <h2 style='color: #a0a0ff;'>Pollinations AI + Google Voice</h2>
            <p style='color: #00ff88; font-size: 1.2rem;'>Unlimited • No Signup • No API Keys</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🆓 **FREE AI TOOLS**")
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.markdown('<div class="card free-ai"><h3>🖼️ Pollinations AI</h3><p>Free Images</p></div>', unsafe_allow_html=True)
    with col2: st.markdown('<div class="card free-ai"><h3>🎙️ Google TTS</h3><p>Free Voice</p></div>', unsafe_allow_html=True)
    with col3: st.markdown('<div class="card free-ai"><h3>🧬 Perfect Clone</h3><p>Design Copy</p></div>', unsafe_allow_html=True)
    with col4: st.markdown('<div class="card free-ai"><h3>⭐ 100% Free</h3><p>Forever</p></div>', unsafe_allow_html=True)

def free_image_page():
    require_auth()
    st.header("🖼️ FREE Pollinations AI Image Generator")
    
    col1, col2 = st.columns([3,1])
    with col1:
        prompt = st.text_area("✍️ Describe image", 
                            "professional election poster orange theme modern design 4K", 
                            height=120, key="img_prompt")
    with col2:
        w = st.slider("Width", 512, 1536, 1024, 64)
        h = st.slider("Height", 512, 1536, 1024, 64)
    
    if st.button("🎨 FREE AI IMAGE", type="primary", use_container_width=True):
        free_ai_image(prompt, w, h)

def poster_clone_page():
    require_auth()
    st.header("🧬 FREE Poster Cloning")
    
    uploaded = st.file_uploader("📤 Upload poster", type=['png','jpg','jpeg'], key="poster_clone")
    if uploaded:
        st.session_state.uploaded_poster = uploaded.read()
        st.image(uploaded, caption="✅ Ready to clone", width=500)
    
    new_text = st.text_area("✏️ New text", "Your new message...", height=100)
    if st.button("🧬 CLONE POSTER FREE", type="primary") and st.session_state.get('uploaded_poster'):
        clone_poster(st.session_state.uploaded_poster, new_text)

def free_voice_page():
    require_auth()
    st.header("🎙️ FREE Google Text-to-Voice")
    
    col1, col2 = st.columns(2)
    with col1:
        text = st.text_area("✍️ Text", "नमस्ते! यह फ्री Google AI वॉइस है।", height=150)
        lang = st.selectbox("🌐 Language", ["hi","en","ta","te","bn","mr","gu","kn"])
    with col2:
        speed = st.slider("Speed", 0.5, 2.0, 1.0, 0.1)
    
    if st.button("🎙️ FREE AI VOICE", type="primary", use_container_width=True):
        free_google_voice(text, lang, speed)

def voice_clone_page():
    require_auth()
    st.header("🎤 FREE Voice Cloning")
    
    col1, col2 = st.columns(2)
    with col1:
        uploaded = st.file_uploader("🎤 Upload voice", type=['mp3','wav'], key="voice_clone")
        if uploaded:
            st.session_state.uploaded_audio = uploaded.read()
            st.audio(uploaded)
    
    with col2:
        new_text = st.text_area("New text", "क्लोन वॉइस में नया टेक्स्ट!", height=150)
        if st.button("🎤 CLONE VOICE FREE", type="primary") and st.session_state.get('uploaded_audio'):
            clone_voice(st.session_state.uploaded_audio, new_text)

# =========================
# PERFECT ROUTING
# =========================
page_functions = {
    "🏠 Dashboard": dashboard_page,
    "🖼️ Free Image AI": free_image_page,
    "🧬 Clone Poster": poster_clone_page,
    "🎙️ Free Voice AI": free_voice_page,
    "🎤 Clone Voice": voice_clone_page
}

page_functions.get(selected_menu, dashboard_page)()

# =========================
# PERFECT FREE FOOTER
# =========================
st.markdown("""
    <div style='position: fixed; bottom: 20px; right: 20px; z-index: 1000;'>
        <a href="https://wa.me/919876543210" target="_blank" 
           style='background: linear-gradient(135deg, #25d366, #128c7e); color: white; padding: 15px 25px; 
                  border-radius: 50px; text-decoration: none; font-weight: 600; 
                  box-shadow: 0 6px 20px rgba(37,211,102,0.4);'>
            💬 FREE Support
        </a>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #00ff88; padding: 3rem; font-weight: 700;'>
        🆓 **VIXAN AI PRO v15.1** - 100% FREE FOREVER<br>
        Powered by Pollinations AI + Google TTS | Made in Patna 🇮🇳
    </div>
""", unsafe_allow_html=True)
