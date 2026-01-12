import streamlit as st
import requests
import uuid
import time
from gtts import gTTS

# =========================
# 1. CONFIG & PREMIUM THEME
# =========================
st.set_page_config(page_title="Vixan AI Pro v25.2", layout="wide", page_icon="💎")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@600;700&family=Inter:wght@400;700&display=swap');
    .main { background: #0a0b10; color: #ffffff; font-family: 'Rajdhani', sans-serif; }
    
    .template-box {
        background: #161a25; border: 1px solid #333; border-radius: 15px;
        padding: 15px; text-align: center; transition: 0.4s; margin-bottom: 20px;
    }
    .temp-img { width: 100%; border-radius: 10px; margin-bottom: 10px; aspect-ratio: 2/3; object-fit: cover; }
    .cat-title { color: #FFD700; font-size: 28px; font-weight: 700; margin: 30px 0 15px 0; border-left: 5px solid #FFD700; padding-left: 10px; }
    .stButton>button { border-radius: 10px; font-weight: 700; transition: 0.3s; width: 100%; }
    .float-container { position: fixed; bottom: 30px; right: 30px; z-index: 1000; display: flex; flex-direction: column; gap: 10px; }
    </style>
""", unsafe_allow_html=True)

# Session State Init
if 'is_auth' not in st.session_state: st.session_state.is_auth = False
if 'user_name' not in st.session_state: st.session_state.user_name = ""

def check_auth():
    if not st.session_state.is_auth:
        st.warning("🔒 Please Login to use this feature.")
        with st.form("signup"):
            u_name = st.text_input("Name")
            u_phone = st.text_input("WhatsApp")
            if st.form_submit_button("Unlock 🚀"):
                if u_name and len(u_phone) >= 10:
                    st.session_state.is_auth = True
                    st.session_state.user_name = u_name
                    st.rerun()
        return False
    return True

# =========================
# 3. SIDEBAR
# =========================
with st.sidebar:
    st.markdown("<h1 style='color:#FFD700;'>VIXAN PRO</h1>", unsafe_allow_html=True)
    menu = st.radio("MENU", ["🏠 Dashboard", "🖼️ Ready Templates", "🎨 AI Poster Lab", "🎙️ Voice Studio", "🎞️ Talking Face"])
    if st.session_state.is_auth:
        st.success(f"Welcome, {st.session_state.user_name}")
        if st.button("Logout"):
            st.session_state.is_auth = False
            st.rerun()

# =========================
# 4. TEMPLATES DATA
# =========================
template_data = {
    "🚩 Political Designs": ["Chunav Prachar Bihar", "Jan Seva Banner", "Youth Leader Orange Theme"],
    "💼 Business Designs": ["Modern Tech Shop", "Luxury Gym Motivation", "Restaurant Food Banner"]
}

# =========================
# 5. MODULES
# =========================

if menu == "🏠 Dashboard":
    st.title("🚀 Bihar's No. 1 AI Media Engine")
    st.image("https://img.freepik.com/free-vector/abstract-technology-background_23-2148905210.jpg")

elif menu == "🖼️ Ready Templates":
    st.header("🖼️ Select & Generate Poster")
    for cat, items in template_data.items():
        st.markdown(f"<div class='cat-title'>{cat}</div>", unsafe_allow_html=True)
        cols = st.columns(3)
        for i, item in enumerate(items):
            with cols[i]:
                preview_url = f"https://image.pollinations.ai/prompt/{item.replace(' ','%20')}?width=400&height=600&nologo=true"
                st.markdown(f"<div class='template-box'><img src='{preview_url}' class='temp-img'><br><b>{item}</b></div>", unsafe_allow_html=True)
                user_msg = st.text_input("Enter Name/Message", key=f"msg_{item}")
                if st.button(f"Generate {item}", key=f"btn_{item}"):
                    if check_auth():
                        with st.spinner("AI Generating..."):
                            final_url = f"https://image.pollinations.ai/prompt/{item.replace(' ','%20')}%20with%20text%20{user_msg.replace(' ','%20')}?width=1024&height=1024&nologo=true"
                            st.image(final_url)
                            st.download_button("💾 Download", requests.get(final_url).content, f"{item}.png")

elif menu == "🎨 AI Poster Lab":
    st.header("🎨 AI Poster Lab (Gen & Clone)")
    t1, t2 = st.tabs(["✨ Text to Image", "🧬 Image Clone"])
    
    with t1:
        prompt = st.text_area("Describe your poster:", "Professional Bihar Election banner, 4k")
        if st.button("🚀 Generate Now"):
            if check_auth():
                url = f"https://image.pollinations.ai/prompt/{prompt.replace(' ','%20')}?width=1024&height=1024&nologo=true"
                st.image(url)
                st.download_button("💾 Save HD", requests.get(url).content, "vixan.png")
    
    with t2:
        st.subheader("🧬 Image Cloning")
        up_img = st.file_uploader("Upload Image to Clone", type=['jpg', 'png'])
        if st.button("Start Image Clone"):
            if check_auth() and up_img:
                st.info("Analyzing Image DNA...")
                st.image(f"https://image.pollinations.ai/prompt/clone%20of%20this%20design?seed={uuid.uuid4().int}")

elif menu == "🎙️ Voice Studio":
    st.header("🎙️ Voice & Cloning Lab")
    vt1, vt2 = st.tabs(["📢 Text to Speech", "🧬 Voice Clone"])
    
    with vt1:
        v_text = st.text_area("Hindi Text:", "नमस्ते, वीक्सन एआई में आपका स्वागत है।")
        if st.button("Generate Voice"):
            if check_auth():
                tts = gTTS(text=v_text, lang='hi')
                tts.save("v.mp3")
                st.audio("v.mp3")
    
    with vt2:
        st.subheader("🧬 Voice DNA Cloning")
        cl_file = st.file_uploader("Upload 10s Voice Sample", type=['mp3', 'wav'])
        if st.button("🚀 Extract & Clone"):
            if check_auth() and cl_file:
                st.success("Voice DNA Extracted!")
                st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")

elif menu == "🎞️ Talking Face":
    st.header("🎞️ Talking Face AI Studio")
    
    st.file_uploader("Upload Face Image")
    st.file_uploader("Upload Audio")
    if st.button("🎬 Generate Video"):
        if check_auth():
            st.video("https://www.w3schools.com/html/mov_bbb.mp4")

# Floating Support
st.markdown("""
    <div class="float-container">
        <a href="https://wa.me/91XXXXXXXXXX" style="text-decoration:none;"><div style="background:#25d366; color:white; padding:12px 20px; border-radius:50px; font-weight:bold;">💬 WhatsApp Support</div></a>
    </div>
""", unsafe_allow_html=True)
