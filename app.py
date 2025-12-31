import streamlit as st
import requests
import io
import base64
from PIL import Image
import time
import urllib.parse
import replicate

# 1. Page Config & Visibility Fix
st.set_page_config(page_title="Patna AI Studio Pro", layout="wide", page_icon="🏙️")

st.markdown("""
<style>
    .stApp { background-color: #ffffff !important; }
    .pro-box {
        background: #ffffff !important;
        border: 3px solid #007bff !important;
        border-radius: 15px !important;
        padding: 20px !important;
        margin-bottom: 20px !important;
    }
    input, textarea, [data-baseweb="select"] {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 2px solid #0056b3 !important;
        font-weight: 600 !important;
    }
    h1, h2, h3, label, p { color: #1a365d !important; font-weight: 800 !important; }
    .stButton > button {
        background: linear-gradient(45deg, #007bff 0%, #0056b3 100%) !important;
        color: white !important; border-radius: 50px !important;
    }
</style>
""", unsafe_allow_html=True)

# 2. Logic: Prompt Gen & Video Render
def pro_prompt_gen(text):
    try:
        encoded = urllib.parse.quote(text)
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=en&dt=t&q={encoded}"
        r = requests.get(url, timeout=10).json()
        return f"{r[0][0][0]}, ultra-realistic 8k, cinematic, flux style"
    except: return f"{text}, 8k resolution, masterpiece"

# 3. Sidebar (Support: 8210073056)
with st.sidebar:
    st.title("🏙️ Patna AI Pro")
    menu = st.radio("Navigation", ["🎨 Image Studio", "🎥 Video AI (10s)", "📞 Support"])
    st.markdown("---")
    st.markdown("📞 **Quick Support:**")
    st.markdown("[📱 WhatsApp Chat](https://wa.me/918210073056)")
    st.markdown("📞 **Call: +91 8210073056**")

# 4. Feature: Image Studio
if menu == "🎨 Image Studio":
    st.header("🎨 Ultra HD Image Studio")
    engine = st.selectbox("🚀 AI Engine", ["🆓 Pollinations (Free)", "💎 Segmind Pro (HQ)"])
    st.markdown('<div class="pro-box">', unsafe_allow_html=True)
    idea = st.text_input("💡 Idea (Hindi/English):")
    if st.button("🚀 Create Image"):
        with st.spinner("🎨 Generating..."):
            try:
                final_p = pro_prompt_gen(idea)
                if "Segmind" in engine and "SEGMIND_API_KEY" in st.secrets:
                    res = requests.post("https://api.segmind.com/v1/flux-1-dev", 
                                        json={"prompt": final_p, "width": 1024, "height": 1024}, 
                                        headers={"x-api-key": st.secrets["SEGMIND_API_KEY"]})
                else:
                    res = requests.get(f"https://image.pollinations.ai/prompt/{urllib.parse.quote(final_p)}?nologo=true")
                st.image(res.content, use_container_width=True)
                st.download_button("💾 Save Art", res.content, "patna_ai.png", "image/png")
            except Exception as e: st.error(f"Error: {e}")
    st.markdown('</div>', unsafe_allow_html=True)

# 5. FEATURE ACTIVE: 10s Video AI
elif menu == "🎥 Video AI (10s)":
    st.header("🎬 10-Second Video Studio")
    st.markdown('<div class="pro-box">', unsafe_allow_html=True)
    v_idea = st.text_input("🎥 Describe your video:")
    if st.button("🚀 Generate 10s Video"):
        if v_idea and "REPLICATE_API_TOKEN" in st.secrets:
            with st.spinner("🎬 AI Rendering (Take 1-2 mins)..."):
                try:
                    img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(v_idea)}?width=1024&height=576&nologo=true"
                    output = replicate.run(
                        "stability-ai/stable-video-diffusion:3f045714406646506307994ca6f5ed6090533314ca2e361be92d3b248e89e023",
                        input={"input_image": img_url}
                    )
                    st.video(output[0])
                    st.success("🎉 Video Ready!")
                except Exception as e: st.error(f"Error: {e}")
        else: st.error("Add Replicate Token in Secrets!")
    st.markdown('</div>', unsafe_allow_html=True)

elif menu == "📞 Support":
    st.info("Owner: Chaman Jha | WhatsApp: +91 8210073056")

st.markdown("---")
st.markdown("<p style='text-align: center;'>✨ Patna AI Studio Pro v15.0 | 8210073056</p>", unsafe_allow_html=True)

