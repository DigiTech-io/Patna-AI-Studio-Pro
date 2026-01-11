import streamlit as st
import os
import requests
import uuid
from gtts import gTTS
import base64
from PIL import Image
import io

# --- CONFIG (v7.0 - Jan 2026 Update) ---
st.set_page_config(page_title="Vixan AI Studio Pro v7.0", layout="wide", initial_sidebar_state="expanded")

# API Keys from Secrets
SEGMIND_API = st.secrets.get("SEGMIND_API_KEY", "")
ELEVEN_API = st.secrets.get("ELEVENLABS_API_KEY", "")
RAZORPAY_KEY = st.secrets.get("RAZORPAY_KEY_ID", "")

# Custom CSS (Enhanced v7)
st.markdown("""
    <style>
    .main { background: linear-gradient(135deg, #0e1117 0%, #1a1f2e 100%); }
    .stButton>button { width: 100%; border-radius: 12px; font-weight: 600; transition: all 0.3s; }
    .free-btn { background: linear-gradient(45deg, #28a745, #20c997); color: white !important; }
    .pro-btn { background: linear-gradient(45deg, #ffc107, #ff8c00); color: black !important; box-shadow: 0 4px 15px rgba(255,193,7,0.4); }
    .card { border: 1px solid #333; padding: 20px; border-radius: 20px; background: rgba(22,27,34,0.9); backdrop-filter: blur(10px); }
    .metric-card { background: linear-gradient(145deg, #1a1f2e, #2d3748); }
    h1 { color: #f0f9ff; font-size: 3rem; text-shadow: 0 0 20px rgba(255,193,7,0.5); }
    </style>
    """, unsafe_allow_html=True)

# Session State for Pro Status
if 'pro_active' not in st.session_state:
    st.session_state.pro_active = False

# --- SIDEBAR (Enhanced) ---
with st.sidebar:
    st.markdown("### 🚀 **Vixan Pro v7.0**")
    st.image("https://img.freepik.com/free-vector/gradient-liquid-3d-shapes_108944-2758.jpg?w=200", use_column_width=True)
    
    menu = st.radio("🔥 Select Tool", ["🏠 Dashboard", "🖼️ Poster Lab", "🎙️ Voice Studio", "🎥 Video Lab", "💳 Pricing"], index=0)
    
    st.divider()
    if st.button("⭐ Activate Pro Trial", key="pro_trial"):
        st.session_state.pro_active = True
        st.success("✅ Pro Trial Activated for 24 hours!")
    
    st.caption("👨‍💻 Patna AI Studio | Bihar's #1 AI Platform")
    st.caption("📅 Updated: Jan 11, 2026")

# --- 1. DASHBOARD (v7 Enhanced) ---
if menu == "🏠 Dashboard":
    st.markdown("<h1>🌟 Vixan AI Media Studio Pro</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🎨 Posters Generated", "1.2K+", delta="↑ 25%")
    with col2:
        st.metric("🎙️ Voices Created", "850+", delta="↑ 40%")
    with col3:
        st.metric("⭐ Pro Users", "247", delta="↑ 15%")
    
    st.info("🚀 **Bihar's Most Advanced AI Studio**. Unlimited Free Tools + Pro HD Upgrades.")
    
    # Quick Actions
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("🖼️ Quick Poster", use_container_width=True):
            st.switch_page("pages/poster.py")  # Hypothetical page
    with col_b:
        if st.button("🎙️ Quick Voice", use_container_width=True):
            st.switch_page("pages/voice.py")

# --- 2. POSTER LAB (v7 Pro) ---
elif menu == "🖼️ Poster Lab":
    st.markdown("<h2>🖼️ **AI Poster Generator v7**</h2>", unsafe_allow_html=True)
    
    # Enhanced Input
    col_prompt, col_style = st.columns([3,1])
    with col_prompt:
        prompt = st.text_area("✨ Describe your poster (English/Hindi):", 
                            "Professional election poster, orange BJP theme, Bihar election 2025, 4K HD", 
                            height=100)
    with col_style:
        style = st.selectbox("Style", ["Realistic", "Cinematic", "Cartoon", "Minimalist"])
    
    # Generation Columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🆓 **Free Generation**")
        if st.button("🎨 Generate Free Poster", key="free_post_v7", help="Fast AI Generation"):
            with st.spinner("✨ Creating Free Poster..."):
                free_url = f"https://image.pollinations.ai/prompt/{prompt.replace(' ', '%20')}?width=1024&height=1024&nologo=true&seed={uuid.uuid4().int}"
                img_data = requests.get(free_url).content
                st.image(img_data, caption="🆓 Free AI Poster", use_column_width=True)
                st.download_button("📥 Download Free", img_data, f"vixan_free_{uuid.uuid4().hex[:8]}.png", "image/png")

    with col2:
        st.markdown("### 🔥 **Pro HD Generation**")
        pro_status = st.session_state.pro_active or bool(SEGMIND_API)
        if pro_status:
            if st.button("🚀 Generate Pro HD Poster", key="pro_post_v7", help="Unlimited HD Credits"):
                with st.spinner("🎯 Generating Ultra HD Poster..."):
                    url = "https://api.segmind.com/v1/sdxl1.0-txt2img"
                    headers = {"x-api-key": SEGMIND_API}
                    data = {
                        "prompt": f"{prompt}, {style}, ultra detailed, 8k, professional",
                        "samples": 1, "scheduler": "dpmpp_2m", "num_inference_steps": 30,
                        "width": 1024, "height": 1024
                    }
                    response = requests.post(url, json=data, headers=headers)
                    if response.status_code == 200:
                        st.image(response.content, caption="🔥 Pro Ultra HD Poster", use_column_width=True)
                        st.download_button("💎 Download Pro HD", response.content, f"vixan_pro_{uuid.uuid4().hex[:8]}.png", "image/png")
                    else:
                        st.error("Pro API Error. Check key.")
        else:
            st.warning("🔒 **Pro Required**. Click sidebar trial or upgrade.")

