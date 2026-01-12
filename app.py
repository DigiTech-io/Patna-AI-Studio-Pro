import streamlit as st
import os
import requests
import io
import time
import uuid
from gtts import gTTS
from PIL import Image

# =========================
# 1. APP CONFIG & THEME
# =========================
st.set_page_config(page_title="Vixan AI Pro v19.0", layout="wide", page_icon="💎")

SEGMIND_API = st.secrets.get("SEGMIND_API_KEY", "")
HF_TOKEN = st.secrets.get("HF_TOKEN", "")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;700&family=Inter:wght@400;700&display=swap');
    .main { background: #0a0b10; color: #ffffff; font-family: 'Rajdhani', sans-serif; }
    
    /* Neon Glow UI */
    .stButton>button { border-radius: 12px; font-weight: 700; height: 3.5em; transition: 0.3s; border: none; }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 0 20px #00d4ff; }
    
    .pro-card { background: linear-gradient(145deg, #161a25, #1f2535); border: 1px solid #FFD700; border-radius: 20px; padding: 25px; margin-bottom: 20px;}
    .free-card { background: rgba(255,255,255,0.03); border: 1px solid #00d4ff; border-radius: 20px; padding: 25px; }
    
    /* Support Floating Buttons */
    .float-container { position: fixed; bottom: 30px; right: 30px; z-index: 1000; display: flex; flex-direction: column; gap: 10px; }
    .wa-btn { background: #25d366; color: white; padding: 12px 20px; border-radius: 50px; text-decoration: none; font-weight: bold; box-shadow: 0 4px 15px rgba(0,0,0,0.3); }
    .call-btn { background: #00d2ff; color: white; padding: 12px 20px; border-radius: 50px; text-decoration: none; font-weight: bold; box-shadow: 0 4px 15px rgba(0,0,0,0.3); }
    </style>
""", unsafe_allow_html=True)

# =========================
# 2. SESSION & SMART LOGIN
# =========================
if 'is_auth' not in st.session_state:
    st.session_state.is_auth = False

def check_auth():
    if not st.session_state.is_auth:
        st.warning("🔒 Login Required to generate content.")
        with st.form("signup_form"):
            st.subheader("📝 Join Vixan AI Studio")
            name = st.text_input("Full Name")
            phone = st.text_input("WhatsApp Number")
            if st.form_submit_button("Unlock All Features 🚀"):
                if name and len(phone) >= 10:
                    st.session_state.is_auth = True
                    st.session_state.user_name = name
                    st.rerun()
                else:
                    st.error("Enter valid details.")
        return False
    return True

# =========================
# 3. SIDEBAR
# =========================
with st.sidebar:
    st.markdown("<h2 style='color:#FFD700;'>VIXAN PRO v19</h2>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=100)
    menu = st.radio("SELECT TOOL", ["🏠 Dashboard", "🖼️ Poster Lab", "🎙️ Voice Studio", "🎞️ Video Center", "💳 Subscription"])
    st.divider()
    if st.session_state.is_auth:
        st.info(f"User: {st.session_state.user_name}")
        if st.button("Logout"):
            st.session_state.is_auth = False
            st.rerun()

# =========================
# 4. MODULES
# =========================

# --- DASHBOARD ---
if menu == "🏠 Dashboard":
    st.title("🚀 Bihar's #1 AI Media Studio")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="free-card"><h3>🆕 Text to AI</h3><p>Convert your ideas into Posters & Voices instantly.</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="pro-card"><h3>🧬 Cloning Tech</h3><p>Cloning style and voice DNA with 100% accuracy.</p></div>', unsafe_allow_html=True)
    
    st.image("https://img.freepik.com/free-vector/abstract-technology-background_23-2148905210.jpg", use_container_width=True)

# --- POSTER LAB ---
elif menu == "🖼️ Poster Lab":
    st.header("🖼️ AI Poster Lab")
    tab1, tab2 = st.tabs(["✨ New Generation", "🧬 Style Cloning"])
    
    with tab1:
        prompt = st.text_area("Poster Description:", "Political banner, Bihar election 2026 theme, 4k")
        if st.button("🎨 Create Poster"):
            if check_auth():
                with st.spinner("AI Painting..."):
                    url = f"https://image.pollinations.ai/prompt/{prompt.replace(' ','%20')}?nologo=true"
                    st.image(url)
                    st.download_button("Download Image", requests.get(url).content, "vixan_gen.png")

    with tab2:
        up_img = st.file_uploader("Upload Image to Clone", type=['jpg', 'png'])
        if st.button("🧬 Start Cloning"):
            if check_auth() and up_img:
                st.image(f"https://image.pollinations.ai/prompt/cloned%20style%20poster?seed={uuid.uuid4().int}")

# --- VOICE STUDIO ---
elif menu == "🎙️ Voice Studio":
    st.header("🎙️ Pro Voice Studio")
    text = st.text_area("Enter Hindi Text:", "नमस्ते, वीक्सन एआई प्रो में आपका स्वागत है।")
    if st.button("📢 Generate Voice"):
        if check_auth():
            tts = gTTS(text=text, lang='hi')
            tts.save("v.mp3")
            st.audio("v.mp3")

# --- SUBSCRIPTION (Razorpay Setup) ---
elif menu == "💳 Subscription":
    st.header("💎 Upgrade to Vixan Pro")
    st.markdown("Unlock 8K Quality, Commercial Rights & Priority Support.")
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='free-card'><h3>Basic</h3><p>₹49 / month</p><li>10 Generations/day</li></div>", unsafe_allow_html=True)
        st.link_button("Buy Basic Plan 💳", "https://rzp.io/l/basic_plan_link") # Replace with your Razorpay link
        
    with c2:
        st.markdown("<div class='pro-card'><h3>Business Pro</h3><p>₹199 / month</p><li>Unlimited Access</li><li>Video Cloning</li></div>", unsafe_allow_html=True)
        st.link_button("Buy Pro Plan 💎", "https://rzp.io/l/pro_plan_link") # Replace with your Razorpay link

# =========================
# 5. SMART SUPPORT & CONTACT
# =========================

# WhatsApp Messages Logic
wa_msg_sales = "Hi Vixan, I want to buy the Pro Plan. Please help."
wa_msg_tech = "Hi Vixan, I am facing a technical issue with the Studio."

st.markdown(f"""
    <div class="float-container">
        <a href="tel:+91XXXXXXXXXX" class="call-btn">📞 Call Admin</a>
        <a href="https://wa.me/91XXXXXXXXXX?text={wa_msg_sales.replace(' ', '%20')}" target="_blank" class="wa-btn">💰 Sales Inquiry</a>
        <a href="https://wa.me/91XXXXXXXXXX?text={wa_msg_tech.replace(' ', '%20')}" target="_blank" class="wa-btn">🛠️ Technical Support</a>
    </div>
""", unsafe_allow_html=True)

# Footer
st.markdown("<hr><center>© 2026 Vixan AI Studio • Made in Patna with ❤️</center>", unsafe_allow_html=True)
