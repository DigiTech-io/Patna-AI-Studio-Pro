import streamlit as st
import requests
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
import io
import urllib.parse
import time
import os
from streamlit_option_menu import option_menu
import numpy as np

st.set_page_config(page_title="Patna AI Studio Pro", page_icon="💎", layout="wide")

# CSS
st.markdown("""
<style>
.luxury-title {color: #ffd700; font-size: 4rem; text-align: center;}
.gold-btn {background: linear-gradient(45deg, #ffd700, #ffed4e); color: #1a1a2e; font-weight: bold; border-radius: 20px;}
.feature-box {background: rgba(255,215,0,0.1); border: 2px solid #ffd700; border-radius: 20px; padding: 2rem;}
</style>
""", unsafe_allow_html=True)

def build_pro_prompt(shop_name, product, offer, style="Luxury", landmark=""):
    base = f"Professional {style} advertisement for {shop_name}, premium {product}"
    if offer:
        base += f" with {offer} offer"
    if landmark:
        base += f" near {landmark}"
    
    quality = "8K cinematic lighting, golden accents, sharp focus, luxury showcase, masterpiece"
    return base + ", " + quality

@st.cache_resource
def load_fonts():
    try:
        font = ImageFont.truetype("NotoSansDevanagari-VariableFont_wdth,wght.ttf", 48)
    except:
        font = ImageFont.load_default()
    return font

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
    
    # Dark background strip
    overlay_h = h // 3
    overlay = Image.new("RGBA", (w, overlay_h), (0,0,0,180))
    img = Image.alpha_composite(img, overlay)
    draw = ImageDraw.Draw(img)
    
    y = h - overlay_h + 20
    
    # Shop name
    text = f"✨ {shop_name} ✨"
    bbox = draw.textbbox((0,0), text, font=fonts)
    text_w = bbox[2] - bbox[0]
    draw.text(((w-text_w)//2, y), text, fill="#ffd700", font=fonts)
    y += 60
    
    # Product offer
    text = f"{product} - {offer}"
    bbox = draw.textbbox((0,0), text, font=fonts)
    text_w = bbox[2] - bbox[0]
    draw.text(((w-text_w)//2, y), text, fill="#ffed4e", font=fonts)
    y += 50
    
    # Contact
    text = f"📞 {contact}"
    bbox = draw.textbbox((0,0), text, font=fonts)
    text_w = bbox[2] - bbox[0]
    draw.text(((w-text_w)//2, y), text, fill="white", font=fonts)
    y += 40
    
    # Landmark
    if landmark:
        text = f"📍 {landmark}"
        bbox = draw.textbbox((0,0), text, font=fonts)
        text_w = bbox[2] - bbox[0]
        draw.text(((w-text_w)//2, y), text, fill="#e0e0e0", font=fonts)
        y += 35
    
    # Address - FIXED SYNTAX
    if address:
        # Split address by newline properly
        addr_parts = address.splitlines()
        for part in addr_parts[:2]:
            if part.strip():
                text = f"📬 {part.strip()}"
                bbox = draw.textbbox((0,0), text, font=fonts)
                text_w = bbox[2] - bbox[0]
                draw.text(((w-text_w)//2, y), text, fill="#d0d0d0", font=fonts)
                y += 30
    
    buf = io.BytesIO()
    img.convert("RGB").save(buf, "PNG", quality=95)
    return buf.getvalue()

# UI
st.markdown('<h1 class="luxury-title">💎 पटना AI स्टूडियो प्रो</h1>', unsafe_allow_html=True)

with st.sidebar:
    selected = option_menu("Main Menu", ["🚀 AI Ad Maker"], icons=["cast"])

if selected == "🚀 AI Ad Maker":
    st.markdown('<div class="feature-box"><h2>🎨 Business Ad Generator</h2></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        shop_name = st.text_input("🏪 Business Name", "Patna Jewellers")
        product = st.text_input("📦 Product", "Gold Necklace")
        offer = st.text_input("🎁 Offer", "50% OFF")
        contact = st.text_input("📞 Contact", "8210073056")
    
    with col2:
        landmark = st.text_input("📍 Landmark", "Fraser Road")
        address = st.text_area("🏠 Full Address", "Patna City, Bihar
800001", height=80)
    
    if st.button("✨ Generate Luxury Ad", key="generate"):
        if shop_name and product:
            with st.spinner("🎨 Creating AI Ad..."):
                prompt = build_pro_prompt(shop_name, product, offer, landmark=landmark)
                img_bytes = generate_image(prompt)
                
                if img_bytes:
                    final_img = add_overlay(img_bytes, shop_name, product, offer, 
                                          contact, landmark, address)
                    
                    st.image(final_img, use_container_width=True)
                    st.download_button("⬇️ Download Ad", final_img, "luxury_ad.png")
                    st.success("✅ Ad Ready!")
                else:
                    st.error("🌐 AI service busy. Try again!")
        else:
            st.warning("Please fill business name & product")

st.markdown("---")
st.markdown("© 2026 Patna AI Studio Pro | +91 8210073056")
