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

# Page Config & CSS
st.set_page_config(page_title="Patna AI Studio Pro", layout="wide", page_icon="🏙️")

st.markdown("""
<style>
.stButton > button {
    width: 100%; border-radius: 25px; 
    background: linear-gradient(45deg, #FF4B2B, #FF416C);
    color: white; font-weight: bold; border: none; height: 3.5em;
    transition: 0.3s;
}
.stButton > button:hover { transform: scale(1.05); }
</style>
""", unsafe_allow_html=True)

# Logic Functions
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

# Session State
if 'counter' not in st.session_state: 
    st.session_state.counter = 0
if 'unlocked' not in st.session_state: 
    st.session_state.unlocked = False

# Sidebar - ✅ FIXED
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
    st.info("Bihar's #1 AI Platform 🚀
Patna Creators")  # ✅ Single line with 


# Main App Logic
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

    elif menu == "✂️ BG Remover":
        st.header("🪄 BG Remover")
        uploaded = st.file_uploader("Upload Image", type=['jpg','png'])
        if uploaded and st.button("✂️ Remove Background"):
            if "REMOVE_BG_KEY" not in st.secrets:
                st.error("❌ API Key Missing! Add REMOVE_BG_KEY in Secrets.toml")
            else:
                with st.spinner("🧹 Cleaning..."):
                    res = requests.post(
                        'https://api.remove.bg/v1.0/removebg',
                        files={'image_file': uploaded.getvalue()},
                        data={'size': 'auto'},
                        headers={'X-Api-Key': st.secrets["REMOVE_BG_KEY"]}
                    )
                    if res.status_code == 200:
                        st.image(res.content, caption="✅ Clean PNG")
                        st.download_button("💾 Download", res.content, "no_bg.png")
                    else: 
                        st.error("❌ API Error!")

    elif menu == "🎥 10s Video AI":
        st.header("🎬 AI Video Studio")
        if VIDEO_READY:
            st.success("✅ Replicate ready! Video feature coming soon.")
        else:
            st.warning("⚠️ `pip install replicate` for video generation")

    elif menu == "📞 Support":
        st.header("📱 Support & Contact")
        # ✅ FIXED Line 125: Separate st.info calls - No triple quotes issue
        st.info("WhatsApp: +91 7004332903")
        st.info("Email: chamanjha2015@gmail.com")
        st.success("⭐ Patna AI Studio Pro - Bihar's #1 AI Tool!")
        
else:
    st.error("🔒 PRO Unlock Required!")

# Footer
st.markdown("---")
st.markdown("*Made with ❤️ in Patna, Bihar | v3.0*")
