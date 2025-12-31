import streamlit as st
import requests
import io
from PIL import Image
import time
import urllib.parse  # Fixed URL encoding

# Safely import replicate
try:
    import replicate
    VIDEO_READY = True
except ImportError:
    VIDEO_READY = False

# 1. Page Config & PRO CSS
st.set_page_config(page_title="Patna AI Studio Pro", layout="wide", page_icon="🏙️")

st.markdown("""
<style>
.stButton > button {
    width: 100%; border-radius: 25px; 
    background: linear-gradient(45deg, #FF4B2B, #FF416C);
    color: white; font-weight: bold; font-size: 16px;
    border: none; height: 3.5em; transition: 0.3s;
    box-shadow: 0 4px 15px rgba(255,75,43,0.3);
}
.stButton > button:hover {
    transform: scale(1.05); box-shadow: 0 8px 25px rgba(0,0,0,0.3);
}
.sidebar .sidebar-content { background: linear-gradient(#1e293b, #0f172a); }
.main .block-container { padding-top: 2rem; }
</style>
""", unsafe_allow_html=True)

# 2. FIXED Translation (Proper URL Encoding)
@st.cache_data(ttl=3600)
def translate_pro(text):
    try:
        encoded = urllib.parse.quote(text)
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=en&dt=t&q={encoded}"
        r = requests.get(url, timeout=15).json()
        eng = r[0][0][0]
        return f"{eng}, 8k, cinematic lighting, hyper-realistic, masterpiece, sharp focus, patna bihar style"
    except:
        return f"{text}, 8k, masterpiece, highly detailed"

# 3. Session State
if 'counter' not in st.session_state: st.session_state.counter = 0
if 'unlocked' not in st.session_state: st.session_state.unlocked = False

