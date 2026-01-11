import streamlit as st
import os

# Page Config for Premium Look
st.set_page_config(page_title="Vixan AI Media Studio Pro", layout="wide")

# Sidebar for Navigation
st.sidebar.title("🚀 Vixan Studio Menu")
page = st.sidebar.radio("Go to:", ["🏠 Home", "🖼️ AI Poster Lab", "🎙️ Voice Studio", "💳 Payments"])

# Path for Fonts and Music
FONT_DIR = "fonts"
MUSIC_DIR = "music"

if page == "🏠 Home":
    st.title("Welcome to Vixan AI Media Studio Pro")
    st.info("Bihar's first advanced AI platform for professional media.")
    st.write("Aap niche diye gaye tools use karke posters aur voice generate kar sakte hain.")

elif page == "🖼️ AI Poster Lab":
    st.header("🖼️ Hindi Poster Maker")
    
    # Check if fonts exist
    available_fonts = [f for f in os.listdir(FONT_DIR) if f.endswith('.ttf')]
    selected_font = st.selectbox("Apna Font Chunein:", available_fonts)
    
    name = st.text_input("Leader Name:", "Rahul Kumar")
    slogan = st.text_input("Slogan:", "आपका विश्वास, हमारा विकास")
    
    if st.button("Generate HD Poster"):
        st.success(f"Poster ban raha hai {selected_font} font ke saath...")
        # (Poster generation logic yahan aayega)

elif page == "🎙️ Voice Studio":
    st.header("🎙️ AI Voice Studio")
    
    # Audio Samples from your folder
    audio_files = [f for f in os.listdir(MUSIC_DIR) if f.endswith(('.m4a', '.mp3'))]
    if audio_files:
        sample = st.selectbox("Sample Voice Sunnein:", audio_files)
        st.audio(os.path.join(MUSIC_DIR, sample))
    
    st.text_area("Yahan text likhein jise voice mein badalna hai:")
    st.slider("Voice Speed Control", 0.5, 2.0, 1.0)
    st.button("Generate AI Voice")

elif page == "💳 Payments":
    st.header("💳 Premium Subscription")
    st.write("Razorpay activation ke baad yahan payment links dikhenge.")
    st.button("Pay Now (Razorpay)")
