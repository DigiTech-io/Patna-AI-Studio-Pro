import streamlit as st
import requests
import io
import base64
import time
import urllib.parse
from PIL import Image  # ✅ FIXED: Added missing import

# 1. Visibility & UI Fix
st.set_page_config(page_title="Patna AI Studio Pro", layout="wide", page_icon="🎨")
st.markdown("""
<style>
    .stApp { background-color: #ffffff !important; }
    input, textarea { 
        background-color: #ffffff !important; 
        color: black !important; 
        border: 2px solid #007bff !important; 
        font-weight: 600 !important;
        border-radius: 8px !important;
    }
    .pro-box { 
        border: 2px solid #007bff; 
        padding: 25px; 
        border-radius: 15px; 
        background: #ffffff;
        box-shadow: 0 8px 25px rgba(0,123,255,0.1);
        margin: 10px 0;
    }
    h1, h2, h3, label { color: #1a365d !important; font-weight: 800 !important; }
    .stButton > button {
        background: linear-gradient(45deg, #007bff, #0056b3) !important;
        color: white !important;
        border-radius: 25px !important;
        font-weight: bold !important;
        height: 3em !important;
    }
</style>
""", unsafe_allow_html=True)

# 2. Smart Prompt Generator
def make_pro_prompt(idea):
    return f"{idea}, ultra realistic, 8k, cinematic lighting, masterpiece, highly detailed, flux style"

# 3. Sidebar (Support: 8210073056)
with st.sidebar:
    st.title("🏙️ Patna AI Pro")
    engine = st.selectbox("🚀 Select AI Engine", 
                         ["🆓 Pollinations (Unlimited Free)", "💎 Segmind Pro (Backup)"])
    menu = st.radio("Navigation", ["🎨 Image Studio", "🎥 Video AI", "📱 Reels Magic", "📞 Support"])
    st.markdown("---")
    st.markdown(f"**📞 Help:** +91 8210073056")
    st.markdown("[💬 WhatsApp](https://wa.me/918210073056)")

# 4. MAIN SECTIONS
if menu == "🎨 Image Studio":
    st.header("🎨 AI Image Studio")
    st.markdown('<div class="pro-box">', unsafe_allow_html=True)
    
    idea = st.text_input("💡 Apna idea likhein (Hindi/English):", placeholder="Tiger at Patna Zoo...")
    
    if st.button("🚀 Ultra HD Generate"):
        if idea:
            with st.spinner("🎨 AI is creating your masterpiece..."):
                try:
                    pro_prompt = make_pro_prompt(idea)
                    if "Segmind" in engine and "SEGMIND_API_KEY" in st.secrets:
                        # ✅ Segmind Logic
                        res = requests.post(
                            "https://api.segmind.com/v1/flux-1-dev",
                            json={"prompt": pro_prompt, "width": 1024, "height": 1024},
                            headers={"x-api-key": st.secrets["SEGMIND_API_KEY"]}
                        )
                        img = Image.open(io.BytesIO(res.content))
                    else:
                        # Pollinations
                        url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(pro_prompt)}?width=1024&height=1024&nologo=true"
                        res = requests.get(url)
                        img = Image.open(io.BytesIO(res.content))
                    
                    st.image(img, use_container_width=True)
                    
                    img_byte = io.BytesIO()
                    img.save(img_byte, format='PNG')
                    st.download_button("💾 Save HD Image", img_byte.getvalue(), "patna_ai.png", "image/png")
                    st.balloons()
                except Exception as e:
                    st.error(f"❌ Error: {e}")
    st.markdown('</div>', unsafe_allow_html=True)

elif menu == "🎥 Video AI":
    st.header("🎬 AI Animation Studio")
    st.info("💡 Hint: Moving images/GIFs ke liye cinematic keywords use karein.")
    st.markdown('<div class="pro-box">', unsafe_allow_html=True)
    v_idea = st.text_input("🎥 Video description:")
    if st.button("🎬 Generate Animation"):
        if v_idea:
            # High speed animation workaround
            gif_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(v_idea + ', animated motion')}?nologo=true&seed={int(time.time())}"
            st.image(gif_url, caption="Cinematic Animation Ready")
    st.markdown('</div>', unsafe_allow_html=True)

elif menu == "📞 Support":
    st.success("👨‍💼 **Chaman Jha - Patna AI Studio**")
    st.info("WhatsApp/Call: +91 8210073056")

st.markdown("---")
st.markdown("<p style='text-align: center; color: #007bff; font-weight: bold;'>✨ Patna AI Studio Pro | 8210073056</p>", unsafe_allow_html=True)

