import streamlit as st
import requests
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import io
import urllib.parse
import time
import base64
import os
from streamlit_option_menu import option_menu

st.set_page_config(page_title="💎 Patna AI Studio Pro", page_icon="💎", layout="wide")

st.markdown("""
<style>
.luxury-title {color: #ffd700; font-size: 4.2rem; text-align: center; text-shadow: 0 0 30px rgba(255,215,0,0.8);}
.gold-btn {background: linear-gradient(45deg, #ffd700, #ffed4e); color: #1a1a2e; font-weight: 700; border-radius: 25px;}
.feature-box {background: linear-gradient(135deg, rgba(255,215,0,0.1), rgba(255,215,0,0.05)); border: 2px solid rgba(255,215,0,0.3); border-radius: 25px; padding: 2.5rem;}
.premium-badge {background: linear-gradient(45deg, #8b5cf6, #a855f7); color: white; padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.85rem;}
</style>
""", unsafe_allow_html=True)

### PREMIUM API INTEGRATION ###
def generate_premium_image(prompt):
    """Segmind Premium API"""
    try:
        api_key = st.secrets.get("SEGMIND_API_KEY")
        if not api_key:
            return None
        
        url = "https://api.segmind.com/v1/sdxl1.0-txt2img"
        payload = {
            "prompt": prompt,
            "negative_prompt": "blurry, low quality, watermark",
            "width": 1024,
            "height": 1024,
            "steps": 30
        }
        headers = {"x-api-key": api_key}
        
        resp = requests.post(url, json=payload, headers=headers, timeout=60)
        if resp.status_code == 200:
            r = resp.json()
            img_data = base64.b64decode(r['images'][0])
            return img_data
    except Exception as e:
        st.error(f"Premium API: {e}")
        return None

def generate_free_image(prompt):
    """Pollinations Free API"""
    try:
        url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt)}?width=1024&height=1024&nologo=true&seed={int(time.time())}"
        resp = requests.get(url, timeout=20)
        return resp.content if resp.status_code == 200 else None
    except:
        return None

def smart_generate_image(prompt, use_premium=False):
    """Hybrid: Premium → Free Fallback"""
    if use_premium:
        img = generate_premium_image(prompt)
        if img:
            st.success("✅ Premium AI used!")
            return img
    
    # Free fallback
    img = generate_free_image(prompt)
    if img:
        st.info("✅ Free AI (Fast & Reliable)")
        return img
    
    return None

# Rest of your existing functions (unchanged)
def build_pro_prompt(shop_name, product, offer, landmark=""):
    base = f"Luxury advertisement for {shop_name}, showcasing premium {product}"
    if offer: base += f" with '{offer}' promotion"
    if landmark: base += f" located at {landmark}"
    quality = "professional 8K photography, cinematic golden lighting, sharp focus, elegant composition, masterpiece"
    return base + " | " + quality

@st.cache_resource
def load_fonts():
    font_paths = ["NotoSansDevanagari-VariableFont_wdth,wght.ttf", "NotoSansDevanagari-Regular.ttf"]
    for path in font_paths:
        try:
            if os.path.exists(path):
                return ImageFont.truetype(path, 46)
        except:
            continue
    return ImageFont.load_default()

fonts = load_fonts()

def safe_split_address(address):
    if not address:
        return []
    lines = address.split("
")  # ✅ User Enter handling
    clean_lines = [line.strip() for line in lines if line.strip()]
    return clean_lines[:2]

def create_luxury_overlay(img_bytes, shop_name, product, offer, contact, landmark, address):
    img = Image.open(io.BytesIO(img_bytes)).convert("RGBA")
    w, h = img.size
    
    overlay_h = h // 2.3
    overlay = Image.new("RGBA", (w, h), (0,0,0,0))
    draw = ImageDraw.Draw(overlay)
    
    for i in range(overlay_h):
        alpha = int(210 * (i / overlay_h) ** 0.8)
        draw.rectangle([0, h-i, w, h-i+1], fill=(12, 25, 50, alpha))
    
    base_y = h - overlay_h + 20
    
    draw.text((w//2, base_y), f"✨ {shop_name.upper()} ✨", fill="#ffd700", font=fonts, anchor="mm")
    draw.text((w//2, base_y + 65), product, fill="#ffed4e", font=fonts, anchor="mm")
    draw.text((w//2, base_y + 105), offer, fill="#ffd700", font=fonts, anchor="mm")
    draw.text((w//2, base_y + 155), f"📞 {contact}", fill="white", font=fonts, anchor="mm")
    
    if landmark:
        draw.text((w//2, base_y + 200), f"📍 {landmark}", fill="#e8f4fd", font=fonts, anchor="mm")
    
    addr_lines = safe_split_address(address)
    for i, line in enumerate(addr_lines):
        y_pos = base_y + 245 + (i * 32)
        draw.text((w//2, y_pos), f"📬 {line}", fill="#d4e6f1", font=fonts, anchor="mm")
    
    result = Image.alpha_composite(img, overlay)
    enhancer = ImageEnhance.Sharpness(result.convert("RGB"))
    final_img = enhancer.enhance(1.25)
    
    buf = io.BytesIO()
    final_img.save(buf, "PNG", quality=98)
    return buf.getvalue()

# === MAIN APP ===
st.markdown('<h1 class="luxury-title">💎 पटना AI स्टूडियो प्रो</h1>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### ⚡ AI Engine")
    use_premium = st.checkbox("⭐ Premium AI (Segmind - Faster/Better)", value=False)
    
    if use_premium:
        st.markdown('<span class="premium-badge">PREMIUM MODE</span>', unsafe_allow_html=True)
        st.info("🔑 Add SEGMIND_API_KEY in Streamlit Secrets")
    
    selected = option_menu("मेन्यू", ["🚀 AI ऐड मेकर"], icons=["cast"])

if selected == "🚀 AI ऐड मेकर":
    st.markdown('<div class="feature-box"><h2>🎨 प्रोफेशनल ऐड जनरेटर</h2></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1.2, 1])
    with col1:
        shop_name = st.text_input("🏪 दुकान", "पटना ज्वेलर्स")
        product = st.text_input("📦 प्रोडक्ट", "गोल्ड सेट")
        offer = st.text_input("🎁 ऑफर", "50% OFF")
        contact = st.text_input("📞 नंबर", "8210073056")
    
    with col2:
        landmark = st.text_input("📍 लैंडमार्क", "फ्रेजर रोड")
        address = st.text_area("🏠 पूरा पता", "पटना सिटी
फ्रेजर रोड
बिहार 800001", height=95)
    
    if st.button("✨ लग्ज़री ऐड बनाएं", key="generate", use_container_width=True):
        if shop_name.strip() and product.strip():
            with st.spinner("🎨 AI प्रोसेसिंग..."):
                prompt = build_pro_prompt(shop_name, product, offer, landmark)
                img_bytes = smart_generate_image(prompt, use_premium)
                
                if img_bytes:
                    final_ad = create_luxury_overlay(img_bytes, shop_name, product, 
                                                   offer, contact, landmark, address)
                    
                    st.image(final_ad, use_container_width=True)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.download_button("⬇️ PNG डाउनलोड", final_ad, "luxury_ad.png")
                    with col2:
                        st.balloons()
                        st.success("✅ **परफेक्ट ऐड तैयार!**")
                else:
                    st.error("❌ AI अनुपलब्ध। नेटवर्क चेक करें।")
        else:
            st.warning("⚠️ सभी फ़ील्ड भरें!")

st.markdown("---")
st.markdown("💎 Patna AI Studio Pro | Bihar's #1 AI Tool 🇮🇳")