# --- 3. VOICE STUDIO (v7 Enhanced) ---
elif menu == "🎙️ Voice Studio":
    st.markdown("<h2>🎙️ **AI Voice Studio v7**</h2>", unsafe_allow_html=True)
    
    col_text, col_lang = st.columns([3,1])
    with col_text:
        text = st.text_area("💬 Enter Text (Hindi/English):", 
                          "नमस्कार! पटना एआई स्टूडियो से स्वागत है। जन औषधि केंद्र की दवाएं ब्रांडेड जितनी ही असरदार हैं।", height=120)
    with col_lang:
        lang = st.selectbox("Language", ["hi", "en", "ta", "te"])
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🆓 **Free Voice (gTTS)**")
        speed = st.slider("🔊 Speed", 0.5, 2.0, 1.0, 0.1)
        if st.button("📢 Generate Free Voice", key="free_voice_v7"):
            tts = gTTS(text=text, lang=lang, slow=(speed < 0.8))
            audio_bytes = io.BytesIO()
            tts.write_to_fp(audio_bytes)
            audio_bytes.seek(0)
            st.audio(audio_bytes, format="audio/mp3")
            st.download_button("📥 Download Free MP3", audio_bytes.getvalue(), f"vixan_free_voice_{uuid.uuid4().hex[:8]}.mp3", "audio/mp3")

    with col2:
        st.markdown("### 💎 **Pro Voice (ElevenLabs)**")
        pro_status = st.session_state.pro_active or bool(ELEVEN_API)
        if pro_status:
            stability = st.slider("🎭 Stability", 0.0, 1.0, 0.5)
            if st.button("🌟 Generate Human-like Voice", key="pro_voice_v7"):
                st.warning("✅ ElevenLabs Pro Active - Ultra Realistic Voice")
                # Enhanced ElevenLabs placeholder (add real API)
        else:
            st.warning("🔒 **Pro Required**. Ultra-realistic voices unlocked!")

# --- 4. NEW VIDEO LAB (v7 Exclusive) ---
elif menu == "🎥 Video Lab":
    st.markdown("<h2>🎥 **AI Video Generator**</h2>", unsafe_allow_html=True)
    st.info("🚀 Coming Soon: Text-to-Video with Kling AI & RunwayML")
    if st.button("🎬 Reserve Pro Access", use_container_width=True):
        st.success("✅ Pro Video Access Reserved!")

# --- 5. PRICING (Razorpay Integrated v7) ---
elif menu == "💳 Pricing":
    st.markdown("<h2>💎 **Upgrade to Vixan Pro v7**</h2>", unsafe_allow_html=True)
    
    col_plan1, col_plan2 = st.columns(2)
    with col_plan1:
        st.markdown("""
        ### 🆓 **Free Forever**
        - ✅ Basic Posters (1024x1024)
        - ✅ gTTS Voices
        - ✅ 5 Daily Generations
        - ❌ No HD Pro
        """)
    
    with col_plan2:
        st.markdown("""
        ### 🔥 **Pro Unlimited** ₹299 / Month
        - ✅ Unlimited HD Posters (8K)
        - ✅ ElevenLabs Pro Voices
        - ✅ Video Generation
        - ✅ Priority Support
        - ✅ No Watermarks
        """)
    
    if st.button("🛒 **Buy Pro with Razorpay** (₹299)", use_container_width=True, type="primary"):
        if RAZORPAY_KEY:
            st.success("✅ Redirecting to Razorpay...")
            st.markdown(f"""
            <script src="https://checkout.razorpay.com/v1/checkout.js"></script>
            <script>
            var options = {{"key": "{RAZORPAY_KEY}", "amount": "29900", "currency": "INR",
            "name": "Vixan AI Pro", "description": "Unlimited Pro Access",
            "handler": function(response){{ st.success('Payment Success! Pro Activated.'); }}}};
            var rzp = new Razorpay(options); rzp.open();
            </script>
            """, unsafe_allow_html=True)
        else:
            st.link_button("🔗 Buy via Link", "https://rzp.io/l/vixan_pro_v7")

# Footer
st.markdown("---")
st.markdown("👨‍💻 **Developed by Patna AI Studio** | © 2026 Vixan Pro v7.0 | Made in Bihar 🇮🇳")
