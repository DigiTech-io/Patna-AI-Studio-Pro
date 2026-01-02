
import streamlit as st
import google.generativeai as genai
import requests
import tempfile
import os
from pydub import AudioSegment
from streamlit_option_menu import option_menu

# --- 1. SECURE CONFIG ---
try:
    # Secrets se key uthana
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    ELEVENLABS_API_KEY = st.secrets["ELEVENLABS_API_KEY"]
except KeyError:
    st.error("🚫 API Keys missing in Secrets dashboard!")
    st.stop()

# --- 2. RELIABLE MODEL SETUP ---
genai.configure(api_key=GEMINI_API_KEY)
# Seedha naam use kar rahe hain taaki 'Unreachable' error na aaye
model = genai.GenerativeModel('gemini-1.5-flash')

# --- 3. AUDIO ENGINE ---
def generate_voice(text):
    url = "https://api.elevenlabs.io/v1/text-to-speech/pNInz6obpg8ndclAY7gu"
    headers = {"xi-api-key": ELEVENLABS_API_KEY, "Content-Type": "application/json"}
    data = {"text": text[:2000], "model_id": "eleven_multilingual_v2"}
    try:
        r = requests.post(url, json=data, headers=headers, timeout=30)
        if r.status_code == 200:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
                f.write(r.content)
                return f.name
    except: return None

def mix_audio(voice_path, music_name):
    try:
        voice = AudioSegment.from_file(voice_path)
        if music_name != "No Music":
            music_path = os.path.join("music", music_name)
            if os.path.exists(music_path):
                music = AudioSegment.from_file(music_path) - 22
                if len(music) > len(voice): music = music[:len(voice)]
                final = music.overlay(voice)
                path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
                final.export(path, format="mp3")
                return path
    except: pass
    return voice_path

# --- 4. PRO UI DESIGN ---
st.set_page_config(page_title="Patna AI Studio Pro v11.0", layout="wide")

with st.sidebar:
    st.markdown("<h2 style='color:#e91e63; text-align:center;'>Patna AI Studio Pro</h2>", unsafe_allow_html=True)
    # Aapke saare options yahan wapas aa gaye hain
    selected = option_menu(
        "🎯 Control Panel", 
        ["🗳️ Election Tool", "🚀 Ad Studio", "📊 Dashboard", "📞 Support"], 
        icons=["mic", "sparkles", "bar-chart", "phone"],
        default_index=0
    )
    is_followed = st.checkbox("✅ YouTube Subscribed", value=True)
    st.markdown("---")
    st.info("WhatsApp Support: 8210073056")

# --- 5. APP SECTIONS ---

if selected == "🗳️ Election Tool":
    st.markdown("<h1 style='color:#e91e63; text-align:center;'>Election Campaign Audio Generator</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Candidate Name", "Eknath Jha")
        pad = st.selectbox("Post", ["Mukhiya", "Sarpanch", "Zila Parishad", "Pramukh"])
    with col2:
        panchayat = st.text_input("Panchayat/Block", "Patna City")
        symbol = st.text_input("Symbol", "Motorcycle")

    # Music list scan
    music_files = [f for f in os.listdir("music") if f.endswith(('.mp3', '.m4a'))] if os.path.exists("music") else []
    selected_music = st.selectbox("🎵 Background Music", ["No Music"] + music_files)

    if st.button("🎙️ GENERATE AUDIO", type="primary"):
        if not is_followed: st.warning("Please subscribe on YouTube first!")
        else:
            with st.spinner("🧠 AI Script & Studio Voice taiyar ho raha hai..."):
                prompt = f"Powerful 25-word Hindi election slogan for {name} ({pad}) in {panchayat} with symbol {symbol}."
                try:
                    script = model.generate_content(prompt).text
                    st.success(f"📜 Script: {script}")
                    v_file = generate_voice(script)
                    if v_file:
                        final = mix_audio(v_file, selected_music)
                        st.audio(final)
                        st.download_button("💾 Download Campaign MP3", open(final, 'rb'), "campaign.mp3")
                except Exception as e:
                    st.error(f"AI Error: {str(e)}")

elif selected == "🚀 Ad Studio":
    st.markdown("<h1 style='text-align:center;'>🚀 Professional Ad Maker</h1>", unsafe_allow_html=True)
    biz_name = st.text_input("Shop/Business Name")
    biz_type = st.selectbox("Type", ["Grocery", "Clothing", "Electronics", "Other"])
    if st.button("Generate Ad"):
        with st.spinner("Writing Ad..."):
            prompt = f"Create a 20-word catchy Hindi commercial for {biz_name} {biz_type} shop."
            script = model.generate_content(prompt).text
            st.info(script)

elif selected == "📊 Dashboard":
    st.markdown("<h1>📊 Analytics</h1>", unsafe_allow_html=True)
    st.metric("Daily Active Projects", "12")

elif selected == "📞 Support":
    st.write("Instant Help: [WhatsApp Support](https://wa.me/918210073056)")
