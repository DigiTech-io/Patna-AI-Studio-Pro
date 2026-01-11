import streamlit as st
import os
import requests
import uuid
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont
import io

# =========================
# 1. PAGE SETUP & THEME
# =========================
st.set_page_config(page_title="Vixan AI Pro v9.0", layout="wide", page_icon="🚀")

st.markdown("""
    <style>
    .main { background: #0a0e17; color: white; }
    div.stButton > button {
        background: linear-gradient(45deg, #FFD700, #FFA500);
        color: black; border-radius: 12px; font-weight: bold; border: none; height: 3.5em;
    }
    .status-box { padding: 20px; border-radius: 15px; background: #161b22; border: 1px solid #FFD700; }
    </style>
    """, unsafe_allow_html=True)

# =========================
# 2. IMAGE HELPER FUNCTION (Writing Text on Image)
# =========================
def add_text_to_image(image_bytes, text_top, text_bottom, font_path):
    img = Image.open(io.BytesIO(image_bytes))
    draw = ImageDraw.Draw(img)
    width, height = img.size
    
    # Font Size Calculation
    font_size_top = int(height * 0.08)
    font_size_bottom = int(height * 0.06)
    
    try:
        font_top = ImageFont.truetype(font_path, font_size_top)
        font_bottom = ImageFont.truetype(font_path, font_size_bottom)
    except:
        font_top = ImageFont.load_default()
        font_bottom = ImageFont.load_default()

    # Draw Top Text (Leader Name)
    w_top, h_top = draw.textbbox((0, 0), text_top, font=font_top)[2:]
    draw.text(((width - w_top) / 2, height * 0.75), text_top, font=font_top, fill="white", stroke_width=2, stroke_fill="black")

    # Draw Bottom Text (Slogan)
    w_bot, h_bot = draw.textbbox((0, 0), text_bottom, font=font_bottom)[2:]
    draw.text(((width - w_bot) / 2, height * 0.85), text_bottom, font=font_bottom, fill="#FFD700", stroke_width=2, stroke_fill="black")
    
    # Save back to bytes
    byte_io = io.BytesIO()
    img.save(byte_io, 'PNG')
    return byte_io.getvalue()

# =========================
# 3. SIDEBAR & MENU
# =========================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=80)
    st.title("Vixan Studio v9.0")
    menu = st.radio("Navigation", ["🏠 Home", "🖼️ AI Poster Lab", "🎙️ Voice Studio", "🎞️ Video Clone"])
    st.divider()
    st.caption("Developed by Patna AI Studio")

# =========================
# 4. AI POSTER LAB (With Fonts & Text)
# =========================
if menu == "🖼️ AI Poster Lab":
    st.header("🖼️ AI Poster Lab with Smart Text")
    
    col_input, col_preview = st.columns([1, 1.2])
    
    with col_input:
        st.markdown("### 🖋️ Design Details")
        leader_name = st.text_input("Leader Name / Brand:", "आपका नाम यहाँ")
        slogan = st.text_input("Hindi Slogan:", "आपका विश्वास, हमारा विकास")
        
        # Font Selector from your 'fonts' folder
        font_dir = "fonts"
        available_fonts = [f for f in os.listdir(font_dir) if f.endswith(".ttf")] if os.path.exists(font_dir) else []
        selected_font = st.selectbox("Choose Hindi Font Style:", available_fonts) if available_fonts else st.info("Please upload fonts to 'fonts' folder.")
        
        prompt = st.text_area("Background Prompt (English):", "Professional political background, orange and blue gradients, high quality, 4k")
        
        gen_btn = st.button("🚀 Generate & Write Text")

    with col_preview:
        if gen_btn and selected_font:
            with st.spinner("AI is generating background & writing text..."):
                # 1. Get Background from Pollinations
                bg_url = f"https://image.pollinations.ai/prompt/{prompt.replace(' ','%20')}?width=1024&height=1024&nologo=true"
                bg_data = requests.get(bg_url).content
                
                # 2. Add Text using Pillow
                font_path = os.path.join(font_dir, selected_font)
                final_poster = add_text_to_image(bg_data, leader_name, slogan, font_path)
                
                # 3. Display Result
                st.image(final_poster, caption="Vixan AI Generated Poster", use_container_width=True)
                st.download_button("📥 Download HD Poster", final_poster, "vixan_poster.png", "image/png")
        else:
            st.info("Fill details and select a font to generate.")

# =========================
# 5. VOICE & VIDEO (Simplified for stability)
# =========================
elif menu == "🎙️ Voice Studio":
    st.header("🎙️ Advanced Voice Studio")
    text = st.text_area("Hindi Text:", "नमस्ते, वीक्सन एआई स्टूडियो में आपका स्वागत है।")
    if st.button("📢 Generate Voice"):
        tts = gTTS(text=text, lang='hi')
        tts.save("v.mp3")
        st.audio("v.mp3")

elif menu == "🏠 Home":
    st.title("Vixan AI Media Studio Pro")
    st.image("https://img.freepik.com/free-vector/gradient-liquid-3d-shapes_108944-2758.jpg", use_container_width=True)
