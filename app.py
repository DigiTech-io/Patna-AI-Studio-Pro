import streamlit as st
import requests
import io
from PIL import Image
import time

# 1. Page Config
st.set_page_config(page_title="Patna AI Studio Pro", layout="wide", page_icon="🏙️")

# 2. Translation & Pro Prompt Logic
def get_pro_prompt(text):
    try:
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=en&dt=t&q={text}"
        r = requests.get(url, timeout=10)
        eng = r.json()[0][0][0]
        return f"{eng}, cinematic lighting, 8k, masterpiece, highly detailed"
    except:
        return f"{text}, high quality, 4k"

# 3. Session State
if 'counter' not in st.session_state:
    st.session_state.counter = 0

# 4. Sidebar
with st.sidebar:
    st.title("🏙️ Patna AI Studio Pro")
    menu = st.radio("🛠️ Menu", ["🎨 Image Generator", "✂️ BG Remover"])
    st.markdown("---")
    st.metric("Daily Trials", f"{st.session_state.counter}/5")
    st.info("Bihar's Lite & Fast AI 🚀")

# --- FEATURE 1: IMAGE GENERATOR ---
if menu == "🎨 Image Generator":
    st.header("🎨 AI Image Studio")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        user_input = st.text_area("Aapka Idea (Hindi/English):")
    with col2:
        ratio = st.selectbox("Size (Aspect Ratio)", ["1:1 Square", "16:9 YouTube", "9:16 Reel"])
        dim = {"1:1 Square": (1024,1024), "16:9 YouTube": (1280,720), "9:16 Reel": (720,1280)}
        w, h = dim[ratio]

    if st.button("🚀 Generate"):
        if user_input:
            with st.spinner("Processing..."):
                pro = get_pro_prompt(user_input)
                st.info(f"✨ **Pro Prompt:** `{pro}`")
                
                img_url = f"https://image.pollinations.ai/prompt/{pro.replace(' ', '%20')}?width={w}&height={h}&nologo=true"
                res = requests.get(img_url)
                img = Image.open(io.BytesIO(res.content))
                
                st.image(img, use_container_width=True)
                buf = io.BytesIO()
                img.save(buf, format="PNG")
                st.download_button("📥 Download", buf.getvalue(), "patna_ai.png")
                st.session_state.counter += 1
                st.balloons()

# --- FEATURE 2: BG REMOVER (LITE MODE) ---
elif menu == "✂️ BG Remover":
    st.header("✂️ Background Remover")
    st.warning("⚠️ Lite Version: We are connecting external API to avoid Pytorch errors.")
    st.info("Please use 'Image Generator' while we finalize the API connection.")

