import streamlit as st
import requests

# --- CONFIG ---
st.set_page_config(page_title="Vixan AI Studio Pro", layout="wide")

# CSS for Premium Look
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] { background-color: #262730; border-radius: 5px; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- SECRETS ---
ELEVEN_KEY = st.secrets.get("ELEVENLABS_API_KEY")

# --- AUDIO ENGINE FUNCTION ---
def generate_audio(text, stability, clarity, style_exaggeration, voice_id):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVEN_KEY
    }
    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": stability,
            "similarity_boost": clarity,
            "style": style_exaggeration,
            "use_speaker_boost": True
        }
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        return response.content
    else:
        return None

# --- APP LAYOUT ---
st.title("🚀 Vixan AI Studio Pro")

tab1, tab2, tab3 = st.tabs(["🎙️ Advanced Audio AI", "🎨 Image Studio", "💳 Payment & WhatsApp"])

# --- TAB 1: AUDIO CLONING & CONTROL ---
with tab1:
    st.subheader("Professional Voice Settings")
    col1, col2 = st.columns(2)
    
    with col1:
        text_input = st.text_area("Write Script (Hindi/English)", "Namaste, Vixan AI Studio mein aapka swagat hai.")
        voice_id = st.selectbox("Select Voice Type", [
            ("Adam - Deep Male", "pNInz6obpgDQGcFmaJgB"),
            ("Antoni - Friendly", "ErXwbc3VNb7s19Cc71v0"),
            ("Bella - Soft Female", "EXAVITQu4vr4xnSDxMaL")
        ])
        
    with col2:
        st.write("🎚️ Sound Control Settings")
        stab = st.slider("Stability (Low: Emotional | High: Steady)", 0.0, 1.0, 0.5)
        clarity = st.slider("Clarity + Similarity Boost", 0.0, 1.0, 0.75)
        style = st.slider("Style Exaggeration", 0.0, 1.0, 0.0)

    if st.button("Generate & Preview Audio 🔊"):
        if not ELEVEN_KEY:
            st.error("ElevenLabs API Key missing!")
        else:
            with st.spinner("Creating AI Voice..."):
                audio_content = generate_audio(text_input, stab, clarity, style, voice_id[1])
                if audio_content:
                    st.audio(audio_content, format='audio/mp3')
                    st.download_button("Download Audio", audio_content, "vixan_audio.mp3")
                else:
                    st.error("Error generating audio. Check API quota.")

# --- TAB 2: IMAGE STUDIO (Hindi Prompt Fix) ---
with tab2:
    st.subheader("Image Generator (Hindi Prompt Support)")
    # AI ko Hindi likhne ke liye instruction dena padta hai
    hindi_text = st.text_input("Poster par kya likhna hai? (Hindi mein)")
    style_type = st.selectbox("Style", ["Political", "Cinematic", "3D Render"])
    
    if st.button("Generate Image 🖼️"):
        # Yahan hum prompt ko optimize kar rahe hain taaki AI Hindi fonts behtar banaye
        prompt = f"A professional {style_type} poster. In the center, large bold Devanagari Hindi text saying '{hindi_text}'. High quality, 8k, vibrant colors."
        img_url = f"https://image.pollinations.ai/prompt/{prompt.replace(' ', '%20')}?width=1024&height=1280&nologo=true"
        st.image(img_url, caption="Note: AI kabhi-kabhi Hindi spelling galat kar sakta hai.")

# --- TAB 3: PAYMENT & WHATSAPP ---
with tab3:
    st.info("Razorpay Payment Gateway")
    st.markdown(f"[![Pay Now](https://img.shields.io/badge/Pay%20Now-Razorpay-blue?style=for-the-badge)](https://rzp.io/l/your_link)")
    
    st.write("---")
    st.subheader("WhatsApp Auto-Reply")
    wa_num = st.text_input("WhatsApp Number")
    if st.button("Create WhatsApp Link"):
        link = f"https://wa.me/{wa_num}?text=Mujhe%20Vixan%20AI%20Premium%20chahiye"
        st.success(f"Link Ready: {link}")

st.sidebar.title("Vixan Partner Panel")
st.sidebar.write("Unique Feature: **Auto-Content Suggestion**")
