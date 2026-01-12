import streamlit as st
import os, requests, uuid
from gtts import gTTS
from PIL import Image
import io

# =========================================================
# 1. APP CONFIG
# =========================================================
st.set_page_config(
    page_title="Vixan AI Pro v12.0",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# 2. PREMIUM UI / THEME
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Rajdhani', sans-serif;
    background: linear-gradient(135deg, #020111, #050625);
    color: white;
}

.glass {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(0,210,255,0.3);
    border-radius: 20px;
    padding: 20px;
    box-shadow: 0 0 25px rgba(0,210,255,0.15);
}

.glass:hover {
    border-color:#00d2ff;
    box-shadow:0 0 35px rgba(0,210,255,0.35);
    transform: translateY(-4px);
    transition:0.3s;
}

.stButton>button {
    background: linear-gradient(90deg,#00d2ff,#3a7bd5);
    color:white;
    border:none;
    border-radius:14px;
    padding:12px 24px;
    font-weight:700;
    width:100%;
}

.stButton>button:hover {
    box-shadow:0 0 25px #00d2ff;
    letter-spacing:1px;
}

.float-support {
    position:fixed;
    bottom:25px;
    left:25px;
    display:flex;
    flex-direction:column;
    gap:12px;
    z-index:999;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# 3. SESSION STATE
# =========================================================
if "auth" not in st.session_state:
    st.session_state.auth = False
if "user" not in st.session_state:
    st.session_state.user = ""

# =========================================================
# 4. AUTH FUNCTION
# =========================================================
def auth_gate():
    st.warning("🔒 Login Required to Unlock AI Power")
    with st.container():
        name = st.text_input("👤 Full Name")
        phone = st.text_input("📱 WhatsApp Number")
        if st.button("🚀 Unlock Vixan AI"):
            if name and len(phone) >= 10:
                st.session_state.auth = True
                st.session_state.user = name
                st.success(f"Welcome {name}")
                st.rerun()
            else:
                st.error("Enter valid details")

# =========================================================
# 5. SIDEBAR
# =========================================================
with st.sidebar:
    st.markdown("<h2 style='color:#00d2ff'>VIXAN AI</h2>", unsafe_allow_html=True)
    st.caption("Next-Gen AI Media Engine")
    menu = st.radio(
        "Navigation",
        ["🏠 Dashboard", "🖼️ Poster Lab", "🎙️ Voice Studio", "🎞️ Video AI", "ℹ️ About"]
    )
    st.divider()
    if st.session_state.auth:
        st.success(f"Logged in as {st.session_state.user}")
        if st.button("Logout"):
            st.session_state.auth = False
            st.rerun()

# =========================================================
# 6. DASHBOARD
# =========================================================
if menu == "🏠 Dashboard":
    st.title("⚡ Vixan AI Pro")
    st.subheader("India’s Next-Gen AI Design & Voice Platform")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<div class='glass'><h3>🖼️ Poster AI</h3><p>4K Political & Business Designs</p></div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='glass'><h3>🎙️ Voice AI</h3><p>Human-like Hindi / English</p></div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<div class='glass'><h3>🎞️ Video AI</h3><p>Talking Posters (Soon)</p></div>", unsafe_allow_html=True)

# =========================================================
# 7. POSTER LAB
# =========================================================
elif menu == "🖼️ Poster Lab":
    st.header("🖼️ AI Poster Lab")

    name = st.text_input("Leader / Brand Name", "आपका नाम")
    slogan = st.text_input("Hindi Slogan", "नया भारत, नई पहचान")
    prompt = st.text_area(
        "Background Prompt",
        "Professional political banner, cinematic lighting, orange gold theme, ultra HD"
    )

    if st.button("🎨 Generate Poster"):
        if not st.session_state.auth:
            auth_gate()
        else:
            with st.spinner("Generating AI Poster..."):
                url = f"https://image.pollinations.ai/prompt/{prompt.replace(' ','%20')}?width=1024&height=1024&nologo=true"
                img = requests.get(url).content
                st.image(img, use_container_width=True)
                st.download_button("📥 Download Poster", img, "vixan_poster.png")

# =========================================================
# 8. VOICE STUDIO
# =========================================================
elif menu == "🎙️ Voice Studio":
    st.header("🎙️ AI Voice Studio")

    text = st.text_area("Enter Script", "नमस्ते, Vixan AI में आपका स्वागत है।")
    speed = st.slider("Speech Speed", 0.5, 1.5, 1.0)

    if st.button("🎧 Generate Voice"):
        if not st.session_state.auth:
            auth_gate()
        else:
            with st.spinner("Synthesizing Voice..."):
                tts = gTTS(text=text, lang="hi", slow=(speed < 1))
                tts.save("voice.mp3")
                st.audio("voice.mp3")
                with open("voice.mp3","rb") as f:
                    st.download_button("📥 Download MP3", f, "vixan_voice.mp3")

# =========================================================
# 9. VIDEO AI
# =========================================================
elif menu == "🎞️ Video AI":
    st.header("🎞️ AI Video Engine")
    st.info("🚧 Talking Posters & Lip-Sync launching soon")

# =========================================================
# 10. ABOUT
# =========================================================
else:
    st.header("ℹ️ About Vixan AI")
    st.markdown("""
    **Vixan AI Pro** is a next-generation AI platform for:
    - Political Campaign Media
    - Business Promotions
    - AI Voice Announcements
    - Digital Creators
    """)

# =========================================================
# 11. FLOATING SUPPORT
# =========================================================
st.markdown("""
<div class="float-support">
<a href="https://wa.me/91XXXXXXXXXX" target="_blank">
<button style="background:#25D366;color:white;border:none;border-radius:30px;padding:12px;">
💬 WhatsApp Support
</button></a>
<a href="tel:+91XXXXXXXXXX">
<button style="background:#00d2ff;color:white;border:none;border-radius:30px;padding:12px;">
📞 Call Now
</button></a>
</div>
""", unsafe_allow_html=True)
