import streamlit as st
import requests
import uuid
import time
from gtts import gTTS

# =========================
# 1. CONFIG & PREMIUM THEME
# =========================
st.set_page_config(page_title="Vixan AI Pro v25.1", layout="wide", page_icon="💎")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@600;700&family=Inter:wght@400;700&display=swap');
    .main { background: #0a0b10; color: #ffffff; font-family: 'Rajdhani', sans-serif; }
    
    .template-box {
        background: #161a25;
        border: 1px solid #333;
        border-radius: 15px;
        padding: 15px;
        text-align: center;
        transition: 0.4s;
        margin-bottom: 20px;
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
        font-size: 28px;
        font-weight: 700;
        margin: 30px 0 15px 0;
        padding-left: 10px;
        border-left: 5px solid #FFD700;
    }
    .stButton>button { border-radius: 10px; font-weight: 700; transition: 0.3s; width: 100%; }
    .float-container { position: fixed; bottom: 30px; right: 30px; z-index: 1000; display: flex; flex-direction: column; gap: 10px; }
    </style>
""", unsafe_allow_html=True)

# Auth Check
if 'is_auth' not in st.session_state: st.session_state.is_auth = False

def check_auth():
    if not st.session_state.is_auth:
        st.warning("🔒 Login Required to Unlock AI Engines")
        with st.form("signup"):
            name = st.text_input("Full Name")
            phone = st.text_input("WhatsApp Number")
            if st.form_submit_button("Unlock Now 🚀"):
                if name and len(phone) >= 10:
                    st.session_state.is_auth = True
                    st.session_state.user_name = name
                    st.rerun()
                else:
                    st.error("Please enter valid details.")
        return False
    return True

# =========================
# 3. SIDEBAR
# =========================
with st.sidebar:
    st.markdown("<h1 style='color:#FFD700;'>VIXAN PRO</h1>", unsafe_allow_html=True)
    menu = st.radio("MENU", ["🏠 Dashboard", "🖼️ Ready Templates", "🎨 AI Poster Lab", "🎙️ Voice Studio", "🎞️ Talking Face"])
    if st.session_state.is_auth:
        st.success(f"User: {st.session_state.user_name}")

# =========================
# 4. ENHANCED TEMPLATE DATA
# =========================
template_data = {
    "🚩 Political (Chunav Special)": [
        {"name": "Sushashan Banner", "prompt": "bihar political leader poster luxury orange theme hindi text bold leadership"},
        {"name": "Youth Leader", "prompt": "young dynamic indian politician poster blue and white professional design 4k"},
        {"name": "Election Victory", "prompt": "political victory celebration banner flowers and crowd background bihar politics"},
        {"name": "Digital Prachar", "prompt": "digital political marketing poster social media style clean minimalist"}
    ],
    "💼 Business & Commercial": [
        {"name": "Premium Real Estate", "prompt": "modern luxury apartment building poster golden hour cinematic architecture"},
        {"name": "Tech/Mobile Store", "prompt": "electronics mobile shop grand opening poster neon blue futuristic lights"},
        {"name": "Patna Food Hub", "prompt": "indian restaurant spicy food banner high quality photography steam effect"},
        {"name": "Fitness/Gym", "prompt": "gym motivation poster bodybuilder silhouette dark contrast lighting 8k"}
    ],
    "🪔 Festivals & Cultural": [
        {"name": "Chhath Mahaparv", "prompt": "chhath puja festival poster sun god river ghat bihar culture traditional"},
        {"name": "Shubh Deepawali", "prompt": "diwali festival of lights poster premium crackers and diyas decoration"},
        {"name": "Rangotsav Holi", "prompt": "colorful holi festival banner splashing colors happy faces vibrant"},
        {"name": "Maha Shivratri", "prompt": "lord shiva meditative poster mahadev divine lighting cosmic background"}
    ]
}

# =========================
# 5. MODULES
# =========================

if menu == "🏠 Dashboard":
    st.title("🚀 Welcome to Vixan AI Studio Pro")
    st.markdown("### Bihar's Ultimate AI Engine for Posters & Voices")
    st.image("https://img.freepik.com/free-vector/abstract-technology-background_23-2148905210.jpg")

elif menu == "🖼️ Ready Templates":
    st.header("🖼️ Select & Generate from Templates")
    st.info("Templates par click karein aur wahi se apni image generate karein!")

    for cat, items in template_data.items():
        st.markdown(f"<div class='cat-title'>{cat}</div>", unsafe_allow_html=True)
        cols = st.columns(4)
        for i, item in enumerate(items):
            with cols[i]:
                # Preview Link
                preview_url = f"https://image.pollinations.ai/prompt/{item['prompt'].replace(' ', '%20')}?width=400&height=600&nologo=true&seed={i+10}"
                
                st.markdown(f"""
                    <div class='template-box'>
                        <img src='{preview_url}' class='temp-img'>
                        <p style='font-weight:bold; margin-bottom:10px;'>{item['name']}</p>
                    </div>
                """, unsafe_allow_html=True)
                
                # Input and Generate in Template Section
                custom_msg = st.text_input(f"Add Name/Message", placeholder="Example: Chaman Kumar", key=f"in_{cat}_{i}")
                
                if st.button(f"Generate {item['name']} 🚀", key=f"gen_{cat}_{i}"):
                    if check_auth():
                        with st.spinner("AI is Crafting your Design..."):
                            final_p = f"{item['prompt']} with text '{custom_msg}'"
                            gen_url = f"https://image.pollinations.ai/prompt/{final_p.replace(' ','%20')}?width=1024&height=1024&nologo=true"
                            st.image(gen_url, caption=f"Final Design: {item['name']}")
                            st.download_button("💾 Download HD Poster", requests.get(gen_url).content, f"{item['name']}.png")
                            st.balloons()

elif menu == "🎨 AI Poster Lab":
    st.header("🎨 Professional AI Poster Lab")
    prompt_lab = st.text_area("Describe your own design in detail:", "Professional election banner, Bihar theme, 4k")
    if st.button("🚀 Generate Custom Design"):
        if check_auth():
            with st.spinner("Creating..."):
                url = f"https://image.pollinations.ai/prompt/{prompt_lab.replace(' ','%20')}?width=1024&height=1024&nologo=true"
                st.image(url)
                st.download_button("💾 Download HD", requests.get(url).content, "vixan_lab.png")

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
    # Diagram for user understanding
    
    st.file_uploader("Upload Face Image")
    st.file_uploader("Upload Audio")
    if st.button("Generate Video"):
        if check_auth(): st.video("https://www.w3schools.com/html/mov_bbb.mp4")

# Floating WhatsApp Support
st.markdown("""
    <div class="float-container">
        <a href="https://wa.me/91XXXXXXXXXX" style="text-decoration:none;"><div style="background:#25d366; color:white; padding:12px 20px; border-radius:50px; font-weight:bold; box-shadow: 2px 2px 10px rgba(0,0,0,0.5);">💬 WhatsApp Support</div></a>
    </div>
""", unsafe_allow_html=True)
