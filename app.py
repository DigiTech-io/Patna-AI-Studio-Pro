import streamlit as st
import requests
import io
from PIL import Image
import time
import urllib.parse

# 1. Page Configuration
st.set_page_config(page_title="Patna AI Studio Pro", layout="wide", page_icon="🏙️")

# 2. 100% Visibility UI Fix (Har Mode mein saaf dikhega)
st.markdown("""
<style>
    /* Background ko hamesha dark blue rakha hai taaki contrast bana rahe */
    .stApp {
        background-color: #0e1117 !important;
    }
    
    /* Main Content Area ko saaf dikhane ke liye */
    [data-testid="stVerticalBlock"] > div {
        color: white !important;
    }

    /* Input Boxes aur Textarea ko White kar diya hai taaki black text saaf dikhe */
    input, textarea, [data-baseweb="select"] {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 2px solid #4facfe !important;
        border-radius: 10px !important;
        font-weight: bold !important;
    }

    /* Pro-box ko thoda solid background diya hai visibility ke liye */
    .pro-box {
        background: rgba(255, 255, 255, 0.08);
        border-radius: 15px;
        border: 1px solid #4facfe;
        padding: 20px;
        margin-bottom: 20px;
    }

    /* Titles aur Labels ko Bright White kiya hai */
    h1, h2, h3, label, p, .stMarkdown {
        color: #ffffff !important;
        font-weight: bold !important;
        text-shadow: 1px 1px 2px black;
    }
    
    /* Sidebar buttons aur text visibility */
    [data-testid="stSidebar"] * {
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. Prompt Magic Logic
@st.cache_data(ttl=3600)
def convert_to_mj_pro(text):
    try:
        encoded = urllib.parse.quote(text)
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=en&dt=t&q={encoded}"
        r = requests.get(url, timeout=10).json()
        eng = r[0][0][0]
        return f"{eng}, hyper-realistic, 8k, cinematic lighting, masterpiece, flux style"
    except Exception:
        return f"{text}, 8k, masterpiece"

# 4. Session State Setup
if 'user_name' not in st.session_state: st.session_state.user_name = ""
if 'magic_p' not in st.session_state: st.session_state.magic_p = ""

# 5. Sidebar (Dono Engine ke saath)
with st.sidebar:
    st.title("🏙️ Patna AI Pro")
    if not st.session_state.user_name:
        st.subheader("👤 Join Studio")
        name_input = st.text_input("Enter Your Name", key="name_input")
        if st.button("✅ Join", key="join_btn"):
            if name_input.strip():
                st.session_state.user_name = name_input.strip()
                st.rerun()
    else:
        st.success(f"👋 Namaste, {st.session_state.user_name}!")
    
    st.markdown("---")
    engine = st.selectbox("🚀 AI Engine", ["🆓 Pollinations (Free)", "💎 Segmind Pro (HQ)"], key="engine_select")
    menu = st.radio("Navigation", ["🎨 Image Studio", "🎥 Video AI", "📞 Support"], key="main_menu")
    st.markdown("---")
    st.link_button("📱 WhatsApp", "https://wa.me/918210073056")
    st.link_button("📞 Call Admin", "tel:+918210073056")

# 6. Main Logic
if menu == "🎨 Image Studio":
    st.header(f"✨ {engine} Powered")
    
    # Step 1: Prompt Converter
    st.markdown('<div class="pro-box">', unsafe_allow_html=True)
    st.subheader("🪄 Step 1: Pro Prompt")
    user_idea = st.text_input("Describe your idea:", placeholder="Example: Tiger in Patna...", key="user_idea")
    if st.button("🪄 Convert", key="convert_btn"):
        if user_idea.strip():
            with st.spinner("🔮 Converting..."):
                st.session_state.magic_p = convert_to_mj_pro(user_idea)
                st.rerun()
    
    if st.session_state.magic_p:
        st.code(st.session_state.magic_p)
    st.markdown('</div>', unsafe_allow_html=True)

    # Step 2: Image Generation
    st.markdown('<div class="pro-box">', unsafe_allow_html=True)
    st.subheader("🖼️ Step 2: Generate HD Art")
    final_prompt = st.text_area("Final Prompt:", value=st.session_state.magic_p, height=100, key="final_prompt")
    ratio = st.selectbox("📐 Size", ["1:1 Square", "9:16 Reels", "16:9 YouTube"], key="ratio")
    dims = {"1:1 Square": (1024,1024), "9:16 Reels": (720,1280), "16:9 YouTube": (1280,720)}
    w, h = dims[ratio]
    
    if st.button("🚀 Generate HD Image", key="gen_btn"):
        if final_prompt.strip():
            with st.spinner(f"🎨 Generating..."):
                try:
                    if "Segmind" in engine and "SEGMIND_API_KEY" in st.secrets:
                        api_url = "https://api.segmind.com/v1/flux-1-dev"
                        data = {"prompt": final_prompt, "seed": int(time.time()), "steps": 25, "width": w, "height": h}
                        headers = {"x-api-key": st.secrets["SEGMIND_API_KEY"]}
                        res = requests.post(api_url, json=data, headers=headers, timeout=90)
                    else:
                        encoded_p = urllib.parse.quote(final_prompt)
                        api_url = f"https://image.pollinations.ai/prompt/{encoded_p}?width={w}&height={h}&nologo=true"
                        res = requests.get(api_url, timeout=60)
                    
                    if res.status_code == 200:
                        st.image(res.content, use_container_width=True)
                        st.download_button("💾 Download", res.content, "PatnaAI.png", "image/png")
                        st.balloons()
                    else: st.error("Engine busy, try again!")
                except Exception as e: st.error(f"Error: {e}")
    st.markdown('</div>', unsafe_allow_html=True)

elif menu == "📞 Support":
    st.header("📱 Support")
    st.info("WhatsApp: +91 8210073056")
    st.success("Patna, Bihar")

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: white;'>✨ Patna AI Studio Pro v8.3</p>", unsafe_allow_html=True)

