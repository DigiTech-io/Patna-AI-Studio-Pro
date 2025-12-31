import streamlit as st
import requests
import io
from PIL import Image
import time
import urllib.parse

# 1. Page Configuration
st.set_page_config(page_title="Patna AI Studio Pro", layout="wide", page_icon="🏙️")

# 2. Neon Glassmorphism UI Design (Fixed)
st.markdown("""
<style>
    .main { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); color: white; }
    [data-testid="stSidebar"] { background-color: rgba(15, 23, 42, 0.95); border-right: 1px solid rgba(255, 255, 255, 0.1); }
    
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
        transition: 0.3s ease-in-out;
    }
    .stButton > button:hover { transform: scale(1.05); box-shadow: 0 6px 20px rgba(0, 242, 254, 0.6); }
    
    .stTextInput > div > div > input { 
        border-radius: 15px; 
        background: rgba(255,255,255,0.1); 
        color: white; 
        border: 1px solid #4facfe; 
    }
    .stTextArea > div > div > textarea {
        border-radius: 15px;
        background: rgba(255,255,255,0.1);
        color: white;
        border: 1px solid #4facfe;
    }
</style>
""", unsafe_allow_html=True)

# 3. Midjourney Prompt Magic Logic (Cached & Error-Proof)
@st.cache_data(ttl=3600)
def convert_to_mj_pro(text):
    try:
        encoded = urllib.parse.quote(text)
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=en&dt=t&q={encoded}"
        r = requests.get(url, timeout=10).json()
        eng = r[0][0][0]
        return f"{eng}, hyper-realistic, 8k resolution, cinematic lighting, shot on 35mm lens, f/1.8, unreal engine 5, octane render, photorealistic masterpiece, sharp focus, highly detailed texture"
    except Exception:
        return f"{text}, hyper-realistic, 8k, cinematic lighting, masterpiece"

# 4. Session State Management (Fixed)
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""
if 'magic_p' not in st.session_state:
    st.session_state.magic_p = ""

# 5. Sidebar (Signup, Credits & Support) - FIXED SCOPE
with st.sidebar:
    st.title("🏙️ Patna AI Pro")
    
    # User Signup Section
    if not st.session_state.user_name:
        st.subheader("👤 New Signup")
        name_input = st.text_input("Enter Your Name")
        if st.button("✅ Join Studio"):
            if name_input.strip():
                st.session_state.user_name = name_input.strip()
                st.rerun()
            else:
                st.error("Please enter your name!")
    else:
        st.success(f"👋 Namaste, {st.session_state.user_name}!")
        st.info("🪙 Credits: 10/10 (Free Plan)")
    
    st.markdown("---")
    menu = st.radio("🚀 Studio Features", ["🎨 Image Studio", "🎞️ Video AI", "📞 Support"])
    
    st.markdown("---")
    st.markdown("💬 **Instant Help**")
    st.link_button("📱 WhatsApp", "https://wa.me/917004332903")
    st.link_button("📞 Call Now", "tel:+917004332903")

# 6. Main Feature Logic - FIXED VARIABLE SCOPE
if 'menu' in locals():
    if menu == "🎨 Image Studio":
        st.header("✨ Magic Prompt & 8K Image Gen")
        
        # PHASE 1: MAGIC CONVERTER
        st.markdown('<div class="pro-box">', unsafe_allow_html=True)
        st.subheader("🪄 Step 1: Normal Text to Pro Prompt")
        user_idea = st.text_input(
            "Describe in Hindi/English:", 
            placeholder="Example: Ek Bihari ladka futuristic Patna mein...",
            key="user_idea"
        )
        
        if st.button("🪄 Convert to Midjourney Prompt", key="convert_btn"):
            if user_idea.strip():
                with st.spinner("🔮 Magic in progress..."):
                    st.session_state.magic_p = convert_to_mj_pro(user_idea)
                    st.success("✅ Your Midjourney Level Prompt is Ready!")
            else:
                st.error("Please enter some text first!")
        
        if st.session_state.magic_p:
            st.subheader("🔥 Copy Pro Prompt:")
            st.code(st.session_state.magic_p, language=None)
            st.info("✅ Copy this prompt or use it directly below!")
            if st.button("🔄 New Prompt", key="new_prompt"):
                st.session_state.magic_p = ""
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        # PHASE 2: IMAGE GENERATOR
        st.markdown('<div class="pro-box">', unsafe_allow_html=True)
        st.subheader("🖼️ Step 2: Generate & Download HD")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            final_prompt = st.text_area(
                "Final Prompt:", 
                value=st.session_state.magic_p, 
                height=100,
                key="final_prompt"
            )
        with col2:
            ratio = st.selectbox(
                "📐 Aspect Ratio", 
                ["1:1 (Square)", "9:16 (Reels)", "16:9 (YouTube)", "4:3 (Poster)"]
            )
            dims = {
                "1:1 (Square)": (1024,1024), 
                "9:16 (Reels)": (720,1280), 
                "16:9 (YouTube)": (1280,720), 
                "4:3 (Poster)": (1024,768)
            }
            w, h = dims[ratio]
            gen_btn = st.button("🚀 Generate 8K Art", key="gen_btn")

        if gen_btn and final_prompt.strip():
            with st.spinner("🎨 AI is painting your masterpiece... (30s)"):
                encoded_final = urllib.parse.quote(final_prompt)
                img_url = f"https://image.pollinations.ai/prompt/{encoded_final}?width={w}&height={h}&nologo=true&seed={int(time.time())}"
                
                try:
                    res = requests.get(img_url, timeout=45, stream=True)
                    if res.status_code == 200:
                        img = Image.open(io.BytesIO(res.content))
                        st.image(img, use_container_width=True)
                        st.download_button(
                            "💾 Download to Gallery", 
                            res.content, 
                            f"patna_ai_art_{int(time.time())}.png", 
                            "image/png"
                        )
                        st.balloons()
                        st.success("🎉 HD Image Generated Successfully!")
                    else:
                        st.error("❌ Generation failed. Try different prompt.")
                except Exception as e:
                    st.error(f"❌ Network error. Please retry. {str(e)[:50]}")
        elif gen_btn:
            st.error("❌ Please enter a prompt first!")
        st.markdown('</div>', unsafe_allow_html=True)

    elif menu == "🎞️ Video AI":
        st.header("🎬 AI Video Generation")
        st.info("🔥 SVD-XT Video Models - **Coming Soon for Patna Creators!**")
        st.markdown("""
        **✨ Upcoming Features:**
        • 10s HD Video from Text
        • Patna-style Reels 
        • YouTube Shorts
        **📱 Contact WhatsApp for Early Access!**
        """)

    elif menu == "📞 Support":
        st.header("📱 24/7 Local Support - Patna")
        col1, col2 = st.columns(2)
        with col1:
            st.info("**📍 Location**
Patna, Bihar")
            st.info("**💼 Services**
• Custom AI Apps
• YouTube Content
• Reels Editing")
        with col2:
            st.info("**📱 WhatsApp**
+91 7004332903")
            st.info("**✉️ Email**
chamanjha2015@gmail.com")
        st.success("💰 Recharge Credits via UPI - Contact Admin!")

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #4facfe;'>✨ Patna AI Studio Pro v6.1 | Bihar's First AI Business Hub 🚀</p>", 
    unsafe_allow_html=True
)
