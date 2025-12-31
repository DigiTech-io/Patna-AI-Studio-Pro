import streamlit as st
import requests
import io
from PIL import Image
import time
import urllib.parse

# 1. Page Configuration
st.set_page_config(page_title="Patna AI Studio Pro", layout="wide", page_icon="🏙️")

# 2. PERFECT VISIBILITY UI (Light Mode Optimized - Crystal Clear)
st.markdown("""
<style>
    /* Crystal Clear White Background */
    .stApp { 
        background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%) !important; 
    }
    
    /* Sidebar - Clean Professional */
    section[data-testid="stSidebar"] {
        background: linear-gradient(135deg, #ffffff 0%, #f1f3f4 100%) !important;
        border-right: 1px solid #e0e0e0 !important;
    }
    
    /* PERFECT Content Boxes - High Visibility */
    .pro-box {
        background: #ffffff !important;
        border: 2px solid #007bff !important;
        border-radius: 20px !important;
        padding: 25px !important;
        margin-bottom: 25px !important;
        box-shadow: 0 8px 25px rgba(0,123,255,0.15) !important;
    }
    
    /* INPUTS - Ultra Clear Black Text on White */
    input, textarea, [data-baseweb="select"] {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 2px solid #007bff !important;
        border-radius: 12px !important;
        font-size: 16px !important;
        font-weight: 500 !important;
        padding: 12px !important;
    }
    
    /* TEXT VISIBILITY - Deep Blue Bold */
    h1, h2, h3, h4, label, p {
        color: #1a365d !important;
        font-weight: 700 !important;
    }
    
    /* PREMIUM BUTTONS - Professional Blue */
    .stButton > button {
        background: linear-gradient(45deg, #007bff 0%, #0056b3 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 50px !important;
        height: 50px !important;
        font-size: 16px !important;
        font-weight: 700 !important;
        box-shadow: 0 6px 20px rgba(0,123,255,0.3) !important;
        transition: all 0.3s !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(0,123,255,0.4) !important;
    }
    
    /* Info/Success Boxes */
    .stInfo, .stSuccess {
        background-color: #e3f2fd !important;
        border: 1px solid #2196f3 !important;
        border-radius: 10px !important;
        color: #1565c0 !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. Hindi-to-Pro Prompt Magic
@st.cache_data(ttl=3600)
def pro_prompt_gen(text):
    try:
        encoded = urllib.parse.quote(text)
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=en&dt=t&q={encoded}"
        r = requests.get(url, timeout=10).json()
        eng = r[0][0][0]
        return f"{eng}, ultra-realistic 8k, cinematic lighting, masterpiece, sharp focus, highly detailed, professional photography, flux style"
    except:
        return f"{text}, 8k, masterpiece, ultra-realistic"

# 4. Session State
if 'pro_prompt' not in st.session_state: 
    st.session_state.pro_prompt = ""
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""

# 5. Sidebar (Clean & Professional)
with st.sidebar:
    st.title("🏙️ Patna AI Pro")
    st.markdown("---")
    
    # User Greeting
    if st.session_state.user_name:
        st.success(f"👋 Namaste {st.session_state.user_name}!")
    else:
        name = st.text_input("Your Name", key="name_input")
        if st.button("✅ Join Studio", key="join_btn"):
            if name.strip():
                st.session_state.user_name = name.strip()
                st.rerun()
    
    st.markdown("---")
    st.subheader("🚀 AI Engine")
    engine = st.selectbox("Choose Engine", ["🆓 Pollinations (Unlimited Free)", "💎 Segmind Pro (High Quality)"], key="engine")
    
    st.markdown("---")
    menu = st.radio("📋 Navigation", ["🎨 Image Studio", "🎥 Video AI", "📞 Support"], key="main_menu")
    
    st.markdown("---")
    st.markdown("### 📞 **Quick Support**")
    st.markdown("**[WhatsApp Chat](https://wa.me/918210073056)**")
    st.markdown("**📞 Call: +91 8210073056**")

# 6. Main Application Logic (CRYSTAL CLEAR)
if menu == "🎨 Image Studio":
    st.markdown('<div class="pro-box">', unsafe_allow_html=True)
    st.header("🪄 **Step 1: Hindi → Ultra Pro Prompt**")
    
    idea = st.text_input(
        "💡 Apna idea Hindi/English mein:", 
        placeholder="Example: Ek sher Patna zoo mein roaring...",
        key="idea_input"
    )
    
    col1, col2 = st.columns([3,1])
    with col1:
        if st.button("🪄 **Generate Pro Prompt**", key="prompt_btn"):
            if idea.strip():
                with st.spinner("🔮 AI enhancing your idea..."):
                    st.session_state.pro_prompt = pro_prompt_gen(idea)
                    st.success("✅ **Ultra HD Prompt Ready!**")
                    st.rerun()
            else:
                st.error("❌ Idea enter karein!")
    
    if st.session_state.pro_prompt:
        st.markdown("### 🔥 **Your Professional Prompt:**")
        st.code(st.session_state.pro_prompt)
        if st.button("🔄 **New Prompt**", key="clear_btn"):
            st.session_state.pro_prompt = ""
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.pro_prompt:
        st.markdown('<div class="pro-box">', unsafe_allow_html=True)
        st.header("🖼️ **Step 2: Generate 8K HD Art**")
        
        col1, col2 = st.columns([2,1])
        with col1:
            final_prompt = st.text_area(
                "✍️ **Final Prompt** (Edit kar sakte hain):", 
                value=st.session_state.pro_prompt, 
                height=120,
                key="final_prompt"
            )
        
        with col2:
            ratio = st.selectbox("📐 **Image Size**", ["1:1 Square", "9:16 Reels", "16:9 YouTube"], key="ratio")
            dims = {"1:1 Square": (1024,1024), "9:16 Reels": (720,1280), "16:9 YouTube": (1280,720)}
            w, h = dims[ratio]
            st.info(f"**Resolution: {w}×{h}px**")
        
        if st.button("🚀 **Generate HD Masterpiece**", key="generate_btn"):
            if final_prompt.strip():
                with st.spinner(f"🎨 Creating via {engine} (25s)..."):
                    try:
                        if "Segmind" in engine and "SEGMIND_API_KEY" in st.secrets:
                            # Segmind Pro API
                            api_url = "https://api.segmind.com/v1/flux-1-dev"
                            data = {
                                "prompt": final_prompt,
                                "seed": int(time.time()),
                                "steps": 25,
                                "width": w,
                                "height": h
                            }
                            headers = {"x-api-key": st.secrets["SEGMIND_API_KEY"]}
                            res = requests.post(api_url, json=data, headers=headers, timeout=90)
                        else:
                            # Pollinations FREE (Always Works)
                            encoded_p = urllib.parse.quote(final_prompt)
                            api_url = f"https://image.pollinations.ai/prompt/{encoded_p}?width={w}&height={h}&nologo=true&seed={int(time.time())}"
                            res = requests.get(api_url, timeout=60)
                        
                        if res.status_code == 200:
                            img = Image.open(io.BytesIO(res.content))
                            st.image(img, use_container_width=True)
                            timestamp = int(time.time())
                            st.download_button(
                                "💾 **Download HD Art**", 
                                res.content, 
                                f"PatnaAI_{timestamp}.png",
                                "image/png"
                            )
                            st.balloons()
                            st.success("🎉 **8K HD Image Ready!**")
                        else:
                            st.error("❌ Engine busy! Free engine try karein.")
                    except Exception as e:
                        st.error(f"❌ Network issue: {str(e)[:80]}")
            else:
                st.error("❌ Prompt enter karein!")
        st.markdown('</div>', unsafe_allow_html=True)

elif menu == "🎥 Video AI":
    st.markdown('<div class="pro-box">', unsafe_allow_html=True)
    st.header("🎬 **Video AI Studio**")
    st.info("🔥 **SVD-XT + Kling Models** - Launching January 2026!")
    st.markdown("""
    **✨ Features:**
    • Text-to-10s HD Video
    • Patna Reels Templates
    • YouTube Shorts (60s)
    **📱 WhatsApp for Early Access**
    """)
    st.markdown('</div>', unsafe_allow_html=True)

elif menu == "📞 Support":
    st.markdown('<div class="pro-box">', unsafe_allow_html=True)
    st.header("📱 **24/7 Patna Support**")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("""
        **📍 Location**
        Patna, Bihar
        
        **💼 Services**
        • Unlimited AI Images
        • Video Generation
        • Custom Apps
        • YouTube Content
        """)
    
    with col2:
        st.success("""
        **📱 WhatsApp**
        +91 8210073056
        
        **✉️ Email**
        chamanjha2015@gmail.com
        """)
    
    st.markdown("---")
    st.success("🆓 **Unlimited FREE Credits Active!**")
    st.markdown('</div>', unsafe_allow_html=True)

# 7. Professional Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 20px; background: #f8f9fa; border-radius: 15px; margin: 20px;'>
    <h3 style='color: #007bff; margin: 0;'>✨ Patna AI Studio Pro v12.0</h3>
    <p style='color: #1a365d; font-size: 16px; margin: 5px 0;'>
        Bihar's #1 FREE AI Platform | <a href='https://wa.me/918210073056' style='color: #007bff; text-decoration: none;'>WhatsApp: 8210073056</a>
    </p>
</div>
""", unsafe_allow_html=True)
