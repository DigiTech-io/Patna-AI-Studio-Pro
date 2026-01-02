
import streamlit as st
import google.generativeai as genai
import requests
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import io
import os
from pydub import AudioSegment
from streamlit_option_menu import option_menu

# --- 1. CONFIGURATION (Direct Keys) ---
GEMINI_API_KEY = "AIzaSyBj30UE5TqeQab1-igbRtE-x-L7SkIvvsg"
ELEVENLABS_API_KEY = "sk_f3d35f5de4846b323eda8bbacf8ed0fb9249ae180a170b86"

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# --- 2. AUDIO ENGINE ---
def generate_voice(text, output_path):
    url = "https://api.elevenlabs.io/v1/text-to-speech/pNInz6obpg8ndclAY7gu"
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVENLABS_API_KEY
    }
    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        with open(output_path, "wb") as f:
            f.write(response.content)
        return True
    return False

def mix_audio(voice_path, music_name):
    voice = AudioSegment.from_file(voice_path)
    # Music folder se file uthana
    music_path = f"music/{music_name}"
    if os.path.exists(music_path):
        bg_music = AudioSegment.from_file(music_path)
        bg_music = bg_music - 20 # Background music ki volume kam karna
        # Voice aur Music ko merge karna
        combined = bg_music.overlay(voice)
        final_path = "final_election_ad.mp3"
        combined.export(final_path, format="mp3")
        return final_path
    return voice_path

# --- 3. UI SETUP ---
st.set_page_config(page_title="Patna AI Studio Pro v5.2", layout="wide")

with st.sidebar:
    selected = option_menu("Main Menu", ["🚀 Ad Maker", "🗳️ Election Tool", "📞 Support"], 
                          icons=["magic", "mic", "whatsapp"], default_index=0)
    is_followed = st.checkbox("I have Followed/Subscribed ✅", value=False)

# --- SECTION 1: BUSINESS AD MAKER (Purana Code) ---
if selected == "🚀 Ad Maker":
    st.markdown("### 💎 Professional Business Ad Maker")
    # ... (Yahan aapka purana Image generation logic as-it-is rahega)
    st.info("Aapka purana Ad Maker yahan surakshit hai.")

# --- SECTION 2: ELECTION TOOL (Naya Code) ---
elif selected == "🗳️ Election Tool":
    st.header("🗳️ Election Audio Campaign Maker")
    
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Candidate Name", "Mukesh Kumar")
        pad = st.text_input("Pad (Post)", "Mukhiya")
    with col2:
        panchayat = st.text_input("Panchayat", "Patna City")
        chinh = st.text_input("Chunav Chinh", "Kalam")

    # Music Box: Folder se gaane scan karna
    music_files = os.listdir("music") if os.path.exists("music") else []
    selected_music = st.selectbox("Apna Background Music Chune:", music_files)

    if st.button("🚀 GENERATE CAMPAIGN AUDIO", disabled=not is_followed):
        with st.spinner("Gemini Script Likh Raha Hai..."):
            prompt = f"Write a powerful 20-word election campaign script in Hindi for {name} for the post of {pad} in {panchayat} with symbol {chinh}."
            script = model.generate_content(prompt).text
            st.write(f"**Script:** {script}")

        with st.spinner("ElevenLabs Awaaz Bana Raha Hai..."):
            if generate_voice(script, "temp_voice.mp3"):
                final_audio = mix_audio("temp_voice.mp3", selected_music)
                st.audio(final_audio)
                st.success("Aapka Chunavi Ad Taiyar Hai! 💎")
            else:
                st.error("Voice generation failed. Key check karein.")

elif selected == "📞 Support":
    st.link_button("Contact on WhatsApp", "https://wa.me/918210073056")
