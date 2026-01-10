import streamlit as st
import requests
import base64
from io import BytesIO

# --- UI SETTINGS ---
st.set_page_config(page_title="Vixan AI Studio Pro", layout="wide", page_icon="🚀")

# --- SECRETS & CONFIG ---
# Make sure these are set in your .streamlit/secrets.toml
SEGMIND_KEY = st.secrets.get("SEGMIND_API_KEY")
ELEVEN_KEY = st.secrets.get("ELEVENLABS_API_KEY")

# --- HELPER FUNCTIONS ---
def generate_image(prompt):
    """Calls Segmind Flux Schnell API"""
    url = "https://api.segmind.com/v1/flux-schnell" # Using Flux Schnell for speed
    payload = {
        "prompt": prompt,
        "steps": 4,
        "seed": 12345,
        "sampler": "euler",
        "samples": 1,
        "guidance_scale": 3.5,
        "shape": "landscape"
    }
    headers = {"x-api-key": SEGMIND_KEY}
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.content
    else:
        st.error(f"Error: {response.text}")
        return None

# --- APP LOGIC ---
st.title("🚀 Vixan AI Studio Pro")
st.markdown("---")

tab1, tab2, tab3 = st.tabs(["🎨 Poster Studio", "🖼️ Imagine (Text-to-Image)", "🎙️ AI Audio"])

# --- TAB 1: POSTER STUDIO ---
with tab1:
    st.header("Political & Business Poster Maker")
    col1, col2 = st.columns([1, 2])
    
    with col1:
        name = st.text_input("Naam Likhein (Person Name)")
        slogan = st.text_input("Slogan (Naara)")
        theme = st.selectbox("Theme", ["Professional Business", "Political Campaign", "Movie Style"])
        btn_poster = st.button("Generate Poster ✨")

    with col2:
        if btn_poster:
            if SEGMIND_KEY:
                with st.spinner("Designing your poster..."):
                    # Crafting a detailed prompt for better results
                    full_prompt = f"A high-quality {theme} poster for {name} with text '{slogan}'. Professional lighting, cinematic background, 8k resolution."
                    img_data = generate_image(full_prompt)
                    if img_data:
                        st.image(img_data, caption=f"Poster for {name}")
                        st.download_button("Download Poster", img_data, file_name="poster.jpg", mime="image/jpeg")
            else:
                st.error("API Key Missing! Please add SEGMIND_API_KEY in secrets.")

# --- TAB 2: IMAGINE ENGINE ---
with tab2:
    st.header("AI Imagine Engine")
    prompt = st.text_area("Describe your imagination in detail...", placeholder="A futuristic city with flying cars and neon lights...")
    if st.button("Generate Art 🖼️"):
        if prompt and SEGMIND_KEY:
            with st.spinner("Creating high-resolution art..."):
                img_data = generate_image(prompt)
                if img_data:
                    st.image(img_data, use_container_width=True)
                    st.download_button("Download Image", img_data, file_name="ai_art.jpg", mime="image/jpeg")
        else:
            st.warning("Please enter a prompt and ensure API key is set.")

# --- TAB 3: AI AUDIO ---
with tab3:
    st.header("Professional Audio Studio")
    script = st.text_area("Script for Audio", placeholder="Namaste, Vixan AI Studio mein aapka swagat hai.")
    voice_id = "pNInz6obpgDQGcFmaJgB" # Example voice (Adam)
    
    if st.button("Generate Audio 🎙️"):
        if ELEVEN_KEY and script:
            with st.spinner("Synthesizing voice..."):
                url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
                headers = {"xi-api-key": ELEVEN_KEY, "Content-Type": "application/json"}
                data = {"text": script, "model_id": "eleven_multilingual_v2"}
                
                response = requests.post(url, json=data, headers=headers)
                if response.status_code == 200:
                    st.audio(response.content, format='audio/mp3')
                    st.success("Audio Ready!")
                else:
                    st.error("Audio generation failed. Check your ElevenLabs API quota.")
        else:
            st.error("API Key missing or Script empty!")

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/artificial-intelligence.png")
    st.title("Settings")
    st.info("App Version: 2.0.1")
    st.warning("🎬 Video Gen: Coming Soon in Pro+")
