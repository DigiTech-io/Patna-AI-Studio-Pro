import streamlit as st
import os
import requests
import uuid
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont
import io

# Page config
st.set_page_config(page_title="Vixan AI Pro v10.0", layout="wide", page_icon="🚀")

# CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');
.main { background: linear-gradient(135deg, #0a0e17 0%, #1a1f2e 100%); }
div.stButton > button {
    background: linear-gradient(45deg, #FFD700, #FFA500); color: black; 
    border-radius: 15px; font-weight: 700; border: none; height: 3.5em; width: 100%;
    box-shadow: 0 8px 25px rgba(255,215,0,0.4);
}
.glass-card { 
    background: rgba(22,27,34,0.9); border-radius: 20px; padding: 25px; 
    border: 1px solid #FFD700; box-shadow: 0 15px 35px rgba(0,0,0,0.5);
}
.neon-text { color: #FFD700; font-weight: 800; }
</style>
""", unsafe_allow_html=True)

# FIXED IMAGE FUNCTION - NO SYNTAX ERRORS
def add_text_to_image(image_bytes, leader_name, slogan):
    img = Image.open(io.BytesIO(image_bytes)).convert("RGBA")
    draw = ImageDraw.Draw(img)
    width, height = img.size
    
    # Safe font loading
    try:
        font_main = ImageFont.truetype("fonts/hindi.ttf", int(height * 0.08))
        font_sub = ImageFont.truetype("fonts/hindi.ttf", int(height * 0.06))
    except:
        font_main = ImageFont.load_default()
        font_sub = ImageFont.load_default()
    
    # ✅ LINE 59 FIXED - PROPER DOUBLE QUOTES
    lines_main = leader_name.split("
")
    lines_sub = slogan.split("
")
    
    # Main title
    y_pos = height * 0.72
    for i, line in enumerate(lines_main):
        bbox = draw.textbbox((0, 0), line, font=font_main)
        text_w = bbox[2] - bbox[0]
        x = (width - text_w) / 2
        draw.text((x+2, y_pos+i*40), line, font=font_main, fill="black")
        draw.text((x, y_pos+i*40), line, font=font_main, fill="white")
    
    # Slogan
    y_pos_slogan = height * 0.83
    for i, line in enumerate(lines_sub):
        bbox = draw.textbbox((0, 0), line, font=font_sub)
        text_w = bbox[2] - bbox[0]
        x = (width - text_w) / 2
        draw.text((x+2, y_pos_slogan+i*35), line, font=font_sub, fill="#CC5500")
        draw.text((x, y_pos_slogan+i*35), line, font=font_sub, fill="#FFD700")
    
    # QR placeholder
    qr_size = int(height * 0.1)
    qr_bg = Image.new('RGBA', (qr_size, qr_size), (255,255,255,100))
    img.paste(qr_bg, (width-qr_size-30, height-qr_size-30), qr_bg)
    
    # Save PNG
    rgb_img = Image.new('RGB', img.size, (0,0,0))
    rgb_img.paste(img, mask=img.split()[-1])
    img_bytes = io.BytesIO()
    rgb_img.save(img_bytes, 'PNG', quality=95)
    return img_bytes.getvalue()

# State
if 'credits' not in st.session_state:
    st.session_state.credits = 10

# Sidebar
with st.sidebar:
    st.markdown("""
    <div class='glass-card' style='text-align:center;'>
        <h3 class='neon-text'>🚀 Vixan Pro v10.0</h3>
        <p>Patna AI Studio</p>
    </div>
    """, unsafe_allow_html=True)
    
    menu = st.radio("Navigation", ["🏠 Dashboard", "🖼️ Poster Lab", "🎙️ Voice", "💳 Plans"])
    
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔥 Free Trial"):
            st.session_state.credits = 10
            st.rerun()
    with col2:
        st.metric("Credits", st.session_state.credits)

# Pages
if menu == "🏠 Dashboard":
    st.markdown("<h1 class='neon-text'>Vixan AI Studio Pro</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1: st.metric("Posters", "3.8K")
    with col2: st.metric("Voices", "2.1K")
    with col3: st.metric("Users", "1.2K")

elif menu == "🖼️ Poster Lab":
    st.markdown("<h2 class='neon-text'>AI Poster Generator</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        leader_name = st.text_area("Leader Name", "नितिन गडकरी
Union Minister", height=80)
        slogan = st.text_area("Slogan", "विकास की नई ऊँचाइयों तक", height=80)
    
    with col2:
        prompt = st.text_area("Background", "political background orange blue gradient 8k", height=120)
    
    if st.button("🚀 Generate Poster") and st.session_state.credits > 0:
        st.session_state.credits -= 1
        
        with st.spinner("Generating..."):
            url = f"https://image.pollinations.ai/prompt/{prompt.replace(' ','%20')}?width=1024&height=1024"
            bg_data = requests.get(url).content
            poster = add_text_to_image(bg_data, leader_name, slogan)
            
            st.image(poster, use_container_width=True)
            st.download_button("Download PNG", poster, f"poster_{uuid.uuid4().hex[:8]}.png")

elif menu == "🎙️ Voice":
    st.markdown("<h2 class='neon-text'>Voice Studio</h2>", unsafe_allow_html=True)
    text = st.text_area("Text", "नमस्कार! Vixan AI Studio")
    if st.button("Generate Voice"):
        tts = gTTS(text=text, lang='hi')
        audio_bytes = io.BytesIO()
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)
        st.audio(audio_bytes.getvalue())
        st.download_button("MP3", audio_bytes.getvalue(), "voice.mp3")

# Footer
st.markdown("---")
st.markdown("<div style='text-align:center;color:#888;'>Patna AI Studio | Vixan v10.0 | Bihar 🇮🇳</div>", unsafe_allow_html=True)
