
import streamlit as st
import google.generativeai as genai
import requests
import tempfile
import os
from pydub import AudioSegment
from streamlit_option_menu import option_menu

# --- 1. PRODUCTION SECURE CONFIG (v8.0) ---
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    ELEVENLABS_API_KEY = st.secrets["ELEVENLABS_API_KEY"]
except KeyError:
    st.error("🚫 API Keys required! Add to Streamlit Cloud → Settings → Secrets")
    st.stop()

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')  # Latest stable

# --- 2. BULLETPROOF AUDIO ENGINE ---
def generate_voice(text):
    """Hindi-optimized voice generation with full error handling"""
    url = "https://api.elevenlabs.io/v1/text-to-speech/pNInz6obpg8ndclAY7gu"
    headers = {
        "Accept": "audio/mpeg",
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "text": text[:2800],  # API safe limit
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.55, 
            "similarity_boost": 0.8,
            "style": 0.1
        }
    }
    try:
        response = requests.post(url, json=data, headers=headers, timeout=60)
        response.raise_for_status()
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmpf:
            tmpf.write(response.content)
            return tmpf.name
    except requests.exceptions.RequestException as e:
        st.error(f"🔴 Voice API failed: {str(e)[:100]}")
    except Exception as e:
        st.error(f"🔴 Voice error: {str(e)}")
    return None

def mix_audio(voice_path, music_name):
    """Professional audio mixing with duration sync"""
    try:
        voice = AudioSegment.from_file(voice_path).normalize()
        if music_name and music_name != "No Music":
            music_path = os.path.join("music", music_name)
            if os.path.exists(music_path):
                bg_music = AudioSegment.from_file(music_path) - 25  # Background quieter
                # Sync lengths
                voice_duration = len(voice)
                bg_music = bg_music[:voice_duration]
                mixed = bg_music.overlay(voice)
                final_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
                mixed.export(final_path, format="mp3", bitrate="192k")
                return final_path
        return voice_path
    except Exception as e:
        st.warning(f"⚠️ Music mixing skipped: {str(e)}")
        return voice_path

# --- 3. ENTERPRISE UI SETUP ---
st.set_page_config(
    page_title="Patna AI Studio Pro v8.0", 
    layout="wide", 
    page_icon="🗳️",
    initial_sidebar_state="expanded"
)

