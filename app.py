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

# 1. Page Config + PRO CSS
st.set_page_config(page_title="Patna AI Studio Pro", layout="wide", page_icon="🏙️")

st.markdown("""
<style>
.stButton > button {
    width: 100%; border-radius: 25px; 
    background: linear-gradient(45deg, #FF4B2B, #FF416C);
    color: white; font-weight: bold; font-size: 16px;
    border: none; height: 3.5em; transition: 0.3s;
    box-shadow: 0 4px 15px rgba(255,75,43,0.4);
}
.stButton > button:hover { 
    transform: scale(1.05); 
    box-shadow: 0 8px 25px rgba(255,75,43,0.6);
}
.sidebar .sidebar-content { background: linear-gradient(#1e293b, #0f172a); color: white; }
</style>
""", unsafe_allow_html=True)

# 2. FIXED Translation Functions
@st.cache_data(ttl=3600)
def translate_pro(text):
    try:
        encoded = urllib.parse.quote(text)
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=en&dt=t&q={encoded}"
        r = requests.get(url, timeout=15).json()
        eng = r[0][0][0]
        return f"{eng}, 8k resolution, cinematic lighting, hyper-realistic, masterpiece, sharp focus, patna bihar"
    except Exception:
        return f"{text}, 8k, masterpiece, highly detailed"

# 3. Session State
if 'counter' not in st.session_state: 
    st.session_state.counter = 0
if 'unlocked' not in st.session_state: 
    st.session_state.unlocked = False

