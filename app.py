import streamlit as st
import requests
from PIL import Image, ImageDraw, ImageFont
import io
import urllib.parse
import os

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Vixan AI Studio Pro",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================= PREMIUM CSS =================
st.markdown("""
<style>
.stApp {
    background-color: #0e1117;
    color: white;
}
h1, h2, h3 {
    color: #f1f1f1;
}
.stButton>button {
    background: linear-gradient(45deg, #00d2ff, #3a7bd5);
    color: white;
    font-weight: bold;
    border: none;
    padding: 10px;
    border-radius: 10px;
}
.razorpay-box {
    border: 2px solid #3a7bd5;
    padding: 22px;
    border-radius: 16px;
    text-align: center;
    background: rgba(58, 123, 213, 0.12);
}
</style>
""", unsafe_allow_html=True)

# ================= CONFIG =================
RAZORPAY_PAY_LINK = "https://rzp.io/l/vixanaistudiopro"
FONT_PATH = "Khand-Bold.ttf"   # upload this in repo root

# ================= HINDI TEXT FUNCTION =================
def add_hindi_text(image_bytes, text, font_size=64):
    img = Image.open(io.BytesIO(image_bytes)).convert("RGBA")
    draw = ImageDraw.Draw(img)

    # Load font safely
    if os.path.exists(FONT_PATH):
        font = ImageFont.truetype(FONT_PATH, font_size)
    else:
        font = ImageFont.load_default()
        st.warning("⚠️ Hindi font file missing. Please upload Khand-Bold.ttf")

    width, height = img.size

    # Multi-line text center alignment
    lines = text.split("\n")
    y_position = height - (len(lines) * font_size) - 40

    for line in lines:
        text_width = draw.textlength(line, font=font)
        x = (width - text_width) / 2
        draw.text(
            (x, y_position),
            line,
            font=font,
            fill="white",
            stroke_width=2,
            stroke_fill="black"
        )
        y_position += font_size + 6

    output = io.BytesIO()
    img.save(output, format="PNG")
    return output.getvalue()

# ================= APP HEADER =================
st.title("🚀 Vixan AI Studio Pro")
st.caption("Advanced Marketing Hub • Hindi Poster • Premium Payments")

tab1, tab2, tab3 = st.tabs([
    "🎨 Professional Poster",
    "🎙️ Audio Studio",
    "💳 Payment & Links"
])

# ================= TAB 1 : POSTER =================
with tab1:
    st.subheader("Hindi Poster Maker (Custom Font Support)")

    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Leader / Brand Name", "Rahul Kumar")
        hindi_slogan = st.text_input(
            "Hindi Slogan (Devanagari)",
            "आपका विश्वास, हमारा विकास"
        )

        if st.button("⚡ Generate HD Poster"):
            with st.spinner("AI background generate ho raha hai..."):
                prompt = (
                    "Professional political poster background, "
                    "abstract blue and saffron theme, "
                    "cinematic lighting, ultra quality, 8k"
                )

                encoded_prompt = urllib.parse.quote_plus(prompt)
                bg_url = (
                    f"https://image.pollinations.ai/prompt/{encoded_prompt}"
                    "?width=1024&height=1280&nologo=true"
                )

                response = requests.get(bg_url, timeout=60)

                if response.status_code == 200:
                    final_img = add_hindi_text(
                        response.content,
                        f"{name}\n{hindi_slogan}"
                    )
                    st.session_state["poster"] = final_img
                else:
                    st.error("Background generate nahi ho paaya")

    with col2:
        if "poster" in st.session_state:
            st.image(st.session_state["poster"])
            st.download_button(
                "⬇️ Download Poster",
                st.session_state["poster"],
                "vixan_poster.png"
            )

# ================= TAB 2 : AUDIO =================
with tab2:
    st.subheader("🎙️ Audio Studio (Coming Soon)")
    st.info("Advanced AI Voice & Cloning module next upgrade me enable hoga.")

# ================= TAB 3 : PAYMENT & LINKS =================
with tab3:
    st.markdown(f"""
    <div class="razorpay-box">
        <h2>💎 Upgrade to Premium</h2>
        <p>Unlock unlimited posters, audio & video tools</p>
        <a href="{RAZORPAY_PAY_LINK}" target="_blank">
            <button style="width:260px; cursor:pointer;">PAY VIA RAZORPAY</button>
        </a>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.subheader("📲 WhatsApp Smart Link")

    wa_num = st.text_input("WhatsApp Number (with country code)", "91XXXXXXXXXX")

    if st.button("Generate WhatsApp Link"):
        wa_link = (
            f"https://wa.me/{wa_num}"
            "?text=Mujhe%20Vixan%20AI%20Premium%20Plan%20chahiye"
        )
        st.success("WhatsApp Link Ready")
        st.code(wa_link)
        st.markdown(f"[Open Chat]({wa_link})")

# ================= SIDEBAR =================
st.sidebar.title("🤝 Partner Dashboard")
st.sidebar.success("Hindi Font Engine: Active ✅")
st.sidebar.success("Poster Generator: Live ✅")
st.sidebar.info("Razorpay: Connected ✅")