# Luxury CSS
st.markdown("""
<style>
    .main-header {
        color: #d63384; 
        font-size: 3.5rem; 
        text-align: center; 
        text-shadow: 0 0 20px rgba(214,51,132,0.5);
        margin-bottom: 2rem;
    }
    .premium-btn {
        background: linear-gradient(45deg, #ffd700, #ffed4e, #ffd700);
        color: #1a1a2e !important;
        border-radius: 25px;
        padding: 12px 30px;
        font-weight: bold;
        font-size: 18px;
        border: none;
    }
    .sidebar-title {
        color: #d63384;
        font-size: 1.8rem;
        text-align: center;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# === SIDEBAR === Professional Navigation
with st.sidebar:
    st.markdown('<div class="sidebar-title">Patna AI Studio Pro v8.0</div>', unsafe_allow_html=True)
    
    selected = option_menu(
        menu_title="🔥 Main Dashboard",
        options=["🚀 Ad Maker", "🗳️ Election Tool", "📱 Video Suite", "📊 Analytics", "📞 Support"],
        icons=["sparkles", "mic", "video", "graph", "headset"],
        default_index=1,
        styles={
            "container": {"padding": "15px", "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"},
            "nav-link": {"font-size": "15px", "text-align": "left", "margin": "5px 0", "--hover-color": "#ff6b6b"},
            "nav-link-selected": {"background": "rgba(255,255,255,0.2)"}
        }
    )
    
    st.markdown("---")
    is_followed = st.checkbox("✅ YouTube Subscribed / Followed", value=False, 
                             help="Unlock unlimited generations!")
    
    if st.button("🔓 Activate Premium", type="primary", disabled=not is_followed,
                help="Subscribe first to unlock!"):
        st.session_state.premium_active = True
        st.rerun()
    
    st.markdown("---")
    st.markdown('<a href="https://wa.me/918210073056?text=Patna+AI+Studio+v8+Help" target="_blank">[📱 Instant WhatsApp]</a>', unsafe_allow_html=True)

# === MAIN SECTIONS ===
if selected == "🚀 Ad Maker":
    st.markdown('<h1 class="main-header">💎 AI Business Ad Creator</h1>', unsafe_allow_html=True)
    st.info("✨ Generate professional promotional videos with voiceover - Launching soon!")

elif selected == "🗳️ Election Tool":
    st.markdown('<h1 class="main-header">🗳️ Professional Election Campaign Generator</h1>', unsafe_allow_html=True)
    
    # === INPUT FORM ===
    st.markdown("## 📝 Campaign Details")
    col1, col2, col3 = st.columns([1,1,1])
    
    with col1:
        st.markdown("**👤 Candidate**")
        name = st.text_input("Full Name", "Mukesh Kumar Sah", placeholder="Enter candidate name")
        
    with col2:
        st.markdown("**📋 Position**")
        pad = st.selectbox("Select Post", 
                          ["Mukhiya", "Pramukh", "Zila Parishad Sadasya", "Panchayat Samiti", "Nagar Panchayat"])
        
    with col3:
        st.markdown("**🗳️ Details**")
        panchayat = st.text_input("Panchayat/Block", "Patna Sadar")
        chinh = st.text_input("Election Symbol", "Kalam (Pen)")
    
    # Music Selection
    st.markdown("## 🎵 Background Music")
    music_dir = "music"
    music_files = []
    if os.path.exists(music_dir):
        music_files = [f for f in os.listdir(music_dir) 
                      if f.lower().endswith(('.mp3', '.wav', '.m4a', '.ogg'))]
    
    if music_files:
        selected_music = st.selectbox("Choose Track", ["No Music"] + music_files, 
                                     format_func=lambda x: f"🎵 {x}")
    else:
        selected_music = "No Music"
        st.warning("💡 Add MP3/WAV files to `music/` folder for background music")
    
    # === GENERATION BUTTON ===
    st.markdown("---")
    if st.button("🚀 CREATE PROFESSIONAL CAMPAIGN AUDIO", 
                type="primary", 
                use_container_width=True,
                disabled=not is_followed and not st.session_state.get('premium_active', False),
                help="✅ Subscribe on YouTube to unlock!"):
        
        # Script Generation
        with st.spinner("🤖 Gemini 1.5 Flash generating emotional script..."):
            prompt = f"""Create POWERFUL, emotional 28-second Hindi election campaign speech for:
            
✅ Candidate: **{name}**
✅ Post: **{pad}**
✅ Area: **{panchayat}**  
✅ Symbol: **{chinh}**

Style: Crowd-chanting rhythm, emotional appeal, strong voter call-to-action.
Word count: 90-110 words exactly.
Format: Natural spoken Hindi (NOT written script style)."""
            
            try:
                response = model.generate_content(prompt)
                script = response.text.strip()
                st.session_state.generated_script = script
                
                st.markdown("### 📜 AI Generated Script")
                st.info(script)
                
            except Exception as e:
                st.error(f"❌ Script generation failed: {str(e)}")
                st.stop()
        
        # Audio Pipeline
        with st.spinner("🗣️ ElevenLabs generating studio-quality Hindi voice..."):
            voice_file = generate_voice(st.session_state.generated_script)
            if not voice_file:
                st.error("❌ Voice generation failed. Check ElevenLabs quota/API key.")
                st.stop()
        
        with st.spinner("🎼 Professional mixing with background music..."):
            final_audio_path = mix_audio(voice_file, selected_music)
            
            # Playback & Download
            st.markdown("### 🎧 Final Professional Campaign Audio")
            st.audio(final_audio_path)
            
            with open(final_audio_path, "rb") as audio_file:
                st.download_button(
                    label="💾 Download HD MP3 (192kbps)",
                    data=audio_file.read(),
                    file_name=f"Election_Campaign_{name}_{pad}_{panchayat}.mp3",
                    mime="audio/mpeg",
                    use_container_width=True
                )
            
            st.balloons()
            st.success("🎉 **Campaign Ready!** Share instantly with voters via WhatsApp 📱")
        
        # Auto Cleanup
        try:
            os.unlink(voice_file)
            os.unlink(final_audio_path)
        except:
            pass

elif selected == "📱 Video Suite":
    st.markdown('<h1 class="main-header">🎥 AI Video Campaign Creator</h1>', unsafe_allow_html=True)
    st.info("🔥 Image-to-video + text-to-video with voiceover - Under development")

elif selected == "📊 Analytics":
    st.markdown('<h1 class="main-header">📊 Usage Dashboard</h1>', unsafe_allow_html=True)
    st.info("✅ Generation history, quota tracking - Premium feature")

elif selected == "📞 Support":
    st.markdown('<h1 class="main-header">📞 Priority Support</h1>', unsafe_allow_html=True)
    col_support1, col_support2 = st.columns(2)
    
    with col_support1:
        st.markdown("### 🚀 Quick Actions")
        st.link_button("💬 WhatsApp Support", "https://wa.me/918210073056?text=PatnaAI+v8+help")
        st.link_button("📹 YouTube Tutorials", "https://youtube.com/yourchannel")
    
    with col_support2:
        st.markdown("### ⚙️ Setup Guide")
        st.info("""
        **✅ Production Checklist:**
        1. Secrets.toml → API keys added
        2. music/ folder → MP3 background tracks  
        3. Deploy → Streamlit Cloud (Free)
        4. Test → Local: `streamlit run app.py`
        """)

# === GLOBAL FOOTER ===
st.markdown("""
<div style='
    background: linear-gradient(90deg, #d63384, #ff6b6b); 
    color: white; 
    padding: 20px; 
    text-align: center; 
    border-radius: 15px; 
    margin-top: 40px;
'>
    <h3>© 2026 Patna AI Studio Pro v8.0</h3>
    <p>Bihar's #1 AI Election Campaign Platform | <strong>📞 8210073056</strong></p>
</div>
""", unsafe_allow_html=True)
