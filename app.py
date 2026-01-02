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
    st.error("🚫 API Keys not found in Secrets!")
    st.stop()

# AI Model Setup (FALLBACK Mechanism to avoid 404)
genai.configure(api_key=GEMINI_API_KEY)
model_names = ['gemini-1.5-flash-latest', 'gemini-1.5-flash', 'gemini-pro']
model = None
for name in model_names:
    try:
        model = genai.GenerativeModel(name)
        model.generate_content("test", generation_config={"max_output_tokens": 1})
        st.sidebar.success(f"✅ Active Model: {name}")
        break
    except: 
        continue

if model is None:
    st.error("🚫 No working AI model found!")
    st.stop()

# --- 2. COMPLETE AUDIO ENGINE ---
def generate_voice(text):
    url = "https://api.elevenlabs.io/v1/text-to-speech/pNInz6obpg8ndclAY7gu"
    headers = {
        "Accept": "audio/mpeg",
        "xi-api-key": ELEVENLABS_API_KEY, 
        "Content-Type": "application/json"
    }
    data = {
        "text": text[:2500],
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}
    }
    try:
        response = requests.post(url, json=data, headers=headers, timeout=45)
        if response.status_code == 200:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
                f.write(response.content)
                return f.name
        st.error(f"Voice API Error: {response.status_code}")
    except Exception as e:
        st.error(f"Voice generation failed: {str(e)}")
    return None

def mix_audio(voice_path, music_name):
    try:
        voice = AudioSegment.from_file(voice_path)
        if music_name and music_name != "No Music":
            music_path = os.path.join("music", music_name)
            if os.path.exists(music_path):
                music = AudioSegment.from_file(music_path) - 22
                if len(music) > len(voice):
                    music = music[:len(voice)]
                combined = music.overlay(voice)
                final_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
                combined.export(final_path, format="mp3")
                return final_path
        return voice_path
    except Exception as e:
        st.warning(f"Music mix skipped: {str(e)}")
        return voice_path

# --- 3. PRO UI DESIGN ---
st.set_page_config(page_title="Patna AI Studio Pro v10.0", layout="wide", page_icon="💎")

st.markdown("""
<style>
.main-title {color: #e91e63; font-size: 3.5rem; text-align: center; text-shadow: 2px 2px 8px rgba(0,0,0,0.3);}
.btn-generate {background: linear-gradient(45deg, #ff4081, #f50057); color: white; border-radius: 25px; padding: 15px 30px; font-size: 18px;}
.section-card {background: #f8f9fa; padding: 25px; border-radius: 15px; border-left: 5px solid #e91e63; margin: 20px 0;}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("<h2 style='color:#e91e63; text-align:center;'>Patna AI Studio Pro v10.0</h2>", unsafe_allow_html=True)
    selected = option_menu(
        "🎯 Control Panel", 
        ["🗳️ Election Tool", "🚀 Ad Studio", "📊 Dashboard", "📞 Support"], 
        icons=["mic", "sparkles", "bar-chart", "phone"],
        default_index=0
    )
    is_followed = st.checkbox("✅ YouTube Subscribed", value=False)
    st.markdown("---")
    st.markdown("[📱 Direct WhatsApp](https://wa.me/918210073056)")

# --- MAIN SECTIONS WITH FULL AUDIO PIPELINE ---
if selected == "🗳️ Election Tool":
    st.markdown('<h1 class="main-title">Professional Campaign Audio Generator</h1>', unsafe_allow_html=True)
    
    # Input Form
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 👤 Candidate Details")
        name = st.text_input("Full Name", "Eknath Jha")
        pad = st.selectbox("Post", ["Mukhiya", "Sarpanch", "Zila Parishad", "Pramukh"])
    with col2:
        st.markdown("### 🗳️ Campaign Info")
        panchayat = st.text_input("Panchayat/Ward", "Manikchouk")
        symbol = st.text_input("Symbol", "Motorcycle")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Music Selection
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("### 🎵 Background Music")
    music_files = []
    if os.path.exists("music"):
        music_files = [f for f in os.listdir("music") if f.endswith(('.mp3', '.m4a', '.wav'))]
    
    selected_music = st.selectbox("Choose Track", ["No Music"] + music_files)
    if not music_files:
        st.warning("💡 Add MP3 files to `music/` folder")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Generate Button
    col_btn_left, col_btn_right = st.columns([3,1])
    with col_btn_left:
        if st.button("🎙️ GENERATE PRO CAMPAIGN AUDIO", type="primary", 
                    disabled=not is_followed, use_container_width=True,
                    help="Subscribe on YouTube first!"):
            
            with st.spinner("🤖 Step 1/3: AI Script Generation..."):
                prompt = f"""Hindi election campaign speech for:
                {name} - {pad} ({panchayat})
                Symbol: {symbol}
                
                25 words. Emotional, rhythmic, powerful CTA."""
                script = model.generate_content(prompt).text.strip()
                st.session_state.script = script
                st.success(f"✅ **Script Ready:**
{script}")
            
            with st.spinner("🗣️ Step 2/3: Voice Synthesis..."):
                voice_file = generate_voice(st.session_state.script)
                if not voice_file:
                    st.error("❌ Voice failed. Check ElevenLabs quota.")
                    st.stop()
            
            with st.spinner("🎼 Step 3/3: Professional Mixing..."):
                final_audio = mix_audio(voice_file, selected_music)
                
                st.markdown("### 🎧 **FINAL OUTPUT**")
                st.audio(final_audio)
                
                with open(final_audio, "rb") as audio_f:
                    st.download_button(
                        "💾 Download Campaign MP3", 
                        audio_f.read(),
                        f"Campaign_{name}_{pad}.mp3",
                        "audio/mpeg"
                    )
                
                st.balloons()
                st.success("🎉 **Ready for Broadcast!**")
            
            # Auto cleanup
            try:
                os.unlink(voice_file)
                os.unlink(final_audio)
            except: pass

elif selected == "🚀 Ad Studio":
    st.markdown('<h1 class="main-title">Business Ad Creator</h1>', unsafe_allow_html=True)
    st.info("🔥 Commercial video ads - Premium feature")

elif selected == "📊 Dashboard":
    st.markdown('<h1 class="main-title">Analytics Dashboard</h1>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1: st.metric("Campaigns Created", 247, 32)
    with col2: st.metric("Success Rate", "99.2%", "0.8%")
    with col3: st.metric("Avg Length", "27s")

elif selected == "📞 Support":
    st.markdown('<h1 class="main-title">Priority Support</h1>', unsafe_allow_html=True)
    st.columns(1)[0].markdown("""
    ### 🚀 **Instant Help**
    - 💬 [WhatsApp Support](https://wa.me/918210073056)
    - 📱 Call: **8210073056**
    
    ### ⚙️ **Production Setup**
    ```
    1. Secrets.toml → API keys ✅
    2. music/ → MP3 files ✅
    3. Deploy → Streamlit Cloud ✅
    ```
    """)

# Footer
st.markdown("""
<div style='text-align:center; padding:30px; background:linear-gradient(90deg,#e91e63,#9c27b0); color:white; border-radius:20px; margin:40px 0;'>
    <h2>© 2026 Patna AI Studio Pro v10.0</h2>
    <p><strong>Bihar's #1 AI Campaign Platform</strong> | 📞 8210073056</p>
</div>
""", unsafe_allow_html=True)
