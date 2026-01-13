import streamlit as st
import requests
import uuid
from gtts import gTTS

# =========================
# UI THEME & SETUP
# =========================
st.set_page_config(page_title="Vixan AI Pro v27.5", layout="wide", page_icon="💎")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    [data-testid="stSidebar"] { background-color: #1a1c24 !important; border-right: 2px solid #FFD700; }
    .stButton>button { border-radius: 12px; background: linear-gradient(90deg, #00d2ff, #3a7bd5); color: white; font-weight: bold; width: 100%; }
    .pro-box { border: 2px solid #FFD700; padding: 20px; border-radius: 15px; background: #1f222d; text-align: center; }
    </style>
""", unsafe_allow_html=True)

# Navigation
with st.sidebar:
    st.markdown("<h1 style='color:#FFD700;'>💎 VIXAN PRO</h1>", unsafe_allow_html=True)
    menu = st.radio("MENU", ["🏠 Dashboard", "💳 Buy Pro Plan", "🖼️ AI Poster Lab", "🎙️ Voice Studio", "🎞️ Talking Face"])
    st.divider()
    st.info("Patna AI Studio Pro")

# =========================
# MODULES LOGIC
# =========================

if menu == "🏠 Dashboard":
    st.title("🚀 Bihar's No. 1 AI Media Engine")
    st.write("Ab banaiye Professional Posters, Voice aur Videos ek click mein.")
    st.image("https://img.freepik.com/free-vector/abstract-technology-background_23-2148905210.jpg")
    
    # Hero Call to Action
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 👑 Golden Pro Access")
        st.write("Unlimited features unlock karne ke liye upgrade karein.")
    with col2:
        st.link_button("🚀 Upgrade to Pro Now", "https://rzp.io/rzp/MdpzHUc")

elif menu == "💳 Buy Pro Plan":
    st.header("💎 Unlock Golden Pro Features")
    st.markdown("<div class='pro-box'>", unsafe_allow_html=True)
    st.markdown("""
        ## ₹199 / Month
        * ✅ Unlimited 8K Political Posters
        * ✅ Business Promotion Banners
        * ✅ AI Voice Cloning Access
        * ✅ Talking Face AI Video Studio
        * ✅ 24/7 WhatsApp Priority Support
    """, unsafe_allow_html=True)
    
    # YOUR LIVE LINK INTEGRATED HERE
    st.link_button("PAY ₹199 & GET ACCESS 💳", "https://rzp.io/rzp/MdpzHUc")
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.warning("⚠️ Payment karne ke baad transaction screenshot WhatsApp support par bhejein.")

elif menu == "🖼️ AI Poster Lab":
    st.header("🎨 AI Poster Lab")
    prompt = st.text_input("Enter Prompt (e.g. Bihar Election 2026 Poster)")
    if st.button("Generate Poster"):
        url = f"https://image.pollinations.ai/prompt/{prompt}?nologo=true&seed={uuid.uuid4().int}"
        st.image(url)

elif menu == "🎙️ Voice Studio":
    st.header("🎙️ AI Voice Studio")
    text = st.text_area("Write Text here:")
    if st.button("Generate Hindi Voice"):
        tts = gTTS(text=text, lang='hi')
        tts.save("v.mp3")
        st.audio("v.mp3")

elif menu == "🎞️ Talking Face":
    st.header("🎞️ Talking Face Studio")
    st.error("🔒 This is a PRO feature. Please buy Golden Plan to unlock.")
    st.link_button("Unlock Now 🚀", "https://rzp.io/rzp/MdpzHUc")

# =========================
# WHATSAPP SUPPORT (Your Number)
# =========================
st.markdown("""
    <div style="position:fixed;bottom:30px;right:30px;z-index:100;">
        <a href="https://wa.me/918210073056?text=I%20have%20made%20the%20payment%20for%20Vixan%20Pro" target="_blank">
            <div style="background:#25d366;color:white;padding:15px 25px;border-radius:50px;font-weight:bold;box-shadow:2px 2px 10px rgba(0,0,0,0.5);">
                💬 Send Screenshot (Support)
            </div>
        </a>
    </div>
""", unsafe_allow_html=True)
