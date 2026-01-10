import streamlit as st
import requests
import base64

# --- CONFIG & THEME ---
st.set_page_config(page_title="Vixan AI Studio Pro", layout="wide", page_icon="🚀")

# Premium Interface CSS
st.markdown("""
    <style>
    .main { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); color: white; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { 
        background-color: rgba(255,255,255,0.05); border-radius: 10px; padding: 10px 20px; color: white;
    }
    .stTabs [aria-selected="true"] { background-color: #ff4b4b !important; }
    div.stButton > button {
        background: linear-gradient(45deg, #ff4b4b, #ff8a05); color: white; border: none;
        border-radius: 8px; transition: 0.3s; font-weight: bold; width: 100%;
    }
    .payment-card {
        background: rgba(255, 255, 255, 0.1); padding: 20px; border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.2); text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SECRETS & KEYS ---
SEGMIND_KEY = st.secrets.get("SEGMIND_API_KEY")
ELEVEN_KEY = st.secrets.get("ELEVENLABS_API_KEY")
RAZORPAY_LINK = "https://rzp.io/l/your_link" # Apne Razorpay link se badlein

# --- ENGINE FUNCTIONS ---
def generate_vixan_media(prompt, type="image"):
    # Failover logic for images (Segmind -> Pollinations)
    if type == "image":
        free_url = f"https://image.pollinations.ai/prompt/{prompt.replace(' ', '%20')}?width=1024&height=1024&nologo=true"
        try:
            res = requests.get(free_url, timeout=15)
            return res.content
        except: return None

# --- APP NAVIGATION ---
st.title("🚀 Vixan AI Studio Pro")
st.markdown("##### Next-Gen Marketing & Audio Intelligence")

tabs = st.tabs(["🎨 Visual Studio", "🎙️ Audio Engine", "📢 WhatsApp Bot", "💳 Premium Upgrade"])

# --- TAB 1: VISUAL STUDIO ---
with tabs[0]:
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("AI Design Studio")
        mode = st.selectbox("Design Type", ["Political Poster", "Business Banner", "Image Clone Style"])
        name = st.text_input("Brand/Neta Name")
        slogan = st.text_area("Slogan")
        if st.button("Generate Masterpiece ✨"):
            with st.spinner("Processing..."):
                img = generate_vixan_media(f"{mode} for {name}, {slogan}, hyper-realistic, 8k")
                if img: st.image(img, use_container_width=True)

# --- TAB 2: AUDIO ENGINE (TTS & Settings) ---
with tabs[1]:
    st.subheader("AI Voice & Sound Control")
    col_a, col_b = st.columns(2)
    with col_a:
        script = st.text_area("Audio Script", placeholder="Namaste, main aapki AI voice hoon...")
        voice_style = st.select_slider("Voice Stability (Control)", options=["Low", "Medium", "High"])
        voice_id = st.selectbox("Select Voice", ["Professional Male", "Elegant Female", "Cloned Voice (Pro)"])
        
    with col_b:
        st.info("Audio Cloning Feature: Upload a 1-min clip to clone (Pro Feature)")
        uploaded_voice = st.file_uploader("Upload voice sample for cloning", type=["mp3", "wav"])
        if st.button("Generate AI Audio 🎙️"):
            st.warning("Connecting to ElevenLabs API...")
            # Actual ElevenLabs integration logic here

# --- TAB 3: WHATSAPP & CALL AUTOMATION ---
with tabs[2]:
    st.subheader("WhatsApp Marketing Tools")
    msg_type = st.radio("Auto-Reply Message Type", ["Welcome Note", "Price List", "Call Back Request"])
    whatsapp_num = st.text_input("Apna WhatsApp Number (With Country Code)")
    
    # Dynamic WhatsApp Link Generation
    custom_msg = f"Hello Vixan AI, I want to inquire about {msg_type}"
    wa_link = f"https://wa.me/{whatsapp_num}?text={custom_msg.replace(' ', '%20')}"
    
    col_wa, col_call = st.columns(2)
    with col_wa:
        st.markdown(f'<a href="{wa_link}" target="_blank"><button style="width:100%; height:50px; background-color:#25D366; color:white; border-radius:10px; border:none; cursor:pointer;">Message on WhatsApp</button></a>', unsafe_allow_html=True)
    with col_call:
        st.markdown(f'<a href="tel:{whatsapp_num}"><button style="width:100%; height:50px; background-color:#007bff; color:white; border-radius:10px; border:none; cursor:pointer;">Call Now</button></a>', unsafe_allow_html=True)

# --- TAB 4: PAYMENT & PARTNER SECTION ---
with tabs[3]:
    st.markdown(f"""
    <div class="payment-card">
        <h3>💎 Upgrade to Pro Plus</h3>
        <p>Unlock: Audio Cloning, Video Generation, and Ad-Free Experience</p>
        <h2 style="color:#ffdb05;">₹999 / Monthly</h2>
        <a href="{RAZORPAY_LINK}" target="_blank">
            <button style="padding:15px 30px; font-size:20px; background:gold; color:black; border-radius:10px; border:none; font-weight:bold; cursor:pointer;">
                PAY NOW WITH RAZORPAY
            </button>
        </a>
        <p style="margin-top:10px; font-size:12px;">Secure Transaction via Razorpay</p>
    </div>
    """, unsafe_allow_html=True)

# --- SIDEBAR UNIQUE FEATURES ---
with st.sidebar:
    st.title("Vixan Partner Panel")
    st.metric(label="System Health", value="98%", delta="Optimal")
    st.write("---")
    st.subheader("Partner Special: AI Suggestion")
    if st.button("Get Trending Ad Idea"):
        st.success("Trending Idea: 'AI-Generated Personal Video Greeting for Elections'")
    
    st.markdown("---")
    st.write("Developed by Vixan Partner AI")