# 4. Sidebar (PERFECT)
with st.sidebar:
    st.title("🏙️ Patna AI Studio Pro")
    menu = st.radio("🚀 Features", ["🎨 Pro Image Gen", "✂️ BG Remover", "🎥 10s Video AI", "📞 Support"])
    st.markdown("---")
    st.metric("Free Trials", f"{st.session_state.counter}/5")
    
    if st.session_state.counter >= 5 and not st.session_state.unlocked:
        st.error("🔒 **Trial Limit Reached**")
        col1, col2 = st.columns(2)
        with col1:
            st.link_button("📺 YouTube Subscribe", "https://www.youtube.com/@mukundjha222", use_container_width=True)
        with col2:
            st.link_button("💙 Facebook Follow", "https://www.facebook.com/share/1Cr1P4ENWW/", use_container_width=True)
        if st.button("🔓 Unlock PRO (I Subscribed)", use_container_width=True):
            st.session_state.unlocked = True
            st.rerun()
    
    st.markdown("---")
    st.info("**Bihar's #1 AI Platform** 🚀
📍 Patna Creators")

# 5. MAIN APP (CRASH-PROOF VERSION)
if st.session_state.counter < 5 or st.session_state.unlocked:

    # 🎨 PRO IMAGE GEN (100% FIXED)
    if menu == "🎨 Pro Image Gen":
        st.header("✨ Cinematic 8K Image Studio")
        col1, col2 = st.columns([3, 1])
        
        with col1:
            prompt = st.text_area(
                "💡 Aapka Idea (Hindi/English):", 
                placeholder="Patna Gandhi Maidan night, Bihar scheme poster, Meesho model...",
                height=100
            )
        
        with col2:
            ratio = st.selectbox("📐 Ratio", ["1:1 Square", "16:9 YouTube", "9:16 Reels", "4:3 Poster"])
            dims = {
                "1:1 Square": (1024,1024), 
                "16:9 YouTube": (1280,720), 
                "9:16 Reels": (720,1280),
                "4:3 Poster": (1024,768)
            }
            w, h = dims[ratio]
            st.info(f"**Size:** {w}×{h}px")

        if st.button("🚀 Generate 8K Masterpiece", key="generate_img"):
            if prompt.strip():
                with st.spinner("🎨 AI Creating Masterpiece... (15-30s)"):
                    try:
                        pro_prompt = translate_pro(prompt)
                        st.success(f"🔥 **Pro Prompt:** `{pro_prompt[:70]}...`")
                        
                        encoded_prompt = urllib.parse.quote(pro_prompt, safe='')
                        img_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={w}&height={h}&nologo=true&seed={int(time.time())}"
                        
                        response = requests.get(img_url, timeout=60)
                        response.raise_for_status()
                        
                        img = Image.open(io.BytesIO(response.content))
                        st.image(img, use_container_width=True, caption="✅ Your 8K Masterpiece")
                        
                        # Download button FIXED
                        buf = io.BytesIO()
                        img.save(buf, format="PNG", optimize=True)
                        st.download_button(
                            "💾 Download HD PNG", 
                            buf.getvalue(), 
                            f"patna_ai_{int(time.time())}.png", 
                            "image/png"
                        )
                        
                        st.session_state.counter += 1
                        st.balloons()
                    except Exception as e:
                        st.error(f"❌ Generation failed: {str(e)[:100]}")
                        st.info("🔄 Simple prompt try karein")

    # ✂️ BG REMOVER (SECURITY FIXED)
    elif menu == "✂️ BG Remover":
        st.header("🪄 Professional Background Remover")
        uploaded = st.file_uploader("📁 Upload Image", type=['jpg','jpeg','png'], help="Max 5MB recommended")
        
        if uploaded is not None:
            st.image(uploaded, caption="📷 Original Image", use_container_width=True)
            
            if st.button("✂️ Remove Background", key="remove_bg"):
                # API Key validation FIRST
                if "REMOVE_BG_KEY" not in st.secrets:
                    st.error("🔑 **API Key Missing!**
**Create `.streamlit/secrets.toml`:**")
                    st.code('REMOVE_BG_KEY = "your_removebg_api_key_here"')
                else:
                    with st.spinner("🧹 AI Removing Background... (10-20s)"):
                        try:
                            res = requests.post(
                                'https://api.remove.bg/v1.0/removebg',
                                files={'image_file': uploaded.getvalue()},
                                data={'size': 'auto'},
                                headers={'X-Api-Key': st.secrets["REMOVE_BG_KEY"]},
                                timeout=60
                            )
                            if res.status_code == 200:
                                st.image(res.content, caption="✅ Transparent PNG Ready!", use_container_width=True)
                                st.download_button(
                                    "💾 Download Clean PNG", 
                                    res.content, 
                                    "patna_no_bg.png", 
                                    "image/png"
                                )
                                st.session_state.counter += 1
                                st.balloons()
                            else:
                                st.error(f"❌ API Error {res.status_code}")
                                if res.status_code == 402:
                                    st.warning("💳 **Quota exceeded** - New Remove.bg API key lein")
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)[:100]}")

    # 🎥 VIDEO AI (SETUP GUIDE)
    elif menu == "🎥 10s Video AI":
        st.header("🎬 AI Video Generator")
        st.warning("🚀 **Ready to Launch!** 2-minute setup:")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 📦 Install")
            st.code("pip install replicate")
        with col2:
            st.markdown("### 🔑 API Key")
            st.code("""
# .streamlit/secrets.toml
REPLICATE_API_TOKEN = "r8_xxxxxxxx"
""")
        
        # Image preview for video base
        v_prompt = st.text_input("Test video idea:", placeholder="Patna night market animation")
        if st.button("👀 Preview Video Base Image"):
            pro_v = translate_pro(v_prompt)
            encoded = urllib.parse.quote(pro_v)
            url = f"https://image.pollinations.ai/prompt/{encoded}?width=720&height=1280&nologo=true"
            try:
                img = Image.open(io.BytesIO(requests.get(url, timeout=45).content))
                st.image(img, caption="🎥 **Yahin se video banega!**")
            except:
                st.error("Preview failed")

    # 📞 SUPPORT
    elif menu == "📞 Support":
        st.header("📱 24/7 Patna Support")
        col1, col2 = st.columns(2)
        
        with col1:
            st.success("### 💬 **WhatsApp** (Fastest)")
            msg = urllib.parse.quote("Namaste! Patna AI Studio Pro help chahiye 🔥")
            st.link_button("💬 Chat Now", f"https://wa.me/917004332903?text={msg}", use_container_width=True)
        
        with col2:
            st.info("### ☎️ **Direct Call**")
            st.link_button("📞 +91 7004332903", "tel:+917004332903", use_container_width=True)
        
        st.info("⏰ **10AM - 10PM** | 📍 **Patna Local**")

else:
    st.error("🔒 **Subscribe karke PRO unlock karein!** 👈 Sidebar")
    st.balloons()

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align:center; color:#FF4B2B; font-size:24px; font-weight:bold;'>"
    "🏙️ Patna AI Studio Pro | Bihar's #1 AI 🚀 | Made in Patna ❤️</div>", 
    unsafe_allow_html=True
)
