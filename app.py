import streamlit as st
import google.generativeai as genai
import requests
import tempfile
import os
from pydub import AudioSegment
from streamlit_option_menu import option_menu

# --- 1. CONFIGURATION ---
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    ELEVENLABS_API_KEY = st.secrets["ELEVENLABS_API_KEY"]
except KeyError:
    st.error("🚫 API Keys missing in Streamlit Secrets!")
    st.stop()

# --- 2. AI MODEL SETUP ---
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('models/gemini-1.5-flash-latest')

# --- 3. CORE AUDIO FUNCTIONS ---
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

# --- 4. NAVIGATION & UI ---
st.set_page_config(page_title="Patna AI Studio Pro v11.0", layout="wide")

with st.sidebar:
    st.markdown("<h2 style='color:#e91e63; text-align:center;'>Patna AI Studio</h2>", unsafe_allow_html=True)
    selected = option_menu(
        "🎯 Control Panel", 
        ["🗳️ Election Tool", "🚀 Ad Studio", "📊 Dashboard", "📞 Support"], 
        icons=["mic", "sparkles", "bar-chart", "phone"],
        default_index=0
    )
    is_followed = st.checkbox("✅ YouTube Subscribed", value=True)

# --- 5. LOGIC FOR EACH FEATURE ---

if selected == "🗳️ Election Tool":
    st.header("🗳️ Election Campaign Audio")
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Candidate Name", "Eknath Jha")
        pad = st.selectbox("Post", ["Mukhiya", "Sarpanch", "Zila Parishad"])
    with col2:
        panchayat = st.text_input("Panchayat", "Patna City")
        symbol = st.text_input("Symbol", "Motorcycle")
    
    music_files = [f for f in os.listdir("music") if f.endswith(('.mp3', '.m4a'))] if os.path.exists("music") else []
    selected_music = st.selectbox("Select Background Music", ["No Music"] + music_files)

    if st.button("🎙️ GENERATE CAMPAIGN AUDIO", type="primary"):
        with st.spinner("AI is working..."):
            prompt = f"Powerful 25-word Hindi election slogan for {name} ({pad}) in {panchayat} with symbol {symbol}."
            script = model.generate_content(prompt).text
            st.success(f"📜 Script: {script}")
            v_file = generate_voice(script)
            if v_file:
                final = mix_audio(v_file, selected_music)
                st.audio(final)
                st.download_button("💾 Download MP3", open(final, 'rb'), "campaign.mp3")

elif selected == "🚀 Ad Studio":
    st.header("🚀 Professional Ad Maker")
    biz_name = st.text_input("Business Name")
    biz_type = st.selectbox("Category", ["Grocery", "Clothing", "Electronics", "Restaurant"])
    offer = st.text_input("Special Offer (e.g. 20% Off)")
    
    if st.button("Generate Ad"):
        with st.spinner("Creating Ad..."):
            prompt = f"Create a catchy 20-word Hindi ad for {biz_name} ({biz_type}) with offer: {offer}."
            script = model.generate_content(prompt).text
            st.info(script)
            # यहाँ भी आप वॉइस जनरेशन जोड़ सकते हैं

elif selected == "📊 Dashboard":
    st.header("📊 Performance Dashboard")
    st.write("Current Session Analytics:")
    st.metric("Total Audio Generated", "15")
    st.metric("Top Category", "Election")

elif selected == "📞 Support":
    st.markdown("### 📞 Contact Support\nWhatsApp: [8210073056](https://wa.me/918210073056)")

