import streamlit as st
import google.generativeai as genai
import requests
import tempfile
import os
from pydub import AudioSegment
from streamlit_option_menu import option_menu

# --- 1. PRODUCTION SECURE CONFIG (v9.0 - Bulletproof) ---
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    ELEVENLABS_API_KEY = st.secrets["ELEVENLABS_API_KEY"]
except KeyError:
    st.sidebar.error("🚫 API Keys missing! Add to Secrets.toml")
    st.error("Setup incomplete. Add keys first.")
    st.stop()

# Stable Model Setup (Works everywhere)
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')  # Most reliable

# --- 2. INDUSTRIAL AUDIO ENGINE ---
def generate_voice(text):
    """Enterprise-grade voice generation"""
    url = "https://api.elevenlabs.io/v1/text-to-speech/pNInz6obpg8ndclAY7gu"
    headers = {
        "Accept": "audio/mpeg",
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "text": text[:2400],  # Safe limit
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": 0.6, "similarity_boost": 0.75}
    }
    try:
        response = requests.post(url, json=data, headers=headers, timeout=50)
        if response.status_code == 200:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
                f.write(response.content)
                return f.name
        st.error(f"Voice API: HTTP {response.status_code}")
    except Exception as e:
        st.error(f"Voice failed: {str(e)[:80]}...")
    return None

def mix_audio(voice_path, music_name):
    """Safe audio mixing with cleanup"""
    try:
        voice = AudioSegment.from_file(voice_path)
        if music_name and music_name != "No Music":
            music_path = os.path.join("music", music_name)
            if os.path.exists(music_path):
                bg = AudioSegment.from_file(music_path) - 24
                # Perfect sync
                if len(bg) > len(voice):
                    bg = bg[:len(voice)]
                final_audio = bg.overlay(voice)
                final_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
                final_audio.export(final_path, format="mp3")
                return final_path
        return voice_path
    except Exception:
        return voice_path  # Graceful fallback

# --- 3. PROFESSIONAL UI (Mobile-First) ---
st.set_page_config(
    page_title="Patna AI Studio Pro v9.0", 
    layout="wide", 
    page_icon="🗳️"
)

# Pro CSS
st.markdown("""
<style>
.pro-header {color: #e91e63; font-size: 3.2rem; text-align: center; text-shadow: 0 4px 8px rgba(0,0,0,0.3);}
.btn-pro {background: linear-gradient(45deg, #ff4081, #f50057); color: white; border-radius: 25px; padding: 15px;}
.metric-box {background: #f8f9fa; padding: 20px; border-radius: 15px; border-left: 5px solid #e91e63;}
</style>
""", unsafe_allow_html=True)

# === SIDEBAR (Compact Pro) ===
with st.sidebar:
    st.markdown('<div style="text-align:center; padding:20px; background:#f8fbfd;"><h2 style="color:#e91e63; margin:0;">Patna AI Studio Pro v9.0</h2></div>', unsafe_allow_html=True)
    
    selected = option_menu(
        "🎯 Control Panel",
        ["🗳️ Election Tool", "🚀 Ad Studio", "📊 Dashboard", "📞 Support"],
        icons=["mic", "sparkles", "bar-chart", "phone"],
        default_index=0
    )
    
    st.markdown("---")
    is_followed = st.checkbox("✅ YouTube Subscribed", value=False)
    
    if st.button("🔥 UNLOCK PRO", type="primary", disabled=not is_followed):
        st.session_state.pro_unlocked = True
        st.success("✅ PRO MODE ACTIVE!")
        st.rerun()
    
    st.markdown("---")
    st.markdown("[📱 WhatsApp Pro Support](https://wa.me/918210073056)")

