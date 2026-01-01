import streamlit as st
import requests
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import io
import urllib.parse
import time
import base64
import os
from streamlit_option_menu import option_menu

# --- PAGE CONFIG ---
st.set_page_config(page_title="💎 Patna AI Studio Pro", page_icon="💎", layout="wide")

# --- LUXURY UI DESIGN ---
st.markdown("""
<style>
.luxury-title {color: #ffd700; font-size: 3.5rem; text-align: center; text-shadow: 0 0 20px rgba(255,215,0,0.5);}
.feature-box {background: rgba(255,215,0,0.05); border: 2px solid #ffd700; border-radius: 20px; padding: 20px;}
.stButton>button {background: linear-gradient(45deg, #ffd700, #ffed4e); color: #1a1a2e; font-weight: bold; border-radius: 20px; width: 100%;}
</style>
""", unsafe_allow_html=True)

# --- ENGINE LOGIC ---
def generate_premium_image(prompt):
    """Segmind API Integration"""
    try:
        api_key = st.secrets.get("SEGMIND_API_KEY") #
        if not api_key: return None
        url = "https://api.segmind.com/v1/sdxl1.0-txt2img"
        payload = {"prompt": prompt, "negative_prompt": "blurry, low quality", "width": 1024, "height": 1024, "steps": 25}
        headers = {"x-api-key": api_key}
        resp = requests.post(url, json=payload, headers=headers, timeout=60)
        if resp.status_code == 200:
            return base64.b64decode(resp.json()['images'][0])
    except: return None

def generate_free_image(prompt):
    """Pollinations AI Integration"""
    url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt)}?width=1024&height=1024&nologo=true"
    try:
        resp = requests.get(url, timeout=25)
        return resp.content if resp.status_code == 200 else None
    except: return None

@st.cache_resource
def load_hindi_font():
    """Load Devanagari Font"""
    paths = ["NotoSansDevanagari-VariableFont_wdth,wght.ttf", "NotoSansDevanagari-Regular.ttf"]
    for p in paths:
        if os.path.exists(p): return ImageFont.truetype(p, 45) #
    return ImageFont.load_default()

fonts = load_hindi_font()

# --- IMAGE OVERLAY LOGIC ---
def create_ad_overlay(img_bytes, shop, prod, offer, contact, land, addr):
    img = Image.open(io.BytesIO(img_bytes)).convert("RGBA")
    w, h = img.size
    overlay = Image.new("RGBA", (w, h), (0,0,0,0))
    draw = ImageDraw.Draw(overlay)
    
    # Bottom Dark Gradient
    draw.rectangle([0, h - (h//2.5), w, h], fill=(0,0,0,190))
    y = h - (h//2.5) + 30

    # Draw Text with Anchor='mm' for perfect centering
    draw.text((w//2, y), f"✨ {shop.upper()} ✨", fill="#ffd700", font=fonts, anchor="mm")
    draw.text((w//2, y+65), f"🔥 {prod} - {offer}", fill="#ffed4e", font=fonts, anchor="mm")
    draw.text((w//2, y+120), f"📞 {contact}", fill="white", font=fonts, anchor="mm")
    
    if land:
        draw.text((w//2, y+170), f"📍 {land}", fill="#e8f4fd", font=fonts, anchor="mm")
    
    if addr:
        lines = [l.strip() for l in addr.split('\n') if l.strip()][:2] #
        for i, line in enumerate(lines):
            draw.text((w//2, y+215+(i*35)), f"📬 {line}", fill="#d4e6f1", font=fonts, anchor="mm")

    result = Image.alpha_composite(img, overlay).convert("RGB")
    final = ImageEnhance.Sharpness(result).enhance(1.2)
    buf = io.BytesIO()
    final.save(buf, "PNG", quality=95)
    return buf.getvalue()

# --- MAIN UI ---
st.markdown('<h1 class="luxury-title">💎 पटना AI स्टूडियो प्रो</h1>', unsafe_allow_html=True)

with st.sidebar:
    selected = option_menu("मेन्यू", ["🚀 AI ऐड मेकर"], icons=["cast"])
    use_premium = st.checkbox("⭐ Use Premium Engine (Segmind)", value=False)
    st.info("Patna AI Studio v4.0 - Ready to Deploy! 🇮🇳")

if selected == "🚀 AI ऐड मेकर":
    col1, col2 = st.columns([1.2, 1])
    with col1:
        shop = st.text_input("🏪 दुकान का नाम", "पटना ज्वेलर्स")
        prod = st.text_input("📦 प्रोडक्ट", "Diamond Set")
        off = st.text_input("🎁 ऑफर", "50% OFF")
        num = st.text_input("📞 संपर्क", "8210073056")
    with col2:
        land = st.text_input("📍 लैंडमार्क", "फ्रेजर रोड")
        addr = st.text_area("🏠 पूरा पता", "पटना सिटी\nबिहार 800001")

    if st.button("✨ प्रोफेशनल ऐड बनाएं"):
        if shop and prod:
            with st.spinner("🎨 AI Magic in Progress..."):
                prompt = f"Luxury advertisement for {shop}, {prod}, cinematic lighting, 8k"
                img_data = generate_premium_image(prompt) if use_premium else generate_free_image(prompt)
                
                if not img_data: img_data = generate_free_image(prompt) # Fallback
                
                if img_data:
                    final_ad = create_ad_overlay(img_data, shop, prod, off, num, land, addr)
                    st.image(final_ad, use_container_width=True)
                    st.download_button("⬇️ HD डाउनलोड", final_ad, "ad.png", use_container_width=True)
                    st.balloons()
                else: st.error("AI Busy! Dobara try karein.")
        else: st.warning("Dukan aur Product bharein!")

st.markdown("---")
st.markdown("<center>© 2026 Patna AI Studio Pro | Made in Bihar</center>", unsafe_allow_html=True)

