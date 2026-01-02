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
    st.error("🚫 API Keys missing in Secrets!")
    st.stop()

# --- 2. SMART MODEL SETUP (Avoids 404 Errors) ---
genai.configure(api_key=GEMINI_API_KEY)

def get_model():
    """उपलब्ध मॉडल को अपने आप चुनने वाला फंक्शन"""
    models_to_try = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
    for m in models_to_try:
        try:
            test_model = genai.GenerativeModel(m)
            test_model.generate_content("test", generation_config={"max_output_tokens": 1})
            return test_model
        except: continue
    return None

model = get_model()
if not model:
    st.error("🚫 Google AI is unreachable. Check API Key or Internet.")
    st.stop()

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
st.set_page_config(page_title="Patna AI Studio Pro", layout="wide")

with st.sidebar:
    st.markdown("<h2 style='color:#e91e63; text-align:center;'>Patna AI Studio</h2>", unsafe_allow_html=True)
    # यहाँ 'Ad Studio' और 'Dashboard' वापस आ गए हैं!
    selected = option_menu(
        "🎯 Control Panel", 
        ["🗳️ Election Tool", "🚀 Ad Studio", "📊 Dashboard", "📞 Support"], 
        icons=["mic", "sparkles", "bar-chart", "phone"],
        default_index=0
    )
    is_followed = st.checkbox("✅ YouTube Subscribed", value=True)
    st.markdown("---")
    st.info("WhatsApp: 8210073056")

# --- 5. MAIN LOGIC SECTIONS ---

if selected == "🗳️ Election Tool":
    st.markdown("<h1 style='color:#e91e63; text-align:center;'>Election Campaign Studio</h1>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Candidate Name", "Eknath Jha")
        pad = st.selectbox("Post", ["Mukhiya", "Sarpanch", "Zila Parishad", "Pramukh"])
    with col2:
        panchayat = st.text_input("Panchayat", "Patna City")
        symbol = st.text_input("Symbol", "Motorcycle")

    music_files = [f for f in os.listdir("music") if f.endswith(('.mp3', '.m4a'))] if os.path.exists("music") else []
    selected_music = st.selectbox("Select Music", ["No Music"] + music_files)

    if st.button("🎙️ GENERATE CAMPAIGN AUDIO", type="primary"):
        if not is_followed: st.warning("Subscribe to YouTube first!")
        else:
            with st.spinner("AI Script & Voice taiyar ho raha hai..."):
                prompt = f"Powerful 25-word Hindi election slogan for {name} for {pad} in {panchayat} with symbol {symbol}."
                script = model.generate_content(prompt).text
                st.success(f"Script: {script}")
                v_file = generate_voice(script)
                if v_file:
                    final = mix_audio(v_file, selected_music)
                    st.audio(final)
                    st.download_button("💾 Download MP3", open(final, 'rb'), "campaign.mp3")

elif selected == "🚀 Ad Studio":
    st.markdown("<h1 style='text-align:center;'>🚀 Business Ad Maker</h1>", unsafe_allow_html=True)
    st.info("यहाँ आप अपनी दुकान या बिजनेस के लिए विज्ञापन बना पाएंगे। (Working on this feature...)")
    business_name = st.text_input("Business Name")
    offer = st.text_area("Offer Details")
    if st.button("Generate Ad Script"):
        prompt = f"Create a catchy 20-word Hindi radio ad for {business_name} offering {offer}."
        st.write(model.generate_content(prompt).text)

elif selected == "📊 Dashboard":
    st.markdown("<h1>📊 Your Analytics</h1>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    col1.metric("Campaigns Done", "124")
    col2.metric("Business Ads", "45")

elif selected == "📞 Support":
    st.write("For Priority Support: [WhatsApp 8210073056](https://wa.me/918210073056)")

