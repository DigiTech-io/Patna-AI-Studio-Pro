import streamlit as st
import google.generativeai as genai
import requests
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import io
import os
import tempfile
from pydub import AudioSegment
from streamlit_option_menu import option_menu
import time

# --- 1. CONFIGURATION (v6.0 - Updated Models & Error Handling) ---
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "AIzaSyDmS8gvEJ3Xuu_84HtJhWVjZvCs9yjXtkk")
ELEVENLABS_API_KEY = st.secrets.get("ELEVENLABS_API_KEY", "sk_f3d35f5de4846b323eda8bbacf8ed0fb9249ae180a170b86")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash-exp')  # Latest stable model [web:20]

# --- 2. ENHANCED AUDIO ENGINE (Hindi-optimized Voice + Better Mixing) ---
@st.cache_data(ttl=3600)
def generate_voice(text, voice_id="pNInz6obpg8ndclAY7gu"):  # Hindi-compatible voice [web:21][web:29]
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVENLABS_API_KEY
    }
    data = {
        "text": text[:3000],  # Truncate for API limits
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": 0.6, "similarity_boost": 0.8, "style": 0.2}
    }
    try:
        response = requests.post(url, json=data, headers=headers, timeout=30)
        if response.status_code == 200:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
                tmp.write(response.content)
                return tmp.name
        else:
            st.error(f"Voice API Error: {response.status_code} - Check API key limits [web:21]")
            return None
    except Exception as e:
        st.error(f"Voice generation failed: {str(e)}")
        return None

def mix_audio(voice_path, music_name):
    try:
        voice = AudioSegment.from_file(voice_path) - 3  # Normalize voice
        music_dir = "music"
        music_path = os.path.join(music_dir, music_name)
        if os.path.exists(music_path):
            bg_music = AudioSegment.from_file(music_path) - 25  # Quieter BG [web:23]
            # Match lengths
            duration = len(voice)
            bg_music = bg_music[:duration]
            combined = bg_music.overlay(voice)
            final_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
            combined.export(final_path, format="mp3")
            return final_path
        return voice_path
    except Exception as e:
        st.warning(f"Music mix failed (using voice only): {str(e)} [web:23]")
        return voice_path

# --- 3. PRODUCTION UI SETUP ---
st.set_page_config(
    page_title="Patna AI Studio Pro v6.0", 
    layout="wide",
    page_icon="🗳️",
    initial_sidebar_state="expanded"
)

# Custom CSS for Professional Look
st.markdown("""
<style>
.main-header {color: #ff6b35; font-size: 3rem; text-align: center; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);}
.gold-btn {background: linear-gradient(45deg, #ffd700, #ffed4e); color: #1a1a2e; border-radius: 20px; padding: 10px 20px;}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("<h1 style='color: #ff6b35;'>Patna AI Studio Pro v6.0</h1>", unsafe_allow_html=True)
    selected = option_menu("Main Menu", 
                          ["🚀 Ad Maker", "🗳️ Election Tool", "📱 Video Ads", "📞 Support"], 
                          icons=["magic", "mic", "video", "whatsapp"], 
                          menu_icon="cast", default_index=1,
                          styles={"container": {"padding": "10px", "background": "#f0f2f6"}})
    
    st.markdown("---")
    is_followed = st.checkbox("✅ Followed on YouTube/Instagram", value=False, help="Unlock full features!")
    
    if st.button("🔑 Verify Subscription", type="primary", disabled=not is_followed):
        st.session_state.unlocked = True
        st.success("✅ Premium Unlocked!")
    
    st.markdown("---")
    st.markdown("[📱 WhatsApp Support](https://wa.me/918210073056)")

# --- 4. ENHANCED SECTIONS ---
if selected == "🚀 Ad Maker":
    st.markdown("<h1 class='main-header'>💎 Professional Business Ad Maker</h1>", unsafe_allow_html=True)
    st.info("🔥 Naye Gemini 1.5 + Hindi Voice Engine ke saath taiyar! Business ads banao.")

elif selected == "🗳️ Election Tool":
    st.markdown("<h1 class='main-header'>🗳️ Chunavi Campaign Audio Generator</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1,1])
    with col1:
        name = st.text_input("👤 Candidate Name", "Mukesh Kumar", help="Pura naam likhein")
        pad = st.selectbox("📋 Pad (Post)", ["Mukhiya", "Pramukh", "Zila Parishad", "MLA"], index=0)
    with col2:
        panchayat = st.text_input("🏘️ Panchayat/Block", "Patna City")
        chinh = st.text_input("🗳️ Chunav Chinh/Symbol", "Kalam")

    st.markdown("---")
    music_files = [f for f in os.listdir("music") if f.endswith(('.mp3','.wav'))] if os.path.exists("music") else []
    if not music_files:
        st.warning("📁 music/ folder mein BG tracks add karein (MP3/WAV)")
    selected_music = st.selectbox("🎵 Background Music:", ["No Music"] + music_files)

    col_gen, col_preview = st.columns([1,1])
    with col_gen:
        if st.button("🚀 GENERATE FULL CAMPAIGN AUDIO", type="primary", 
                     disabled=not is_followed and not st.session_state.get('unlocked', False),
                     help="Follow checkbox tick karein pehle!"):
            with st.spinner("🤖 Super AI Script Likh Raha Hai (Gemini 1.5)..."):
                enhanced_prompt = f"""Write a POWERFUL 25-30 second Hindi election campaign script for candidate {name}, 
                post: {pad} in {panchayat}, symbol: {chinh}. 
                Make it emotional, rhythmic, crowd-chanting style. End with strong call-to-action. 
                Keep under 120 words for perfect voice timing."""
                response = model.generate_content(enhanced_prompt)
                script = response.text.strip()
                st.session_state.script = script
                st.success(f"✅ **AI Script Ready:**
{script}")

            if 'script' in st.session_state:
                with st.spinner("🗣️ Voice Generate + Music Mix Kar Raha..."):
                    voice_file = generate_voice(st.session_state.script)
                    if voice_file:
                        final_audio = mix_audio(voice_file, selected_music if selected_music != "No Music" else None)
                        with col_preview:
                            st.audio(final_audio)
                            st.download_button("💾 Download MP3", open(final_audio, 'rb').read(), 
                                             file_name=f"{name}_{pad}_campaign.mp3", mime="audio/mpeg")
                        st.balloons()
                        st.markdown("---")
                        st.success("🎉 Aapka Professional Chunavi Ad Taiyar! Share karein voters mein!")
                        
                        # Cleanup
                        try:
                            os.unlink(voice_file)
                            if final_audio != voice_file:
                                os.unlink(final_audio)
                        except:
                            pass

elif selected == "📱 Video Ads":
    st.header("🎥 Coming Soon: AI Video Campaign Maker")
    st.info("Image-to-Video + Voiceover integration (MoviePy + Gemini Vision)")

elif selected == "📞 Support":
    st.markdown("<h1 class='main-header'>📞 24/7 Support Center</h1>", unsafe_allow_html=True)
    st.link_button("💬 WhatsApp Chat", "https://wa.me/918210073056?text=Patna%20AI%20Studio%20Pro%20Help")
    st.info("🔧 Common Fixes:
• API Keys: .streamlit/secrets.toml mein add karein
• Music: music/ folder create + MP3 files
• Deploy: Render/HuggingFace use karein")

# --- FOOTER ---
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    © 2026 Patna AI Studio Pro v6.0 | Bihar's #1 AI Campaign Tool | 
    <a href='tel:+918210073056' style='color: #ff6b35;'>📞 8210073056</a>
</div>
""", unsafe_allow_html=True)
