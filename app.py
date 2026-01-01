import streamlit as st
import requests
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import io
import urllib.parse
import time
import base64
import os
from streamlit_option_menu import option_menu

# --- 1. RESPONSIVE SETUP ---
st.set_page_config(page_title="Patna AI Studio Pro", layout="wide")

st.markdown("""
<style>
    .main { background-color: #0e1117; }
    .luxury-text { color: #ffd700; text-align: center; font-family: 'serif'; }
    /* Mobile optimization */
    @media (max-width: 600px) { .luxury-title { font-size: 2rem !important; } }
</style>
""", unsafe_allow_html=True)

# --- 2. BULLETPROOF HINDI FONT ---
@st.cache_resource
def get_pro_font(size=50):
    font_paths = ["NotoSansDevanagari-Regular.ttf", "NotoSansDevanagari-VariableFont_wdth,wght.ttf"]
    for path in font_paths:
        if os.path.exists(path):
            return ImageFont.truetype(path, size) #
    return ImageFont.load_default()

# --- 3. PREMIUM AI ENGINE (FIXED) ---
def generate_pro_image(prompt, is_premium):
    if is_premium:
        api_key = st.secrets.get("SEGMIND_API_KEY") #
        if api_key:
            try:
                url = "https://api.segmind.com/v1/sdxl1.0-txt2img"
                data = {"prompt": prompt, "width": 1024, "height": 1024, "steps": 30, "samples": 1}
                headers = {"x-api-key": api_key}
                resp = requests.post(url, json=data, headers=headers, timeout=60)
                if resp.status_code == 200:
                    return base64.b64decode(resp.json()['images'][0])
            except: pass
    
    # FREE FALLBACK
    free_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt)}?width=1024&height=1024&nologo=true&seed={int(time.time())}"
    return requests.get(free_url).content

# --- 4. SMART OVERLAY (CENTERED & SHARP) ---
def apply_pro_overlay(img_bytes, shop, prod, off, num, land, addr):
    img = Image.open(io.BytesIO(img_bytes)).convert("RGBA")
    draw = ImageDraw.Draw(img)
    w, h = img.size
    f_h = get_pro_font(55)
    f_s = get_pro_font(35)

    # Gradient Bottom Shadow
    overlay = Image.new("RGBA", img.size, (0,0,0,0))
    d_ov = ImageDraw.Draw(overlay)
    d_ov.rectangle([0, h*0.65, w, h], fill=(0,0,0,180))
    img = Image.alpha_composite(img, overlay)
    draw = ImageDraw.Draw(img)

    y = h * 0.7
    # Text with Anchor 'mm' for perfect centering
    draw.text((w/2, y), f"✨ {shop} ✨", fill="#ffd700", font=f_h, anchor="mm")
    draw.text((w/2, y+70), f"🔥 {prod} | {off}", fill="#ffed4e", font=f_s, anchor="mm")
    draw.text((w/2, y+130), f"📞 WhatsApp: {num} | 📍 {land}", fill="white", font=f_s, anchor="mm")
    
    # Address Lines
    if addr:
        lines = addr.split('\n')[:2] #
        for i, line in enumerate(lines):
            draw.text((w/2, y+180+(i*40)), f"📬 {line}", fill="#d4e6f1", font=f_s, anchor="mm")

    # Final Polish
    img = img.convert("RGB")
    img = ImageEnhance.Sharpness(img).enhance(1.4)
    img = ImageEnhance.Contrast(img).enhance(1.1)
    
    buf = io.BytesIO()
    img.save(buf, "PNG", quality=100)
    return buf.getvalue()

# --- 5. UI INTERFACE ---
st.markdown("<h1 class='luxury-title'>💎 PATNA AI STUDIO PRO v5.1</h1>", unsafe_allow_html=True)

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
    is_premium = st.checkbox("⭐ Use Segmind Premium Engine", value=True)
    st.info("Ensure API Key is in Secrets for Pro Quality!")

# Input Fields
col1, col2 = st.columns([1, 1])
with col1:
    shop = st.text_input("🏪 Business Name (Hindi/Eng)", "भवानी किराना स्टोर")
    prod = st.text_input("📦 Product", "शुद्ध देसी घी")
    off = st.text_input("🎁 Offer", "10% Discount")
with col2:
    num = st.text_input("📞 Number", "8210073056")
    land = st.text_input("📍 Landmark", "Main Road, Patna")
    addr = st.text_area("🏠 Address", "Patna City\nBihar")

if st.button("🚀 CREATE PRO AD", use_container_width=True):
    with st.spinner("💎 Crafting your Premium Ad..."):
        # AI prompt selection based on shop name
        prompt = f"Professional commercial photography of {prod} in an Indian {shop}, 8k cinematic lighting, luxury style"
        img_raw = generate_pro_image(prompt, is_premium)
        
        if img_raw:
            final_ad = apply_pro_overlay(img_raw, shop, prod, off, num, land, addr)
            st.image(final_ad, use_container_width=True)
            st.download_button("⬇️ Download HD Ad", final_ad, "pro_ad.png", "image/png", use_container_width=True)

