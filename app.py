import streamlit as st
import requests

# --- UI SETTINGS ---
st.set_page_config(page_title="Vixan AI Studio Pro", layout="wide", page_icon="🚀")

# --- SECRETS ---
SEGMIND_KEY = st.secrets.get("SEGMIND_API_KEY")

# --- IMAGE GENERATION ENGINE ---
def generate_image_logic(prompt):
    """Try Segmind first, if fails, use Pollinations (Free)"""
    
    # 1. Try Segmind Flux Schnell
    if SEGMIND_KEY:
        url = "https://api.segmind.com/v1/flux-schnell"
        payload = {
            "prompt": prompt,
            "steps": 4,
            "seed": 12345,
            "sampler": "euler",
            "samples": 1,
            "guidance_scale": 3.5,
            "shape": "landscape"
        }
        headers = {"x-api-key": SEGMIND_KEY}
        
        try:
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                return response.content, "Segmind (Premium)"
            else:
                st.warning("Segmind Credits khatam ya error hai. Free Engine use kar rahe hain...")
        except Exception as e:
            st.error(f"Segmind Error: {e}")

    # 2. Fallback to Pollinations AI (Free & Unlimited)
    free_url = f"https://image.pollinations.ai/prompt/{prompt.replace(' ', '%20')}?width=1024&height=1024&nologo=true"
    try:
        free_response = requests.get(free_url)
        if free_response.status_code == 200:
            return free_response.content, "Pollinations AI (Free)"
    except Exception as e:
        st.error(f"Free Engine Error: {e}")
    
    return None, None

# --- APP UI ---
st.title("🚀 Vixan AI Studio Pro")
st.markdown("Automated Image Engine: **Segmind + Free Fallback**")

tab1, tab2 = st.tabs(["🎨 Poster Studio", "🖼️ Imagine Engine"])

with tab1:
    st.header("Political & Business Poster Maker")
    col1, col2 = st.columns([1, 2])
    
    with col1:
        name = st.text_input("Naam Likhein")
        slogan = st.text_input("Slogan (Naara)")
        btn_poster = st.button("Generate Poster ✨")

    with col2:
        if btn_poster:
            with st.spinner("Designing your poster..."):
                full_prompt = f"Professional poster for {name}, with slogan '{slogan}', high resolution, realistic style."
                img_data, engine_name = generate_image_logic(full_prompt)
                
                if img_data:
                    st.success(f"Generated using: {engine_name}")
                    st.image(img_data)
                    st.download_button("Download Poster", img_data, file_name="vixan_poster.jpg")

with tab2:
    st.header("AI Imagine Engine")
    prompt = st.text_area("Describe your imagination...")
    if st.button("Generate Art 🖼️"):
        if prompt:
            with st.spinner("Creating Art..."):
                img_data, engine_name = generate_image_logic(prompt)
                if img_data:
                    st.success(f"Generated using: {engine_name}")
                    st.image(img_data)
                    st.download_button("Download Art", img_data, file_name="vixan_art.jpg")
