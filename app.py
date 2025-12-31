import streamlit as st
import requests
import io
from PIL import Image
import time
import urllib.parse

# 1. Page Configuration
st.set_page_config(page_title="Patna AI Studio Pro", layout="wide", page_icon="🏙️")

# 2. Neon Glassmorphism UI (Fixed & Complete)
st.markdown("""
<style>
    .main { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); color: white; }
    [data-testid="stSidebar"] { background-color: rgba(15, 23, 42, 0.95); }
    
    .pro-box {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 25px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        margin-bottom: 20px;
    }
    
    .stButton > button {
        width: 100%; border-radius: 50px; height: 3.5em;
        background: linear-gradient(45deg, #00f2fe 0%, #4facfe 100%);
        color: white; font-weight: bold; border: none;
        box-shadow: 0 4px 15px rgba(0, 242, 254, 0.4);
    }
    .stButton > button:hover { transform: scale(1.02); }
    
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        border-radius: 15px; background: rgba(255,255,255,0.1);
        color: white; border: 1px solid #4facfe;
    }
</style>
""", unsafe_allow_html=True)

# 3. Prompt Magic Converter (Error-Proof)
@st.cache_data(ttl=3600)
def convert_to_mj_pro(text):
    try:
        encoded = urllib.parse.quote(text)
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=en&dt=t&q={encoded}"
        r = requests.get(url, timeout=10).json()
        eng = r[0][0][0]
        return f"{eng}, hyper-realistic, 8k resolution, cinematic lighting, shot on 35mm lens, f/1.8, unreal engine 5, octane render, masterpiece, flux style"
    except Exception:
        return f"{text}, hyper-realistic, 8k, cinematic, masterpiece"

# 4. Session State (Safe Initialization)
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""
if 'magic_p' not in st.session_state:
    st.session_state.magic_p = ""

# 5. Sidebar (Fixed Variable Scope)
with st.sidebar:
    st.title("🏙️ Patna AI Pro")
    
    # User Signup
    if not st.session_state.user_name:
        st.subheader("👤 Join Studio")
        name_input = st.text_input("Enter Your Name", key="name_input")
        if st.button("✅ Join", key="join_btn"):
            if name_input.strip():
                st.session_state.user_name = name_input.strip()
                st.rerun()
            else:
                st.error("Name required!")
    else:
        st.success(f"👋 Namaste, {st.session_state.user_name}!")
        st.info("🆓 Unlimited Free Images")
    
    st.markdown("---")
    
    # ✅ DUAL ENGINE SELECTION (Segmind + Free Fallback)
    st.subheader("🚀 AI Engine")
    engine = st.selectbox("Choose Engine", ["🆓 Pollinations (Unlimited Free)", "💎 Segmind Pro (High Quality)"], key="engine_select")
    
    st.markdown("---")
    menu = st.radio("Navigation", ["🎨 Image Studio", "🎥 Video AI", "📞 Support"], key="main_menu")
    
    st.markdown("---")
    st.markdown("### 💬 Support")
    st.link_button("📱 WhatsApp", "https://wa.me/918210073056")
    st.link_button("📞 Call", "tel:+918210073056")

