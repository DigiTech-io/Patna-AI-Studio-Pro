import streamlit as st
import requests
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import io
import urllib.parse
import time
import os
from streamlit_option_menu import option_menu

st.set_page_config(page_title="Patna AI Studio Pro", page_icon="💎", layout="wide")

st.markdown("""
<style>
.luxury-title {color: #ffd700; font-size: 4rem; text-align: center;}
.gold-btn {background: linear-gradient(45deg, #ffd700, #ffed4e); color: #1a1a2e;}
.feature-box {background: rgba(255,215,0,0.1); border: 2px solid #ffd700; border-radius: 20px; padding: 2rem;}
</style>
""", unsafe_allow_html=True)

def build_pro_prompt(shop_name, product, offer, landmark=""):
    base = f"Luxury ad for {shop_name}, {product}"
    if offer: base += f" {offer}"
    if landmark: base += f" {landmark}"
    return base + " 8K professional photography"

@st.cache_resource
def load_fonts():
    try:
        return ImageFont.truetype("NotoSansDevanagari-VariableFont_wdth,wght.ttf", 42)
    except:
        return ImageFont.load_default()

fonts = load_fonts()

@st.cache_data(ttl=1800)
def generate_image(prompt):
    url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt)}?width=1024&height=1024"
    try:
        resp = requests.get(url, timeout=20)
        return resp.content if resp.status_code == 200 else None
    except:
        return None

def add_overlay(img_bytes, shop_name, product, offer, contact, landmark, address):
    img = Image.open(io.BytesIO(img_bytes)).convert("RGBA")
    w, h = img.size
    
    overlay = Image.new("RGBA", (w, h), (0,0,0,0))
    draw = ImageDraw.Draw(overlay)
    
    # Dark bottom strip
    draw.rectangle([0, h-int(h/3), w, h], fill=(0,0,0,160))
    
    y = h - int(h/3) + 20
    
    # Shop name
    text = f"✨ {shop_name} ✨"
    bbox = draw.textbbox((0, 0), text, font=fonts)
    tw = bbox[2] - bbox[0]
    draw.text((w/2 - tw/2, y), text, fill="#ffd700", font=fonts)
    y += 50
    
    # Product
    text = f"{product}"
    bbox = draw.textbbox((0, 0), text, font=fonts)
    tw = bbox[2] - bbox[0]
    draw.text((w/2 - tw/2, y), text, fill="#ffed4e", font=fonts)
    y += 45
    
    # Offer
    text = offer
    bbox = draw.textbbox((0, 0), text, font=fonts)
    tw = bbox[2] - bbox[0]
    draw.text((w/2 - tw/2, y), text, fill="#ffd700", font=fonts)
    y += 40
    
    # Contact
    text = f"📞 {contact}"
    bbox = draw.textbbox((0, 0), text, font=fonts)
    tw = bbox[2] - bbox[0]
    draw.text((w/2 - tw/2, y), text, fill="white", font=fonts)
    y += 35
    
    # Landmark
    if landmark:
        text = f"📍 {landmark}"
        bbox = draw.textbbox((0, 0), text, font=fonts)
        tw = bbox[2] - bbox[0]
        draw.text((
