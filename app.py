import streamlit as st
import requests
import io
from PIL import Image
import time
import urllib.parse

# Safely import replicate
try:
    import replicate
    VIDEO_READY = True
except ImportError:
    VIDEO_READY = False

# 1. Page Config
st.set_page_config(page_title="Patna AI Studio Pro", layout="wide", page_icon="🏙️")

# Attractive CSS
st.markdown("""
<style>
.stButton > button {
    width: 100%; border-radius: 25px; 
    background: linear-gradient(45deg, #FF4B2B, #FF416C);
    color: white; font-weight: bold; font-size: 16px;
    border: none; height: 3.5em; transition: 0.3s;
}
.stButton > button:hover { transform: scale(1.05); }
</style>
""", unsafe_allow_html=True)

# 2. Logic Functions
@st.cache_data(ttl=3600)
def translate_pro(text):
    try:
        encoded = urllib.parse.quote(text)
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=en&dt=t&q={encoded}"
        r = requests.get(url, timeout=15).json()
        eng = r[0][0][0]
        return f"{eng}, 8k, cinematic lighting, hyper-realistic, masterpiece, sharp focus"
    except:
        return f"{text}, 8k, masterpiece"

# 3. Session State
if 'counter' not in st.session_state: 
    st.session_state.counter = 0
if 'unlocked' not in st.session_state: 
    st.session_state.unlocked = False

# 4. Sidebar (FIXED - Line 72 Error Resolved)
with st.sidebar:
    st.title("🏙️ Patna AI Studio Pro")
    menu = st.radio("🚀 Features", ["🎨 Pro Image Gen", "✂️ BG Remover", "🎥 10s Video AI", "📞 Support"])
    st.markdown("---")
    st.metric("Free Trials", f"{st.session_state.counter}/5")
    
    if st.session_state.counter >= 5 and not st.session_state.unlocked:
        st.error("🔒 Trial Limit Reached")
        st.link_button("📺 YouTube Subscribe", "https://www.youtube.com/@mukundjha222")
        st.link_button("💙 Facebook Follow", "https://www.facebook.com/share/1Cr1P4ENWW/")
        if st.button("🔓 Unlock PRO"):
            st.session_state.unlocked = True
            st.rerun()
    
    st.markdown("---")
    # ✅ FIXED: Triple quotes multiline string
    st.info("""Bihar's #1 AI Platform 🚀
Patna Creators""")

# 5. Main App Logic
if st.session_state.counter < 5 or st.session_state.unlocked:
    if menu == "🎨 Pro Image Gen":
        st.header("✨ Cinematic 8K Image Studio")
        prompt = st.text_area("💡 Aapka Idea (Hindi/English):")
        ratio = st.selectbox("📐 Ratio", ["1:1 Square", "16:9 YouTube", "9:16 Reels"])
        dims = {"1:1 Square": (1024,1024), "16:9 YouTube": (1280,720), "9:16 Reels": (720,1280)}
        w, h = dims[ratio]

        if st.button("🚀 Generate 8K Masterpiece"):
            if prompt:
                with st.spinner("🎨 Creating..."):
                    pro = translate_pro(prompt)
                    encoded_p = urllib.parse.quote(pro)
                    img_url = f"https://image.pollinations.ai/prompt/{encoded_p}?width={w}&height={h}&nologo=true&seed={int(time.time())}"
                    res = requests.get(img_url, timeout=60)
                    img = Image.open(io.BytesIO(res.content))
                    st.image(img, use_container_width=True)
                    st.session_state.counter += 1
                    st.balloons()
                    st.success("✅ Image Generated! Trials left: 5 - " + str(st.session_state.counter))

    elif menu == "✂️ BG Remover":
        st.header("🪄 BG Remover")
        uploaded = st.file_uploader("Upload Image", type=['jpg','png'])
        if uploaded and st.button("✂️ Remove Background"):
            if "REMOVE_BG_KEY" not in st.secrets:
                st.error("❌ API Key Missing! Add REMOVE_BG_KEY in Secrets.toml")
                st.info("Get free API key: https://remove.bg/api")
            else:
                with st.spinner("🧹 Cleaning Background..."):
                    res = requests.post(
                        'https://api.remove.bg/v1.0/removebg',
                        files={'image_file': uploaded.getvalue()},
                        data={'size': 'auto'},
                        headers={'X-Api-Key': st.secrets["REMOVE_BG_KEY"]}
                    )
                    if res.status_code == 200:
                        st.image(res.content, caption="✅ Background Removed!")
                        st.download_button("💾 Download PNG", res.content, "clean_bg.png", "image/png")
                    else: 
                        st.error(f"❌ API Error: {res.status_code}")

    elif menu == "🎥 10s Video AI":
        st.header("🎬 AI Video Studio")
        if VIDEO_READY:
            st.info("✅ Replicate library detected! Video feature coming soon.")
            st.code("pip install replicate")
        else:
            st.warning("⚠️ Install: `pip install replicate` for video generation")
            st.info("Video feature setup ke liye 'replicate' library install karein.")

    elif menu == "📞 Support":
        st.header("📱 Support & Contact")
        col1, col2 = st.columns(2)
        with col1:
            st.info("**WhatsApp:**
+91 7004332903")
        with col2:
            st.info("**Email:**
chamanjha2015@gmail.com")
        st.markdown("---")
        st.success("⭐ Patna AI Studio Pro - Bihar's #1 AI Tool!")
        
else:
    st.error("🔒 PRO Unlock Required! Sidebar se unlock karein.")
    st.balloons()

# Footer
st.markdown("---")
st.markdown("*Made with ❤️ in Patna, Bihar | v2.0*")
