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
    st.error("🚫 API Keys not found in Secrets! Please check Streamlit dashboard.")
    st.stop()

# --- STABLE MODEL SETUP ---
genai.configure(api_key=GEMINI_API_KEY)
# Multiple models to avoid 404 error
model_names = ['gemini-1.5-flash-latest', 'gemini-1.5-flash', 'gemini-pro']
model = None
for name in model_names:
    try:
        model = genai.GenerativeModel(name)
        model.generate_content("test", generation_config={"max_output_tokens": 1})
        break
    except: 
        continue

if model is None:
    st.error("🚫 No working AI model found! Check your Gemini API key.")
    st.stop()

# --- 2. AUDIO ENGINE ---
def generate_voice(text):
    url = "https://api.elevenlabs.io/v1/text-to-speech/pNInz6obpg8ndclAY7gu"
    headers = {"xi-api-key": ELEVENLABS_API_KEY, "Content-Type": "application/json"}
    data = {
        "text": text[:2000], 
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}
    }
    try:
        r = requests.post(url, json=data, headers=headers, timeout=30)
        if r.status_code == 200:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
                f.write(r.content)
                return f.name
    except Exception as e:
        st.error(f"Voice error: {e}")
    return None

def mix_audio(voice_path, music_name):
    try:
        voice = AudioSegment.from_file(voice_path)
        if music_name and music_name != "No Music":
            music_path = os.path.join("music", music_name)
            if os.path.exists(music_path):
                # Background music volume reduction (-20dB)
                music = AudioSegment.from_file(music_path) - 20
                if len(music) > len(voice):
                    music = music[:len(voice)]
                combined = music.overlay(voice)
                final_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
                combined.export(final_path, format="mp3")
                return final_path
        return voice_path
    except:
        return voice_path

# --- 3. UI DESIGN ---
st.set_page_config(page_title="Patna AI Studio Pro v10.1", layout="wide")

st.markdown("""
<style>
.main-header {color: #e91e63; text-align: center; font-size: 3rem; font-weight: bold;}
.stButton>button {width: 100%; border-radius: 20px; background: linear-gradient(45deg, #ff4081, #f50057); color: white;}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## 🎯 Control Panel")
    selected = option_menu("Menu", ["Election Tool", "Support"], icons=["mic", "phone"])
    is_followed = st.checkbox("✅ YouTube Subscribed", value=True)

if selected == "Election Tool":
    st.markdown("<h1 class='main-header'>🗳️ Election Audio Studio</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Candidate Name", "Eknath Jha")
        pad = st.selectbox("Post", ["Mukhiya", "Sarpanch", "Zila Parishad", "Pramukh"])
    with col2:
        panchayat = st.text_input("Panchayat/Ward", "Patna City")
        symbol = st.text_input("Symbol", "Motorcycle")

    # Music scanning (.mp3, .m4a support)
    music_files = []
    if os.path.exists("music"):
        music_files = [f for f in os.listdir("music") if f.endswith(('.mp3', '.m4a', '.wav'))]
    
    selected_music = st.selectbox("🎵 Select Background Music", ["No Music"] + music_files)

    if st.button("🎙️ GENERATE CAMPAIGN AUDIO"):
        if not is_followed:
            st.warning("Please subscribe on YouTube to unlock!")
        else:
            with st.spinner("🤖 Writing Script & Generating Voice..."):
                # Script generation
                prompt = f"Write a 25-word powerful Hindi election slogan for {name} for the post of {pad} in {panchayat} with symbol {symbol}."
                script_response = model.generate_content(prompt)
                script = script_response.text.strip()
                
                st.success(f"✅ **Script Ready:** {script}")
                
                # Voice generation
                voice_file = generate_voice(script)
                if voice_file:
                    final_file = mix_audio(voice_file, selected_music)
                    st.audio(final_file)
                    
                    with open(final_file, "rb") as f:
                        st.download_button("💾 Download MP3", f.read(), f"Campaign_{name}.mp3", "audio/mpeg")
                    
                    st.balloons()
                    
                    # Cleanup temp files
                    try:
                        os.unlink(voice_file)
                        if final_file != voice_file:
                            os.unlink(final_file)
                    except: pass
                else:
                    st.error("Voice generation failed. Check API limits.")

elif selected == "Support":
    st.markdown("### 📞 Support Center")
    st.write("WhatsApp: [8210073056](https://wa.me/918210073056)")

