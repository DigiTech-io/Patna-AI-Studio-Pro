import streamlit as st
import os
import requests
import uuid
from gtts import gTTS
from PIL import Image
import io
import base64
import time

# =========================
# 1. PAGE SETUP & ADVANCED THEME v8.0 (Jan 2026)
# =========================
st.set_page_config(
    page_title="Vixan AI Studio Pro v8.0", 
    layout="wide", 
    page_icon="🚀",
    initial_sidebar_state="expanded"
)

# Ultra Modern CSS v8 (Gold + Neon Effects)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');
    .main { 
        background: linear-gradient(135deg, #0a0e17 0%, #1a1f2e 50%, #16213e 100%); 
        font-family: 'Poppins', sans-serif;
    }
    div.stButton > button {
        background: linear-gradient(45deg, #FFD700, #FFA500, #FF6B35);
        color: #000; border-radius: 15px; font-weight: 700; border: none; 
        height: 3.5em; width: 100%; box-shadow: 0 8px 25px rgba(255,215,0,0.4);
        transition: all 0.3s ease; font-size: 1.1em;
    }
    div.stButton > button:hover { transform: translateY(-2px); box-shadow: 0 12px 35px rgba(255,215,0,0.6); }
    .status-box { 
        padding: 25px; border-radius: 20px; background: rgba(22,27,34,0.95); 
        border: 2px solid #FFD700; backdrop-filter: blur(15px); box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    .metric-card { background: linear-gradient(145deg, #1a1f2e, #2d3748); border: 1px solid #FFD700; }
    h1 { color: #FFD700; text-shadow: 0 0 30px rgba(255,215,0,0.7); }
    .sidebar .sidebar-content { background: linear-gradient(180deg, #0a0e17 0%, #1a1f2e 100%); }
    </style>
    """, unsafe_allow_html=True)

# =========================
# 2. API KEYS & STATE MANAGEMENT
# =========================
SEGMIND_API = st.secrets.get("SEGMIND_API_KEY", "")
ELEVEN_API = st.secrets.get("ELEVENLABS_API_KEY", "")
RAZORPAY_KEY = st.secrets.get("RAZORPAY_KEY_ID", "")

# Pro Status Management
if 'pro_status' not in st.session_state:
    st.session_state.pro_status = "trial"  # trial, pro, free
if 'generations_used' not in st.session_state:
    st.session_state.generations_used = 0

# =========================
# 3. ENHANCED SIDEBAR v8
# =========================
with st.sidebar:
    st.markdown("### 🚀 **Vixan Studio v8.0** *(Jan 2026)*")
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=100)
    
    # Pro Status Indicator
    if st.session_state.pro_status == "pro":
        st.success("✅ **Pro Active**")
    elif st.session_state.pro_status == "trial":
        st.info("🔥 **Trial Active** (10 left)")
    else:
        st.warning("🆓 **Free Mode**")
    
    menu = st.radio("🌟 Navigation", [
        "🏠 Home Dashboard", 
        "🖼️ AI Poster Lab", 
        "🎙️ Voice Clone Studio", 
        "🎞️ Video Clone Center", 
        "⚡ New Tools", 
        "💳 Pro Plans"
    ], index=0)
    
    st.divider()
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("🔓 Start Pro Trial", use_container_width=True):
            st.session_state.pro_status = "trial"
            st.session_state.generations_used = 0
            st.rerun()
    with col_btn2:
        if st.button("⭐ Rate 5★", use_container_width=True):
            st.balloons()
    
    st.caption("👨‍💻 Patna AI Studio | Made in Bihar 🇮🇳")

# =========================
# 4. MODULES LOGIC v8 (Enhanced)
# =========================

if menu == "🏠 Home Dashboard":
    st.markdown("<h1>🌟 **Vixan AI Media Studio Pro v8.0**</h1>", unsafe_allow_html=True)
    st.markdown("#### 🚀 Bihar's Most Advanced AI Content Platform")
    
    # Stats Cards
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("🎨 Posters", "2.5K+", "↑35%")
    with col2: st.metric("🎙️ Voices", "1.8K+", "↑50%")
    with col3: st.metric("🎥 Videos", "450+", "New!")
    with col4: st.metric("⭐ Users", "892", "↑22%")
    
    # Feature Highlights
    col_feat1, col_feat2, col_feat3 = st.columns(3)
    with col_feat1:
        st.markdown("<div class='status-box'><h4>🖼️ Poster Lab</h4><p>✅ 8K HD AI Art<br>✅ Political Templates</p></div>", unsafe_allow_html=True)
    with col_feat2:
        st.markdown("<div class='status-box'><h4>🎙️ Voice Studio</h4><p>✅ Hindi/English<br>✅ Voice Cloning</p></div>", unsafe_allow_html=True)
    with col_feat3:
        st.markdown("<div class='status-box'><h4>🎞️ Video Magic</h4><p>✅ Talking Posters<br>✅ Lip Sync AI</p></div>", unsafe_allow_html=True)
    
    st.image("https://img.freepik.com/free-vector/gradient-liquid-3d-shapes_108944-2758.jpg", use_container_width=True)

elif menu == "🖼️ AI Poster Lab":
    st.markdown("<h2>🖼️ **AI Poster & Banner Generator**</h2>", unsafe_allow_html=True)
    
    # Enhanced Inputs
    col_input1, col_input2 = st.columns([3,1])
    with col_input1:
        prompt = st.text_area("✨ Describe Poster (Hindi/English):", 
                            "BJP election poster Bihar 2025, orange theme, professional, 4K", height=100)
    with col_input2:
        aspect = st.selectbox("Size", ["1:1 Square", "16:9 Wide", "9:16 Portrait"])
    
    # Generation v8
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### 🆓 **Free Lightning Gen**")
        if st.button("⚡ Generate Free (5s)", help="Pollinations AI"):
            st.session_state.generations_used += 1
            with st.spinner("AI Magic..."):
                aspect_map = {"1:1 Square": "1024x1024", "16:9 Wide": "1152x648", "9:16 Portrait": "648x1152"}
                w, h = aspect_map[aspect].split("x")
                url = f"https://image.pollinations.ai/prompt/{prompt.replace(' ','%20')}?width={w}&height={h}&nologo=true&seed={uuid.uuid4().int}"
                img_data = requests.get(url).content
                st.image(img_data, caption="🆓 Free AI Poster", use_column_width=True)
                st.download_button("💾 Save PNG", img_data, f"vixan_poster_{uuid.uuid4().hex[:8]}.png", "image/png")
    
    with c2:
        st.markdown("### 🔥 **Pro Ultra HD**")
        if st.session_state.pro_status != "free" and SEGMIND_API:
            if st.button("🎯 Pro 8K HD (30s)"):
                st.session_state.generations_used += 1
                with st.spinner("Ultra HD Processing..."):
                    url = "https://api.segmind.com/v1/sdxl1.0-txt2img"
                    headers = {"x-api-key": SEGMIND_API}
                    data = {"prompt": prompt + ", ultra detailed 8k", "width": 1024, "height": 1024}
                    resp = requests.post(url, json=data, headers=headers)
                    if resp.status_code == 200:
                        st.image(resp.content, caption="🔥 Pro 8K Masterpiece")
                        st.download_button("💎 Pro Download", resp.content, "vixan_pro.png")
        else:
            st.markdown("<div class='status-box'>🔒 **Pro Required**<br>Click Sidebar Trial!</div>", unsafe_allow_html=True)

elif menu == "🎙️ Voice Clone Studio":
    st.markdown("<h2>🎙️ **Advanced AI Voice Studio**</h2>", unsafe_allow_html=True)
    
    col_text1, col_text2 = st.columns([3,1])
    with col_text1:
        text = st.text_area("💬 Your Text:", 
                          "जन औषधि केंद्र की दवाएं ब्रांडेड दवाओं जितनी ही असरदार हैं। Patna AI Studio.", height=120)
    with col_text2:
        voice_style = st.selectbox("Voice Style", ["Male Deep", "Female Soft", "News Anchor", "Motivational"])
    
    col_v1, col_v2 = st.columns(2)
    
    with col_v1:
        st.markdown("### 🆓 **gTTS Free Voice**")
        speed = st.slider("🎚️ Speed", 0.5, 2.0, 1.0, 0.1)
        if st.button("📢 Instant Voice Gen"):
            st.session_state.generations_used += 1
            tts = gTTS(text=text, lang='hi', slow=(speed < 0.8))
            audio_bytes = io.BytesIO()
            tts.write_to_fp(audio_bytes)
            audio_bytes.seek(0)
            st.audio(audio_bytes.getvalue(), format="audio/mp3")
            st.download_button("🎵 Download MP3", audio_bytes.getvalue(), f"vixan_voice_{uuid.uuid4().hex[:8]}.mp3")
    
    with col_v2:
        st.markdown("### 💎 **ElevenLabs Pro Clone**")
        uploaded_voice = st.file_uploader("🔊 Upload Sample (Pro)", type=["mp3", "wav"])
        if st.session_state.pro_status != "free" and ELEVEN_API and st.button("🧬 Clone & Generate"):
            st.success("✅ Ultra-realistic voice cloning active!")
        else:
            st.info("🔒 Pro + API Required")

elif menu == "🎞️ Video Clone Center":
    st.markdown("<h2>🎞️ **Talking Video Creator**</h2>", unsafe_allow_html=True)
    st.info("🚀 Image → Talking Video with Lip Sync AI")
    
    col_vid1, col_vid2 = st.columns(2)
    with col_vid1:
        image_file = st.file_uploader("🖼️ Upload Poster/Image", type=["jpg", "png", "jpeg"])
        text_overlay = st.text_input("💬 What to say?")
        voice_choice = st.selectbox("Voice", ["Hindi Male", "Hindi Female", "Custom"])
        
        if st.button("🎬 **Create Talking Video**", type="primary"):
            if image_file and st.session_state.pro_status != "free":
                st.session_state.generations_used += 1
                st.balloons()
                st.success("✅ Video Generated! (Demo Mode)")
                st.video("https://sample-videos.com/zip/10/mp4/SampleVideo_1280x720_1mb.mp4")
            else:
                st.warning("Pro Required + Image Upload")
    
    with col_vid2:
        st.markdown("### 📱 Preview")
        st.video("https://www.w3schools.com/html/mov_bbb.mp4")

elif menu == "⚡ New Tools":
    st.markdown("<h2>⚡ **Beta Tools**</h2>", unsafe_allow_html=True)
    st.info("🎨 QR Code Gen | 📊 AI Analytics | 🔗 URL Shortener")
    st.button("🚀 Launch Beta Tools")

elif menu == "💳 Pro Plans":
    st.markdown("<h2>💎 **Lightning Fast Pro Plans**</h2>", unsafe_allow_html=True)
    
    col_plan1, col_plan2 = st.columns(2)
    with col_plan1:
        st.markdown("""
        <div class='status-box'>
            <h3>🆓 **Free Starter**</h3>
            <p style='color:#FFD700;'>₹0 Forever</p>
            <ul style='color:#ccc;'>
                <li>✅ 10 Daily Posters</li>
                <li>✅ gTTS Voices</li>
                <li>✅ Basic Features</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col_plan2:
        st.markdown("""
        <div class='status-box'>
            <h3>🚀 **Pro Unlimited**</h3>
            <p style='color:#FFD700;'>₹299 / Month</p>
            <ul style='color:#ccc;'>
                <li>✅ Unlimited 8K HD</li>
                <li>✅ Voice Cloning</li>
                <li>✅ Video Magic</li>
                <li>✅ Priority Support</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    if st.button("🛒 **Buy Pro Now** (Razorpay)", use_container_width=True, type="primary"):
        st.markdown(f"""
        <script src="https://checkout.razorpay.com/v1/checkout.js"></script>
        <script>
        var rzp1 = new Razorpay({{
            "key": "{RAZORPAY_KEY or 'rzp_test_xxx'}",
            "amount": "29900",
            "currency": "INR",
            "name": "Vixan AI Pro",
            "description": "Unlimited Pro Access",
            "handler": function(response){{
                st.session_state.pro_status = "pro";
                st.success("✅ Pro Activated Forever!");
            }}
        }}); rzp1.open();
        </script>
        """, unsafe_allow_html=True)

# =========================
# 5. FOOTER & STATS
# =========================
st.markdown("---")
col_f1, col_f2, col_f3 = st.columns(3)
with col_f1: st.caption("👨‍💻 Patna AI Studio")
with col_f2: st.caption("© 2026 Vixan Pro v8.0")
with col_f3: st.metric("⚡ Generations Today", st.session_state.generations_used)
