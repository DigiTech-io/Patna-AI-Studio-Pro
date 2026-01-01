import streamlit as st
import requests
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import io
import urllib.parse
import time
import base64
import os
from streamlit_option_menu import option_menu

# --- PAGE SETUP ---
st.set_page_config(page_title="💎 Patna AI Studio Pro v5.0", page_icon="💎", layout="wide")

# --- LUXURY CSS ---
st.markdown("""
<style>
.luxury-title {color: #ffd700; font-size: 3.5rem; text-align: center; text-shadow: 0 0 20px rgba(255,215,0,0.5);}
.stButton>button {background: linear-gradient(45deg, #ffd700, #ffed4e); color: #1a1a2e; font-weight: bold; border-radius: 20px;}
.social-box {background: rgba(255,215,0,0.1); border: 1px solid #ffd700; padding: 15px; border-radius: 15px; text-align: center;}
</style>
""", unsafe_allow_html=True)

# --- SMART PROMPT LOGIC (Fixing Kirana Issue) ---
def build_smart_prompt(shop_name, product, style):
    shop_lower = shop_name.lower()
    if "kirana" in shop_lower or "store" in shop_lower or "grocery" in shop_lower:
        base = f"Authentic Indian grocery store interior, organized shelves with spices, lentils, and products, professional commercial photography, warm lighting"
    elif "jewel" in shop_lower:
        base = f"Luxury jewelry showcase, 8k cinematic lighting, golden ornaments, sharp focus"
    else:
        base = f"Professional commercial advertisement for {product}, high-end product photography"
    
    return f"{base}, masterpiece, highly detailed, {style} style"

# --- CORE FUNCTIONS ---
def generate_image(prompt, use_premium):
    if use_premium:
        api_key = st.secrets.get("SEGMIND_API_KEY") #
        if api_key:
            try:
                url = "https://api.segmind.com/v1/sdxl1.0-txt2img"
                payload = {"prompt": prompt, "width": 1024, "height": 1024, "steps": 25}
                headers = {"x-api-key": api_key}
                resp = requests.post(url, json=payload, headers=headers)
                if resp.status_code == 200:
                    return base64.b64decode(resp.json()['images'][0])
            except: pass
    
    # Fallback to Free
    url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt)}?width=1024&height=1024&nologo=true"
    return requests.get(url).content

# --- MAIN APP INTERFACE ---
st.markdown('<h1 class="luxury-title">💎 PATNA AI STUDIO PRO v5.0</h1>', unsafe_allow_html=True)

with st.sidebar:
    selected = option_menu("Control Panel", ["🚀 Ad Maker", "👤 User Profile", "📞 Support"], icons=["magic", "person", "whatsapp"])
    
    st.markdown("### 📢 Social Growth Panel")
    st.markdown('<div class="social-box">', unsafe_allow_html=True)
    st.write("Unlock Unlimited Use:")
    st.link_button("Subscribe YouTube", "https://youtube.com/@AapkaChannel")
    st.link_button("Follow Facebook", "https://facebook.com/AapkaPage")
    st.markdown('</div>', unsafe_allow_html=True)
    
    is_followed = st.checkbox("I have Followed/Subscribed ✅")
    use_premium = st.checkbox("⭐ Use Premium Engine (Segmind)", value=False)

if selected == "🚀 Ad Maker":
    if not is_followed:
        st.warning("⚠️ Please Follow/Subscribe from sidebar to enable Pro Generation!")
    
    col1, col2 = st.columns([1.2, 1])
    with col1:
        shop = st.text_input("🏪 Shop Name", "Bhawan Kirana Store")
        prod = st.text_input("📦 Product Name", "Pure Desi Ghee")
        off = st.text_input("🎁 Current Offer", "10% OFF")
        num = st.text_input("📞 WhatsApp Number", "8210073056")
    with col2:
        land = st.text_input("📍 Landmark", "Main Road, Patna")
        addr = st.text_area("🏠 Shop Address", "Patna City, Bihar")

    if st.button("✨ CREATE PRO AD", disabled=not is_followed):
        with st.spinner("🚀 Generating Pro Quality Assets..."):
            prompt = build_smart_prompt(shop, prod, "Cinematic")
            img_data = generate_image(prompt, use_premium)
            
            if img_data:
                # Assuming create_ad_overlay function exists from previous version
                # final_img = create_ad_overlay(img_data, shop, prod, off, num, land, addr)
                st.image(img_data, use_container_width=True)
                st.success("✅ Pro Ad Generated!")
                st.download_button("⬇️ Download HD Ad", img_data, "ad.png")

elif selected == "📞 Support":
    st.header("Contact Owner")
    col_a, col_b = st.columns(2)
    with col_a:
        st.link_button("Chat on WhatsApp 💬", f"https://wa.me/918210073056")
    with col_b:
        st.link_button("Call Now 📞", "tel:+918210073056")

st.markdown("---")
st.markdown("<center>© 2026 Patna AI Studio Pro | Support: +91 8210073056</center>", unsafe_allow_html=True)

