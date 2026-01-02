import streamlit as st
import google.generativeai as genai
import requests
import tempfile
import os
from pydub import AudioSegment
from streamlit_option_menu import option_menu

# CONFIG - Use secrets for production
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "AIzaSyDmS8gvEJ3Xuu_84HtJhWVjZvCs9yjXtkk")
ELEVENLABS_API_KEY = st.secrets.get("ELEVENLABS_API_KEY", "sk_f3d35f5de4846b323eda8bbacf8ed0fb9249ae180a170b86")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# AUDIO FUNCTIONS
def generate_voice(text):
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
    try:
        response = requests.post(url, json=data, headers=headers, timeout=30)
        if response.status_code == 200:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
                f.write(response.content)
                return f.name
    except:
        pass
    return None

def mix_audio(voice_path, music_name):
    try:
        voice = AudioSegment.from_file(voice_path)
        if music_name != "No Music":
            music_path = f"music/{music_name}"
            if os.path.exists(music_path):
                music = AudioSegment.from_file(music_path) - 20
                combined = music.overlay(voice)
                final_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
                combined.export(final_path, format="mp3")
                return final_path
        return voice_path
    except:
        return voice_path

# PAGE SETUP
st.set_page_config(page_title="Patna AI Studio Pro v6.2", layout="wide", page_icon="🗳️")

st.markdown("""
<style>
.header {color: #ff4444; font-size: 2.5rem; text-align: center;}
.btn-primary {background: #ff6b35;}
</style>
""", unsafe_allow_html=True)

# SIDEBAR
with st.sidebar:
    st.markdown("<h2>Patna AI Studio Pro</h2>", unsafe_allow_html=True)
    selected = option_menu(
        "Main Menu", 
        ["🚀 Ad Maker", "🗳️ Election Tool", "📞 Support"], 
        icons=["magic", "mic", "whatsapp"], 
        default_index=1
    )
    is_followed = st.checkbox("✅ Followed YouTube")
    st.markdown("[WhatsApp Support](https://wa.me/918210073056)")

# MAIN SECTIONS
if selected == "🚀 Ad Maker":
    st.markdown("<h1 class='header'>💎 Business Ad Maker</h1>", unsafe_allow_html=True)
    st.info("Professional ads with AI")

elif selected == "🗳️ Election Tool":
    st.markdown("<h1 class='header'>🗳️ Election Campaign Audio</h1>", unsafe_allow_html=True)
    
    # INPUTS
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Candidate Name", "Mukesh Kumar")
        pad = st.selectbox("Post", ["Mukhiya", "Pramukh"])
    with col2:
        panchayat = st.text_input("Panchayat", "Patna City")
        chinh = st.text_input("Symbol", "Kalam")
    
    music_files = os.listdir("music") if os.path.exists("music") else []
    selected_music = st.selectbox("Music", ["No Music"] + music_files)
    
    # GENERATE BUTTON
    if st.button("🚀 GENERATE AUDIO", type="primary", disabled=not is_followed):
        with st.spinner("Creating script..."):
            prompt = f"20-word Hindi election script for {name} {pad} {panchayat} symbol {chinh}"
            response = model.generate_content(prompt)
            script = response.text
            st.session_state.script = script
            st.success("Script: " + script)
        
        if hasattr(st.session_state, 'script'):
            with st.spinner("Generating voice..."):
                voice_file = generate_voice(st.session_state.script)
                if voice_file:
                    final_audio = mix_audio(voice_file, selected_music)
                    st.audio(final_audio)
                    with open(final_audio, 'rb') as f:
                        st.download_button("Download", f.read(), "campaign.mp3")
                    st.success("Ready!")
                    
                    os.unlink(voice_file)
                    if final_audio != voice_file:
                        os.unlink(final_audio)

elif selected == "📞 Support":
    st.markdown("<h1 class='header'>📞 Support</h1>", unsafe_allow_html=True)
    st.link_button("WhatsApp", "https://wa.me/918210073056")
    st.info("Add API keys in secrets.toml")

# FOOTER
st.markdown("---")
st.markdown("<center>© 2026 Patna AI Studio Pro v6.2</center>", unsafe_allow_html=True)
