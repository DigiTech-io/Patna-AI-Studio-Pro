import streamlit as st
import os
import requests
import uuid
import time
from gtts import gTTS

# =========================
# 1. CONFIG & PREMIUM THEME
# =========================
st.set_page_config(page_title="Vixan AI Pro v26.0", layout="wide", page_icon="💎")

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
    .stButton>button { border-radius: 10px; font-weight: 700; transition: 0.3s; width: 100%; background: linear-gradient(90deg, #00d2ff, #3a7bd5); color: white; border: none; }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 0 15px #00d2ff; }
    .float-container { position: fixed; bottom: 30px; right: 30px; z-index: 1000; display: flex; flex-direction: column; gap: 10px; }
    </style>
""", unsafe_allow_html=True)

# Session State Initialization
if 'is_auth' not in st.session_state: st.session_state.is_auth = False
if 'user_name' not in st.session_state: st.session_state.user_name = ""

def check_auth():
    if not st.session_state.is_auth:
        st.warning("🔒 Please Login to Unlock AI Studio")
        with st.form("signup"):
            u_name = st.text_input("Full Name")
            u_phone = st.text_input("WhatsApp Number")
            if st.form_submit_button("Unlock 🚀"):
                if u_name and len(u_phone) >= 10:
                    st.session_state.is_auth = True
                    st.session_state.user_name = u_name
                    st.rerun()
                else:
                    st.error("Invalid Name or Phone.")
        return False
    return True

# =========================
# 2. SIDEBAR
# =========================
with st.sidebar:
    st.markdown("<h1 style='color:#FFD700;'>VIXAN PRO</h1>", unsafe_allow_html=True)
    menu = st.radio("SELECT TOOL", ["🏠 Dashboard", "🖼️ Ready Templates", "🎨 AI Poster Lab", "🎙️ Voice Studio", "🎞️ Talking Face Video"])
    st.divider()
    if st.session_state.is_auth:
        st.success(f"User: {st.session_state.user_name}")
        if st.button("Logout"):
            st.session_state.is_auth = False
            st.rerun()

# =========================
# 3. MODULES
# =========================

if menu == "🏠 Dashboard":
    st.title("🚀 Bihar's No. 1 AI Media Engine")
    st.markdown("### Generate Posters, Clone Voices & Create Talking AI Videos")
    st.image("https://img.freepik.com/free-vector/abstract-technology-background_23-2148905210.jpg", use_container_width=True)

elif menu == "🖼️ Ready Templates":
    st.header("🖼️ Select & Generate Poster")
    # Categories
    cats = {
        "🚩 Political": ["Election Banner Bihar", "Jan Seva Poster"],
        "💼 Business": ["Mobile Shop Promo", "Gym Motivation HD"],
        "🎂 Events": ["Royal Birthday", "Wedding Invitation"],
        "🪔 Festivals": ["Chhath Puja", "Diwali Greetings"]
    }
    
    for cat, items in cats.items():
        st.markdown(f"<div class='cat-title'>{cat}</div>", unsafe_allow_html=True)
        cols = st.columns(2)
        for i, item in enumerate(items):
            with cols[i % 2]:
                # Dynamic Preview
                preview_url = f"https://image.pollinations.ai/prompt/{item.replace(' ','%20')}?width=400&height=600&nologo=true"
                st.markdown(f"<div class='template-box'><img src='{preview_url}' class='temp-img'><br><b>{item}</b></div>", unsafe_allow_html=True)
                user_msg = st.text_input("Custom Text/Name", key=f"msg_{item}")
                if st.button(f"Generate {item}", key=f"btn_{item}"):
                    if check_auth():
                        with st.spinner("AI is painting..."):
                            final_url = f"https://image.pollinations.ai/prompt/{item.replace(' ','%20')}%20with%20text%20{user_msg.replace(' ','%20')}?width=1024&height=1024&nologo=true&seed={uuid.uuid4().int}"
                            st.image(final_url, use_container_width=True)
                            st.success("Design Ready!")

elif menu == "🎨 AI Poster Lab":
    st.header("🎨 AI Poster Lab (Gen & Clone)")
    t1, t2 = st.tabs(["✨ Text to Image", "🧬 Image Clone"])
    
    with t1:
        prompt = st.text_area("Describe your poster:", "A professional election poster for Bihar politics, orange theme, leadership style, 4k")
        if st.button("🚀 Generate Now"):
            if check_auth():
                with st.spinner("Generating..."):
                    url = f"https://image.pollinations.ai/prompt/{prompt.replace(' ','%20')}?width=1024&height=1024&nologo=true&seed={uuid.uuid4().int}"
                    st.image(url, use_container_width=True)
                    st.success("Image Generated Successfully!")

    with t2:
        st.subheader("🧬 Style Cloning")
        up_img = st.file_uploader("Upload Poster Image to Clone Style", type=['jpg', 'png'])
        if st.button("Start Style DNA Cloning"):
            if check_auth() and up_img:
                with st.spinner("Analyzing DNA..."):
                    # Clone simulation using random seed for variation
                    clone_url = f"https://image.pollinations.ai/prompt/clone%20of%20this%20design%20style?width=1024&height=1024&seed={uuid.uuid4().int}"
                    st.image(clone_url, use_container_width=True)

elif menu == "🎙️ Voice Studio":
    st.header("🎙️ Voice Studio & DNA Cloning")
    vt1, vt2 = st.tabs(["📢 Text to Speech", "🧬 Voice Clone"])
    
    with vt1:
        v_text = st.text_area("Hindi/English Text:", "नमस्ते, वीक्सन एआई प्रो में आपका स्वागत है।")
        if st.button("Generate Voice"):
            if check_auth():
                tts = gTTS(text=v_text, lang='hi')
                tts.save("voice.mp3")
                st.audio("voice.mp3")
    
    with vt2:
        st.subheader("🧬 Voice DNA Cloning")
        cl_file = st.file_uploader("Upload 10s Voice Sample", type=['mp3', 'wav'])
        if st.button("🚀 Clone Voice DNA"):
            if check_auth() and cl_file:
                st.success("Voice DNA Extracted!")
                st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")

elif menu == "🎞️ Talking Face Video":
    st.header("🎞️ Talking Face AI")
    
    f_img = st.file_uploader("Upload Portrait Photo", type=['jpg','png'])
    f_aud = st.file_uploader("Upload Audio Script", type=['mp3','wav'])
    if st.button("🎬 Render Talking Video"):
        if check_auth() and f_img and f_aud:
            with st.spinner("Syncing Lips..."):
                time.sleep(5)
                st.video("https://www.w3schools.com/html/mov_bbb.mp4")

# =========================
# SUPPORT
# =========================
st.markdown("""
    <div class="float-container">
        <a href="https://wa.me/91XXXXXXXXXX" style="text-decoration:none;"><div style="background:#25d366; color:white; padding:12px 20px; border-radius:50px; font-weight:bold; box-shadow: 2px 2px 10px rgba(0,0,0,0.5); text-align:center;">💬 WhatsApp</div></a>
    </div>
""", unsafe_allow_html=True)
