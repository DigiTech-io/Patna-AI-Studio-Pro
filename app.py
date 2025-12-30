import streamlit as st
import requests
import io
from PIL import Image
import time
import numpy as np

# ERROR PREVENTION: rembg conditionally load karo
try:
    from rembg import remove
    BG_AVAILABLE = True
except:
    BG_AVAILABLE = False
    st.warning("BG Remover temporarily unavailable")

st.set_page_config(page_title="Patna AI Studio Pro", layout="wide", page_icon="🏙️")

# Session State
if 'counter' not in st.session_state:
    st.session_state.counter = 0

with st.sidebar:
    st.title("🏙️ Patna AI Studio Pro")
    menu = st.radio("🛠️ Choose Service", ["🎨 Image Generator", "✂️ BG Remover"])
    st.metric("Trials", f"{st.session_state.counter}/5")

def pro_prompt(text):
    try:
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=en&dt=t&q={text}"
        r = requests.get(url, timeout=10)
        eng = r.json()[0][0][0]
        return f"{eng}, 8k, cinematic, masterpiece"
    except:
        return text

if menu == "🎨 Image Generator":
    st.header("🎨 AI Image Generator")
    prompt = st.text_area("Hindi/English prompt:")
    
    if st.button("🚀 Generate", type="primary"):
        if prompt:
            with st.spinner("Generating..."):
                pro = pro_prompt(prompt)
                st.info(f"**Pro:** {pro}")
                
                url = f"https://image.pollinations.ai/prompt/{pro.replace(' ', '%20')}?width=1024&height=1024&nologo=true"
                res = requests.get(url, timeout=30)
                img = Image.open(io.BytesIO(res.content))
                
                st.image(img, use_column_width=True)
                buf = io.BytesIO()
                img.save(buf, "PNG")
                st.download_button("💾 Download", buf.getvalue(), "ai.png", "image/png")
                st.session_state.counter += 1
        else:
            st.warning("Prompt enter karo!")

elif menu == "✂️ BG Remover":
    st.header("✂️ Background Remover")
    if BG_AVAILABLE:
        file = st.file_uploader("Upload", type=['png','jpg'])
        if file:
            img = Image.open(file)
            st.image(img, caption="Original", width=300)
            
            if st.button("🧹 Remove BG"):
                with st.spinner("Processing..."):
                    result = remove(img)
                    st.image(result, caption="Clean!", width=300)
                    
                    buf = io.BytesIO()
                    result.save(buf, "PNG")
                    st.download_button("💾 Download", buf.getvalue(), "clean.png", "image/png")
                    st.session_state.counter += 1
    else:
        st.info("🔧 BG Remover setup ho raha hai... Image Generator use karo!")

st.markdown("---")
st.markdown("*Patna AI Studio - Bihar Pride 🚀*")
