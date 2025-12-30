import streamlit as st
import requests
import io
from PIL import Image
import time
import replicate # Secrets check: OK

# 1. Page Configuration
st.set_page_config(page_title="Patna AI Studio Pro", layout="wide", page_icon="🏙️")

# 2. Hindi to Pro English Logic
def translate_pro(text):
    try:
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=en&dt=t&q={text}"
        r = requests.get(url, timeout=10)
        eng = r.json()[0][0][0]
        return f"{eng}, 8k resolution, cinematic lighting, masterpiece, highly detailed"
    except:
        return f"{text}, high quality, 4k"

# 3. Session State for Trials
if 'counter' not in st.session_state:
    st.session_state.counter = 0
if 'unlocked' not in st.session_state:
    st.session_state.unlocked = False

# 4. Sidebar Navigation
with st.sidebar:
    st.title("🏙️ Patna AI Studio Pro")
    menu = st.radio("🛠️ Full Features", ["🎨 Image Gen", "✂️ BG Remove", "🎥 Video"])
    st.markdown("---")
    st.metric("Daily Trials", f"{st.session_state.counter}/5")
    
    if st.session_state.counter >= 5 and not st.session_state.unlocked:
        st.error("🚫 Limit Reached!")
        st.link_button("📺 YouTube", "https://www.youtube.com/@mukundjha222")
        if st.button("🔓 Unlock Pro"):
            st.session_state.unlocked = True
            st.rerun()

# 5. Main Logic Gate
if st.session_state.counter < 5 or st.session_state.unlocked:
    
    # --- 🎨 IMAGE GENERATOR ---
    if menu == "🎨 Image Gen":
        st.header("✨ AI Image Generator")
        col1, col2 = st.columns([3,1])
        with col1:
            prompt = st.text_area("Hindi/English:", placeholder="Patna Junction ki cinematic photo...")
        with col2:
            aspect = st.selectbox("Ratio", ["1:1", "16:9 (YouTube)", "9:16 (Reels)"])
            sizes = {"1:1": (1024,1024), "16:9 (YouTube)": (1280,720), "9:16 (Reels)": (720,1280)}
            w,h = sizes[aspect]
        
        if st.button("🚀 Generate", type="primary", use_container_width=True):
            if prompt:
                with st.spinner("🧠 AI Thinking..."):
                    pro = translate_pro(prompt)
                    st.info(f"✨ **Pro Prompt:** `{pro}`")
                    url = f"https://image.pollinations.ai/prompt/{pro.replace(' ', '%20')}?width={w}&height={h}&nologo=true&seed={int(time.time())}"
                    res = requests.get(url, timeout=30)
                    img = Image.open(io.BytesIO(res.content))
                    st.image(img, use_container_width=True)
                    buf = io.BytesIO()
                    img.save(buf, "PNG")
                    st.download_button("💾 Download PNG", buf.getvalue(), "patna_ai.png", "image/png")
                    st.session_state.counter += 1
                    st.balloons()

    # --- ✂️ BG REMOVER (API Based) ---
    elif menu == "✂️ BG Remove":
        st.header("🧹 AI Background Remover")
        uploaded = st.file_uploader("Upload Image", type=['png','jpg','jpeg'])
        if uploaded:
            st.image(Image.open(uploaded), caption="Original", width=300)
            if st.button("🪄 Remove BG", type="primary"):
                with st.spinner("Processing..."):
                    response = requests.post(
                        'https://api.remove.bg/v1.0/removebg',
                        files={'image_file': uploaded.getvalue()},
                        data={'size': 'auto'},
                        headers={'X-Api-Key': st.secrets["REMOVE_BG_KEY"]},
                    )
                    if response.status_code == 200:
                        st.image(response.content, caption="✅ Clean PNG", width=300)
                        st.download_button("💾 Download", response.content, "no_bg.png", "image/png")
                        st.session_state.counter += 1
                    else:
                        st.error("API Key check karein!")

    # --- 🎥 VIDEO GENERATOR (Replicate API) ---
    elif menu == "🎥 Video":
        st.header("🎥 AI Short Video (3s)")
        v_prompt = st.text_input("Describe scene:")
        if st.button("🎬 Generate Video", type="primary"):
            if v_prompt:
                with st.spinner("Creating Animation (1-2 mins)..."):
                    try:
                        pro_v = translate_pro(v_prompt)
                        # Stable Video Diffusion model call
                        output = replicate.run(
                            "stability-ai/stable-video-diffusion:3f045761ed782710cc3a452338830e3024c3a55e9d2b01560e30696b6bb768ed",
                            input={"input_image": "https://image.pollinations.ai/prompt/" + pro_v.replace(' ', '%20')}
                        )
                        st.video(output[0])
                        st.session_state.counter += 1
                    except Exception as e:
                        st.error(f"Video Error: {e}. Secrets check karein!")

else:
    st.error("🚫 Sidebar se unlock karein!")

st.markdown("---")
st.markdown("<center><b>Patna AI Studio Pro - Bihar's #1 AI Platform 🚀</b></center>", unsafe_allow_html=True)

