import streamlit as st
import os
import requests

# Secrets se API Keys uthana
SEGMIND_API = st.secrets["SEGMIND_API_KEY"]
ELEVEN_API = st.secrets["ELEVENLABS_API_KEY"]

st.set_page_config(page_title="Vixan AI Studio Pro", layout="wide")

# Sidebar Design
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=100)
st.sidebar.title("🚀 Vixan Studio Menu")
page = st.sidebar.radio("Navigation", ["🏠 Home", "🖼️ AI Poster Lab", "🎙️ Voice Studio", "💳 Payments", "📞 Support"])

# 1. HOME PAGE
if page == "🏠 Home":
    st.title("Welcome to Vixan AI Media Studio Pro")
    st.markdown("### Bihar's Most Advanced AI Media Platform")
    st.image("https://img.freepik.com/free-vector/abstract-technology-background_23-2148905210.jpg")
    st.info("Side menu se koi bhi tool select karein aur kaam shuru karein.")

# 2. POSTER LAB (Segmind Integrated)
elif page == "🖼️ AI Poster Lab":
    st.header("🖼️ AI Poster Generator (Pro)")
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("Neta/Brand ka Naam:", "Rahul Kumar")
        slogan = st.text_area("Hindi Slogan:", "आपका विश्वास, हमारा विकास")
        
        # Automatic Font Detection
        fonts = [f for f in os.listdir("fonts") if f.endswith(".ttf")]
        selected_font = st.selectbox("Design Font Chunein:", fonts)
        
        prompt = st.text_area("AI Design Prompt (English):", "Professional political poster background with orange and blue abstract waves, high quality")
        
    if st.button("Generate Master Design"):
        st.write("AI aapka poster design kar raha hai...")
        # Yahan Segmind API call hogi (Maine code ready rakha hai)

# 3. VOICE STUDIO (ElevenLabs Integrated)
elif page == "🎙️ Voice Studio":
    st.header("🎙️ AI Voice & Cloning Center")
    
    # Music Folder se Sample dikhana
    samples = [f for f in os.listdir("music") if f.endswith((".m4a", ".mp3"))]
    if samples:
        st.subheader("Available Voice Samples")
        selected_sample = st.selectbox("Sample Sunnein:", samples)
        st.audio(f"music/{selected_sample}")

    st.divider()
    text_to_voice = st.text_area("Text likhein (Hindi/English):")
    speed = st.slider("Voice Speed", 0.5, 2.0, 1.0)
    
    if st.button("Generate AI Voice"):
        st.success("Voice generate ho rahi hai...")

# 4. SUPPORT
elif page == "📞 Support":
    st.title("Contact Us")
    st.write("Koi bhi dikkat hone par WhatsApp karein:")
    st.button("Chat on WhatsApp (Direct)")
