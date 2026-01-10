import streamlit as st
import requests
import urllib.parse

# ================== PAGE CONFIG ==================
st.set_page_config(
    page_title="Vixan AI Studio Pro",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================== PREMIUM UI CSS ==================
st.markdown("""
<style>
.stApp {
    background-color: #0e1117;
    color: white;
}
h1, h2, h3 {
    color: #f1f1f1;
}
.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
}
.stTabs [data-baseweb="tab"] {
    background-color: #1f2937;
    border-radius: 8px;
    padding: 8px 16px;
    color: white;
}
.stButton>button {
    width: 100%;
    background: linear-gradient(90deg, #ff416c, #ff4b2b);
    color: white;
    border-radius: 10px;
    height: 3em;
    border: none;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ================== SECRETS ==================
ELEVEN_KEY = st.secrets.get("ELEVENLABS_API_KEY")

# ================== AUDIO FUNCTION ==================
def generate_audio(text, stability, clarity, style_exaggeration, voice_id):
    if not ELEVEN_KEY:
        return None, "ElevenLabs API Key missing"

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVEN_KEY
    }
    payload = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": stability,
            "similarity_boost": clarity,
            "style": style_exaggeration,
            "use_speaker_boost": True
        }
    }

    response = requests.post(url, json=payload, headers=headers, timeout=60)

    if response.status_code == 200:
        return response.content, None
    else:
        return None, response.text

# ================== APP HEADER ==================
st.title("🚀 Vixan AI Studio Pro")
st.caption("Advanced Audio • Hindi Image AI • Payments • WhatsApp Automation")

tab1, tab2, tab3 = st.tabs([
    "🎙️ Advanced Audio AI",
    "🎨 Image Studio",
    "💳 Payment & WhatsApp"
])

# ================== TAB 1 : AUDIO AI ==================
with tab1:
    st.subheader("Professional AI Voice Generator")

    col1, col2 = st.columns(2)

    with col1:
        text_input = st.text_area(
            "Script (Hindi / English)",
            "Namaste! Vixan AI Studio mein aapka swagat hai."
        )

        voice_name = st.selectbox(
            "Select Voice",
            [
                "Adam (Deep Male)",
                "Antoni (Friendly)",
                "Bella (Soft Female)"
            ]
        )

        voice_map = {
            "Adam (Deep Male)": "pNInz6obpgDQGcFmaJgB",
            "Antoni (Friendly)": "ErXwbc3VNb7s19Cc71v0",
            "Bella (Soft Female)": "EXAVITQu4vr4xnSDxMaL"
        }

    with col2:
        st.markdown("### 🎚️ Voice Controls")
        stability = st.slider("Stability", 0.0, 1.0, 0.5)
        clarity = st.slider("Clarity / Similarity", 0.0, 1.0, 0.75)
        style = st.slider("Style Exaggeration", 0.0, 1.0, 0.0)

    if st.button("🔊 Generate & Preview Audio"):
        with st.spinner("Generating studio-quality voice..."):
            audio, error = generate_audio(
                text_input,
                stability,
                clarity,
                style,
                voice_map[voice_name]
            )

            if audio:
                st.audio(audio, format="audio/mp3")
                st.download_button(
                    "⬇️ Download MP3",
                    audio,
                    "vixan_voice.mp3"
                )
            else:
                st.error(f"Audio generation failed: {error}")

# ================== TAB 2 : IMAGE AI ==================
with tab2:
    st.subheader("Hindi Prompt Image Generator")

    hindi_text = st.text_input(
        "Poster Text (Hindi)",
        "आपका विश्वास, हमारा विकास"
    )

    style_type = st.selectbox(
        "Visual Style",
        ["Political", "Cinematic", "3D Render"]
    )

    if st.button("🖼️ Generate Image"):
        prompt = (
            f"A {style_type} poster with bold, clear Devanagari Hindi text "
            f"'{hindi_text}', centered composition, professional lighting, "
            f"high contrast, ultra quality, 8k"
        )

        encoded_prompt = urllib.parse.quote_plus(prompt)

        image_url = (
            f"https://image.pollinations.ai/prompt/{encoded_prompt}"
            "?width=1024&height=1280&nologo=true"
        )

        st.image(
            image_url,
            caption="AI Generated Image (Hindi spelling may slightly vary)"
        )

# ================== TAB 3 : PAYMENT & WHATSAPP ==================
with tab3:
    st.subheader("💳 Razorpay Payment")

    st.markdown(
        "[![Pay Now](https://img.shields.io/badge/Pay%20Now-Razorpay-blue?style=for-the-badge)]"
        "(https://rzp.io/l/your_link)"
    )

    st.divider()

    st.subheader("📲 WhatsApp Auto Reply Link")

    wa_num = st.text_input("WhatsApp Number (with country code)")

    if st.button("Create WhatsApp Link"):
        if wa_num:
            wa_link = (
                f"https://wa.me/{wa_num}"
                "?text=Mujhe%20Vixan%20AI%20Premium%20chahiye"
            )
            st.success("WhatsApp Link Generated")
            st.code(wa_link)
        else:
            st.warning("Please enter a valid WhatsApp number")

# ================== SIDEBAR ==================
st.sidebar.title("🤝 Vixan Partner Panel")
st.sidebar.markdown("""
**Platform Features**
- AI Voice Studio (ElevenLabs)
- Hindi Poster Generator
- Razorpay Ready
- WhatsApp Automation
- Future Video AI Ready 🚀
""")
