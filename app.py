import streamlit as st
import requests
from PIL import Image, ImageDraw, ImageFont
import io
import urllib.parse
import time
import os
from streamlit_option_menu import option_menu

st.set_page_config(page_title="Patna AI Studio Pro", page_icon="💎", layout="wide")

st.markdown("""
<style>
.luxury-title {color: #ffd700; font-size: 4rem; text-align: center;}
.gold-btn {background: linear-gradient(45deg, #ffd700, #ffed4e); color: #1a1a2e; font-weight: bold; border-radius: 20px;}
.feature-box {background: rgba(255,215,0,0.1); border: 2px solid #ffd700; border-radius: 20px; padding: 2rem;}
</style>
""", unsafe_allow_html=True)

def build_pro_prompt(shop_name, product, offer, landmark=""):
    base = f"Professional luxury advertisement for {shop_name}, premium {product}"
    if offer:
        base += f" with {offer} offer"
    if landmark:
        base += f" near {landmark}"
    quality = "8K cinematic lighting, golden accents, sharp focus, luxury showcase"
    return base + ", " + quality

@st.cache_resource
def load_fonts():
    try:
        return ImageFont.truetype("NotoSansDevanagari-VariableFont_wdth,wght.ttf", 44)
    except:
        return ImageFont.load_default()

fonts = load_fonts()

@st.cache_data(ttl=1800)
def generate_image(prompt):
    url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt)}?width=1024&height=1024&nologo=true"
    try:
        resp = requests.get(url, timeout=20)
        return resp.content if resp.status_code == 200 else None
    except:
        return None

def add_overlay(img_bytes, shop_name, product, offer, contact, landmark, address):
    img = Image.open(io.BytesIO(img_bytes)).convert("RGBA")
    w, h = img.size
    
    # Dark overlay layer
    overlay = Image.new("RGBA", img.size, (0,0,0,0))
    draw = ImageDraw.Draw(overlay)
    
    # Bottom dark rectangle
    draw.rectangle([0, h - (h//3), w, h], fill=(0,0,0,180))
    
    y = h - (h//3) + 20
    
    # Shop name (CENTERED)
    text = f"✨ {shop_name} ✨"
    bbox = draw.textbbox((0,0), text, font=fonts)
    text_w = bbox[2] - bbox[0]
    draw.text((w//2 - text_w//2, y), text, fill="#ffd700", font=fonts)
    y += 55
    
    # Product + Offer
    text = f"{product} - {offer}"
    bbox = draw.textbbox((0,0), text, font=fonts)
    text_w = bbox[2] - bbox[0]
    draw.text((w//2 - text_w//2, y), text, fill="#ffed4e", font=fonts)
    y += 45
    
    # Contact
    text = f"📞 {contact}"
    bbox = draw.textbbox((0,0), text, font=fonts)
    text_w = bbox[2] - bbox[0]
    draw.text((w//2 - text_w//2, y), text, fill="white", font=fonts)
    y += 40
    
    # Landmark
    if landmark:
        text = f"📍 {landmark}"
        bbox = draw.textbbox((0,0), text, font=fonts)
        text_w = bbox[2] - bbox[0]
        draw.text((w//2 - text_w//2, y), text, fill="#e0e0e0", font=fonts)
        y += 35
    
    # Address - PROPER MULTI-LINE HANDLING
    if address:
        # Split by 
 and clean each line
        addr_lines = []
        for line in address.split("
"):
            clean_line = line.strip()
            if clean_line:
                addr_lines.append(clean_line)
        
        # Show max 2 lines
        for i in range(min(2, len(addr_lines))):
            text = f"📬 {addr_lines[i]}"
            bbox = draw.textbbox((0,0), text, font=fonts)
            text_w = bbox[2] - bbox[0]
            draw.text((w//2 - text_w//2, y), text, fill="#d0d0d0", font=fonts)
            y += 30
    
    # Combine image + overlay
    combined = Image.alpha_composite(img, overlay)
    
    buf = io.BytesIO()
    combined.convert("RGB").save(buf, "PNG", quality=95)
    return buf.getvalue()

# MAIN UI
st.markdown('<h1 class="luxury-title">💎 पटना AI स्टूडियो प्रो</h1>', unsafe_allow_html=True)

with st.sidebar:
    selected = option_menu("मेन्यू", ["🚀 AI ऐड मेकर"], icons=["cast"])

if selected == "🚀 AI ऐड मेकर":
    st.markdown('<div class="feature-box"><h2>🎨 बिज़नेस ऐड बनाएं</h2></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        shop_name = st.text_input("🏪 दुकान का नाम", "पटना ज्वेलर्स")
        product = st.text_input("📦 प्रोडक्ट", "गोल्ड सेट")
        offer = st.text_input("🎁 ऑफर", "50% छूट")
        contact = st.text_input("📞 नंबर", "8210073056")
    
    with col2:
        landmark = st.text_input("📍 लैंडमार्क", "फ्रेजर रोड")
        address = st.text_area("🏠 पूरा पता", "पटना सिटी
बिहार 800001", height=80)
    
    col1, col2 = st.columns(2)
    if col1.button("✨ ऐड बनाएं", key="generate"):
        if shop_name and product:
            with st.spinner("🎨 AI बना रहा है..."):
                prompt = build_pro_prompt(shop_name, product, offer, landmark)
                img_bytes = generate_image(prompt)
                
                if img_bytes:
                    final_img = add_overlay(img_bytes, shop_name, product, offer, 
                                          contact, landmark, address)
                    
                    st.image(final_img, use_container_width=True)
                    st.download_button("⬇️ डाउनलोड", final_img, "business_ad.png")
                    st.success("✅ तैयार!")
                else:
                    st.error("🌐 AI busy है!")
        else:
            st.warning("दुकान और प्रोडक्ट भरें!")

st.markdown("---")
st.markdown("© 2026 Patna AI Studio Pro | +91 8210073056")
