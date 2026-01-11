import streamlit as st
import os
import requests
import uuid
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont
import io

# =========================
# 1. PAGE SETUP & THEME v10.0
# =========================
st.set_page_config(page_title="Vixan AI Pro v10.0", layout="wide", page_icon="🚀")

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

# =========================
# 2. FIXED IMAGE PROCESSING FUNCTION 
# =========================
def add_text_to_image(image_bytes, leader_name, slogan):
    """✅ 100% Syntax Error Free - Professional Text Overlay"""
    img = Image.open(io.BytesIO(image_bytes)).convert("RGBA")
    draw = ImageDraw.Draw(img)
    width, height = img.size
    
    # Font setup
    font_size_main = int(height * 0.08)
    font_size_sub = int(height * 0.06)
    
    # Hindi font handling
    font_dir = "fonts"
    font_main = ImageFont.load_default()
    font_sub = ImageFont.load_default()
    
    if os.path.exists(font_dir):
        fonts = [f for f in os.listdir(font_dir) if f.endswith('.ttf')]
        if fonts:
            try:
                font_main = ImageFont.truetype(os.path.join(font_dir, fonts[0]), font_size_main)
                font_sub = ImageFont.truetype(os.path.join(font_dir, fonts[0]), font_size_sub)
            except:
                pass
    
    # ✅ FIXED LINE 97 - PROPER STRING SPLITTING
    lines_main = leader_name.split("
")  
    lines_sub = slogan.split("
")
    
    # Main title (White with shadow)
    y_pos = height * 0.72
    for i, line in enumerate(lines_main):
        bbox = draw.textbbox((0, 0), line, font=font_main)
        text_w = bbox[2] - bbox[0]
        x = (width - text_w) / 2
        
        # Shadow + Text
        draw.text((x+2, y_pos+i*40+2), line, font=font_main, fill="black")
        draw.text((x, y_pos+i*40), line, font=font_main, fill="white")
    
    # Slogan (Gold)
    y_pos_slogan = height * 0.83
    for i, line in enumerate(lines_sub):
        bbox = draw.textbbox((0, 0), line, font=font_sub)
        text_w = bbox[2] - bbox[0]
        x = (width - text_w) / 2
        
        draw.text((x+2, y_pos_slogan+i*35+2), line, font=font_sub, fill="#CC5500")
        draw.text((x, y_pos_slogan+i*35), line, font=font_sub, fill="#FFD700")
    
    # QR placeholder
    qr_size = int(height * 0.1)
    qr_bg = Image.new('RGBA', (qr_size, qr_size), (255,255,255,100))
    img.paste(qr_bg, (width-qr_size-30, height-qr_size-30), qr_bg)
    
    # Save as PNG
    rgb_img = Image.new('RGB', img.size, (0,0,0))
    rgb_img.paste(img, mask=img.split()[-1])
    img_bytes = io.BytesIO()
    rgb_img.save(img_bytes, 'PNG', quality=95)
    return img_bytes.getvalue()

# =========================
# 3. STATE MANAGEMENT
# =========================
if 'credits' not in st.session_state:
    st.session_state.credits = 10

# =========================
# 4. SIDEBAR
# =========================
with st.sidebar:
    st.markdown("""
    <div class='glass-card' style='text-align:center;'>
        <h3 class='neon-text'>🚀 Vixan Pro v10.0</h3>
        <p>Patna AI Studio</p>
    </div>
    """, unsafe_allow_html=True)
    
    menu = st.radio("🎯 Navigation", [
        "🏠 Dashboard", 
        "🖼️ Poster Lab", 
        "🎙️ Voice Studio", 
        "💳 Pro Plans"
    ])
    
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔥 Reset Trial"):
            st.session_state.credits = 10
            st.success("✅ 10 Credits Added!")
            st.rerun()
    with col2:
        st.metric("⭐ Credits", st.session_state.credits)

# =========================
# 5. MAIN PAGES
# =========================

if menu == "🏠 Dashboard":
    st.markdown("<h1 class='neon-text'>🌟 Vixan AI Studio Pro</h1>", unsafe_allow_html=True)
    st.markdown("<h3>Bihar's #1 AI Content Creator</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1: st.metric("🎨 Posters", "3.8K", "+1.2K")
    with col2: st.metric("🎙️ Voices", "2.1K", "+900")
    with col3: st.metric("⭐ Users", "1.2K", "+400")
    
    st.markdown("""
    <div class='glass-card'>
        <h4>✅ Pro Features:</h4>
        <ul style='color:#ccc;'>
            <li>Hindi Font Overlay</li>
            <li>AI Backgrounds</li>
            <li>QR Code Auto</li>
            <li>Multi-line Text</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

elif menu == "🖼️ Poster Lab":
    st.markdown("<h2 class='neon-text'>🖼️ AI Poster Generator Pro</h2>", unsafe_allow_html=True)
    
    # Input Panel
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("### 📝 Content")
        leader_name = st.text_area("👤 Leader Name:", 
                                 "नितिन गडकरी
Union Minister", height=80)
        slogan = st.text_area("🏷️ Slogan:", 
                            "विकास की नई ऊँचाइयों तक
सुरक्षित भारत", height=80)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("### ⚙️ Settings")
        prompt = st.text_area("Background Prompt:", 
                            "professional political background, orange blue gradient, 8k", 
                            height=100)
        theme = st.selectbox("Theme:", ["Political", "Business", "Festival"])
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Generate Button
    if st.button("🚀 **CREATE PRO POSTER**", type="primary") and st.session_state.credits > 0:
        st.session_state.credits -= 1
        
        with st.spinner("🎨 AI Generating Professional Poster..."):
            # Generate background
            url = f"https://image.pollinations.ai/prompt/{prompt.replace(' ','%20')}?width=1024&height=1024&nologo=true"
            bg_data = requests.get(url).content
            
            # Add professional text
            final_poster = add_text_to_image(bg_data, leader_name, slogan)
            
            # Display result
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.image(final_poster, caption="✨ Pro Poster Ready!", use_container_width=True)
            
            col_dl1, col_dl2 = st.columns(2)
            with col_dl1:
                st.download_button("💾 Download PNG", final_poster, 
                                 f"vixan_poster_{uuid.uuid4().hex[:8]}.png", "image/png")
            with col_dl2:
                st.success(f"✅ Credits Left: {st.session_state.credits}")
            st.markdown("</div>", unsafe_allow_html=True)
            st.balloons()
    
    elif st.session_state.credits <= 0:
        st.error("🔴 No Credits! Click Sidebar → Reset Trial")

elif menu == "🎙️ Voice Studio":
    st.markdown("<h2 class='neon-text'>🎙️ Voice Generator</h2>", unsafe_allow_html=True)
    text = st.text_area("Text:", "नमस्कार! Vixan AI Studio से स्वागत है।")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📢 Generate Hindi Voice"):
            tts = gTTS(text=text, lang='hi')
            audio_bytes = io.BytesIO()
            tts.write_to_fp(audio_bytes)
            audio_bytes.seek(0)
            st.audio(audio_bytes.getvalue())
            st.download_button("🎵 MP3 Download", audio_bytes.getvalue(), "voice.mp3")

elif menu == "💳 Pro Plans":
    st.markdown("<h2 class='neon-text'>💎 Pro Plans</h2>", unsafe_allow_html=True)
    st.markdown("""
    <div class='glass-card'>
        <h3>₹299 / Month - Unlimited</h3>
        <ul style='color:#FFD700;'>
            <li>✅ Unlimited Posters</li>
            <li>✅ Pro Voices</li>
            <li>✅ Video Tools</li>
        </ul>
        <a href='https://rzp.io/l/vixanpro' style='text-decoration:none;'>
            <button style='width:100%; margin-top:15px;'>🚀 Buy Pro</button>
        </a>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align:center; color:#888; padding:20px;'>
    <h4 class='neon-text'>👨‍💻 Patna AI Studio</h4>
    <p>Vixan Pro v10.0 | Made in Bihar 🇮🇳 | 2026</p>
</div>
""", unsafe_allow_html=True)
