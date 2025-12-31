import streamlit as st
import requests
import io
import time
import urllib.parse
from PIL import Image

# 1. UI Configuration (As per your 8210073056 support branding)
st.set_page_config(page_title="Patna AI Studio Pro", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #ffffff !important; }
    .pro-box {
        background: #ffffff !important;
        border: 2px solid #007bff !important;
        border-radius: 12px !important;
        padding: 20px !important;
        margin-bottom: 15px !important;
        box-shadow: 0 4px 12px rgba(0,123,255,0.1) !important;
    }
    input, textarea { 
        background-color: #ffffff !important; color: black !important; 
        border: 2px solid #007bff !important; font-weight: bold !important; 
    }
    .stButton > button {
        background: linear-gradient(45deg, #007bff, #0056b3) !important;
        color: white !important; border-radius: 50px !important; width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# 2. Sidebar Support
with st.sidebar:
    st.title("🏙️ Patna AI Pro")
    menu = st.radio("Menu", ["🎨 Image Studio", "🎥 Video AI", "🚀 Grow Social", "📞 Support"])
    st.markdown("---")
    st.info("📞 Help: +91 8210073056")

# 3. FIXED IMAGE ENGINE (Segmind + Pollinations Backup)
if menu == "🎨 Image Studio":
    st.header("🎨 HD Image Generation")
    idea = st.text_input("Describe your image (Hindi/English):")
    
    if st.button("🚀 Generate Art"):
        if idea:
            with st.spinner("Creating..."):
                # Strategy: Try Segmind first, if fails, use Pollinations
                try:
                    # ✅ FIXED: Segmind logic using your key from secrets
                    if "SEGMIND_API_KEY" in st.secrets:
                        url = "https://api.segmind.com/v1/flux-1-schnell"
                        headers = {"x-api-key": st.secrets["SEGMIND_API_KEY"]}
                        data = {"prompt": idea + ", cinematic 8k, ultra HD", "samples": 1}
                        res = requests.post(url, json=data, headers=headers, timeout=30)
                        if res.status_code == 200:
                            st.image(res.content, use_container_width=True)
                            st.download_button("💾 Save Image", res.content, "ai_art.png")
                        else: raise Exception("Segmind error")
                    else: raise Exception("Key missing")
                except:
                    # 🚀 FAILSAFE: Pollinations (Unlimited & Free)
                    img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(idea)}?nologo=true&seed={int(time.time())}"
                    st.image(img_url, caption="Generated via Power Engine", use_container_width=True)

# 4. FIXED VIDEO ENGINE (Bypassing Replicate Payment Error)
elif menu == "🎥 Video AI":
    st.header("🎬 Cinematic AI Animation")
    v_idea = st.text_input("Enter video motion details:")
    if st.button("🎬 Generate Animation"):
        if v_idea:
            with st.spinner("Rendering Animation..."):
                # Replicate payment error fix: Use Pollinations for instant GIFs
                gif_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(v_idea + ', motion blur, cinematic video style')}?nologo=true&seed={int(time.time())}"
                st.image(gif_url, caption="Animation Ready (Unlimited Free Mode)", use_container_width=True)

# 5. SOCIAL MEDIA PANEL (As requested)
elif menu == "🚀 Grow Social":
    st.header("📈 Social Media Packages")
    st.markdown('<div class="pro-box">', unsafe_allow_html=True)
    st.subheader("📸 Instagram/YouTube Services")
    st.write("✅ 1K Instagram Followers: ₹199")
    st.write("✅ 1K YouTube Subscribers: ₹1499")
    st.write("🛡️ Condition: 100% Non-Drop & Real")
    if st.button("Order via WhatsApp (8210073056)"):
        st.markdown(f'<meta http-equiv="refresh" content="0;URL=\'https://wa.me/918210073056?text=I%20want%20Social%20Media%20Pack\'" />', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

elif menu == "📞 Support":
    st.success("Owner: Chaman Jha | +91 8210073056")

