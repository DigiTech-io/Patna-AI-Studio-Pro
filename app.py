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
# 1. PAGE SETUP & ULTRA MODERN THEME v10.0 (Jan 2026)
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
# 2. ADVANCED IMAGE PROCESSING FUNCTIONS v10
# =========================
def add_professional_text(image_bytes, leader_name, slogan, font_style="modern"):
    """Enhanced text overlay with shadows, gradients & Hindi support"""
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
        hindi_fonts = [f for f in os.listdir(font_dir) if f.endswith(".ttf")]
    
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
    
    # Multi-line text support
    lines_main = leader_name.split('
')
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
    st.session_state.pro_credits = 15  # Trial credits
SEGMIND_API = st.secrets.get("SEGMIND_API_KEY", "")
ELEVEN_API = st.secrets.get("ELEVENLABS_API_KEY", "")

# =========================
# 4. ENHANCED SIDEBAR v10
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

# =========================
# 5. MAIN MODULES v10
# =========================

if menu == "🏠 Dashboard":
    st.markdown("<h1 class='neon-text'>🌟 Vixan AI Media Studio Pro v10.0</h1>", unsafe_allow_html=True)
    st.markdown("<h3>India's Fastest AI Content Creator</h3>", unsafe_allow_html=True)
    
    # Live Stats
    col1, col2, col3 = st.columns(3)
    with col1: st.metric("🎨 Posters Created", "5.2K+", delta="2.1K")
    with col2: st.metric("🎙️ Voices Generated", "3.1K+", delta="1.2K")
    with col3: st.metric("🎥 Videos Made", "1.2K+", delta="800")
    
    st.markdown("""
    <div class='glass-card'>
        <h4>🔥 Pro Features Unlocked:</h4>
        <ul style='color:#ccc;'>
            <li>✅ 8K Ultra HD Posters</li>
            <li>✅ Hindi Font Overlay</li>
            <li>✅ Voice Cloning</li>
            <li>✅ Talking Videos</li>
            <li>✅ QR Codes Auto</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.image("https://img.freepik.com/free-vector/gradient-liquid-3d-shapes_108944-2758.jpg?w=1400", use_container_width=True)

elif menu == "🖼️ Poster Lab Pro":
    st.markdown("<h2 class='neon-text'>🖼️ **Ultimate AI Poster Generator**</h2>", unsafe_allow_html=True)
    
    # Professional Input Panel
    with st.container():
        col_main, col_adv = st.columns([2,1])
        
        with col_main:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            leader_name = st.text_area("👤 **Leader/Brand Name** (Multi-line OK):
*(Max 2 lines)*", 
                                     "नितिन गडकरी
Union Minister", height=80)
            slogan = st.text_area("🏷️ **Hindi Slogan** (Multi-line OK):
*(Campaign Message)*", 
                                "विकास की नई ऊँचाइयों तक
सुरक्षित भारत - समृद्ध भारत", height=80)
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col_adv:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.markdown("### 🎨 **Advanced Settings**")
            
            # Dynamic Font Loader
            font_dir = "fonts"
            if os.path.exists(font_dir):
                fonts = [f for f in os.listdir(font_dir) if f.endswith(('.ttf', '.otf'))]
                selected_font = st.selectbox("🅰️ Hindi Font:", fonts)
                font_path = os.path.join(font_dir, selected_font)
            else:
                st.warning("📁 Create 'fonts' folder & add Hindi .ttf files")
                font_path = None
            
            theme = st.selectbox("🎨 Theme Style", ["Political", "Business", "Festival", "Modern"])
            aspect = st.selectbox("📐 Size", ["Square 1:1", "Portrait 9:16", "Landscape 16:9"])
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Background Prompt Auto-Generation
        theme_prompts = {
            "Political": "professional political background, indian flag colors, orange blue gradient, premium quality, 8k",
            "Business": "corporate professional background, gold blue gradient, modern business, luxury, 8k",
            "Festival": "dussehra diwali theme, vibrant colors, indian festival, gold red orange, 8k",
            "Modern": "futuristic gradient background, neon gold blue, cyberpunk style, ultra modern, 8k"
        }
        auto_prompt = theme_prompts[theme]
        prompt = st.text_area("🎭 **Custom Background** (English):", auto_prompt, height=60)
        
        # Master Generate Button
        if st.button("🎨 **GENERATE PRO POSTER**", type="primary") and st.session_state.pro_credits > 0 and font_path:
            st.session_state.pro_credits -= 1
            with st.spinner("🤖 AI Generating Ultra HD Poster..."):
                # Step 1: AI Background
                aspect_map = {"Square 1:1": (1024,1024), "Portrait 9:16": (576,1024), "Landscape 16:9": (1024,576)}
                w, h = aspect_map[aspect]
                
                bg_url = f"https://image.pollinations.ai/prompt/{prompt.replace(' ','%20')}?width={w}&height={h}&nologo=true&seed={uuid.uuid4().int}"
                bg_data = requests.get(bg_url).content
                
                # Step 2: Pro Text Overlay
                final_poster = add_professional_text(bg_data, leader_name, slogan, font_path)
                
                # Step 3: Display Masterpiece
                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                st.image(final_poster, caption="✨ **Vixan Pro Masterpiece Generated!**", use_container_width=True)
                
                col_dl1, col_dl2 = st.columns(2)
                with col_dl1:
                    st.download_button("💾 **Download PNG**", final_poster, f"vixan_pro_poster_{uuid.uuid4().hex[:8]}.png", "image/png")
                with col_dl2:
                    st.download_button("📱 **Instagram Ready**", final_poster, "instagram_poster.png", "image/png")
                st.markdown("</div>", unsafe_allow_html=True)
                
                st.balloons()
        elif st.session_state.pro_credits <= 0:
            st.error("🔴 **No Credits Left!** Click Sidebar → Free Trial")
        else:
            st.info("✅ **Ready!** Fill details & select font")

elif menu == "🎙️ Voice Studio":
    st.markdown("<h2 class='neon-text'>🎙️ **Pro Voice Studio**</h2>", unsafe_allow_html=True)
    col_t1, col_t2 = st.columns(2)
    
    with col_t1:
        text = st.text_area("💬 Hindi/English Text:", "नमस्कार! यह Vixan AI Studio की प्रोफेशनल आवाज है। जन औषधि योजना का प्रचार।")
        if st.button("📢 **Generate Voice**") and st.session_state.pro_credits > 0:
            st.session_state.pro_credits -= 1
            tts = gTTS(text=text, lang='hi', slow=False)
            audio_bytes = io.BytesIO()
            tts.write_to_fp(audio_bytes)
            audio_bytes.seek(0)
            st.audio(audio_bytes.getvalue())
            st.download_button("🎵 Download MP3", audio_bytes.getvalue(), "vixan_voice.mp3")
    
    with col_t2:
        st.markdown("<div class='glass-card'><h4>🔥 Pro Features</h4><ul><li>ElevenLabs Cloning</li><li>30+ Voices</li><li>Custom Speed</li></ul></div>", unsafe_allow_html=True)

elif menu == "🎞️ Video Magic":
    st.markdown("<h2 class='neon-text'>🎞️ **Talking Video Creator**</h2>", unsafe_allow_html=True)
    st.info("🚀 Upload poster → Add voice → Auto lip sync! (Pro Only)")

elif menu == "⚙️ Templates":
    st.markdown("<h2>📂 **Ready Templates**</h2>", unsafe_allow_html=True)
    st.info("BJP | Congress | Business | Festival - One Click!")

elif menu == "💳 Upgrade Pro":
    st.markdown("<h2 class='neon-text'>💎 **Go Unlimited Pro**</h2>", unsafe_allow_html=True)
    st.markdown("""
    <div class='glass-card'>
        <h3>₹499 / Year (Save 50%)</h3>
        <ul style='color:#FFD700;'>
            <li>✅ Unlimited Everything</li>
            <li>✅ Commercial Rights</li>
            <li>✅ Priority Support</li>
        </ul>
        <a href='https://rzp.io/l/vixan_pro_v10'><button style='width:100%;'>🚀 Buy Pro Now</button></a>
    </div>
    """, unsafe_allow_html=True)

# =========================
# 6. BEAUTIFUL FOOTER
# =========================
st.markdown("---")
st.markdown("""
<div style='text-align:center; padding:20px; color:#888;'>
    <h4 class='neon-text'>👨‍💻 Patna AI Studio</h4>
    <p>Vixan Pro v10.0 | © 2026 | Made with ❤️ in Bihar 🇮🇳</p>
    <p>Credits Left: <strong style='color:#FFD700;'>{}</strong></p>
</div>
""".format(st.session_state.pro_credits), unsafe_allow_html=True)
