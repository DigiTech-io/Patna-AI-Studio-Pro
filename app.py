import streamlit as st
import requests
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
import io
import urllib.parse
import time
import base64
import os
from streamlit_option_menu import option_menu
import numpy as np

st.set_page_config(page_title="💎 Patna AI Studio Pro v3.0", page_icon="💎", layout="wide")

# Luxury CSS
st.markdown("""
<style>
.luxury-title {color: #ffd700; font-size: 4.5rem; text-align: center; text-shadow: 0 0 40px #ffd700;}
.gold-btn {background: linear-gradient(45deg, #ffd700, #ffed4e); color: #1a1a2e; font-weight: 700; border-radius: 25px; box-shadow: 0 8px 25px rgba(255,215,0,0.4);}
.feature-box {background: rgba(255,215,0,0.1); border: 2px solid rgba(255,215,0,0.3); border-radius: 25px; padding: 2.5rem;}
.music-selector {background: linear-gradient(135deg, #667eea, #764ba2); border-radius: 15px; padding: 1rem;}
</style>
""", unsafe_allow_html=True)

# === ENHANCED PROMPT BUILDER ===
def build_pro_prompt(shop_name, product, offer, style="Luxury", language="Hindi", landmark=""):
    """Ultimate AI Prompt Generator"""
    
    # Core Business Context
    base = f"Professional {style} advertisement for '{shop_name}' - Premium {product}"
    
    # Dynamic Offer Integration
    if offer:
        base += f" with exclusive '{offer}' promotion"
    
    # Location Context
    if landmark:
        base += f", located at {landmark}"
    
    # AI Quality Directives (Pro Keywords)
    quality = [
        "Cinematic studio lighting",
        "8K ultra resolution", 
        "Elegant golden accents",
        "Sharp hyper-detailed focus",
        "Luxury product showcase",
        "Professional photography",
        "Perfect composition",
        "Masterpiece quality"
    ]
    
    # Cultural Enhancement
    if language == "Hindi":
        quality.extend([
            "Rich Indian heritage colors",
            "Warm golden hour lighting", 
            "Traditional-modern fusion aesthetic"
        ])
    
    return f"{base}. {' | '.join(quality)}"

# === ROBUST FONT SYSTEM ===
@st.cache_resource
def load_fonts():
    font_paths = [
        "NotoSansDevanagari-VariableFont_wdth,wght.ttf",
        "NotoSans-Regular.ttf"
    ]
    sizes = {"title": 72, "subtitle": 52, "info": 38, "small": 28}
    fonts = {}
    
    for name, size in sizes.items():
        for path in font_paths:
            try:
                if os.path.exists(path):
                    fonts[name] = ImageFont.truetype(path, size)
                    break
            except:
                pass
        if name not in fonts:
            fonts[name] = ImageFont.load_default()
    
    return fonts

fonts = load_fonts()

# === AI IMAGE GENERATION ===
@st.cache_data(ttl=1800)
def generate_image(prompt, width=1024, height=1024):
    """Multi-API Fallback"""
    apis = [
        f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt)}?width={width}&height={height}&nologo=true&seed={int(time.time()*1000)}"
    ]
    
    for url in apis:
        try:
            resp = requests.get(url, timeout=25)
            if resp.status_code == 200:
                return resp.content
        except:
            continue
    return None

