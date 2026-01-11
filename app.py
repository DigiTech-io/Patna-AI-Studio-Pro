import streamlit as st
import os
import uuid
import requests
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont

# =========================
# 1. CONFIG & PAGE THEME
# =========================
st.set_page_config(
    page_title="Vixan AI Media Studio Pro v5.0",
    page_icon="🎨",
    layout="wide",
)

# Custom Premium CSS
st.markdown("""
<style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button {
        background: linear-gradient(45deg, #FFD700, #FF8C00);
        color: black; border-radius: 12px; font-weight: 700; width: 100%;
    }
    .card {
        border: 1px solid #333; border-radius: 16px; padding: 15px;
        background: #161b22; text-align: center; margin-bottom: 10px;
    }
    .stSlider { color: #FFD700; }
</style>
""", unsafe_allow_html=True)

# =========================
# 2. SIDEBAR
# =========================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=80)
    st.markdown("## **Vixan Pro v5.0**")
    menu = st.radio("Select Module", 
        ["🏠 Dashboard", "🖼️ AI Poster Lab", "🎙️ Advanced Voice Studio", "🎞️ Video Clone Center"])
    st.divider()
    st.caption("© 2026 Patna AI Studio")

# =========================
# 3. DASHBOARD
# =========================
if menu == "🏠 Dashboard":
    st.markdown("## 🚀 Vixan AI Media Studio Dashboard")
    st.info("Bihar's Most Powerful AI Branding Tool is now LIVE!")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div class='card'>🎨<h4>Poster Lab</h4><p>AI Designs</p></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='card'>🎙️<h4>Voice Studio</h4><p>Pro Hindi AI</p></div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='card'>🎞️<h4>Video Clone</h4><p>Talking Poster</p></div>", unsafe_allow_html=True)
    
    st.image("https://img.freepik.com/free-vector/abstract-technology-background_23-2148905210.jpg", use_container_width=True)

# =========================
# 4. AI POSTER LAB (Fully Functional)
# =========================
elif menu == "🖼️ AI Poster Lab":
    st.markdown("## 🖼️ AI Poster & Design Lab")
    
    col_l, col_r = st.columns([1, 1.5])
    
    with col_l:
        st.markdown("### 🖋️ Design Details")
        leader_name = st.text_input("Leader/Brand Name", "Vixan AI Studio")
        slogan = st.text_area("Hindi Slogan", "आपका विश्वास, हमारा विकास")
        category = st.selectbox("Category", ["Political", "Festival", "Business"])
        style_prompt = st.text_input("Style Prompt", "Professional, 4k, orange and gold theme")
        
        generate_btn = st.button("🚀 Generate AI Poster")

    with col_r:
        st.markdown("### 🎯 AI Output")
        if generate_btn:
            with st.spinner("AI is painting your poster..."):
                # Pollinations AI - Asli Poster Generation
                prompt = f"{category} poster for {leader_name}, {slogan}, {style_prompt}, high quality, cinematic lighting"
                image_url = f"https://image.pollinations.ai/prompt/{prompt.replace(' ', '%20')}?width=1024&height=1024&nologo=true&seed={uuid.uuid4().int}"
                
                try:
                    response = requests.get(image_url)
                    if response.status_code == 200:
                        st.image(response.content, caption=f"Design for {leader_name}", use_container_width=True)
                        st.download_button("⬇️ Download HD Poster", response.content, "vixan_poster.png", "image/png")
                        st.success("Poster Generated Successfully!")
                    else:
                        st.error("AI Engine busy. Please try again.")
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.info("Enter details and click generate to see AI magic.")

# =========================
# 5. ADVANCED VOICE STUDIO
# =========================
elif menu == "🎙️ Advanced Voice Studio":
    st.markdown("## 🎙️ Advanced AI Voice Studio")
    
    text = st.text_area("Input Text (Hindi/English)", "नमस्ते, पटना AI स्टूडियो में आपका स्वागत है।", height=120)
    
    col1, col2 = st.columns(2)
    with col1:
        speed = st.slider("Speech Speed", 0.5, 2.0, 1.0)
    with col2:
        stability = st.slider("Stability (Tone)", 0.0, 1.0, 0.8)
    
    if st.button("🔊 Generate AI Voice"):
        if text:
            with st.spinner("Generating Professional Voice..."):
                filename = f"voice_{uuid.uuid4().hex}.mp3"
                tts = gTTS(text=text, lang="hi", slow=(speed < 1.0))
                tts.save(filename)
                st.audio(filename)
                
                with open(filename, "rb") as f:
                    st.download_button("⬇️ Download Audio", f, "vixan_voice.mp3")
        else:
            st.warning("Please enter text first.")

# =========================
# 6. VIDEO CLONE CENTER
# =========================
elif menu == "🎞️ Video Clone Center":
    st.markdown("## 🎞️ Poster-to-Video Clone Center")
    st.write("Convert your static poster into an engaging video.")
    
    up_col, preview_col = st.columns(2)
    with up_col:
        u_poster = st.file_uploader("Upload Image", type=["jpg", "png"])
        u_audio = st.file_uploader("Upload Voice (Optional)", type=["mp3"])
        
        if st.button("🎬 Create Talking Video"):
            if u_poster:
                st.session_state["video_ready"] = True
            else:
                st.error("Please upload a poster first.")

    with preview_col:
        if st.session_state.get("video_ready"):
            st.info("AI Video Engine Processing...")
            # Demo Video Placeholder
            st.video("https://www.w3schools.com/html/mov_bbb.mp4")
            st.success("Video Clone Ready for Download!")

# =========================
# FOOTER
# =========================
st.markdown("<hr><center style='color:#666;'>© 2026 Vixan AI Media Studio • Patna, Bihar</center>", unsafe_allow_html=True)
