import streamlit as st
import os
import requests
import time

# --- 1. CONFIGURATION & THEME ---
st.set_page_config(page_title="Vixan AI Studio Pro", layout="wide", initial_sidebar_state="expanded")

# API Keys from Streamlit Secrets
SEGMIND_API = st.secrets.get("SEGMIND_API_KEY", "SG_dummy")
ELEVEN_API = st.secrets.get("ELEVENLABS_API_KEY", "sk_dummy")

# Custom CSS for Premium Interface
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { width: 100%; border-radius: 8px; height: 3.5em; background-image: linear-gradient(to right, #FFD700 , #FFA500); color: black; font-weight: bold; border: none; }
    .stSidebar { background-color: #1a1c24; border-right: 1px solid #333; }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea { background-color: #262730; color: white; border: 1px solid #444; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=80)
    st.title("Vixan Studio Pro")
    st.markdown("---")
    menu = st.radio("Dashboard Navigation", ["🏠 Home Dashboard", "🖼️ AI Poster Lab", "🎙️ Pro Voice Studio", "💳 Plans & Billing", "📞 Support"])
    st.markdown("---")
    st.caption("v2.5 Professional | Powered by Patna AI Studio")

# --- 3. PAGE LOGIC ---

# --- HOME ---
if menu == "🏠 Home Dashboard":
    st.title("Welcome to Vixan AI Media Studio Pro")
    st.subheader("Patna's #1 AI Media Creation Platform")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🖼️ Poster Lab")
        st.write("Generate professional political and business posters with 70+ Hindi fonts.")
    with col2:
        st.markdown("### 🎙️ Voice Studio")
        st.write("Convert text to high-quality AI voices (Male/Female) with speed control.")
    
    st.image("https://img.freepik.com/free-vector/abstract-technology-background_23-2148905210.jpg", use_container_width=True)

# --- POSTER LAB ---
elif menu == "🖼️ AI Poster Lab":
    st.header("🖼️ Advanced AI Poster Generator")
    c1, c2 = st.columns([1, 1.2])
    
    with c1:
        name = st.text_input("Name (Leader/Brand):", "Rahul Kumar")
        slogan = st.text_area("Hindi Slogan:", "आपका विश्वास, हमारा विकास")
        
        # Font Detection
        font_dir = "fonts"
        fonts = [f for f in os.listdir(font_dir) if f.endswith(".ttf")] if os.path.exists(font_dir) else ["Default"]
        selected_font = st.selectbox("Select Premium Hindi Font:", fonts)
        
        prompt = st.text_area("Design Style (AI Prompt):", "Political poster, saffron and green theme, luxury abstract background, 4k")
        
    with c2:
        st.markdown("### Live Preview")
        if st.button("🚀 Generate HD Poster"):
            with st.spinner("AI is crafting your design..."):
                time.sleep(2) # Simulation
                st.success("Design Completed!")
                # Yahan Segmind API integration hoga
                st.info("Poster will be displayed here after API key validation.")

# --- PRO VOICE STUDIO ---
elif menu == "🎙️ Pro Voice Studio":
    st.header("🎙️ Pro Voice Studio & Cloning")
    
    # Predefined Sample Section
    st.subheader("🎵 Audition Voice Samples")
    music_dir = "music"
    samples = [f for f in os.listdir(music_dir) if f.endswith((".m4a", ".mp3"))] if os.path.exists(music_dir) else []
    
    if samples:
        s_col1, s_col2 = st.columns(2)
        with s_col1:
            st.selectbox("Select Sample:", samples)
        with s_col2:
            st.audio(f"{music_dir}/{samples[0]}" if samples else None)

    st.divider()
    
    # Settings Section
    st.subheader("⚙️ AI Voice Settings")
    v_col1, v_col2 = st.columns(2)
    
    with v_col1:
        voice_gender = st.selectbox("Voice Profile:", ["Prem (Deep Male)", "Bella (Sweet Female)", "Antoni (Narrator)"])
        text_to_speak = st.text_area("Hindi/English Text:", "नमस्कार, आप सबका स्वागत है।")
    
    with v_col2:
        speed = st.slider("Speech Speed", 0.5, 2.0, 1.0)
        pitch = st.slider("Pitch (Tone)", -5, 5, 0)
        clarity = st.slider("Clarity/Stability", 0.0, 1.0, 0.7)

    if st.button("🔊 Generate AI Voice & Video Preview"):
        st.info("Generating voice using ElevenLabs AI...")
        # ElevenLabs Code logic
        st.success("Audio Generated!")
        
        st.subheader("📺 Production Video Preview")
        # Placeholder for Video Preview feature
        st.video("https://www.w3schools.com/html/mov_bbb.mp4")
        st.download_button("📥 Download MP3 Audio", "sample_data", "vixan_voice.mp3")

# --- PAYMENTS ---
elif menu == "💳 Plans & Billing":
    st.header("💳 Subscription Plans")
    p1, p2, p3 = st.columns(3)
    
    with p1:
        st.markdown("### 🥈 Basic\n**₹49/mo**\n- 10 Posters/day\n- Standard Voices")
        st.link_button("Buy Basic", "https://rzp.io/l/basic")
    with p2:
        st.markdown("### 🥇 Pro\n**₹199/mo**\n- Unlimited Posters\n- AI Voice Cloning")
        st.link_button("Buy Pro", "https://rzp.io/l/pro")
    with p3:
        st.markdown("### 👑 Enterprise\n**Custom Pricing**\n- API Access\n- Custom Fonts")
        st.link_button("Contact Sales", "https://wa.me/yournumber")

# --- SUPPORT ---
elif menu == "📞 Support":
    st.header("📞 Contact Technical Support")
    st.write("24/7 Support for Patna AI Studio Users.")
    st.success("WhatsApp: +91 XXXXX XXXXX")
    st.button("Open WhatsApp Chat")
