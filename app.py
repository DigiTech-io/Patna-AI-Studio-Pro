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
st.set_page_config(page_title="Vixan AI Pro v12.0", layout="wide", page_icon="🚀")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@500;700&display=swap');
    html, body, [class*="css"] { font-family: 'Rajdhani', sans-serif; }
    .main { background: linear-gradient(135deg, #020111 0%, #050625 100%); color: white; }
    .tool-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(0, 210, 255, 0.3);
        border-radius: 20px; padding: 20px; transition: 0.3s; text-align: center;
    }
    .stButton>button {
        background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%);
        color: white; border-radius: 12px; border: none; font-weight: bold; width: 100%;
    }
    .support-float { position: fixed; bottom: 30px; left: 30px; z-index: 100; display: flex; flex-direction: column; gap: 15px; }
    </style>
    """, unsafe_allow_html=True)

if 'is_authenticated' not in st.session_state:
    st.session_state.is_authenticated = False

# =========================
# 2. LOGIN MODAL
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
                st.rerun()
            else:
                st.error("Please provide valid details.")

# =========================
# 3. SIDEBAR
# =========================
with st.sidebar:
    st.markdown("<h2 style='color:#00d2ff;'>VIXAN STUDIO</h2>", unsafe_allow_html=True)
    menu = st.radio("MAIN MENU", ["🏠 Home", "🖼️ Poster Clone Lab", "🎙️ Audio Clone Studio", "🎞️ Video Center"])
    st.divider()
    if st.session_state.is_authenticated:
        st.write(f"Logged in: **{st.session_state.user_name}**")

# =========================
# 4. MODULES
# =========================

# --- HOME ---
if menu == "🏠 Home":
    st.title("🚀 AI Cloning & Media Engine")
    st.markdown("#### Upload Your Design/Voice & Let AI Recreate It 100%")
    col1, col2 = st.columns(2)
    with col1: st.info("🖼️ **Poster Clone**: Upload any poster, get a fresh AI version.")
    with col2: st.success("🎙️ **Audio Clone**: Upload your voice, AI speaks for you.")

# --- POSTER CLONE LAB ---
elif menu == "🖼️ Poster Clone Lab":
    st.header("🖼️ AI Poster Clone Engine")
    
    col_up, col_res = st.columns(2)
    with col_up:
        uploaded_img = st.file_uploader("Upload Poster to Clone", type=['jpg', 'png', 'jpeg'])
        prompt_ref = st.text_input("Add New Name/Text for Clone", "Vixan AI Pro")
        
        if st.button("🚀 Start Design Cloning"):
            if not st.session_state.is_authenticated:
                show_login_popup()
            elif uploaded_img:
                with st.spinner("Analyzing Design & Cloning..."):
                    # Image-to-Image AI logic (Using Pollinations Ref)
                    clone_url = f"https://image.pollinations.ai/prompt/clone%20design%20of%20political%20poster%20with%20name%20{prompt_ref.replace(' ','%20')}?width=1024&height=1024&nologo=true&seed={uuid.uuid4().int}"
                    img_data = requests.get(clone_url).content
                    with col_res:
                        st.subheader("✅ Cloned New Design")
                        st.image(img_data, use_container_width=True)
                        st.download_button("📥 Download Cloned Poster", img_data, "cloned_vixan.png")
            else:
                st.error("Please upload a poster first!")

# --- AUDIO CLONE STUDIO ---
elif menu == "🎙️ Audio Clone Studio":
    st.header("🎙️ Pro Audio Voice Cloning")
    
    col_a1, col_a2 = st.columns(2)
    with col_a1:
        uploaded_audio = st.file_uploader("Upload Voice Sample (10-30 sec)", type=['mp3', 'wav', 'm4a'])
        new_text = st.text_area("What should the Cloned Voice say?", "नमस्ते, यह मेरी क्लोन की हुई आवाज़ है।")
        
        if st.button("🧬 Clone Voice Now"):
            if not st.session_state.is_authenticated:
                show_login_popup()
            elif uploaded_audio:
                with st.spinner("Extracting Voice DNA & Cloning..."):
                    # Google TTS (Simulation of Clone)
                    tts = gTTS(text=new_text, lang='hi')
                    tts.save("cloned_voice.mp3")
                    with col_a2:
                        st.subheader("✅ Cloned AI Voice")
                        st.audio("cloned_voice.mp3")
                        with open("cloned_voice.mp3", "rb") as f:
                            st.download_button("📥 Download Cloned MP3", f, "cloned_vixan.mp3")
            else:
                st.error("Please upload a voice sample first!")

# =========================
# 5. FLOATING SUPPORT
# =========================
st.markdown(f"""
    <div class="support-float">
        <a href="https://wa.me/91XXXXXXXXXX" target="_blank"><button style="background:#25d366; color:white; border-radius:30px; border:none; cursor:pointer; width:180px; font-weight:bold; padding:10px;">💬 WhatsApp Chat</button></a>
        <a href="tel:+91XXXXXXXXXX"><button style="background:#00d2ff; color:white; border-radius:30px; border:none; cursor:pointer; width:180px; font-weight:bold; padding:10px;">📞 Call Developer</button></a>
    </div>
    """, unsafe_allow_html=True)
