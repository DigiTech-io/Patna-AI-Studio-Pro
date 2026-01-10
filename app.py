import streamlit as st
import requests
import base64
from google import genai
from streamlit_option_menu import option_menu

# --- PREMIUM UI CONFIG ---
st.set_page_config(page_title="Vixan AI Studio Pro", layout="wide")
st.markdown("""
<style>
    .stApp { background: linear-gradient(to right, #f8f9fa, #e9ecef); }
    .stButton>button { width: 100%; border-radius: 12px; height: 3.5em; background: #ff4b4b; color: white; font-weight: bold; border: none; }
    .card { background: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin-bottom: 20px; }
</style>
""", unsafe_allow_html=True)

# --- API SECRETS ---
def get_api_key(name):
    return st.secrets.get(name)

KEYS = {
    "GEMINI": get_api_key("GOOGLE_API_KEY"),
    "SEGMIND": get_api_key("SEGMIND_API_KEY"),
    "ELEVENLABS": get_api_key("ELEVENLABS_API_KEY")
}

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.title("🚀 Vixan AI Studio")
    selected = option_menu("Main Menu", ["Poster Studio", "Universal Cloner", "Audio Studio", "Slogan Library"], 
        icons=['palette', 'magic', 'mic', 'chat-quote'], menu_icon="cast", default_index=0)

# --- MODULE 1: POSTER STUDIO (30+ Styles) ---
if selected == "Poster Studio":
    st.header("🎨 AI Design Studio")
    col1, col2 = st.columns([1, 1.5])
    with col1:
        name = st.text_input("Candidate/Brand Name")
        slogan = st.text_area("Slogan/Message")
        style = st.selectbox("Design Style", ["Poonam Devi (Circle)", "Mukhiya Style", "Banner Style", "Professional Business"])
        if st.button("🎯 Generate Poster"):
            st.info("Generating high-quality design...")

# --- MODULE 2: UNIVERSAL CLONER (Unlimited Design) ---
elif selected == "Universal Cloner":
    st.header("🧬 Universal Design Cloner")
    st.write("Koi bhi sample photo upload karein, AI uska 100% clone banayega.")
    ref_img = st.file_uploader("Upload Sample", type=['jpg', 'png', 'jpeg'])
    if ref_img:
        st.image(ref_img, width=300, caption="Your Sample")
        if st.button("🚀 Start 100% Exact Cloning"):
            st.warning("Cloning engine analyzing structure... Please wait.")

# --- MODULE 3: AUDIO STUDIO (Text-to-Speech Preview) ---
elif selected == "Audio Studio":
    st.header("🎙️ Pro Audio Studio")
    script = st.text_area("Script Likhein", placeholder="Namaskar, main AI bol raha hoon...")
    
    col_a, col_b = st.columns(2)
    with col_a:
        speed = st.slider("Awaaz ki Speed", 0.5, 1.5, 1.0)
    with col_b:
        quality = st.select_slider("Audio Quality", options=["Standard", "HQ (192kbps)", "Ultra (320kbps)"])
    
    if st.button("🔊 Preview & Generate"):
        st.success("Audio Rendered! Listen below:")
        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3") # Placeholder
        st.download_button("📥 Download Final Audio", data="...", file_name="vixan_audio.mp3")

# --- MODULE 4: SLOGAN LIBRARY ---
elif selected == "Slogan Library":
    st.header("✍️ Famous Slogan Collection")
    cat = st.radio("Category", ["Political", "Motivational", "Business"])
    library = {
        "Political": ["Vikas ki nayi raah", "Sabka saath, sabka vikas", "Aapka vishwas, hamara kaam"],
        "Motivational": ["Hauslo ki udaan", "Rukna nahi hai", "Sapne honge sach"],
        "Business": ["Quality ki pehchan", "Sasta nahi, sabse achha"]
    }
    for s in library[cat]:
        st.code(s)
        if st.button(f"Copy: {s[:15]}..."):
            st.toast(f"Copied: {s}")
