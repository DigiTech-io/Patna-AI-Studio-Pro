import streamlit as st
import requests
import io
import base64  # Fixed: Added missing import
from PIL import Image
import time
import urllib.parse
import replicate

# 1. Page Configuration
st.set_page_config(page_title="Patna AI Studio Pro", layout="wide", page_icon="🏙️")

# 2. ULTRA-HD VISIBILITY UI
st.markdown("""
<style>
    .stApp { background-color: #ffffff !important; }
    .pro-box {
        background: #ffffff !important;
        border: 3px solid #007bff !important;
        border-radius: 15px !important;
        padding: 20px !important;
        margin-bottom: 20px !important;
        box-shadow: 0 4px 15px rgba(0,123,255,0.1) !important;
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
        color: white !important; border-radius: 50px !important; font-weight: bold !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. AI Helper Functions
@st.cache_data(ttl=300)
def pro_prompt_gen(text):
    try:
        encoded = urllib.parse.quote(text)
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=en&dt=t&q={encoded}"
        r = requests.get(url, timeout=10).json()
        eng = r[0][0][0]
        return f"{eng}, ultra-realistic 8k, cinematic lighting, masterpiece, flux style"
    except Exception:
        return f"{text}, 8k resolution, masterpiece"

# 4. Session State
if 'pro_prompt' not in st.session_state: st.session_state.pro_prompt = ""
if 'user_name' not in st.session_state: st.session_state.user_name = ""

# 5. Sidebar (Call & WhatsApp: 8210073056)
with st.sidebar:
    st.title("🏙️ Patna AI Pro")
    if st.session_state.user_name:
        st.success(f"👋 Namaste {st.session_state.user_name}!")
    else:
        name_in = st.text_input("Enter Your Name:")
        if st.button("✅ Join Studio"):
            if name_in.strip():
                st.session_state.user_name = name_in.strip()
                st.rerun()
    st.markdown("---")
    menu = st.radio("Navigation", ["🎨 Image Studio", "🎥 Video AI (10s)", "📞 Support"])
    st.markdown("---")
    st.subheader("📞 Quick Support")
    st.markdown("[📱 WhatsApp Chat](https://wa.me/918210073056)")
    st.markdown("📞 **Call: +91 8210073056**")

# 6. FEATURE 1: IMAGE STUDIO
if menu == "🎨 Image Studio":
    st.header("🎨 Ultra HD Image Studio")
    engine = st.selectbox("🚀 Choose Engine", ["🆓 Pollinations (Unlimited Free)", "💎 Segmind Pro (High Quality)"])
    
    st.markdown('<div class="pro-box">', unsafe_allow_html=True)
    idea = st.text_input("💡 Idea (Hindi/English):", placeholder="Example: Tiger at Patna Zoo...")
    
    if st.button("🪄 Auto Generate Pro Prompt"):
        if idea.strip():
            st.session_state.pro_prompt = pro_prompt_gen(idea)
            st.rerun()
    
    if st.session_state.pro_prompt:
        final_p = st.text_area("✏️ Final Prompt:", value=st.session_state.pro_prompt, height=100)
        ratio = st.selectbox("📐 Size", ["1:1 Square", "9:16 Reels", "16:9 YouTube"])
        
        if st.button("🚀 Create Image"):
            with st.spinner("🎨 Generating..."):
                try:
                    dims = {"1:1 Square": (1024,1024), "9:16 Reels": (720,1280), "16:9 YouTube": (1280,720)}
                    w, h = dims[ratio]
                    if "Segmind" in engine and "SEGMIND_API_KEY" in st.secrets:
                        res = requests.post("https://api.segmind.com/v1/flux-1-dev", 
                                            json={"prompt": final_p, "width": w, "height": h}, 
                                            headers={"x-api-key": st.secrets["SEGMIND_API_KEY"]})
                        if res.status_code == 200:
                            img = Image.open(io.BytesIO(res.content))
                    else:
                        res = requests.get(f"https://image.pollinations.ai/prompt/{urllib.parse.quote(final_p)}?width={w}&height={h}&nologo=true")
                        img = Image.open(io.BytesIO(res.content))
                    
                    st.image(img, use_container_width=True)
                    st.download_button("💾 Save HD Art", res.content, "patna_ai.png", "image/png")
                    st.balloons()
                except Exception as e: st.error(f"Error: {e}")
    st.markdown('</div>', unsafe_allow_html=True)

# 7. FEATURE 2: 10s VIDEO AI
elif menu == "🎥 Video AI (10s)":
    st.header("🎬 10-Second Video AI Studio")
    st.markdown('<div class="pro-box">', unsafe_allow_html=True)
    v_idea = st.text_input("🎥 Describe your video:", placeholder="Drone shot of Patna Marine Drive...")
    
    if st.button("🚀 Generate 10s AI Video"):
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
st.markdown("<p style='text-align: center;'>✨ Patna AI Studio Pro v14.1 | 8210073056</p>", unsafe_allow_html=True)