# === PROTECTED TEXT OVERLAY ===
def add_luxury_overlay(img_bytes, shop_name, product, offer, contact, landmark, address):
    img = Image.open(io.BytesIO(img_bytes)).convert("RGBA")
    width, height = img.size
    
    # Dark Protective Rectangle (35% bottom)
    text_h = int(height * 0.38)
    mask = Image.new('RGBA', (width, text_h), (0,0,0,0))
    draw_mask = ImageDraw.Draw(mask)
    
    # Smooth Gradient Background
    for y in range(text_h):
        alpha = int(240 * min(1, (y / text_h) ** 0.8))
        draw_mask.rectangle([0, y, width, y+2], fill=(15, 25, 45, alpha))
    
    # Blur for Premium Effect
    mask = mask.filter(ImageFilter.GaussianBlur(12))
    
    # Composite
    result = Image.alpha_composite(img, mask)
    draw = ImageDraw.Draw(result)
    
    y = height - text_h + 25
    
    # TITLE w/ Shadow
    title = f"✨ {shop_name.upper()} ✨"
    bbox = draw.textbbox((0,0), title, font=fonts["title"])
    tw = bbox[2] - bbox[0]
    draw.text((width//2 - tw//2 + 3, y + 3), title, fill="black", font=fonts["title"])
    draw.text((width//2 - tw//2, y), title, fill="#ffd700", font=fonts["title"])
    y += 85
    
    # OFFER
    offer_t = f"🔥 {product} | {offer}"
    bbox = draw.textbbox((0,0), offer_t, font=fonts["subtitle"])
    tw = bbox[2] - bbox[0]
    draw.text((width//2 - tw//2, y), offer_t, fill="#ffed4e", font=fonts["subtitle"])
    y += 70
    
    # CONTACT
    contact_t = f"📞 {contact}"
    bbox = draw.textbbox((0,0), contact_t, font=fonts["info"])
    tw = bbox[2] - bbox[0]
    draw.text((width//2 - tw//2, y), contact_t, fill="white", font=fonts["info"])
    y += 50
    
    # LANDMARK
    if landmark:
        lm_t = f"📍 {landmark}"
        bbox = draw.textbbox((0,0), lm_t, font=fonts["small"])
        tw = bbox[2] - bbox[0]
        draw.text((width//2 - tw//2, y), lm_t, fill="#e8f4fd", font=fonts["small"])
        y += 38
    
    # ADDRESS
    if address:
        lines = address.split('
')[:2]
        for line in lines:
            if line.strip():
                addr_t = f"📬 {line.strip()}"
                bbox = draw.textbbox((0,0), addr_t, font=fonts["small"])
                tw = bbox[2] - bbox[0]
                draw.text((width//2 - tw//2, y), addr_t, fill="#d4e6f1", font=fonts["small"])
                y += 35
    
    # Save Ultra Quality
    buf = io.BytesIO()
    result.convert("RGB").save(buf, "PNG", quality=99, optimize=True)
    return buf.getvalue()

# === MUSIC VIDEO ===
def create_music_video(img_bytes, music_style="energetic", duration=7):
    try:
        from moviepy.editor import ImageClip, AudioFileClip, vfx
        
        music_files = {
            "energetic": "music/energetic.mp3",
            "calm": "music/calm.mp3", 
            "traditional": "music/traditional.mp3"
        }
        
        img = Image.open(io.BytesIO(img_bytes))
        clip = (ImageClip(np.array(img), duration=duration)
                .resize(lambda t: 1 + 0.03 * t)  # Zoom
                .set_position('center')
                .fx(vfx.fadein, 1).fx(vfx.fadeout, 1))
        
        music_path = music_files.get(music_style)
        if os.path.exists(music_path):
            audio = (AudioFileClip(music_path).subclip(0, duration)
                    .volumex(0.35).fx(vfx.audio_fadein, 1).fx(vfx.audio_fadeout, 1))
            clip = clip.set_audio(audio)
        
        buf = io.BytesIO()
        clip.write_videofile(buf, fps=30, codec='libx264', audio_codec='aac',
                           temp_audiofile='temp.m4a', remove_temp=True, verbose=False)
        return buf.getvalue()
    except:
        return None

# === MAIN UI ===
st.markdown('<h1 class="luxury-title">💎 पटना AI स्टूडियो प्रो v3.0</h1>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 🎵 Music Styles")
    music_style = st.radio("🎼 बैकग्राउंड म्यूजिक:", 
                          ["Energetic 🚀", "Calm 😌", "Traditional 🇮🇳"], 
                          format_func=lambda x: x.split()[1:])
    
    selected = option_menu("💎 फीचर्स", ["🚀 AI ऐड मेकर"], icons=["cast"])

# MAIN AD CREATOR
st.markdown('<div class="feature-box"><h2>🎨 अल्टिमेट लग्ज़री ऐड</h2></div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.subheader("🏪 बिज़नेस डिटेल्स")
    shop_name = st.text_input("नाम", "पटना ज्वेलर्स")
    product = st.text_input("प्रोडक्ट", "Diamond Necklace")
    offer = st.text_input("ऑफर", "50% OFF")
    contact = st.text_input("📞", "8210073056")

with col2:
    st.subheader("📍 लोकेशन")
    landmark = st.text_input("लैंडमार्क", "फ्रेजर रोड")
    address = st.text_area("पूरा पता", "पटना सिटी, बिहार", height=70)

col1, col2 = st.columns(2)
video_mode = col1.checkbox("🎥 Music Video बनाएं")
premium = col2.checkbox("⭐ Fast AI")

if st.button("✨ CREATE LUXURY AD", key="pro", help="Ultimate Magic!"):
    if shop_name and product:
        with st.spinner("💎 Pro AI Processing..."):
            prompt = build_pro_prompt(shop_name, product, offer, "Luxury", "Hindi", landmark)
            img_bytes = generate_image(prompt)
            
            if img_bytes:
                final_img = add_luxury_overlay(img_bytes, shop_name, product, offer, 
                                             contact, landmark, address)
                
                st.image(final_img, use_container_width=True)
                
                # Downloads
                st.download_button("⬇️ Ultra PNG", final_img, f"{shop_name}_ad.png")
                
                # MUSIC VIDEO
                if video_mode:
                    with st.spinner("🎬 Creating Music Video..."):
                        video_bytes = create_music_video(final_img, music_style.lower())
                        if video_bytes:
                            st.video(video_bytes)
                            st.download_button("🎥 MP4 + Music", video_bytes, f"{shop_name}_video.mp4")
                        else:
                            st.success("✅ PNG ready! Video needs music files.")
            else:
                st.error("🌐 AI busy, retry!")

# DEPLOYMENT GUIDE
with st.expander("📋 Deployment Guide"):
    st.markdown("""
    **✅ Ready to Deploy!**
    
    1. **GitHub Repo बनाएं**
    2. ऊपर files upload करें  
    3. Streamlit Cloud → New App → Select Repo
    4. **Auto Deploy!** 🎉
    """)
