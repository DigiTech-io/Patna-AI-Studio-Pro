import streamlit as st
import os
import requests
from gtts import gTTS # Google Text-to-Speech (Free)

# --- CONFIG & THEME ---
st.set_page_config(page_title="Vixan AI Studio Pro", layout="wide")

# --- SIDEBAR ---
with st.sidebar:
    st.title("🚀 Vixan Studio")
    menu = st.radio("Menu", ["🖼️ Poster Lab", "🎙️ Voice Studio", "💳 Upgrade to Pro"])

# --- 1. POSTER LAB (Free & Pro) ---
if menu == "🖼️ Poster Lab":
    st.header("🖼️ AI Poster Generator")
    prompt = st.text_area("Aapko kaisa design chahiye? (English me likhein):", "Political poster background, abstract orange and green, 4k")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎨 Generate Free Poster (Pollinations)"):
            with st.spinner("Free AI design bana raha hai..."):
                # Pollinations AI - 100% Free
                free_url = f"https://image.pollinations.ai/prompt/{prompt.replace(' ', '%20')}?width=1024&height=1024&nologo=true"
                st.image(free_url, caption="Free AI Generated Poster")
                st.info("Ye Pollinations AI dwara banaya gaya hai (Free).")

    with col2:
        if st.button("🔥 Generate Pro Poster (Segmind)"):
            st.warning("Iske liye Segmind API Key ki zaroorat hai.")
            # Segmind logic yahan (Jo pehle diya tha)

# --- 2. VOICE STUDIO (Free & Pro) ---
elif menu == "🎙️ Voice Studio":
    st.header("🎙️ AI Voice Studio")
    text_input = st.text_area("Yahan Hindi text likhein:", "नमस्ते, आपका स्वागत है।")
    
    v_col1, v_col2 = st.columns(2)
    
    with v_col1:
        if st.button("📢 Generate Free Voice (Google)"):
            if text_input:
                with st.spinner("Google AI voice bana raha hai..."):
                    tts = gTTS(text=text_input, lang='hi')
                    tts.save("free_voice.mp3")
                    st.audio("free_voice.mp3")
                    st.success("Google Voice Ready! (Unlimited Free)")
            else:
                st.error("Pehle kuch likhiye!")

    with v_col2:
        if st.button("💎 Generate Pro Voice (ElevenLabs)"):
            st.warning("Premium voice ke liye ElevenLabs key chahiye.")

# --- 3. UPGRADE SECTION ---
elif menu == "💳 Upgrade to Pro":
    st.title("Pro Features se zyada kamayein!")
    st.write("Free version me normal quality milti hai. Pro me HD aur asli insani awaaz milti hai.")
    st.link_button("Buy Pro Plan - ₹199", "https://rzp.io/l/vixan_pro")
