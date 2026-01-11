import streamlit as st
import requests
import uuid
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont
import io

# Page config
st.set_page_config(page_title="Vixan AI Pro", layout="wide", page_icon="🚀")

# Clean CSS - No complex strings
st.markdown("""
<style>
.main {background: linear-gradient(135deg, #0a0e17 0%, #1a1f2e 100%);}
div.stButton > button {background: linear-gradient(45deg, #FFD700, #FFA500); 
color: black; border-radius: 15px; font-weight: 700; border: none; 
height: 3.5em; width: 100%; box-shadow: 0 8px 25px rgba(255,215,0,0.4);}
.glass-card {background: rgba(22,27,34,0.9); border-radius: 20px; padding: 25px; 
border: 1px solid #FFD700; box-shadow: 0 15px 35px rgba(0,0,0,0.5);}
.neon {color: #FFD700; font-weight: 800;}
</style>
""", unsafe_allow_html=True)

# SIMPLE & SAFE TEXT OVERLAY FUNCTION - NO STRING ERRORS
def create_poster(bg_data, title, subtitle):
    img = Image.open(io.BytesIO(bg_data)).convert("RGBA")
    draw = ImageDraw.Draw(img)
    w, h = img.size
    
    # Safe default font
    try:
        font_large = ImageFont.truetype("arial.ttf", int(h * 0.08))
        font_small = ImageFont.truetype("arial.ttf", int(h * 0.06))
    except:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # SAFE STRING PROCESSING - NO SPLIT ERRORS
    title_lines = title.splitlines()
    subtitle_lines = subtitle.splitlines()
    
    # Title (Top)
    y = h * 0.7
    for line in title_lines:
        bbox = draw.textbbox((0,0), line, font=font_large)
        x = (w - (bbox[2] - bbox[0])) / 2
        draw.text((x+2, y), line, font=font_large, fill="black")
        draw.text((x, y), line, font=font_large, fill="white")
        y += 45
    
    # Subtitle (Bottom)
    y = h * 0.82
    for line in subtitle_lines:
        bbox = draw.textbbox((0,0), line, font=font_small)
        x = (w - (bbox[2] - bbox[0])) / 2
        draw.text((x+2, y), line, font=font_small, fill="#CC5500")
        draw.text((x, y), line, font=font_small, fill="#FFD700")
        y += 35
    
    # QR Box
    qr_w = int(h * 0.12)
    qr_box = Image.new('RGBA', (qr_w, qr_w), (255,255,255,80))
    img.paste(qr_box, (w-qr_w-30, h-qr_w-30), qr_box)
    
    # Save
    final_img = Image.new('RGB', img.size, (10,10,20))
    final_img.paste(img, mask=img.split()[-1])
    buffer = io.BytesIO()
    final_img.save(buffer, 'PNG')
    return buffer.getvalue()

# Session state
if 'credits' not in st.session_state:
    st.session_state.credits = 8

# Sidebar
with st.sidebar:
    st.markdown("""
    <div class='glass-card' style='text-align:center;'>
    <h3 class='neon'>🚀 Vixan Pro</h3>
    <p>Patna AI Studio</p>
    </div>
    """, unsafe_allow_html=True)
    
    menu = st.radio("Menu", ["🏠 Home", "🖼️ Poster", "🎙️ Voice"])
    
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔥 Trial"):
            st.session_state.credits = 8
            st.rerun()
    with col2:
        st.metric("Credits", st.session_state.credits)

# PAGES
if menu == "🏠 Home":
    st.markdown("<h1 class='neon'>Vixan AI Studio Pro</h1>", unsafe_allow_html=True)
    st.markdown("<h3>Bihar's #1 AI Platform</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1: st.metric("Posters", "4.2K")
    with col2: st.metric("Voices", "2.8K") 
    with col3: st.metric("Users", "1.5K")
    
    st.markdown("""
    <div class='glass-card'>
    <h4>✅ Features:</h4>
    • AI Poster Generator<br>
    • Hindi Text Overlay<br>
    • Voice Studio<br>
    • QR Code Auto
    </div>
    """, unsafe_allow_html=True)

elif menu == "🖼️ Poster":
    st.markdown("<h2 class='neon'>AI Poster Maker</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1.2, 1])
    
    with col1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        title = st.text_area("Title", "नितिन गडकरी
सांसद", height=90)
        subtitle = st.text_area("Slogan", "विकास का नया दौर
बिहार 2025", height=90)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        prompt = st.text_area("Background", "political poster background orange saffron gradient", height=120)
        st.markdown("</div>", unsafe_allow_html=True)
    
    if st.button("🎨 CREATE POSTER", type="primary") and st.session_state.credits > 0:
        st.session_state.credits -= 1
        
        with st.spinner("AI Processing..."):
            url = f"https://image.pollinations.ai/prompt/{prompt.replace(' ','%20')}?width=1024&height=1024"
            bg = requests.get(url).content
            
            poster = create_poster(bg, title, subtitle)
            
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.image(poster, use_container_width=True)
            
            col_dl1, col_dl2 = st.columns(2)
            with col_dl1:
                st.download_button("💾 PNG", poster, f"poster_{uuid.uuid4().hex[:8]}.png")
            with col_dl2:
                st.success(f"Credits: {st.session_state.credits}")
            st.markdown("</div>", unsafe_allow_html=True)

elif menu == "🎙️ Voice":
    st.markdown("<h2 class='neon'>Voice Generator</h2>", unsafe_allow_html=True)
    text = st.text_area("Hindi Text", "नमस्कार! पटना एआई स्टूडियो में आपका स्वागत है।")
    
    if st.button("🔊 Generate Voice", type="primary"):
        tts = gTTS(text=text, lang='hi', slow=False)
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        
        st.audio(audio_buffer.getvalue())
        st.download_button("MP3", audio_buffer.getvalue(), "voice.mp3")

# Footer  
st.markdown("---")
st.markdown("<p style='text-align:center;color:#888;'>Patna AI Studio | Vixan Pro | Made in Bihar 🇮🇳</p>", unsafe_allow_html=True)
