import streamlit as st
import requests
import io
from PIL import Image
import time
import urllib.parse

# 1. Page Configuration
st.set_page_config(page_title="Patna AI Studio Pro", layout="wide", page_icon="🏙️")

# 2. Universal Visibility UI (Fix for 8210073056)
st.markdown("""
<style>
    .stApp { background-color: #0e1117 !important; color: white !important; }
    input, textarea, [data-baseweb="select"] {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 3px solid #00f2fe !important;
        border-radius: 12px !important;
        font-weight: bold !important;
    }
    h1, h2, h3, label, p { color: #00f2fe !important; font-weight: bold !important; }
    .stButton > button {
        background: linear-gradient(45deg, #00f2fe 0%, #4facfe 100%) !important;
        color: white !important; border-radius: 50px !important; font-weight: bold !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. Hindi-to-English + Auto Pro Prompt Logic
def pro_prompt_gen(text):
    try:
        encoded = urllib.parse.quote(text)
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=en&dt=t&q={encoded}"
        r = requests.get(url, timeout=10).json()
        eng = r[0][0][0]
        return f"{eng}, ultra-realistic, 8k resolution, cinematic lighting, masterpiece, sharp focus, highly detailed, flux style"
    except:
        return f"{text}, 8k resolution, masterpiece"

# 4. Session State
if 'pro_prompt' not in st.session_state: st.session_state.pro_prompt = ""

# 5. Sidebar (Call & WhatsApp: 8210073056)
with st.sidebar:
    st.title("🏙️ Patna AI Pro")
    st.markdown("---")
    st.subheader("📞 Contact Support")
    st.link_button("📱 WhatsApp Now", "https://wa.me/918210073056")
    st.link_button("📞 Call Now", "tel:+918210073056")
    st.markdown("---")
    engine = st.selectbox("🚀 Choose Engine", ["🆓 Pollinations (Free)", "💎 Segmind Pro (HQ)"])
    menu = st.radio("Navigation", ["🎨 Image Studio", "🎥 Video AI", "📞 Support"])

# 6. Main Feature
if menu == "🎨 Image Studio":
    st.header("🎨 AI Image Studio")
    
    # Step 1: Converter
    st.subheader("🪄 Step 1: Hindi to Pro Prompt Generator")
    idea = st.text_input("Apna idea Hindi/English mein likhein:", placeholder="Ek ladka Patna junction par...")
    if st.button("🪄 Convert to Pro Prompt"):
        if idea:
            st.session_state.pro_prompt = pro_prompt_gen(idea)
            st.success("✅ Pro Prompt Taiyar Hai!")
    
    if st.session_state.pro_prompt:
        final_p = st.text_area("Final Prompt:", value=st.session_state.pro_prompt, height=100)
        
        # Step 2: Generation
        st.subheader("🖼️ Step 2: Generate HD Image")
        ratio = st.selectbox("📐 Size", ["1:1 Square", "9:16 Reels", "16:9 YouTube"])
        if st.button("🚀 Create Image"):
            with st.spinner("Generating..."):
                try:
                    dims = {"1:1 Square": (1024,1024), "9:16 Reels": (720,1280), "16:9 YouTube": (1280,720)}
                    w, h = dims[ratio]
                    if "Segmind" in engine and "SEGMIND_API_KEY" in st.secrets:
                        res = requests.post("https://api.segmind.com/v1/flux-1-dev", 
                                            json={"prompt": final_p, "width": w, "height": h}, 
                                            headers={"x-api-key": st.secrets["SEGMIND_API_KEY"]})
                    else:
                        res = requests.get(f"https://image.pollinations.ai/prompt/{urllib.parse.quote(final_p)}?width={w}&height={h}&nologo=true")
                    
                    if res.status_code == 200:
                        st.image(res.content, use_container_width=True)
                        st.download_button("💾 Download", res.content, "patna_ai.png", "image/png")
                except Exception as e: st.error(f"Error: {e}")

elif menu == "📞 Support":
    st.info("Owner: Chaman Jha | Contact: +91 8210073056")

st.markdown("---")
st.markdown("<p style='text-align: center;'>✨ Patna AI Studio Pro v10.0 | 8210073056</p>", unsafe_allow_html=True)

