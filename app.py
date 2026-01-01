import streamlit as st
import requests
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import io
import urllib.parse
import time
import base64
import os
from streamlit_option_menu import option_menu

# --- 1. SETUP & RESPONSIVE CSS ---
st.set_page_config(page_title="Patna AI Studio Pro v5.2", page_icon="💎", layout="wide")

st.markdown("""
<style>
    .luxury-title {color: #ffd700; font-size: 3.5rem; text-align: center; text-shadow: 0 0 20px rgba(255,215,0,0.5);}
    .stButton>button {background: linear-gradient(45deg, #ffd700, #ffed4e); color: #1a1a2e; font-weight: bold; border-radius: 20px; width: 100%; height: 50px;}
    .social-box {background: rgba(255,215,0,0.1); border: 2px solid #ffd700; padding: 15px; border-radius: 15px; text-align: center; margin-bottom: 20px;}
    @media (max-width: 600px) { .luxury-title { font-size: 2.2rem !important; } }
</style>
""", unsafe_allow_html=True)

# --- 2. HINDI FONT LOADING ---
@st.cache_resource
def get_hindi_font(size=50):
    # Make sure to upload 'NotoSansDevanagari-Regular.ttf' to your GitHub!
    font_paths = ["NotoSansDevanagari-Regular.ttf", "NotoSansDevanagari-VariableFont_wdth,wght.ttf"]
    for path in font_paths:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()

# --- 3. PRO AI ENGINE (Segmind + Fallback) ---
def generate_pro_image(prompt, is_premium):
    if is_premium:
        api_key = st.secrets.get("SEGMIND_API_KEY")
        if api_key:
            try:
                url = "https://api.segmind.com/v1/sdxl1.0-txt2img"
                data = {"prompt": prompt, "width": 1024, "height": 1024, "steps": 30, "samples": 1}
                headers = {"x-api-key": api_key}
                resp = requests.post(url, json=data, headers=headers, timeout=60)
                if resp.status_code == 200:
                    return base64.b64decode(resp.json()['images'][0])
            except: pass
    
    # Fallback to Free Engine
    free_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt)}?width=1024&height=1024&nologo=true&seed={int(time.time())}"
    return requests.get(free_url).content

# --- 4. SMART OVERLAY (FIXED FOR HINDI) ---
def apply_pro_overlay(img_bytes, shop, prod, off, num, land, addr):
    img = Image.open(io.BytesIO(img_bytes)).convert("RGBA")
    w, h = img.size
    
    # Bottom Shadow
    overlay = Image.new("RGBA", img.size, (0,0,0,0))
    d_ov = ImageDraw.Draw(overlay)
    d_ov.rectangle([0, h*0.65, w, h], fill=(0,0,0,190))
    img = Image.alpha_composite(img, overlay)
    
    draw = ImageDraw.Draw(img)
    f_h = get_hindi_font(55)
    f_s = get_hindi_font(35)

    y = h * 0.7
    # ✨ Center Aligned Text
    draw.text((w/2, y), f"✨ {shop} ✨", fill="#ffd700", font=f_h, anchor="mm")
    draw.text((w/2, y+70), f"🔥 {prod} | {off}", fill="#ffed4e", font=f_s, anchor="mm")
    draw.text((w/2, y+130), f"📞 WhatsApp: {num} | 📍 {land}", fill="white", font=f_s, anchor="mm")
    
    if addr:
        lines = addr.split('\n')[:2]
        for i, line in enumerate(lines):
            draw.text((w/2, y+180+(i*40)), f"📬 {line}", fill="#d4e6f1", font=f_s, anchor="mm")

    # Polish & Sharpness
    img = img.convert("RGB")
    img = ImageEnhance.Sharpness(img).enhance(1.4)
    return img

# --- 5. MAIN UI LOGIC ---
st.markdown("<h1 class='luxury-title'>💎 PATNA AI STUDIO PRO v5.2</h1>", unsafe_allow_html=True)

with st.sidebar:
    selected = option_menu("Main Menu", ["🚀 Ad Maker", "📞 Support"], 
                          icons=["magic", "whatsapp"], default_index=0)
    
    st.markdown("### 📢 Social Growth Panel")
    st.markdown('<div class="social-box">', unsafe_allow_html=True)
    st.write("Unlock Pro Quality:")
    st.link_button("Subscribe YouTube", "https://youtube.com/@AapkaChannel")
    st.link_button("Follow Facebook", "https://facebook.com/AapkaPage")
    st.markdown('</div>', unsafe_allow_html=True)
    
    is_followed = st.checkbox("I have Followed/Subscribed ✅", value=False)
    is_premium = st.checkbox("⭐ Use Premium Engine", value=True)
    st.info("Version 5.2 | Pro Performance")

if selected == "🚀 Ad Maker":
    if not is_followed:
        st.warning("⚠️ Please Subscribe/Follow from sidebar to enable the Start button!")
    
    # Input Layout
    col1, col2 = st.columns([1, 1])
    with col1:
        shop = st.text_input("🏪 Business Name (Hindi Support)", "भवानी किराना स्टोर")
        prod = st.text_input("📦 Product Name", "शुद्ध देसी घी")
        off = st.text_input("🎁 Offer", "10% Discount")
    with col2:
        num = st.text_input("📞 WhatsApp Number", "8210073056")
        land = st.text_input("📍 Landmark", "Main Road, Patna")
        addr = st.text_area("🏠 Address", "Patna City\nBihar")

    if st.button("🚀 CREATE PRO AD", disabled=not is_followed):
        with st.spinner("💎 Generating Pro Advertisement..."):
            # Smart Prompt Logic
            if "kirana" in shop.lower() or "store" in shop.lower():
                prompt = f"Indian grocery store interior, professional product photography of {prod}, cinematic lighting, 8k"
            else:
                prompt = f"Professional commercial photography of {prod} for {shop}, luxury 8k cinematic lighting"
            
            img_raw = generate_pro_image(prompt, is_premium)
            
            if img_raw:
                final_ad = apply_pro_overlay(img_raw, shop, prod, off, num, land, addr)
                st.image(final_ad, use_container_width=True)
                
                # Download
                buf = io.BytesIO()
                final_ad.save(buf, format="PNG")
                st.download_button("⬇️ Download HD Ad", buf.getvalue(), "pro_ad.png", "image/png")
                st.balloons()
            else:
                st.error("AI Busy! Please try again in 10 seconds.")

elif selected == "📞 Support":
    st.header("Contact Support")
    st.write("For any issues or custom tools, contact us:")
    st.link_button("Chat on WhatsApp 💬", "https://wa.me/918210073056")
    st.link_button("Direct Call 📞", "tel:+918210073056")

st.markdown("---")
st.markdown("<center>© 2026 Patna AI Studio Pro | Made in Bihar 🇮🇳</center>", unsafe_allow_html=True)