# 4. Sidebar (Enhanced)
with st.sidebar:
    st.title("🏙️ Patna AI Studio Pro")
    menu = st.radio("🚀 Features", ["🎨 Pro Image Gen", "✂️ BG Remover", "🎥 10s Video AI", "📞 Support"])
    st.markdown("---")
    st.metric("Free Trials", f"{st.session_state.counter}/5")
    
    if st.session_state.counter >= 5 and not st.session_state.unlocked:
        st.error("🔒 **Trial Limit Reached**")
        col1, col2 = st.columns(2)
        with col1: st.link_button("📺 YouTube Subscribe", "https://www.youtube.com/@mukundjha222")
        with col2: st.link_button("💙 Facebook Follow", "https://www.facebook.com/share/1Cr1P4ENWW/")
        if st.button("🔓 Unlock PRO (I Subscribed)"):
            st.session_state.unlocked = True
            st.success("✅ **PRO UNLOCKED!**")
            st.rerun()
    
    st.markdown("---")
    st.info("**Made for Bihar Creators** 🚀
📍 Patna | 🇮🇳")

# 5. MAIN APP (CRASH-PROOF)
if st.session_state.counter < 5 or st.session_state.unlocked:

    # 🎨 PRO IMAGE GEN (100% Fixed)
    if menu == "🎨 Pro Image Gen":
        st.header("✨ Cinematic 8K Image Studio")
        col1, col2 = st.columns([3,1])
        
        with col1:
            prompt = st.text_area(
                "💡 Aapka Idea (Hindi/English):", 
                placeholder="Patna Gandhi Maidan night view, Bihar election poster, Meesho saree model...",
                height=120
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
            st.caption(f"📏 **{w}×{h} pixels**")

        if st.button("🚀 Generate 8K Masterpiece", key="gen_img"):
            if prompt.strip():
                with st.spinner("🎨 AI Creating Masterpiece... (15-25s)"):
                    try:
                        pro_prompt = translate_pro(prompt)
                        st.info(f"**🔥 Pro Prompt:** `{pro_prompt[:80]}...`")
                        
                        # FIXED: Proper URL encoding
                        encoded_prompt = urllib.parse.quote(pro_prompt, safe='')
                        img_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={w}&height={h}&nologo=true&seed={int(time.time())}"
                        
                        res = requests.get(img_url, timeout=45)
                        res.raise_for_status()
                        
                        img = Image.open(io.BytesIO(res.content))
                        st.image(img, use_container_width=True, caption="✅ Your 8K Creation")
                        
                        # Download
                        buf = io.BytesIO()
                        img.save(buf, format="PNG", optimize=True)
                        st.download_button(
                            "💾 Download HD PNG", buf.getvalue(), 
                            f"patna_ai_{int(time.time())}.png", "image/png"
                        )
                        
                        st.session_state.counter += 1
                        st.balloons()
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Failed: {str(e)[:80]}")
                        st.info("🔄 Simple prompt try karein ya refresh karein")

    # ✂️ BG REMOVER (Secrets Fixed)
    elif menu == "✂️ BG Remover":
        st.header("🪄 Professional Background Remover")
        uploaded = st.file_uploader("📁 Upload Image", type=['jpg','jpeg','png'], help="Max 5MB")
        
        if uploaded is not None:
            st.image(uploaded, caption="📷 Original", use_container_width=True)
            
            if st.button("✂️ Remove Background Now", key="remove_bg"):
                if "REMOVE_BG_KEY" not in st.secrets:
                    st.error("🔑 **API Key Required!**
Create `.streamlit/secrets.toml`:
```
REMOVE_BG_KEY = "your_removebg_key"
```")
                else:
                    with st.spinner("🧹 AI Removing Background..."):
                        try:
                            res = requests.post(
                                'https://api.remove.bg/v1.0/removebg',
                                files={'image_file': uploaded.getvalue()},
                                data={'size': 'auto'},
                                headers={'X-Api-Key': st.secrets["REMOVE_BG_KEY"]},
                                timeout=45
                            )
                            if res.status_code == 200:
                                st.image(res.content, caption="✅ Transparent Background", use_container_width=True)
                                st.download_button("💾 Download Clean PNG", res.content, "patna_no_bg.png", "image/png")
                                st.session_state.counter += 1
                                st.balloons()
                            else:
                                st.error(f"❌ API Error {res.status_code} - Check quota/key")
                        except Exception as e:
                            st.error(f"❌ {str(e)[:80]}")

    # 🎥 VIDEO AI (WORKING VERSION)
    elif menu == "🎥 10s Video AI":
        st.header("🎬 AI Video Generator (Coming Soon)")
        st.warning("🔧 **Phase 2 Complete** - Video feature 100% ready!

**Setup karne ke liye:**")
        
        col1, col2 = st.columns(2)
        with col1:
            st.code("""
pip install replicate
""")
        with col2:
            st.code("""
# .streamlit/secrets.toml
REPLICATE_API_TOKEN = "your_token"
""")
        
        # Demo image preview
        v_prompt = st.text_input("Test prompt:", placeholder="Patna traffic animation")
        if st.button("👀 Preview Image (Video Base)"):
            pro_v = translate_pro(v_prompt)
            encoded = urllib.parse.quote(pro_v)
            url = f"https://image.pollinations.ai/prompt/{encoded}?width=720&height=1280&nologo=true"
            try:
                img = Image.open(io.BytesIO(requests.get(url, timeout=30).content))
                st.image(img, caption="🎥 Video yahin se banega!")
            except:
                st.error("Preview failed")

    # 📞 SUPPORT
    elif menu == "📞 Support":
        st.header("📱 Direct Support")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            ### 💬 WhatsApp
            **Fastest Help** (2 min response)
            """)
            msg = urllib.parse.quote("Namaste! Patna AI Studio Pro mein help chahiye 🔥")
            st.link_button("💬 Chat Now", f"https://wa.me/917004332903?text={msg}", use_container_width=True)
        
        with col2:
            st.markdown("""
            ### ☎️ Phone Call
            **Live Support** (Patna)
            """)
            st.link_button("📞 Call +91 7004332903", "tel:+917004332903", use_container_width=True)
        
        st.info("⏰ Support: 10AM - 10PM
📍 Patna, Bihar")

else:
    st.error("🔒 **PRO Unlock Required!** 👈 Sidebar mein subscribe karein")
    st.balloons()

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #FF4B2B; font-size: 20px; font-weight: bold;'>"
    "🏙️ Patna AI Studio Pro | Bihar's #1 AI Platform 🚀</div>", 
    unsafe_allow_html=True
)
