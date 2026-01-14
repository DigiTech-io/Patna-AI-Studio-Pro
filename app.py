import streamlit as st
import requests
import uuid
import time
from gtts import gTTS

# =========================
# UI THEME & PRO STYLING
# =========================
st.set_page_config(page_title="Vixan AI Pro v28.0", layout="wide", page_icon="💎")

st.markdown("""
    <style>
    /* Main Background */
    .stApp { background-color: #0b0e14; color: #e0e0e0; }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] { 
        background: linear-gradient(180deg, #161b22 0%, #0d1117 100%) !important;
        border-right: 1px solid #30363d;
        min-width: 280px !important;
    }
    
    /* Buttons */
    .stButton>button { 
        border-radius: 8px; 
        background: linear-gradient(90deg, #ffd700, #ff8c00); 
        color: black; 
        font-weight: 700; 
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0px 0px 15px rgba(255, 215, 0, 0.4); }

    /* Pro Box */
    .pro-card {
        background: #1c2128;
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #ffd700;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.5);
    }
    </style>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR NAVIGATION
# =========================
with st.sidebar:
    st.markdown("<h1 style='color:#FFD700; text-align:center;'>👑 VIXAN PRO</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:12px;'>Bihar's Most Powerful AI Engine</p>", unsafe_allow_html=True)
    st.divider()
    
    menu = st.radio(
        "EXPLORE FEATURES",
        ["🏠 Dashboard", "🎨 AI Creative Lab", "🎙️ Pro Voice Studio", "🎞️ Talking Face (Pro)", "💳 Upgrade Plan"],
        index=0
    )
    
    st.divider()
    st.success("Status: Server Active 🟢")
    st.info("Version: 28.0 Ultra")

# =========================
# MODULES LOGIC
# =========================

# 1. DASHBOARD
if menu == "🏠 Dashboard":
    st.title("🚀 Welcome to Patna AI Studio")
    st.subheader("Professional AI Tools for Digital Media")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Image Gen", "Unlimited", "FREE")
    with col2:
        st.metric("Voice Clone", "Pro Only", "PREMIUM")
    with col3:
        st.metric("Video Lab", "10/Day", "LIMIT")

    st.image("https://img.freepik.com/free-vector/abstract-technology-background_23-2148905210.jpg", use_container_width=True)

# 2. AI CREATIVE LAB (FREE IMAGE & VIDEO)
elif menu == "🎨 AI Creative Lab":
    st.header("🎨 AI Creative Lab (Free Access)")
    tab1, tab2 = st.tabs(["🖼️ Image Generation", "🎬 Quick Video Fix"])
    
    with tab1:
        prompt = st.text_input("Enter your imagination (e.g. Narendra Modi in 3D animation style)")
        aspect = st.selectbox("Ratio", ["1:1 (Square)", "16:9 (Cinema)", "9:16 (Reel)"])
        
        if st.button("Generate HD Image"):
            with st.spinner("AI is painting your dream..."):
                seed = uuid.uuid4().int
                img_url = f"https://image.pollinations.ai/prompt/{prompt}?width=1024&height=1024&nologo=true&seed={seed}"
                st.image(img_url, caption=f"Result for: {prompt}", use_container_width=True)
                st.download_button("Download Image", requests.get(img_url).content, "vixan_ai.png")

    with tab2:
        st.info("🎬 Video Generation feature loading... (Limited to 2 sec previews)")
        v_prompt = st.text_input("Video Prompt:")
        if st.button("Generate Short Clip"):
            st.warning("Feature Integration in Progress. Use Pollinations API for video.")

# 3. PRO VOICE STUDIO
elif menu == "🎙️ Pro Voice Studio":
    st.header("🎙️ Advanced AI Voice Studio")
    text = st.text_area("Write script for Voice (Hindi/English):")
    voice_type = st.select_slider("Select Tone", ["Normal", "Deep", "Soft", "Professional"])
    
    col_v1, col_v2 = st.columns(2)
    with col_v1:
        if st.button("Generate Hindi AI Voice"):
            if text:
                tts = gTTS(text=text, lang='hi')
                tts.save("voice.mp3")
                st.audio("voice.mp3")
            else:
                st.error("Please write some text first!")
    with col_v2:
        st.button("Clone Custom Voice (PRO) 🔒")

# 4. TALKING FACE (PRO)
elif menu == "🎞️ Talking Face (Pro)":
    st.header("🎞️ Talking Face Studio")
    st.markdown("""
        <div class='pro-card'>
            <h3>🔒 Feature Locked</h3>
            <p>Photo se video banane ke liye Golden Pro Plan chahiye.</p>
        </div>
    """, unsafe_allow_html=True)
    st.link_button("Buy Golden Plan 🚀", "https://rzp.io/rzp/MdpzHUc")

# 5. UPGRADE PLAN (RAZORPAY)
elif menu == "💳 Upgrade Plan":
    st.header("💎 Upgrade to Golden Pro")
    st.markdown("""
        <div class='pro-card'>
            <h2 style='color:#ffd700;'>🥇 Golden Pro Plan</h2>
            <h1 style='font-size:50px;'>₹199 <small style='font-size:15px;'>/mo</small></h1>
            <ul style='text-align:left; display:inline-block;'>
                <li>✅ Unlimited 8K Political Posters</li>
                <li>✅ AI Voice Cloning (Clone Your Voice)</li>
                <li>✅ Talking Face AI Videos</li>
                <li>✅ No Watermark & Priority Support</li>
            </ul><br><br>
    """, unsafe_allow_html=True)
    st.link_button("PAY NOW & UNLOCK 💳", "https://rzp.io/rzp/MdpzHUc")
    st.markdown("</div>", unsafe_allow_html=True)

# =========================
# FLOATING WHATSAPP SUPPORT
# =========================
st.markdown("""
    <div style="position:fixed;bottom:30px;right:30px;z-index:100;">
        <a href="https://wa.me/918210073056?text=I%20want%20to%20verify%20my%20Vixan%20Pro%20Payment" target="_blank">
            <div style="background:#25d366;color:white;padding:15px 25px;border-radius:50px;font-weight:bold;box-shadow:0px 4px 15px rgba(0,0,0,0.3); display:flex; align-items:center;">
                💬 Help & Screenshot
            </div>
        </a>
    </div>
""", unsafe_allow_html=True)
