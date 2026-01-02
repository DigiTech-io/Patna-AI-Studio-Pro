import streamlit as st
import google.generativeai as genai
import requests
import tempfile
import os
from pydub import AudioSegment
from streamlit_option_menu import option_menu

# --- 1. SECURE CONFIG (v7.0 - Production Ready) ---
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    ELEVENLABS_API_KEY = st.secrets["ELEVENLABS_API_KEY"]
except KeyError:
    st.error("🚫 API Keys missing! Add in Streamlit Cloud Secrets.")
    st.stop()

genai.configure(api_key=GEMINI_API_KEY)
try:
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    model = genai.GenerativeModel('gemini-pro')

# --- 2. ROBUST AUDIO ENGINE ---
def generate_voice(text):
    url = "https://api.elevenlabs.io/v1/text-to-speech/pNInz6obpg8ndclAY7gu"
    headers = {
        "Accept": "audio/mpeg",
        "xi-api-key": ELEVENLABS_API_KEY, 
        "Content-Type": "application/json"
    }
    data = {
        "text": text[:2500],  # Safe length
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}
    }
    try:
        response = requests.post(url, json=data, headers=headers, timeout=45)
        if response.status_code == 200:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
                f.write(response.content)
                return f.name
        st.error(f"Voice API: {response.status_code}")
    except Exception as e:
        st.error(f"Voice failed: {str(e)}")
    return None

def mix_audio(voice_path, music_name):
    try:
        voice = AudioSegment.from_file(voice_path) - 2  # Normalize
        if music_name and music_name != "No Music":
            music_path = f"music/{music_name}"
            if os.path.exists(music_path):
                music = AudioSegment.from_file(music_path) - 22
                # Match duration
                if len(music) > len(voice):
                    music = music[:len(voice)]
                combined = music.overlay(voice)
                final_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
                combined.export(final_path, format="mp3")
                return final_path
        return voice_path
    except:
        return voice_path

# --- 3. PROFESSIONAL UI ---
st.set_page_config(page_title="Patna AI Studio Pro v7.0", layout="wide", page_icon="🗳️")

# Custom CSS
st.markdown("""
<style>
.header-text {color: #d63384; font-size: 3rem; text-align: center; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);}
.gold-button {background: linear-gradient(45deg, #ffd700, #ffed4e); color: #333;}
.sidebar .sidebar-content {background: linear-gradient(180deg, #f0f2f6 0%, #e0e6ff 100%);}
</style>
""", unsafe_allow_html=True)

# SIDEBAR
with st.sidebar:
    st.markdown("<h1 style='color: #d63384;'>Patna AI Studio Pro v7.0</h1>", unsafe_allow_html=True)
    selected = option_menu(
        "🔥 Main Menu", 
        ["🚀 Ad Maker", "🗳️ Election Tool", "📞 Support"], 
        icons=["magic", "mic", "whatsapp"], 
        default_index=1,
        styles={
            "container": {"padding": "10px", "background": "#f8f9fa"},
            "nav-link": {"font-size": "16px", "margin": "5px 0"}
        }
    )
    is_followed = st.checkbox("✅ I have Followed/Subscribed", value=False)
    st.markdown("---")
    st.markdown("[📱 WhatsApp Support](https://wa.me/918210073056)")

# MAIN CONTENT
if selected == "🚀 Ad Maker":
    st.markdown("<h1 class='header-text'>💎 Professional Business Ad Maker</h1>", unsafe_allow_html=True)
    st.info("🔥 AI-powered business ads with voiceover - Coming soon!")

elif selected == "🗳️ Election Tool":
    st.markdown("<h1 class='header-text'>🗳️ Election Campaign Audio Generator</h1>", unsafe_allow_html=True)
    
    # INPUT COLUMNS
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("### 👤 Candidate Details")
        name = st.text_input("Candidate Name", "Mukesh Kumar", help="Full name")
        pad = st.selectbox("Post/Pad", ["Mukhiya", "Pramukh", "Zila Parishad", "Panchayat Samiti"])
    with col2:
        st.markdown("### 🗳️ Campaign Details")
        panchayat = st.text_input("Panchayat/Block", "Patna City")
        chinh = st.text_input("Symbol/Chinh", "Kalam")
    
    # MUSIC SELECTION
    st.markdown("### 🎵 Background Music")
    music_files = [f for f in os.listdir("music") if f.endswith(('.mp3', '.wav'))] if os.path.exists("music") else []
    if not music_files:
        st.warning("📁 Add MP3 files to `music/` folder for background music")
    selected_music = st.selectbox("Select Music", ["No Music"] + music_files)
    
    # GENERATE BUTTON
    col_btn, col_status = st.columns([3, 1])
    with col_btn:
        if st.button("🚀 GENERATE CAMPAIGN AUDIO", type="primary", 
                    disabled=not is_followed, 
                    help="First check 'Followed YouTube'"):
            if not is_followed:
                st.warning("✅ Please follow YouTube first to unlock!")
                st.stop()
            
            with st.spinner("🤖 Gemini AI script generating..."):
                prompt = f"""Write POWERFUL 25-word Hindi election campaign script for:
                Candidate: {name}
                Post: {pad}
                Area: {panchayat}
                Symbol: {chinh}
                
                Make it emotional, rhythmic, perfect for crowd chanting. End with strong CTA."""
                try:
                    response = model.generate_content(prompt)
                    script = response.text.strip()
                    st.session_state.script = script
                    
                    st.markdown("### 📜 Generated Script")
                    st.success(script)
                except Exception as e:
                    st.error(f"Script error: {str(e)}")
                    st.stop()
            
            with st.spinner("🗣️ Generating professional voice..."):
                voice_file = generate_voice(st.session_state.script)
                if not voice_file:
                    st.error("❌ Voice generation failed. Check ElevenLabs quota.")
                    st.stop()
                
                with st.spinner("🎼 Mixing with music..."):
                    final_audio = mix_audio(voice_file, selected_music)
                    
                    st.markdown("### 🎧 Final Campaign Audio")
                    st.audio(final_audio)
                    
                    # DOWNLOAD
                    with open(final_audio, "rb") as audio_file:
                        st.download_button(
                            label="💾 Download MP3",
                            data=audio_file.read(),
                            file_name=f"{name}_{pad}_campaign.mp3",
                            mime="audio/mpeg"
                        )
                    
                    st.balloons()
                    st.success("🎉 Professional election ad ready! Share with voters!")
                
                # CLEANUP
                try:
                    os.unlink(voice_file)
                    os.unlink(final_audio)
                except:
                    pass
        else:
            st.info("✅ Follow YouTube checkbox to unlock generator!")

elif selected == "📞 Support":
    st.markdown("<h1 class='header-text'>📞 24/7 Support Center</h1>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.link_button("💬 WhatsApp Chat", "https://wa.me/918210073056?text=Patna+AI+Studio+help")
        st.link_button("📹 YouTube Channel", "https://youtube.com/@yourchannel")
    with col2:
        st.info("""
        **Setup Guide:**
        1. Add API keys in Secrets
        2. Create `music/` folder + MP3 files  
        3. Deploy on Streamlit Cloud
        """)

# FOOTER
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    © 2026 Patna AI Studio Pro v7.0 | Bihar's #1 AI Campaign Tool<br>
    <a href='tel:+918210073056' style='color: #d63384;'>📞 8210073056</a>
</div>
""", unsafe_allow_html=True)