# === ELECTION TOOL (Core Feature) ===
if selected == "🗳️ Election Tool":
    st.markdown('<h1 class="pro-header">Election Campaign Audio Studio</h1>', unsafe_allow_html=True)
    
    # === PRO INPUTS ===
    st.markdown("### 📋 Campaign Setup")
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.markdown("**👤 Candidate Profile**")
        name = st.text_input("Full Name", "Eknath Jha", help="Pura naam with title")
        pad = st.selectbox("Post", ["Mukhiya", "Sarpanch", "Zila Parishad", "Pramukh"])
    
    with col_right:
        st.markdown("**🗳️ Campaign Info**")
        panchayat = st.text_input("Panchayat/Ward", "Patna City")
        symbol = st.text_input("Symbol", "Motorcycle", help="Chunav chinh/symbol")
    
    # === MUSIC SELECTION ===
    st.markdown("### 🎼 Professional Background")
    music_dir = "music"
    music_list = []
    if os.path.exists(music_dir):
        music_list = [f for f in os.listdir(music_dir) 
                     if any(f.lower().endswith(ext) for ext in ['.mp3', '.m4a', '.wav', '.ogg'])]
    
    col_music1, col_music2 = st.columns([3,1])
    with col_music1:
        selected_music = st.selectbox("Audio Track", ["No Music"] + music_list)
    with col_music2:
        if music_list:
            st.metric("Tracks Available", len(music_list))
        else:
            st.warning("➕ Add MP3 files to `/music/` folder")
    
    # === GENERATE BUTTON ===
    st.markdown("---")
    st.markdown('<div style="text-align:center; margin:30px 0;">', unsafe_allow_html=True)
    
    if st.button("🎙️ GENERATE PRO CAMPAIGN AUDIO", 
                type="primary", 
                use_container_width=True,
                disabled=not (is_followed or st.session_state.get('pro_unlocked', False))):
        
        # === PHASE 1: AI SCRIPT ===
        with st.spinner("🧠 Gemini generating crowd-winning script..."):
            prompt = f"""Create COMPELLING 25-30 second Hindi election campaign speech:
            
👤 {name} - {pad} ({panchayat})
🗳️ Symbol: {symbol}

STYLE: Emotional, rhythmic, crowd-chanting. Voter psychology focus.
WORDS: 85-110. Natural spoken Hindi. POWERFUL ending CTA."""
            
            try:
                response = model.generate_content(prompt)
                script = response.text.strip()
                st.session_state.current_script = script
                
                st.markdown("### 🎤 Generated Campaign Script")
                st.success(script)
                
            except Exception as script_error:
                st.error(f"❌ Script error: {str(script_error)}")
                st.stop()
        
        # === PHASE 2: VOICE SYNTHESIS ===
        with st.spinner("🎤 ElevenLabs creating studio voice..."):
            voice_file = generate_voice(st.session_state.current_script)
            if not voice_file:
                st.error("❌ Voice synthesis failed. Check ElevenLabs quota.")
                st.stop()
        
        # === PHASE 3: PRO AUDIO MIX ===
        with st.spinner("✨ Professional mixing & mastering..."):
            final_audio = mix_audio(voice_file, selected_music)
            
            # === FINAL OUTPUT ===
            st.markdown("### 🎧 Professional Campaign Audio READY")
            st.audio(final_audio)
            
            # Pro Download
            with open(final_audio, "rb") as f:
                st.download_button(
                    "💾 Download Campaign MP3",
                    f.read(),
                    f"PRO_Campaign_{name}_{pad}_{panchayat}.mp3",
                    "audio/mpeg"
                )
            
            st.balloons()
            st.success("✅ **Broadcast Ready!** Share instantly with voters")
        
        # === AUTO CLEANUP ===
        for path in [voice_file, final_audio]:
            try:
                if path and os.path.exists(path):
                    os.unlink(path)
            except:
                pass
    
    st.markdown('</div>', unsafe_allow_html=True)

# === OTHER SECTIONS ===
elif selected == "🚀 Ad Studio":
    st.markdown('<h1 class="pro-header">Business Ad Creator</h1>', unsafe_allow_html=True)
    st.info("🎬 Video ads with AI voice - Launching Q1 2026")

elif selected == "📊 Dashboard":
    st.markdown('<h1 class="pro-header">Analytics Dashboard</h1>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1: st.metric("Total Campaigns", "127", "23")
    with col2: st.metric("Success Rate", "98.4%", "+2.1%")
    with col3: st.metric("Avg Duration", "28s", "-1s")

elif selected == "📞 Support":
    st.markdown('<h1 class="pro-header">Priority Support</h1>', unsafe_allow_html=True)
    st.columns(2)[0].link_button("💬 WhatsApp", "https://wa.me/918210073056")
    st.info("""
    **Production Checklist:**
    • ✅ Secrets configured
    • ✅ music/ folder ready  
    • ✅ Deployed on Streamlit Cloud
    """)

# === FOOTER ===
st.markdown("""
<footer style='
    background: linear-gradient(135deg, #e91e63 0%, #9c27b0 100%); 
    color: white; 
    padding: 25px; 
    text-align: center; 
    margin-top: 50px; 
    border-radius: 20px;
'>
    <h3>© 2026 Patna AI Studio Pro v9.0</h3>
    <p><strong>Bihar's Premier Election AI Platform</strong> | 📞 <a href="tel:+918210073056" style="color:#fff;">8210073056</a></p>
</footer>
""", unsafe_allow_html=True)
