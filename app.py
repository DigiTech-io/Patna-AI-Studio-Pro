
import streamlit as st
import requests
import io
import time
import urllib.parse
from PIL import Image

# 1. Page Configuration & UI
st.set_page_config(page_title="Patna AI Studio Pro", layout="wide", page_icon="🏙️")

st.markdown("""
<style>
    .stApp { background-color: #ffffff !important; }
    .pro-box {
        background: #ffffff !important;
        border: 2px solid #007bff !important;
        border-radius: 15px !important;
        padding: 20px !important;
        margin-bottom: 20px !important;
        box-shadow: 0 4px 15px rgba(0,123,255,0.1) !important;
    }
    input, textarea, [data-baseweb="select"] {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 2px solid #0056b3 !important;
        font-weight: 600 !important;
    }
    h1, h2, h3, label, p { color: #1a365d !important; font-weight: 800 !important; }
    .stButton > button {
        background: linear-gradient(45deg, #007bff 0%, #0056b3 100%) !important;
        color: white !important; border-radius: 50px !important; font-weight: bold !important;
    }
    .price-tag { color: #28a745 !important; font-size: 1.2em; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# 2. Sidebar (Call & WhatsApp: 8210073056)
with st.sidebar:
    st.title("🏙️ Patna AI Pro")
    menu = st.radio("Navigation", ["🎨 Image Studio", "🎥 Video AI", "🚀 Grow Social", "📞 Support"])
    st.markdown("---")
    st.subheader("📞 Quick Support")
    st.markdown("[📱 WhatsApp Chat](https://wa.me/918210073056)")
    st.markdown("📞 **Call: +91 8210073056**")

# 3. FEATURE: SOCIAL MEDIA PANEL (Subscription & Followers)
if menu == "🚀 Grow Social":
    st.header("📈 Social Media Growth Panel")
    st.info("💡 Real & Active Followers/Subscribers for your brand!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="pro-box">', unsafe_allow_html=True)
        st.subheader("📸 Instagram Services")
        st.markdown("* **1K Real Followers**: ₹199")
        st.markdown("* **5K Premium Followers**: ₹899")
        st.markdown("**Condition:** 24-48 Hours Delivery | 30 Days Refill Guarantee")
        if st.button("Order Instagram Pack"):
            st.success("Redirecting to Admin (8210073056)...")
            time.sleep(1)
            st.markdown(f'<meta http-equiv="refresh" content="0;URL=\'https://wa.me/918210073056?text=I want Instagram Followers Pack\'" />', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="pro-box">', unsafe_allow_html=True)
        st.subheader("📺 YouTube Services")
        st.markdown("* **1K Subscribers**: ₹1499")
        st.markdown("* **4000h Watch Time**: ₹2999")
        st.markdown("**Condition:** Organic Method | Lifetime Support | No Drop")
        if st.button("Order YouTube Pack"):
            st.success("Redirecting to Admin (8210073056)...")
            time.sleep(1)
            st.markdown(f'<meta http-equiv="refresh" content="0;URL=\'https://wa.me/918210073056?text=I want YouTube Subscribers Pack\'" />', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# 4. FEATURE: IMAGE STUDIO (Dual Engine)
elif menu == "🎨 Image Studio":
    st.header("🎨 Ultra HD Image Studio")
    engine = st.selectbox("🚀 AI Engine", ["🆓 Pollinations (Free)", "💎 Segmind Pro (HQ)"])
    st.markdown('<div class="pro-box">', unsafe_allow_html=True)
    idea = st.text_input("💡 Idea (Hindi/English):")
    if st.button("🚀 Create Image"):
        with st.spinner("Creating..."):
            try:
                # Prompt Enhancement
                final_p = f"{idea}, ultra-realistic 8k, flux style"
                if "Segmind" in engine and "SEGMIND_API_KEY" in st.secrets:
                    res = requests.post("https://api.segmind.com/v1/flux-1-dev", 
                                        json={"prompt": final_p, "width": 1024, "height": 1024}, 
                                        headers={"x-api-key": st.secrets["SEGMIND_API_KEY"]})
                else:
                    res = requests.get(f"https://image.pollinations.ai/prompt/{urllib.parse.quote(final_p)}?nologo=true")
                st.image(res.content, use_container_width=True)
                st.download_button("💾 Save Art", res.content, "patna_ai.png", "image/png")
            except Exception as e: st.error(f"Error: {e}")
    st.markdown('</div>', unsafe_allow_html=True)

elif menu == "🎥 Video AI":
    st.header("🎬 Video Studio")
    st.info("Fast AI Animations are active!")

elif menu == "📞 Support":
    st.info("Owner: Chaman Jha | WhatsApp: +91 8210073056")

st.markdown("---")
st.markdown("<p style='text-align: center;'>✨ Patna AI Studio Pro v17.0 | Social Media & AI Hub | 8210073056</p>", unsafe_allow_html=True)