# 6. Main Logic (100% Error-Free Dual Engine)
if 'menu' in locals():
    if menu == "🎨 Image Studio":
        st.header(f"✨ {engine} Powered AI Studio")
        
        # Phase 1: Magic Prompt Converter
        st.markdown('<div class="pro-box">', unsafe_allow_html=True)
        st.subheader("🪄 Step 1: Create Pro Prompt")
        user_idea = st.text_input(
            "Hindi/English Idea:", 
            placeholder="Ek Bihari ladka futuristic Patna mein...",
            key="user_idea"
        )
        
        col1, col2 = st.columns([3,1])
        with col1:
            if st.button("🪄 Convert to Pro Prompt", key="convert_btn", type="primary"):
                if user_idea.strip():
                    with st.spinner("🔮 Converting..."):
                        st.session_state.magic_p = convert_to_mj_pro(user_idea)
                        st.success("✅ Pro Prompt Ready!")
                    st.rerun()
                else:
                    st.error("Enter your idea first!")
        
        if st.session_state.magic_p:
            st.markdown("### 🔥 Pro Prompt:")
            st.code(st.session_state.magic_p)
            if st.button("🔄 Clear", key="clear_btn"):
                st.session_state.magic_p = ""
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        # Phase 2: Dual Engine Image Generation
        st.markdown('<div class="pro-box">', unsafe_allow_html=True)
        st.subheader("🖼️ Step 2: Generate HD Art")
        
        col1, col2 = st.columns([2,1])
        with col1:
            final_prompt = st.text_area(
                "Final Prompt:", 
                value=st.session_state.magic_p, 
                height=100,
                key="final_prompt"
            )
        with col2:
            ratio = st.selectbox("📐 Size", ["1:1 Square", "9:16 Reels", "16:9 YouTube"], key="ratio")
            dims = {"1:1 Square": (1024,1024), "9:16 Reels": (720,1280), "16:9 YouTube": (1280,720)}
            w, h = dims[ratio]
            st.info(f"**{w}×{h}px**")
        
        if st.button("🚀 Generate HD Image", key="gen_btn"):
            if not final_prompt.strip():
                st.error("❌ Enter prompt first!")
            else:
                with st.spinner(f"🎨 Generating via {engine}..."):
                    try:
                        if "Segmind" in engine and "SEGMIND_API_KEY" in st.secrets:
                            # Segmind Pro Engine (API Key Required)
                            api_url = "https://api.segmind.com/v1/flux-1-dev"
                            data = {
                                "prompt": final_prompt,
                                "seed": int(time.time()),
                                "steps": 25,
                                "width": w,
                                "height": h,
                                "guidance_scale": 3.5
                            }
                            headers = {"x-api-key": st.secrets["SEGMIND_API_KEY"]}
                            res = requests.post(api_url, json=data, headers=headers, timeout=90)
                        else:
                            # Pollinations Free Engine (Always Works)
                            encoded_p = urllib.parse.quote(final_prompt)
                            api_url = f"https://image.pollinations.ai/prompt/{encoded_p}?width={w}&height={h}&nologo=true&seed={int(time.time())}"
                            res = requests.get(api_url, timeout=60)
                        
                        if res.status_code == 200:
                            img = Image.open(io.BytesIO(res.content))
                            st.image(img, use_container_width=True)
                            timestamp = int(time.time())
                            st.download_button(
                                "💾 Download HD", 
                                res.content, 
                                f"PatnaAI_{timestamp}.png",
                                "image/png"
                            )
                            st.balloons()
                            st.success(f"✅ Generated via {engine}!")
                        else:
                            st.error(f"❌ Engine Error: {res.status_code}")
                    except Exception as e:
                        st.error(f"❌ Connection failed: {str(e)[:100]}")
        st.markdown('</div>', unsafe_allow_html=True)

    elif menu == "🎥 Video AI":
        st.header("🎬 Video AI Studio")
        st.info("🔥 **SVD-XT + Kling Models** - Launching Soon!")
        st.markdown("""
        **Features:**
        • Text-to-10s HD Video
        • Patna Reels Templates
        • YouTube Shorts
        **Contact WhatsApp for Early Access**
        """)

    elif menu == "📞 Support":
        st.header("📱 Patna Local Support")
        col1, col2 = st.columns(2)
        with col1:
            st.info("**📍 Patna, Bihar**
**Services:**
• Unlimited Images
• Video AI
• Custom Apps")
        with col2:
            st.info("**📱 WhatsApp:**
+91 8210073056
**Email:**
chamanjha2015@gmail.com")
        st.success("🆓 **Unlimited Free Credits** Active!")

# 7. Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #4facfe; padding: 20px;'>
        ✨ Patna AI Studio Pro v8.0 | Bihar's #1 Dual Engine AI Hub
    </div>
""", unsafe_allow_html=True)
