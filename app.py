import streamlit as st
import requests
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import io
import urllib.parse
import time
import hashlib
import sqlite3
import base64
from streamlit_option_menu import option_menu
import numpy as np

# Page Config
st.set_page_config(
    page_title="Patna AI Studio Pro", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
.main-header {font-size: 3rem; color: #1f77b4; text-align: center; margin-bottom: 2rem;}
.feature-card {background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 15px; color: white;}
.stButton > button {width: 100%; height: 50px; border-radius: 25px; font-weight: bold;}
</style>
""", unsafe_allow_html=True)

# Font Path
FONT_PATH = "NotoSansDevanagari-VariableFont_wdth,wght.ttf"

# Database setup for usage tracking
@st.cache_resource
def init_db():
    conn = sqlite3.connect('usage.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS usage 
                 (id INTEGER PRIMARY KEY, timestamp TEXT, feature TEXT, user_ip TEXT)''')
    conn.commit()
    conn.close()

def log_usage(feature):
    init_db()
    conn = sqlite3.connect('usage.db')
    c = conn.cursor()
    c.execute("INSERT INTO usage (timestamp, feature, user_ip) VALUES (?, ?, ?)",
              (time.strftime("%Y-%m-%d %H:%M:%S"), feature, st.session_state.get('user_ip', 'unknown')))
    conn.commit()
    conn.close()

# Enhanced Business Banner Function
def add_business_banner(image_bytes, biz_name, contact, template="modern"):
    try:
        img = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        width, height = img.size
        
        if template == "modern":
            banner_height = int(height * 0.20)
            new_img = Image.new('RGB', (width, height + banner_height), color=(16, 48, 96))
        else:
            banner_height = int(height * 0.25)
            new_img = Image.new('RGB', (width, height + banner_height), color=(0, 123, 255))
        
        new_img.paste(img, (0, banner_height))
        
        draw = ImageDraw.Draw(new_img)
        
        # Multiple font sizes for better text fitting
        try:
            large_font = ImageFont.truetype(FONT_PATH, 48)
            medium_font = ImageFont.truetype(FONT_PATH, 36)
            small_font = ImageFont.truetype(FONT_PATH, 28)
        except:
            large_font = medium_font = small_font = ImageFont.load_default()
            st.warning("ℹ️ Hindi font not found, using default font.")
        
        # Business name (large)
        name_bbox = draw.textbbox((0, banner_height + 20), biz_name, font=large_font)
        name_width = name_bbox[2] - name_bbox[0]
        name_x = (width - name_width) // 2
        draw.text((name_x, banner_height + 25), biz_name, fill="white", font=large_font)
        
        # Contact info (medium)
        contact_text = f"📞 {contact} | पटना बिहार"
        contact_bbox = draw.textbbox((0, banner_height + 80), contact_text, font=medium_font)
        contact_width = contact_bbox[2] - contact_bbox[0]
        contact_x = (width - contact_width) // 2
        draw.text((contact_x, banner_height + 85), contact_text, fill="#f8f9fa", font=medium_font)
        
        # Tagline (small)
        tagline = "✨ सबसे तेज़ AI बिज़नेस प्रमोशन ✨"
        tagline_bbox = draw.textbbox((0, banner_height + 130), tagline, font=small_font)
        tagline_width = tagline_bbox[2] - tagline_bbox[0]
        tagline_x = (width - tagline_width) // 2
        draw.text((tagline_x, banner_height + 135), tagline, fill="#e9ecef", font=small_font)
        
        # Enhance image quality
        enhancer = ImageEnhance.Sharpness(new_img)
        new_img = enhancer.enhance(1.2)
        
        img_byte_arr = io.BytesIO()
        new_img.save(img_byte_arr, format='PNG', optimize=True, quality=95)
        return img_byte_arr.getvalue()
        
    except Exception as e:
        st.error(f"❌ त्रुटि: {str(e)}")
        return image_bytes

# Get image from URL
@st.cache_data(ttl=300)
def get_image_from_url(url):
    try:
        response = requests.get(url, timeout=15)
        return response.content
    except:
        return None

# Header
st.markdown('<h1 class="main-header">🚀 पटना AI स्टूडियो प्रो</h1>', unsafe_allow_html=True)
st.markdown("### बिहार का सबसे तेज़ AI बिज़नेस ग्रोथ टूल | Made in Patna 🇮🇳")

# Sidebar Menu
with st.sidebar:
    st.markdown("### 📱 मेनू")
    selected = option_menu(
        "मेन मेन्यू", 
        ["🚀 बिज़नेस ग्रोथ", "🎨 इमेज स्टूडियो", "📈 सोशल ग्रोथ", "📞 सपोर्ट"],
        icons=['house', 'image', 'graph-up', 'headset'], 
        menu_icon="cast", 
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "#f0f2f6"},
            "icon": {"color": "#1f77b4", "font-size": "20px"},
            "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "#1f77b4"}
        }
    )
    
    st.markdown("---")
    st.markdown("### 📊 आज का उपयोग")
    st.info("✅ सभी फीचर्स फ्री")

# Main Pages
if selected == "🚀 बिज़नेस ग्रोथ":
    st.markdown('<div class="feature-card">💼 प्रोफेशनल बिज़नेस ऐड बनाएं - 10 सेकंड में!</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("📤 बिज़नेस ऐड जेनरेटर")
        biz_name = st.text_input("🏪 बिज़नेस का नाम", placeholder="जैसे: पटना ढाबा")
        contact = st.text_input("📞 कॉन्टैक्ट नंबर", value="8210073056", placeholder="98XXXXXXX")
        template = st.selectbox("🎨 टेम्पलेट", ["modern", "classic"])
        
        uploaded_file = st.file_uploader("📸 प्रोडक्ट इमेज अपलोड करें", type=["jpg", "jpeg", "png"], help="JPG, PNG फाइलें सपोर्ट")
    
    with col2:
        st.markdown("### ✨ फीचर्स")
        st.markdown("- प्रोफेशनल बैनर")
        st.markdown("- हिंदी फॉन्ट")
        st.markdown("- हाई क्वालिटी")
        st.markdown("- फ्री डाउनलोड")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        if st.button("✨ ब्रांडेड ऐड बनाएं", type="primary", use_container_width=True):
            if uploaded_file and biz_name:
                with st.spinner("🎨 आपका ऐड तैयार हो रहा है..."):
                    log_usage("business_banner")
                    final_ad = add_business_banner(uploaded_file.read(), biz_name, contact, template)
                    
                    st.success("✅ ऐड तैयार!")
                    st.image(final_ad, use_container_width=True)
                    
                    # Download button with Hindi text
                    st.download_button(
                        label="⬇️ ऐड डाउनलोड करें", 
                        data=final_ad, 
                        file_name=f"{biz_name}_ad.png",
                        mime="image/png",
                        use_container_width=True
                    )
            else:
                st.warning("⚠️ बिज़नेस नाम और इमेज जरूरी है!")
    
    st.info("💡 टिप: बेस्ट रिजल्ट के लिए 1080x1080 इमेज इस्तेमाल करें")

elif selected == "🎨 इमेज स्टूडियो":
    st.markdown('<div class="feature-card">🎨 AI से अनलिमिटेड इमेज बनाएं!</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        idea = st.text_area(
            "💭 अपनी इमेज का आइडिया लिखें", 
            placeholder="जैसे: 'पटना में ढाबा का खाना, रंगीन, आकर्षक'",
            height=100
        )
        model = st.selectbox("🤖 AI मॉडल", ["Pollinations AI", "Stable Diffusion"])
        
        col_a, col_b = st.columns(2)
        with col_a:
            width = st.slider("चौड़ाई", 512, 1024, 512, 64)
        with col_b:
            height = st.slider("ऊंचाई", 512, 1024, 512, 64)
    
    with col2:
        st.markdown("### 🚀 उदाहरण प्रॉम्प्ट्स")
        prompts = [
            "पटना का सुंदर सूर्यास्त",
            "बिहार का ट्रेडिशनल ढाबा",
            "मॉडर्न बिज़नेस कार्ड डिज़ाइन",
            "नवरात्रि स्पेशल साड़ी",
            "बिहार लेबर कार्ड प्रमोशन"
        ]
        for prompt in prompts:
            if st.button(prompt, key=prompt):
                idea = prompt
    
    if st.button("🎨 AI इमेज जेनरेट करें", type="primary", use_container_width=True):
        if idea:
            with st.spinner("🖼️ AI इमेज बना रहा है..."):
                log_usage("image_gen")
                if model == "Pollinations AI":
                    img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(idea)}?width={width}&height={height}&nologo=true&seed={int(time.time())}"
                    img_data = get_image_from_url(img_url)
                    if img_data:
                        st.image(img_data, use_container_width=True)
                        st.markdown(f"**प्रॉम्प्ट:** {idea}")
                    else:
                        st.image(img_url, caption=f"Generated: {idea}")
                else:
                    st.info("🔄 अन्य मॉडल जल्द आ रहे हैं!")
        else:
            st.warning("⚠️ प्रॉम्प्ट लिखें!")

elif selected == "📈 सोशल ग्रोथ":
    st.markdown('<div class="feature-card">📱 इंस्टाग्राम रील्स & स्टोरीज़ ऑटोमेशन</div>', unsafe_allow_html=True)
    st.info("🔥 जल्द लॉन्च हो रहा है!")

✅ रील्स ऑटो जेनरेटर
✅ कैप्शन राइटर
✅ हैशटैग जेनरेटर")

elif selected == "📞 सपोर्ट":
    st.markdown('<div class="feature-card">🆘 24x7 सपोर्ट | व्हाट्सएप पर बात करें</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        ### 📞 कॉन्टैक्ट करें
        **व्हाट्सएप:** +91 8210073056  
        **कॉल:** 10AM - 10PM
        
        ### 📧 ईमेल
        patnaaistudio@gmail.com
        """)
    
    with col2:
        st.markdown("""
        ### 💬 आम समस्याएं
        - इमेज न बनना
        - डाउनलोड समस्या  
        - फॉन्ट इश्यू
        - स्पीड स्लो होना
        """)
    
    st.balloons()

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("**© 2026 पटना AI स्टूडियो प्रो**")
with col2:
    st.markdown("**Made in 🇮🇳 Bihar**")
with col3:
    st.markdown("**सपोर्ट: +91 8210073056**")

# Hide Streamlit elements
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)
