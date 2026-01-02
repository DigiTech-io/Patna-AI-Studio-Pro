import streamlit as st
import google.generativeai as genai
import requests
import tempfile
import os
from pydub import AudioSegment
from streamlit_option_menu import option_menu

# --- 1. SECURE CONFIG ---
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    ELEVENLABS_API_KEY = st.secrets["ELEVENLABS_API_KEY"]
except KeyError:
    st.error("🚫 Secrets missing! Settings > Secrets mein keys check karein.")
    st.stop()

# --- 1. STABLE MODEL SETUP (Multi-Fallback) ---
genai.configure(api_key=GEMINI_API_KEY)

# हम 3 अलग-अलग मॉडल नाम ट्राई करेंगे ताकि एरर न आए
model_names = ['gemini-1.5-flash-latest', 'gemini-1.5-flash', 'gemini-pro']

model = None
for name in model_names:
    try:
        model = genai.GenerativeModel(name)
        # छोटा सा टेस्ट कि मॉडल काम कर रहा है या नहीं
        model.generate_content("Hi", generation_config={"max_output_tokens": 1})
        break 
    except:
        continue

if model is None:
    st.error("🚫 Google AI models are currently unavailable for this key.")
    st.stop()

# --- 2. AUDIO ENGINE ---
def generate_voice(text):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/pNInz6obpg8ndclAY7gu"
    headers = {"xi-api-key": ELEVENLABS_API_KEY, "Content-Type": "application/json"}
    data = {"text": text[:2500], "model_id": "eleven_multilingual_v2"}
    try:
        response = requests.post(url, json=data, headers=headers, timeout=45)
        if response.status_code == 200:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
                f.write(response.content)
                return f.name
    except Exception as e:
        st.error(f"Voice error: {str(e)}")
    return None

def mix_audio(voice_path, music_name):
    try:
        voice = AudioSegment.from_file(voice_path)
        if music_name != "No Music":
            music_path = os.path.join("music", music_name)
            if os.path.exists(music_path):
                music = AudioSegment.from_file(music_path) - 20
                if len(music) > len(voice):
                    music = music[:len(voice)]
                combined = music.overlay(voice)
                final = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
                combined.export(final, format="mp3")
                return final
        return voice_path
    except:
        return voice_path

# --- 3. UI ---
st.set_page_config(page_title="Patna AI Studio Pro v9.1", layout="wide", page_icon="🗳️")

st.markdown("""
<style>
.header {color: #e91e63; font-size: 2.8rem; text-align: center;}
.btn-pro {background: linear-gradient(45deg, #ff4081, #f50057);}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("<h2 style='color: #e91e63;'>Patna AI Studio Pro v9.1</h2>", unsafe_allow_html=True)
    selected = option_menu("Main Menu", ["Election Tool", "Support"], 
                          icons=["mic", "whatsapp"], default_index=0)
    is_followed = st.checkbox("✅ Subscribed on YouTube", value=False)

if selected == "Election Tool":
    st.markdown("<h1 class='header'>🗳️ Election Campaign Audio</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Name", "Eknath Jha")
        pad = st.selectbox("Select Post", ["Mukhiya", "Sarpanch", "Zila Parishad"])
    with col2:
        symbol = st.text_input("Election Symbol", "Motorcycle")
    
    music_dir = "music"
    music_files = []
    if os.path.exists(music_dir):
        music_files = [f for f in os.listdir(music_dir) if f.endswith(('.mp3', '.m4a', '.wav'))]
    
    selected_music = st.selectbox("Choose Track", ["No Music"] + music_files)

    if st.button("🚀 CREATE CAMPAIGN AUDIO", type="primary", disabled=not is_followed):
        with st.spinner("AI Script Likh Raha Hai..."):
            prompt = f"Hindi election slogan for {name} for {pad} with symbol {symbol}. 20 words max."
            try:
                script = model.generate_content(prompt).text
                st.success(f"✅ Script: {script}")
                
                voice = generate_voice(script)
                if voice:
                    final = mix_audio(voice, selected_music)
                    st.audio(final)
                    
                    with open(final, "rb") as f:
                        st.download_button("💾 Download", f.read(), "election_ad.mp3")
                    
                    # Cleanup
                    os.unlink(voice)
                    if final != voice:
                        os.unlink(final)
                        
                    st.balloons()
                    st.success("🎉 Campaign ready!")
            except Exception as e:
                st.error(f"Error: {str(e)}")

elif selected == "Support":
    st.header("📞 Support")
    st.link_button("WhatsApp", "https://wa.me/918210073056")
    st.info("""
    **Quick Setup:**
    1. Secrets.toml → API keys
    2. music/ → MP3 files  
    3. Deploy → Streamlit Cloud
    """)

st.markdown("---")
st.markdown("<center>© 2026 Patna AI Studio Pro | Made for Bihar</center>", unsafe_allow_html=True)
