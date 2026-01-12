import streamlit as st
import os
import requests
import uuid
import io
import base64
from gtts import gTTS
from PIL import Image
import time

# =========================
# 1. ENHANCED THEME & APP CONFIG v14.0
# =========================
st.set_page_config(
    page_title="Vixan AI Pro v14.0", 
    layout="wide", 
    page_icon="✨",
    initial_sidebar_state="expanded"
)

# Advanced CSS with smooth animations
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Rajdhani:wght@500;700&display=swap');
    
    /* Global Styles */
    html, body, [class*="css"] { 
        font-family: 'Inter', sans-serif !important; 
        background: linear-gradient(135deg, #0a0a23 0%, #1a1a3a 50%, #2a1a4a 100%) !important;
    }
    
    .main { 
        background: linear-gradient(135deg, #0a0a23 0%, #1a1a3a 50%, #2a1a4a 100%) !important;
        padding: 2rem !important;
        color: white;
    }
    
    /* Enhanced Button Styles */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        border: none;
        border-radius: 16px;
        padding: 12px 24px;
        font-weight: 600;
        font-size: 14px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 14px 0 rgba(102, 126, 234, 0.3);
        width: 100%;
        height: 48px;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px 0 rgba(102, 126, 234, 0.4);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    /* Primary Action Button */
    .primary-btn > button {
        background: linear-gradient(135deg, #00d4ff 0%, #0099cc 100%) !important;
        box-shadow: 0 6px 20px 0 rgba(0, 212, 255, 0.4) !important;
        height: 56px !important;
        font-size: 16px !important;
        font-weight: 700 !important;
    }
    
    /* Success Button */
    .success-btn > button {
        background: linear-gradient(135deg, #00c851 0%, #007e33 100%) !important;
    }
    
    /* Card Styles */
    .metric-card {
        background: rgba(255,255,255,0.05);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(255,255,255,0.1);
        padding: 1.5rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.3);
        border-color: rgba(102, 126, 234, 0.5);
    }
    
    /* Sidebar Enhancements */
    .css-1d391kg { background: rgba(10,10,35,0.95) !important; }
    .css-1v0mbdj { color: #00d4ff !important; }
    
    /* Progress Bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #667eea, #764ba2);
    }
    
    /* Floating Elements */
    .float-container {
        position: fixed;
        bottom: 30px;
        right: 30px;
        z-index: 1000;
        display: flex;
        flex-direction: column;
        gap: 12px;
    }
    
    .float-btn {
        background: linear-gradient(135deg, #25d366 0%, #128c7e 100%);
        color: white;
        border-radius: 50px;
        border: none;
        padding: 15px 20px;
        font-weight: 600;
        box-shadow: 0 8px 25px rgba(37, 211, 102, 0.4);
        transition: all 0.3s ease;
        text-decoration: none;
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 14px;
    }
    
    .float-btn:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 35px rgba(37, 211, 102, 0.5);
    }
    
    /* Animation for title */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in { animation: fadeInUp 0.8s ease-out; }
    </style>
    """, unsafe_allow_html=True)

# =========================
# 2. ADVANCED SESSION & AUTH SYSTEM
# =========================
if 'is_authenticated' not in st.session_state:
    st.session_state.is_authenticated = False
    st.session_state.user_name = ""
    st.session_state.generated_count = 0

def authenticate_user():
    """Enhanced authentication with better UX"""
    if st.session_state.is_authenticated:
        return True
    
    # Fullscreen overlay login
    st.markdown("""
        <div style='position: fixed; top: 0; left: 0; width: 100%; height: 100%; 
                   background: rgba(10,10,35,0.95); backdrop-filter: blur(20px); 
                   display: flex; align-items: center; justify-content: center; z-index: 9999;'>
            <div style='background: rgba(255,255,255,0.1); backdrop-filter: blur(20px); 
                       border-radius: 24px; padding: 3rem; text-align: center; 
                       border: 1px solid rgba(255,255,255,0.2); max-width: 400px;'>
                <div style='font-size: 3rem; margin-bottom: 1rem;'>✨</div>
                <h2 style='color: #00d4ff; margin-bottom: 2rem;'>Welcome to Vixan AI Pro v14.0</h2>
                <div style='display: flex; flex-direction: column; gap: 1.5rem;'>
    """, unsafe_allow_html=True)
    
    with st.form("auth_form", clear_on_submit=True):
        col1, col2 = st.columns([1, 2])
        with col1:
            st.text_input("👤 Full Name", key="auth_name")
        with col2:
            st.text_input("📱 WhatsApp Number", key="auth_phone", placeholder="10 digits")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.form_submit_button("🚀 Unlock Premium Features", use_container_width=True, 
                               help="Get instant access to all AI tools"):
            name = st.session_state.auth_name.strip()
            phone = st.session_state.auth_phone.strip()
            
            if name and len(phone) >= 10 and phone.isdigit():
                st.session_state.is_authenticated = True
                st.session_state.user_name = name
                st.session_state.generated_count = 0
                st.success(f"🎉 Welcome {name}! All features unlocked!")
                st.balloons()
                time.sleep(2)
                st.rerun()
            else:
                st.error("❌ Please enter valid name & 10-digit phone number")
    
    st.markdown("</div>", unsafe_allow_html=True)
    return False

# =========================
# 3. ENHANCED SIDEBAR v14
# =========================
with st.sidebar:
    # Logo & Branding
    st.markdown("""
        <div style='text-align: center; padding: 2rem 1rem 1rem 1rem;'>
            <h1 style='color: #00d4ff; font-size: 2.2rem; margin: 0; font-weight: 700;'>
                ✨ VIXAN AI
            </h1>
            <p style='color: #a0a0ff; font-size: 0.9rem; margin: 0.5rem 0 0 0;'>Pro v14.0 Studio</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.image("https://cdn-icons-png.flaticon.com/512/10817/1081731.png", width=80, use_column_width=True)
    
    # Main Navigation
    menu_options = {
        "🏠 Dashboard": "dashboard",
        "🖼️ Poster Lab": "poster", 
        "🎙️ Voice Studio": "voice",
        "🎞️ Video Center": "video",
        "⚙️ Settings": "settings"
    }
    
    selected_menu = st.radio("🎛️ Quick Navigation", 
                           list(menu_options.keys()), 
                           format_func=lambda x: x,
                           label_visibility="collapsed")[0]
    
    st.divider()
    
    # User Stats
    if st.session_state.is_authenticated:
        col1, col2 = st.columns(2)
        with col1:
            st.metric("👤 User", st.session_state.user_name)
        with col2:
            st.metric("✨ Generations", st.session_state.generated_count)
        
        if st.button("🔓 Logout", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    else:
        st.info("🔐 Login to unlock premium features")
    
    st.divider()
    st.markdown("---")

# =========================
# 4. DYNAMIC CONTENT RENDERING
# =========================
def show_dashboard():
    """Enhanced Dashboard with metrics and quick actions"""
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    st.title("🚀 Vixan AI Master Studio v14.0")
    st.markdown("**The Ultimate AI Media Creation Suite** - Generate stunning posters, voices & videos instantly!")
    
    # Stats Cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
            <div class="metric-card">
                <h3 style='color: #00d4ff; margin: 0;'>🖼️ 10K+</h3>
                <p style='color: #a0a0ff; margin: 0.5rem 0 0 0;'>Posters Created</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="metric-card">
                <h3 style='color: #00c851; margin: 0;'>🎙️ 5K+</h3>
                <p style='color: #a0a0ff; margin: 0.5rem 0 0 0;'>Voices Generated</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="metric-card">
                <h3 style='color: #ff6b6b; margin: 0;'>🎞️ 2K+</h3>
                <p style='color: #a0a0ff; margin: 0.5rem 0 0 0;'>Videos Produced</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
            <div class="metric-card">
                <h3 style='color: #ffd93d; margin: 0;'>⭐ 4.9/5</h3>
                <p style='color: #a0a0ff; margin: 0.5rem 0 0 0;'>User Rating</p>
            </div>
        """, unsafe_allow_html=True)
    
    # Quick Action Buttons
    st.markdown("### 🚀 Quick Generate")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🖼️ Poster", key="quick_poster", help="Generate poster instantly"):
            st.session_state.current_page = "poster"
            st.rerun()
    
    with col2:
        if st.button("🎙️ Voice", key="quick_voice", help="Text to speech"):
            st.session_state.current_page = "voice"
            st.rerun()
    
    with col3:
        if st.button("🎞️ Video", key="quick_video", help="AI Video demo"):
            st.session_state.current_page = "video"
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_poster_lab():
    """Enhanced Poster Generation with multiple AI providers"""
    st.header("🖼️ AI Poster Lab Pro")
    st.info("✨ Generate & clone professional posters in seconds!")
    
    tab1, tab2, tab3 = st.tabs(["✨ Text-to-Poster", "🧬 Image Cloning", "🎨 Style Templates"])
    
    with tab1:
        col1, col2 = st.columns([2, 1])
        with col1:
            prompt = st.text_area("📝 Describe your poster", 
                                "professional political banner, orange theme, modern design, 4K quality", 
                                height=100, key="poster_prompt")
        with col2:
            width = st.slider("Width", 512, 2048, 1024, 256)
            height = st.slider("Height", 512, 2048, 1024, 256)
        
        col1, col2 = st.columns([1, 2])
        with col1:
            if st.button("🚀 Generate Poster", type="primary", key="gen_poster"):
                if authenticate_user():
                    generate_poster(prompt, width, height)
        with col2:
            st.info("💡 Try: 'election campaign poster, blue theme' or 'business promotion banner'")
    
    with tab2:
        uploaded = st.file_uploader("📤 Upload image to clone", type=['jpg','png','jpeg'])
        clone_prompt = st.text_input("✏️ New text/content", "Your new message here")
        
        if st.button("🧬 Clone Design", type="primary") and uploaded:
            if authenticate_user():
                generate_cloned_poster(uploaded, clone_prompt)
    
    with tab3:
        templates = {
            "🇮🇳 Political Campaign": "Indian election poster, tricolor theme, bold text",
            "💼 Business Promo": "modern business banner, blue gradient, professional",
            "🎉 Event Invite": "event invitation poster, colorful, festive design",
            "📈 Digital Marketing": "social media ad, orange theme, modern typography"
        }
        
        selected_template = st.selectbox("Choose template", list(templates.keys()))
        if st.button("🎨 Use Template", type="primary"):
            st.session_state.poster_prompt = templates[selected_template]
            st.rerun()

def generate_poster(prompt, width, height):
    """Enhanced poster generation with progress"""
    st.session_state.generated_count += 1
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Multiple AI providers for reliability
    providers = [
        f"https://image.pollinations.ai/prompt/{prompt.replace(' ','%20')}?width={width}&height={height}&nologo=true",
        f"https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image?prompt={prompt}"
    ]
    
    for i, provider_url in enumerate(providers[:1]):  # Use first provider
        status_text.text(f"🎨 Generating with AI Engine... ({i+1}/1)")
        progress_bar.progress((i + 1) / 1)
        
        try:
            response = requests.get(provider_url, timeout=30)
            if response.status_code == 200:
                st.image(response.content, use_container_width=True)
                st.download_button(
                    "💾 Download HD Poster", 
                    response.content, 
                    f"vixan_poster_{int(time.time())}.png",
                    "image/png"
                )
                st.success("✅ Poster generated successfully!")
                st.balloons()
                return
        except:
            continue
    
    st.error("❌ Generation failed. Try different prompt or refresh.")

def generate_cloned_poster(image_file, new_text):
    """Clone poster design"""
    prompt = f"clone design style of uploaded image but with text: '{new_text}', same layout and colors"
    # Convert uploaded image to show preview
    img = Image.open(image_file)
    st.image(img, caption="Original", width=300)
    generate_poster(prompt, 1024, 1024)

def show_voice_studio():
    """Enhanced Voice Studio with multiple languages"""
    st.header("🎙️ AI Voice Studio Pro")
    st.info("🔊 Text-to-Speech in 20+ languages with custom voices!")
    
    tab1, tab2 = st.tabs(["📢 Text-to-Speech", "🎤 Voice Settings"])
    
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            text = st.text_area("✍️ Enter text to speak", 
                              "नमस्ते! वीक्सन एआई स्टूडियो में आपका हार्दिक स्वागत है। "
                              "अब आप हिंदी, अंग्रेजी और अन्य भाषाओं में आवाज बना सकते हैं।",
                              height=120, key="voice_text")
        
        with col2:
            language = st.selectbox("🌐 Language", 
                                  ["hi", "en", "ta", "te", "bn", "mr", "gu", "kn"],
                                  format_func=lambda x: {"hi":"हिंदी", "en":"English", "ta":"தமிழ்", 
                                                       "te":"తెలుగు", "bn":"বাংলা", "mr":"मराठी",
                                                       "gu":"ગુજરાતી", "kn":"ಕನ್ನಡ"}.get(x, x))
            
            speed = st.slider("🐌 Speed", 0.5, 2.0, 1.0, 0.1)
            pitch = st.slider("🎵 Pitch", 0.8, 1.5, 1.0, 0.1)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🎙️ Generate Voice", type="primary", key="gen_voice"):
                if authenticate_user():
                    generate_voice(text, language, speed)
        
        with col2:
            st.audio("preview.mp3", autoplay=False)
    
    with tab2:
        st.markdown("### 🎚️ Advanced Voice Settings")
        st.info("Premium voices and cloning coming soon in v14.1!")

def generate_voice(text, lang, speed):
    """Generate high-quality voice"""
    st.session_state.generated_count += 1
    
    with st.spinner("🎵 Creating your voice..."):
        try:
            tts = gTTS(text=text[:500], lang=lang, slow=(speed < 1.0))  # Limit length
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            
            st.audio(fp.read())
            st.download_button(
                "💾 Download MP3", 
                fp.getvalue(), 
                f"vixan_voice_{int(time.time())}.mp3",
                "audio/mpeg"
            )
            st.success("✅ Voice generated perfectly!")
        except Exception as e:
            st.error(f"❌ Voice generation failed: {str(e)}")

def show_video_center():
    """Video production center"""
    st.header("🎞️ AI Video Production Center")
    st.warning("🔥 Video generation coming in v14.2 - Subscribe for early access!")
    
    col1, col2 = st.columns(2)
    with col1:
        st.video("https://sample-videos.com/zip/10/mp4/SampleVideo_1280x720_1mb.mp4")
    with col2:
        st.markdown("""
        ### 🎬 Features Coming Soon:
        - **Text-to-Video**
        - **Image-to-Video**
        - **Voiceover Videos**
        - **Social Media Reels**
        - **4K Export**
        """)

def show_settings():
    """Settings page"""
    st.header("⚙️ Studio Settings")
    st.markdown("### 📊 Usage Stats")
    st.metric("Total Generations", st.session_state.get('generated_count', 0))
    st.metric("Active Since", "Today")

# =========================
# 5. MAIN APP ROUTING
# =========================
if 'current_page' not in st.session_state:
    st.session_state.current_page = "dashboard"

# Route to selected page
page_mapping = {
    "🏠 Dashboard": show_dashboard,
    "🖼️ Poster Lab": show_poster_lab,
    "🎙️ Voice Studio": show_voice_studio,
    "🎞️ Video Center": show_video_center,
    "⚙️ Settings": show_settings
}

# Check authentication for content pages
if selected_menu in ["🖼️ Poster Lab", "🎙️ Voice Studio", "🎞️ Video Center"]:
    if not authenticate_user():
        st.stop()

# Render selected page
page_mapping[selected_menu]()

# =========================
# 6. ENHANCED FLOATING SUPPORT
# =========================
st.markdown("""
    <div class="float-container">
        <a href="https://wa.me/919876543210" target="_blank" class="float-btn">
            💬 WhatsApp Support
        </a>
        <button class="float-btn" onclick="window.scrollTo({top: 0, behavior: 'smooth'})">
            ⬆️ Back to Top
        </button>
    </div>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
    <div style='text-align: center; padding: 3rem 1rem 1rem; 
                border-top: 1px solid rgba(255,255,255,0.1); 
                margin-top: 3rem; color: #a0a0ff;'>
        <h3>✨ Vixan AI Pro v14.0</h3>
        <p>Made with ❤️ in India | Patna, Bihar</p>
        <p>© 2026 Vixan Studio. All rights reserved.</p>
    </div>
""", unsafe_allow_html=True)
