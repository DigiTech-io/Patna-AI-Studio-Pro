import streamlit as st
import os
import requests
import uuid
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import io
import base64
import time

# =========================
# 1. PAGE SETUP & ULTRA MODERN THEME v10.0 (FIXED)
# =========================
st.set_page_config(
    page_title="Vixan AI Pro v10.0", 
    layout="wide", 
    page_icon="🚀",
    initial_sidebar_state="expanded"
)

# Revolutionary CSS v10 - Neon Gold + Glass Morphism
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800&display=swap');
    * { font-family: 'Poppins', sans-serif; }
    
    .main { 
        background: linear-gradient(135deg, #0a0e17 0%, #1a1f2e 40%, #16213e 100%); 
        backdrop-filter: blur(20px);
    }
    
    div.stButton > button {
        background: linear-gradient(45deg, #FFD700, #FFA500, #FF6B35, #FFD700);
        background-size: 300% 300%;
        color: #000; border-radius: 20px; font-weight: 700; border: 2px solid rgba(255,215,0,0.3);
        height: 4em; width: 100%; box-shadow: 0 12px 40px rgba(255,215,0,0.4);
        animation: gradientShift 3s ease infinite; transition: all 0.4s cubic-bezier(0.25,0.8,0.25,1);
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    div.stButton > button:hover { 
        transform: translateY(-4px) scale(1.02); 
        box-shadow: 0 20px 50px rgba(255,215,0,0.6); 
        border-color: rgba(255,215,0,0.7);
    }
    
    .glass-card { 
        background: rgba(22,27,34,0.85); 
        backdrop-filter: blur(25px); 
        border: 1px solid rgba(255,215,0,0.2); 
        border-radius: 25px; 
        padding: 30px; 
        box-shadow: 0 20px 60px rgba(0,0,0,0.5);
    }
    
    .neon-text { color: #FFD700; text-shadow: 0 0 30px rgba(255,215,0,0.8); font-weight: 800; }
    h1 { font-size: 3.5rem !important; }
    </style>
    """, unsafe_allow_html=True)

# =========================
# 2. FIXED IMAGE PROCESSING FUNCTION (Line 97 Error Fixed)
# =========================
def add_professional_text(image_bytes, leader_name, slogan, font_style="modern"):
    """Enhanced text overlay with shadows, gradients & Hindi support - FIXED"""
    img = Image.open(io.BytesIO(image_bytes)).convert("RGBA")
    draw = ImageDraw.Draw(img)
    width, height = img.size
    
    # Dynamic Font Sizing
    font_size_main = int(height * 0.09)
    font_size_sub = int(height * 0.065)
    
    # Hindi Font Handling (Auto-detect available fonts)
    font_dir = "fonts"
    hindi_fonts = []
    if os.path.exists(font_dir):
        hindi_fonts = [f for f in os.listdir(font_dir) if f.endswith(('.ttf', '.otf'))]
    
    try:
        if hindi_fonts:
            font_main = ImageFont.truetype(os.path.join(font_dir, hindi_fonts[0]), font_size_main)
            font_sub = ImageFont.truetype(os.path.join(font_dir, hindi_fonts[0]), font_size_sub)
        else:
            font_main = ImageFont.load_default()
            font_sub = ImageFont.load_default()
    except:
        font_main = ImageFont.load_default()
        font_sub = ImageFont.load_default()
    
    # ✅ FIXED: Proper string splitting with correct quotes
    lines_main = leader_name.split('
')      # ← यहाँ था error
    lines_sub = slogan.split('
')
    
    # Main Title (White with Gold Shadow)
    y_offset = height * 0.72
    for i, line in enumerate(lines_main):
        bbox = draw.textbbox((0, 0), line, font=font_main)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) / 2
        
        # Shadow Effect
        draw.text((x+3, y_offset+3*i+3), line, font=font_main, fill="black")
        draw.text((x, y_offset+3*i), line, font=font_main, fill="white")
    
    # Slogan (Gold Gradient)
    y_offset_slogan = height * 0.82
    for i, line in enumerate(lines_sub):
        bbox = draw.textbbox((0, 0), line, font=font_sub)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) / 2
        
        # Gold Shadow
        draw.text((x+2, y_offset_slogan+3*i+2), line, font=font_sub, fill="#CC5500")
        draw.text((x, y_offset_slogan+3*i), line, font=font_sub, fill="#FFD700")
    
    # Add QR Code Placeholder (Bottom Right)
    qr_size = int(height * 0.12)
    qr_placeholder = Image.new('RGBA', (qr_size, qr_size), (255,255,255,128))
    img.paste(qr_placeholder, (width - qr_size - 40, height - qr_size - 40), qr_placeholder)
    
    # Convert back to RGB for PNG
    background = Image.new('RGB', img.size, (0, 0, 0))
    background.paste(img, mask=img.split()[-1])
    
    byte_io = io.BytesIO()
    background.save(byte_io, 'PNG', quality=95)
    return byte_io.getvalue()

# =========================
# 3. STATE & API MANAGEMENT v10
# =========================
if 'pro_credits' not in st.session_state:
    st.session_state.pro_credits = 15
SEGMIND_API = st.secrets.get("SEGMIND_API_KEY", "")
ELEVEN_API = st.secrets.get("ELEVENLABS_API_KEY", "")

# =========================
# 4. ENHANCED SIDEBAR v10 (Remaining code same as before...)
# =========================
with st.sidebar:
    st.markdown("""
    <div class='glass-card' style='text-align:center; margin:10px 0;'>
        <h3 class='neon-text'>🚀 Vixan Pro v10.0</h3>
        <p>Patna AI Studio</p>
    </div>
    """, unsafe_allow_html=True)
    
    menu = st.radio("🎯 Quick Navigation", [
        "🏠 Dashboard", "🖼️ Poster Lab Pro", "🎙️ Voice Studio", 
        "🎞️ Video Magic", "⚙️ Templates", "💳 Upgrade Pro"
    ])
    
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔥 Free Trial (15 Credits)"):
            st.session_state.pro_credits = 15
            st.success("✅ Trial Activated!")
            st.rerun()
    with col2:
        st.metric("⭐ Credits", st.session_state.pro_credits)
    
    st.caption("📅 Jan 11, 2026 | Made in Bihar 🇮🇳")

# बाकी का code same रहेगा... (Dashboard, Poster Lab, Voice Studio सब same)
# सिर्फ line 97 को fix किया गया है

if menu == "🖼️ Poster Lab Pro":
    st.markdown("<h2 class='neon-text'>🖼️ **Ultimate AI Poster Generator**</h2>", unsafe_allow_html=True)
    
    col_main, col_adv = st.columns([2,1])
    
    with col_main:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        leader_name = st.text_area("👤 **Leader/Brand Name**:", "नितिन गडकरी
Union Minister", height=80)
        slogan = st.text_area("🏷️ **Hindi Slogan**:", "विकास की नई ऊँचाइयों तक
सुरक्षित भारत", height=80)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col_adv:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        font_dir = "fonts"
        if os.path.exists(font_dir):
            fonts = [f for f in os.listdir(font_dir) if f.endswith(('.ttf', '.otf'))]
            selected_font = st.selectbox("🅰️ Hindi Font:", fonts)
            font_path = os.path.join(font_dir, selected_font)
        else:
            st.warning("📁 Create 'fonts' folder & add Hindi .ttf files")
            font_path = None
        st.markdown("</div>", unsafe_allow_html=True)
    
    theme = st.selectbox("🎨 Theme", ["Political", "Business", "Festival", "Modern"])
    prompt = st.text_area("🎭 Background:", "professional political background, orange blue gradient, 8k")
    
    if st.button("🎨 **GENERATE PRO POSTER**") and st.session_state.pro_credits > 0 and font_path:
        st.session_state.pro_credits -= 1
        with st.spinner("🤖 AI Generating..."):
            w, h = 1024, 1024
            bg_url = f"https://image.pollinations.ai/prompt/{prompt.replace(' ','%20')}?width={w}&height={h}"
            bg_data = requests.get(bg_url).content
            final_poster = add_professional_text(bg_data, leader_name, slogan, font_path)
            st.image(final_poster, use_container_width=True)
            st.download_button("💾 Download", final_poster, "vixan_poster.png")

# Footer
st.markdown("---")
st.markdown("👨‍💻 **Patna AI Studio** | Vixan Pro v10.0 | Made in Bihar 🇮🇳")
