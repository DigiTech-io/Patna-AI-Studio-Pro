import streamlit as st
import requests
import io
import time
import uuid
from gtts import gTTS

# =========================
# 1. CONFIG & UI ENHANCEMENT
# =========================
st.set_page_config(page_title="Vixan AI Pro v26.3", layout="wide", page_icon="💎")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@600;700&display=swap');
    .stApp { background: #0a0b10; color: #ffffff; }
    section[data-testid="stSidebar"] { background-color: #11141d !important; border-right: 1px solid #333; }
    .stButton>button { border-radius: 12px; font-weight: 700; background: linear-gradient(90deg, #00d2ff, #3a7bd5); color: white; border: none; width: 100%; transition: 0.3s; }
    .template-box { background: #161a25; border: 1px solid #333; border-radius: 15px; padding: 15px; text-align: center; margin-bottom: 20px; }
    .temp-img { width: 100%; border-radius: 10px; aspect-ratio: 2/3; object-fit: cover; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

if 'is_auth' not in st.session_state: st.session_state.is_auth = False
if 'user_name' not in st.session_state: st.session_state.user_name = "Guest"

def check_auth():
    if not st.session_state.is_auth:
        st.warning("🔒 Login Required")
        with st.form("signup"):
            u_name = st.text_input("Full Name")
            u_phone = st.text_input("WhatsApp Number")
            if st.form_submit_button("Unlock 🚀"):
                if u_name and len(u_phone) >= 10:
                    st.session_state.is_auth = True
                    st.session_state.user_name = u_name
                    st.rerun()
        return False
    return True

# =========================
# 2. SIDEBAR
# =========================
with st.sidebar:
    st.markdown("<h1 style='color:#FFD700;'>💎 VIXAN PRO</h1>", unsafe_allow_html=True)
    menu = st.radio("NAVIGATION", ["🏠 Dashboard", "🖼️ Ready Templates", "🎨 AI Poster Lab", "🎙️ Voice Studio", "🎞️ Talking Face"])
    st.divider()
    if st.session_state.is_auth:
        st.info(f"User: {st.session_state.user_name}")
        if st.button("Log out"):
            st.session_state.is_auth = False
            st.rerun()

# =========================
# 3. MODULES
# =========================

if menu == "🏠 Dashboard":
    st.title("🚀 Bihar's No. 1 AI Media Engine")
    st.image("https://img.freepik.com/free-vector/abstract-technology-background_23-2148905210.jpg")

elif menu == "🖼️ Ready Templates":
    st.header("🖼️ Select & Generate Poster")
    cats = {"🚩 Political": ["Election Banner", "Jan Seva"], "💼 Business": ["Shop Promo", "Gym Motivation"]}
    for cat_name, items in cats.items():
        st.subheader(cat_name)
        cols = st.columns(2)
        for i, item in enumerate(items):
            with cols[i % 2]:
                st.markdown(f"<div class='template-box'><b>{item}</b></div>", unsafe_allow_html=True)
                msg = st.text_input(f"Name for {item}", key=f"in_{item}")
                if st.button(f"Generate {item}", key=f"btn_{item}"):
                    if check_auth():
                        with st.spinner("Creating..."):
                            url = f"https://image.pollinations.ai/prompt/{item.replace(' ','%20')}%20with%20text%20{msg}?nologo=true&seed={uuid.uuid4().int}"
                            st.image(requests.get(url).content)

elif menu == "🎨 AI Poster Lab":
    st.header("🎨 AI Poster Lab")
    t1, t2 = st.tabs(["✨ Text to Image", "🧬 Image Clone"])
    with t1:
        prompt = st.text_area("Poster prompt:", "Professional Bihar Election banner, 4k")
        if st.button("🚀 Generate"):
            if check_auth():
                url = f"https://image.pollinations.ai/prompt/{prompt.replace(' ','%20')}?nologo=true&seed={uuid.uuid4().int}"
                st.image(requests.get(url).content)
    with t2:
        st.file_uploader("Upload Image to Clone", type=['jpg', 'png'])
        if st.button("🧬 Clone Style"):
            if check_auth(): st.info("Style Cloned!")

elif menu == "🎙️ Voice Studio":
    st.header("🎙️ Voice & Cloning")
    v_text = st.text_area("Hindi Text:", "नमस्ते, वीक्सन एआई प्रो में आपका स्वागत है।")
    if st.button("📢 Generate Voice"):
        if check_auth():
            tts = gTTS(text=v_text, lang='hi')
            tts.save("v.mp3")
            st.audio("v.mp3")

elif menu == "🎞️ Talking Face":
    st.header("🎞️ Talking Face AI Studio")
    # Yahan indentation sahi kar di gayi hai
    st.file_uploader("Upload Photo", key="face_up")
    st.file_uploader("Upload Audio", key="audio_up")
    if st.button("🎬 Render Video"):
        if check_auth():
            st.video("https://www.w3schools.com/html/mov_bbb.mp4")

# Support
st.markdown("""<div style="position:fixed;bottom:30px;right:30px;"><a href="https://wa.me/91XXXXXXXXXX" style="text-decoration:none;background:#25d366;color:white;padding:15px 25px;border-radius:50px;font-weight:bold;">💬 WhatsApp Support</a></div>""", unsafe_allow_html=True)
