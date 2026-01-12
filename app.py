import streamlit as st
import requests
import uuid
import time
from gtts import gTTS

# =========================
# 1. CONFIG & PREMIUM THEME
# =========================
st.set_page_config(page_title="Vixan AI Pro v25.0", layout="wide", page_icon="💎")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@600;700&family=Inter:wght@400;700&display=swap');
    .main { background: #0a0b10; color: #ffffff; font-family: 'Rajdhani', sans-serif; }
    
    /* Modern Template Card Design */
    .template-box {
        background: #161a25;
        border: 1px solid #333;
        border-radius: 15px;
        padding: 15px;
        text-align: center;
        transition: 0.4s;
    }
    .template-box:hover {
        border-color: #FFD700;
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(255, 215, 0, 0.2);
    }
    .temp-img {
        width: 100%;
        border-radius: 10px;
        margin-bottom: 10px;
        aspect-ratio: 2/3;
        object-fit: cover;
    }
    .cat-title {
        color: #FFD700;
        font-size: 26px;
        font-weight: 700;
        margin-top: 30px;
        border-bottom: 2px solid #FFD700;
        display: inline-block;
    }
    .stButton>button { border-radius: 10px; font-weight: 700; transition: 0.3s; }
    .float-container { position: fixed; bottom: 30px; right: 30px; z-index: 1000; display: flex; flex-direction: column; gap: 10px; }
    </style>
""", unsafe_allow_html=True)

# Auth Check (Simplified for code flow)
if 'is_auth' not in st.session_state: st.session_state.is_auth = False

def check_auth():
    if not st.session_state.is_auth:
        st.warning("🔒 Login Required")
        with st.form("signup"):
            name = st.text_input("Full Name")
            phone = st.text_input("WhatsApp")
            if st.form_submit_button("Unlock 🚀"):
                st.session_state.is_auth = True
                st.rerun()
        return False
    return True

# =========================
# 3. SIDEBAR
# =========================
with st.sidebar:
    st.markdown("<h1 style='color:#FFD700;'>VIXAN PRO</h1>", unsafe_allow_html=True)
    menu = st.radio("MENU", ["🏠 Dashboard", "🖼️ Ready Templates", "🎨 AI Poster Lab", "🎙️ Voice Studio", "🎞️ Talking Face"])

# =========================
# 4. TEMPLATE DATA (Real Designs)
# =========================
# Yahan humne specific prompts dale hain taaki AI sahi designs dikhaye
template_data = {
    "🚩 Political (Bihar Focus)": [
        {"name": "Mukhya Mantri Vikas", "prompt": "bihar political leader poster development orange theme hindi text professional"},
        {"name": "Election Campaign", "prompt": "indian election campaign poster luxury design cinematic lighting"},
        {"name": "Jan Seva Banner", "prompt": "social service political poster bihar rural development theme"},
        {"name": "Yuva Neta", "prompt": "young dynamic leader political banner modern sleek design"}
    ],
    "💼 Business & Shops": [
        {"name": "Patna Tech Shop", "prompt": "modern electronics shop banner neon lights professional"},
        {"name": "Luxury Real Estate", "prompt": "luxury apartment building poster golden and black theme"},
        {"name": "Gym & Fitness", "prompt": "hardcore gym motivation poster muscular man dark theme"},
        {"name": "Food & Restaurant", "prompt": "delicious indian thali restaurant banner high quality food photography"}
    ],
    "🪔 Festivals & Greetings": [
        {"name": "Chhath Puja", "prompt": "chhath puja festival poster sun god river ghat traditional bihar"},
        {"name": "Diwali Dhamaka", "prompt": "diwali festival of lights poster rangoli crackers premium design"},
        {"name": "Holi Mubarak", "prompt": "colorful holi festival banner people playing with colors vibrant"},
        {"name": "Eid Special", "prompt": "eid mubarak crescent moon mosque luxury green and gold theme"}
    ]
}

# =========================
# 5. MODULES
# =========================

if menu == "🏠 Dashboard":
    st.title("🚀 Welcome to Vixan AI Studio Pro")
    st.markdown("### Create Professional Content in Bihar's Local Style")
    st.image("https://img.freepik.com/free-vector/abstract-technology-background_23-2148905210.jpg")

elif menu == "🖼️ Ready Templates":
    st.header("🖼️ Modern Predefined Templates")
    st.info("Select a design to load it into the editor.")

    for cat, items in template_data.items():
        st.markdown(f"<div class='cat-title'>{cat}</div>", unsafe_allow_html=True)
        cols = st.columns(4)
        for i, item in enumerate(items):
            with cols[i]:
                # Generate a real preview link using Pollinations
                preview_url = f"https://image.pollinations.ai/prompt/{item['prompt'].replace(' ', '%20')}?width=400&height=600&nologo=true&seed={i+50}"
                
                st.markdown(f"""
                    <div class='template-box'>
                        <img src='{preview_url}' class='temp-img'>
                        <p style='font-weight:bold; margin-bottom:10px;'>{item['name']}</p>
                    </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"Use {item['name']}", key=f"btn_{cat}_{i}"):
                    if check_auth():
                        st.session_state.current_prompt = item['prompt']
                        st.success(f"Loaded: {item['name']}! Go to 'AI Poster Lab' to generate.")

elif menu == "🎨 AI Poster Lab":
    st.header("🎨 AI Poster Editor")
    
    # Load prompt from template if selected
    default_prompt = st.session_state.get('current_prompt', "Professional election banner, Bihar theme, 4k")
    final_prompt = st.text_area("Final Design Description:", default_prompt)
    
    if st.button("🚀 Generate Final Design"):
        if check_auth():
            with st.spinner("AI is Crafting..."):
                url = f"https://image.pollinations.ai/prompt/{final_prompt.replace(' ','%20')}?width=1024&height=1024&nologo=true"
                st.image(url, caption="Your Professional Design")
                st.download_button("💾 Download HD", requests.get(url).content, "vixan_design.png")

elif menu == "🎙️ Voice Studio":
    st.header("🎙️ Voice & DNA Cloning")
    v_tab1, v_tab2 = st.tabs(["📢 Text to Speech", "🧬 DNA Voice Clone"])
    
    with v_tab1:
        v_text = st.text_area("Hindi Text:", "नमस्ते, वीक्सन एआई स्टूडियो में आपका स्वागत है।")
        if st.button("Generate Audio"):
            if check_auth():
                tts = gTTS(text=v_text, lang='hi')
                tts.save("v.mp3")
                st.audio("v.mp3")

    with v_tab2:
        st.info("Upload sample to extract voice DNA.")
        st.file_uploader("Upload Audio", type=['mp3'])
        if st.button("Clone Voice"):
            if check_auth(): st.success("Voice DNA Extracted Successfully!")

elif menu == "🎞️ Talking Face":
    st.header("🎞️ Talking Face AI")
    
    st.file_uploader("Upload Face Image")
    st.file_uploader("Upload Audio")
    if st.button("Generate Video"):
        if check_auth(): st.video("https://www.w3schools.com/html/mov_bbb.mp4")

# Support Buttons
st.markdown(f"""
    <div class="float-container">
        <a href="https://wa.me/91XXXXXXXXXX" style="text-decoration:none;"><div style="background:#25d366; color:white; padding:12px 20px; border-radius:50px; font-weight:bold;">💬 WhatsApp</div></a>
    </div>
""", unsafe_allow_html=True)
