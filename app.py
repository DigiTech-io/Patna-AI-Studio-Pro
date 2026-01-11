import streamlit as st
import os
import uuid
from gtts import gTTS

# =========================
# 1. CONFIG & PAGE THEME
# =========================
st.set_page_config(
    page_title="Vixan AI Media Studio Pro v4.0",
    page_icon="🎨",
    layout="wide",
)

# -------------------------
# Custom Premium CSS
# -------------------------
st.markdown("""
<style>
body { background-color: #0e1117; color: #ffffff; }
.stButton>button {
    background: linear-gradient(45deg, #FFD700, #FF8C00);
    color: black;
    border-radius: 12px;
    font-weight: 700;
    padding: 0.6rem 1.2rem;
}
.stRadio > div { gap: 10px; }
.card {
    border: 1px solid #333;
    border-radius: 16px;
    padding: 14px;
    background: #161b22;
    text-align: center;
}
.small-text { color: #aaa; font-size: 13px; }
</style>
""", unsafe_allow_html=True)

# =========================
# 2. SIDEBAR
# =========================
with st.sidebar:
    st.image(
        "https://cdn-icons-png.flaticon.com/512/2103/2103633.png",
        width=80
    )
    st.markdown("## **Vixan Pro v4.0**")
    st.caption("AI Media Studio for Branding")
    menu = st.radio(
        "Select Module",
        [
            "🏠 Dashboard",
            "🖼️ Poster Lab (50+ Designs)",
            "🎙️ Advanced Voice Studio",
            "🎞️ Video Clone Center",
        ],
    )

# =========================
# 3. DASHBOARD
# =========================
if menu == "🏠 Dashboard":
    st.markdown("## 🚀 Vixan AI Media Studio")
    st.info(
        "All-in-One AI Platform for Political, Business & Festival Branding.\n\n"
        "• Poster Design\n"
        "• AI Voice\n"
        "• Poster-to-Video\n"
        "• Social Media Ready Output"
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div class='card'>🎨<h4>Poster Lab</h4><p class='small-text'>50+ Pro Templates</p></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='card'>🎙️<h4>Voice Studio</h4><p class='small-text'>Hindi AI Voice</p></div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='card'>🎞️<h4>Video Clone</h4><p class='small-text'>Talking Poster</p></div>", unsafe_allow_html=True)

# =========================
# 4. POSTER LAB
# =========================
elif menu == "🖼️ Poster Lab (50+ Designs)":
    st.markdown("## 🖼️ Poster & Sticker Lab")

    category = st.selectbox(
        "Choose Design Category",
        ["Political (Chunav)", "Festival (Tyohar)", "Business", "Birthday"],
    )

    st.markdown("### 🎯 Select Base Template")

    templates = [
        "Political Design 01",
        "Political Design 02",
        "Festival Design 03",
        "Business Design 04",
        "Birthday Design 05",
    ]

    cols = st.columns(3)
    for i, name in enumerate(templates):
        with cols[i % 3]:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.image(
                f"https://via.placeholder.com/300x400.png?text={name.replace(' ', '+')}",
                use_container_width=True,
            )
            if st.button(f"Select {name}", key=name):
                st.session_state["selected_template"] = name
                st.success(f"{name} selected")
            st.markdown("</div>", unsafe_allow_html=True)

# =========================
# 5. ADVANCED VOICE STUDIO
# =========================
elif menu == "🎙️ Advanced Voice Studio":
    st.markdown("## 🎙️ Advanced AI Voice Studio")

    text = st.text_area(
        "Hindi Text Input",
        "नमस्ते, यह Vixan AI Media Studio की प्रोफेशनल आवाज़ है।",
        height=150,
    )

    st.markdown("### ⚙️ Voice Controls")

    col1, col2 = st.columns(2)
    with col1:
        speed = st.slider("Speech Speed", 0.5, 2.0, 1.0)
    with col2:
        clarity = st.slider("Voice Clarity", 0.0, 1.0, 0.8)

    if st.button("🔊 Generate AI Voice"):
        with st.spinner("AI voice processing..."):
            filename = f"voice_{uuid.uuid4().hex}.mp3"
            tts = gTTS(text=text, lang="hi", slow=(speed < 1.0))
            tts.save(filename)

            st.audio(filename)
            st.success("Voice generated successfully!")

            with open(filename, "rb") as f:
                st.download_button(
                    "⬇️ Download Voice",
                    f,
                    file_name="vixan_ai_voice.mp3",
                    mime="audio/mp3",
                )

# =========================
# 6. VIDEO CLONE CENTER
# =========================
elif menu == "🎞️ Video Clone Center":
    st.markdown("## 🎞️ Poster-to-Video Clone Center")

    col1, col2 = st.columns(2)

    with col1:
        poster = st.file_uploader(
            "Upload Poster Image",
            type=["jpg", "png", "jpeg"],
        )

        voice = st.selectbox(
            "Select AI Voice",
            ["Latest Generated Voice", "Sample Voice"],
        )

    with col2:
        if st.button("🎬 Generate Talking Poster"):
            if poster is None:
                st.warning("Please upload a poster image first.")
            else:
                st.info("AI Video Engine Processing...")
                st.video("https://www.w3schools.com/html/mov_bbb.mp4")

                st.download_button(
                    "📥 Download Final Video",
                    data=b"demo",
                    file_name="vixan_talking_poster.mp4",
                )

# =========================
# FOOTER
# =========================
st.markdown(
    "<hr><center class='small-text'>© 2026 Vixan AI Media Studio • Powered by Digitech</center>",
    unsafe_allow_html=True,
)
