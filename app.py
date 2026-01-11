import streamlit as st
import os
import requests
from PIL import Image
import io

# --- CONFIGURATION & SECRETS ---
st.set_page_config(page_title="Vixan AI Studio Pro", layout="wide", initial_sidebar_state="expanded")

# API Keys from Streamlit Secrets
SEGMIND_API = st.secrets.get("SEGMIND_API_KEY", "")
ELEVEN_API = st.secrets.get("ELEVENLABS_API_KEY", "")

# Custom CSS for Premium Dark/Gold Theme
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #FFD700; color: black; font-weight: bold; }
    .stSidebar { background-color: #1a1c24; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR NAVIGATION ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=80)
st.sidebar.title("Vixan Studio v2.0")
menu = st.sidebar.radio("Menu", ["🏠 Home", "🖼️ AI Poster Lab", "🎙️ Voice Studio", "💳 Pricing & Payments", "📞 Support"])

# --- 1. HOME PAGE ---
if menu == "🏠 Home":
    st.title("Welcome to Vixan AI Media Studio Pro")
    st.subheader("Bihar's Most Advanced AI Content Creation Tool")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("🖼️ **Poster Lab**: Generate HD Political & Business Posters.")
    with col2:
        st.success("🎙️ **Voice Studio**: Professional Text-to-Speech & Cloning.")
    with col3:
        st.warning("💳 **Easy Payments**: Secured by Razorpay.")
    
    st.image("https://img.freepik.com/free-vector/abstract-technology-background_23-2148905210.jpg", use_container_width=True)

# --- 2. AI POSTER LAB ---
elif menu == "🖼️ AI Poster Lab":
    st.header("🖼️ Professional AI Poster Generator")
    
    col_a, col_b = st.columns([1, 1])
    
    with col_a:
        name = st.text_input("Enter Name (Leader/Brand):", "Rahul Kumar")
        slogan = st.text_area("Slogan/Message (Hindi):", "आपका विश्वास, हमारा विकास")
        
        # Automatic Font Detection from your 'fonts' folder
        font_files = [f for f in os.listdir("fonts") if f.endswith(".ttf")] if os.path.exists("fonts") else []
        selected_font = st.selectbox("Select Font Style:", font_files if font_files else ["Default"])
        
        prompt = st.text_area("Describe Background Design:", "Professional political background, saffron and green gradient, high resolution")

    with col_b:
        st.write("### Design Preview")
        if st.button("Generate Master Poster"):
            if not SEGMIND_API:
                st.error("Segmind API Key missing in Secrets!")
            else:
                url = "https://api.segmind.com/v1/sdxl1.0-txt2img"
                data = {
                    "prompt": f"{prompt}, centered text area, high quality, 4k",
                    "negative_prompt": "blurry, distorted face, bad anatomy",
                    "samples": 1, "scheduler": "dpmpp_2m", "num_inference_steps": 25, "guidance_scale": 7.5
                }
                headers = {"x-api-key": SEGMIND_API}
                
                with st.spinner("AI is designing your poster..."):
                    response = requests.post(url, json=data, headers=headers)
                    if response.status_code == 200:
                        st.image(response.content, caption=f"Design for {name}")
                        st.download_button("📥 Download HD Poster", response.content, "vixan_poster.png", "image/png")
                    else:
                        st.error("API Error. Please check your Segmind credits.")

# --- 3. VOICE STUDIO ---
elif menu == "🎙️ Voice Studio":
    st.header("🎙️ AI Voice & Audio Lab")
    
    # Show samples from your 'music' folder
    st.subheader("🎵 Listen to Voice Samples")
    music_files = [f for f in os.listdir("music") if f.endswith((".m4a", ".mp3"))] if os.path.exists("music") else []
    if music_files:
        selected_audio = st.selectbox("Choose a Sample:", music_files)
        st.audio(f"music/{selected_audio}")
    
    st.divider()
    
    text_input = st.text_area("Enter Text for AI Voice:", "नमस्ते, पटना AI स्टूडियो में आपका स्वागत है।")
    voice_speed = st.slider("Voice Speed", 0.5, 2.0, 1.0)
    
    if st.button("Generate AI Voice"):
        if not ELEVEN_API:
            st.error("ElevenLabs API Key missing!")
        else:
            # Simple ElevenLabs TTS Call
            tts_url = "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM"
            headers = {"xi-api-key": ELEVEN_API, "Content-Type": "application/json"}
            data = {"text": text_input, "model_id": "eleven_multilingual_v2"}
            
            with st.spinner("Converting text to professional voice..."):
                res = requests.post(tts_url, json=data, headers=headers)
                if res.status_code == 200:
                    st.audio(res.content, format="audio/mp3")
                    st.download_button("📥 Download Voice", res.content, "vixan_voice.mp3")

# --- 4. PRICING & PAYMENTS ---
elif menu == "💳 Pricing & Payments":
    st.header("💳 Choose Your Plan")
    p1, p2 = st.columns(2)
    
    with p1:
        st.markdown("""
        ### 🥈 Basic Plan
        * 10 Posters / Day
        * Standard Voices
        * **₹49 / Month**
        """)
        st.link_button("Buy Basic Plan", "https://rzp.io/l/your_link") # Update with your Razorpay link

    with p2:
        st.markdown("""
        ### 🥇 Pro Plan
        * Unlimited Posters
        * Voice Cloning Access
        * **₹199 / Month**
        """)
        st.link_button("Buy Pro Plan", "https://rzp.io/l/your_pro_link")

# --- 5. SUPPORT ---
elif menu == "📞 Support":
    st.header("📞 Contact Vixan Support")
    st.write("Facing issues? Reach out to us directly on WhatsApp.")
    st.success("WhatsApp: +91 XXXXX XXXXX") # Apna number dalein
    st.button("Chat on WhatsApp Now")

st.sidebar.markdown("---")
st.sidebar.write("v2.0 Beta | Powered by Patna AI Studio")
