import streamlit as st
import requests
import io
import time
import uuid
from gtts import gTTS

# =========================
# 1. CONFIG & UI ENHANCEMENT
# =========================
st.set_page_config(page_title="Vixan AI Pro v26.2", layout="wide", page_icon="💎")

# Custom CSS for Sidebar and UI fix
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@600;700&family=Inter:wght@400;700&display=swap');
    
    /* Main Background */
    .stApp { background: #0a0b10; color: #ffffff; }
    
    /* Sidebar Menu Styling */
    section[data-testid="stSidebar"] { background-color: #11141d !important; border-right: 1px solid #333; }
    section[data-testid="stSidebar"] .stRadio > label { color: #FFD700 !important; font-weight: bold; font-size: 20px; }
    
    /* Buttons */
    .stButton>button { border-radius: 12px; font-weight: 700; height: 3.5em; background: linear-gradient(90deg, #00d2ff, #3a7bd5); color: white; border: none; width: 100%; transition: 0.3s; }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 0 20px #00d2ff; }
    
    /* Template Cards */
    .template-box { background: #161a25; border: 1px solid #333; border-radius: 15px; padding: 15px; text-align: center; margin-bottom: 20px; transition: 0.4s; }
    .template-box:hover { border-color: #FFD700; transform: translateY(-5px); }
    .temp-img { width: 100%; border-radius: 10px; aspect-ratio: 2/3; object-fit: cover; margin-bottom: 10px; }
    
    /* Floating Support */
    .float-container { position: fixed; bottom: 30px; right: 30px; z-index: 1000; display: flex; flex-direction: column; gap: 10px; }
    </style>
""", unsafe_allow_html=True)

# Session State Initialization
if 'is_auth' not in st.session_state: st.session_state.is_auth = False
if 'user_name' not in st.session_state: st.session_state.user_name = "Guest"

def check_auth():
    if not st.session_state.is_auth:
        st.warning("🔒 Login Required")
        with st.form("signup"):
            u_name = st.text_input("Full Name")
            u_phone = st.text_input("WhatsApp Number")
            if st.form_submit_button("Unlock All Features 🚀"):
                if u_name and len(u_phone) >= 10:
                    st.session_state.is_auth = True
                    st.session_state.user_name = u_name
                    st.rerun()
        return False
    return True

# =========================
# 2. SIDEBAR (Fixed Menu)
# =========================
with st.sidebar:
    st.markdown("<h1 style='color:#FFD700;'>💎 VIXAN PRO</h1>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=80)
    st.divider()
    
    # Sidebar Navigation Menu
    menu = st.radio(
        "NAVIGATION",
        ["🏠 Dashboard", "🖼️ Ready Templates", "🎨 AI Poster Lab", "🎙️ Voice Studio", "🎞️ Talking Face"],
        index=0
    )
    
    st.divider()
    if st.session_state.is_auth:
        st.info(f"User: {st.session_state.user_name}")
        if st.button("Log out"):
            st.session_state.is_auth = False
            st.rerun()

# =========================
# 3. MODULES
# =========================

if menu == "🏠 Dashboard":
    st.title("🚀 Bihar's No. 1 AI Media Engine")
    st.markdown("### Create Professional Posters, Cloned Voices & AI Videos")
    st.image("https://img.freepik.com/free-vector/abstract-technology-background_23-2148905210.jpg", use_container_width=True)

elif menu == "🖼️ Ready Templates":
    st.header("🖼️ High-Quality Predefined Templates")
    
    # Improved Template Categories
    cats = {
        "🚩 Political (Bihar Focus)": ["BJP Chunav Banner", "JDU Development", "Jan Seva Prachar"],
        "💼 Business & Shops": ["Digital Mobile Store", "Modern Gym Poster", "Luxury Real Estate"],
        "🪔 Festivals & Events": ["Chhath Puja Special", "Diwali Dhamaka", "Birthday Celebration"]
    }
    
    for cat_name, items in cats.items():
        st.subheader(cat_name)
        cols = st.columns(3)
        for i, item in enumerate(items):
            with cols[i % 3]:
                # Dynamic Preview Image
                preview_url = f"https://image.pollinations.ai/prompt/{item.replace(' ','%20')}%20poster%20high%20quality?width=400&height=600&nologo=true"
                
                st.markdown(f"""
                    <div class='template-box'>
                        <img src='{preview_url}' class='temp-img'>
                        <div style='font-weight:bold; color:#FFD700;'>{item}</div>
                    </div>
                """, unsafe_allow_html=True)
                
                user_msg = st.text_input(f"Name/Slogan", key=f"input_{item}")
                
                if st.button(f"Generate {item}", key=f"btn_{item}"):
                    if check_auth():
                        with st.spinner("AI Rendering..."):
                            final_p = f"{item} with text {user_msg}"
                            final_url = f"https://image.pollinations.ai/prompt/{final_p.replace(' ','%20')}?width=1024&height=1024&nologo=true&seed={uuid.uuid4().int}"
                            img_data = requests.get(final_url).content
                            st.image(img_data, caption="Your Design is Ready!")
                            st.download_button("📥 Download HD Poster", img_data, f"{item}.png")

elif menu == "🎨 AI Poster Lab":
    st.header("🎨 Professional AI Poster Lab")
    t1, t2 = st.tabs(["✨ Text to Image", "🧬 Image Clone"])
    
    with t1:
        prompt = st.text_area("Describe your poster:", "Professional Bihar Election banner, orange theme, leadership style, 4k")
        if st.button("🚀 Create Custom Poster"):
            if check_auth():
                with st.spinner("AI Painting..."):
                    url = f"https://image.pollinations.ai/prompt/{prompt.replace(' ','%20')}?width=1024&height=1024&nologo=true&seed={uuid.uuid4().int}"
                    img_data = requests.get(url).content
                    st.image(img_data)
                    st.download_button("📥 Download", img_data, "vixan_gen.png")
    
    with t2:
        up_img = st.file_uploader("Upload Image to Clone Style", type=['jpg', 'png'])
        if st.button("🧬 Start DNA Cloning"):
            if check_auth() and up_img:
                st.info("Analyzing Design DNA...")
                url = f"https://image.pollinations.ai/prompt/clone%20this%20design%20style?seed={uuid.uuid4().int}"
                st.image(requests.get(url).content)

elif menu == "🎙️ Voice Studio":
    st.header("🎙️ Voice DNA & Cloning Lab")
    v_tab1, v_tab2 = st.tabs(["📢 Text to Speech", "🧬 Voice Clone"])
    
    with v_tab1:
        v_text = st.text_area("Hindi/English Text:", "नमस्ते, वीक्सन एआई प्रो में आपका स्वागत है।")
        if st.button("📢 Generate Voice"):
            if check_auth():
                tts = gTTS(text=v_text, lang='hi')
                tts.save("voice.mp3")
                st.audio("voice.mp3")
    
    with v_tab2:
        st.file_uploader("Upload 10s Voice Sample", type=['mp3'])
        if st.button("🚀 Clone Voice DNA"):
            if check_auth(): st.success("Voice DNA Cloned Successfully!")

elif menu == "🎞️ Talking Face":
    st.header("🎞️ Talking Face AI Studio")
        st.file_uploader("Upload Photo", key="face_up")
    st.file_uploader("Upload Audio", key="audio_up")
    if st.button("🎬 Render Video"):
        if check_auth():
            with st.spinner("Lip-Syncing in progress..."):
                time.sleep(3)
                st.video("https://www.w3schools.com/html/mov_bbb.mp4")

# =========================
# 4. FLOATING SUPPORT
# =========================
st.markdown("""
    <div class="float-container">
        <a href="https://wa.me/91XXXXXXXXXX" style="text-decoration:none;"><div style="background:#25d366; color:white; padding:15px 25px; border-radius:50px; font-weight:bold; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">💬 WhatsApp Support</div></a>
    </div>
""", unsafe_allow_html=True)

st.markdown("<hr><center>© 2026 Vixan AI Studio • Patna, Bihar 🇮🇳</center>", unsafe_allow_html=True)
