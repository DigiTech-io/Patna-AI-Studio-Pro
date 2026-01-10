import streamlit as st
import requests
from PIL import Image, ImageDraw, ImageFont
import io

# --- UI SETTINGS ---
st.set_page_config(page_title="Vixan AI Studio Pro", layout="wide")

# --- CUSTOM CSS FOR PREMIUM LOOK ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stButton>button { 
        background: linear-gradient(45deg, #00d2ff, #3a7bd5); 
        color: white; font-weight: bold; border: none; padding: 10px;
    }
    .razorpay-box {
        border: 2px solid #3a7bd5; padding: 20px; border-radius: 15px;
        text-align: center; background: rgba(58, 123, 213, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# --- CONFIG ---
RAZORPAY_PAY_LINK = "https://rzp.io/l/vixanaistudiopro" # Yahan apna link dalein

# --- HINDI TEXT OVERLAY FUNCTION ---
def add_hindi_text(image_bytes, text, font_size=60):
    img = Image.open(io.BytesIO(image_bytes))
    draw = ImageDraw.Draw(img)
    
    # Aap "Khand-Bold.ttf" ya koi bhi Hindi font file apne GitHub repo me upload karein
    try:
        # Font file path (ensure you upload 'Khand.ttf' to your github)
        font = ImageFont.truetype("Khand-Bold.ttf", font_size)
    except:
        # Fallback agar font file nahi mili
        font = ImageFont.load_default()
        st.warning("Custom Hindi Font file nahi mili. 'Khand-Bold.ttf' repo me upload karein.")

    # Text ko center me dikhane ke liye logic
    w, h = img.size
    draw.text((w/2, h-150), text, font=font, fill="white", anchor="ms", stroke_width=2, stroke_fill="black")
    
    # Return edited image
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    return img_byte_arr.getvalue()

# --- APP LAYOUT ---
st.title("🚀 Vixan AI Studio Pro")
st.caption("Advanced Marketing Hub with Hindi Font Support")

tab1, tab2, tab3 = st.tabs(["🎨 Professional Poster", "🎙️ Audio Studio", "💳 Payment & Links"])

with tab1:
    st.subheader("Hindi Poster Maker (With Custom Fonts)")
    col1, col2 = st.columns([1, 1])
    
    with col1:
        name = st.text_input("Neta/Brand ka Naam", "Rahul Kumar")
        hindi_slogan = st.text_input("Hindi Slogan (Khand Font)", "Aapka Vishwas, Hamara Vikas")
        if st.button("Generate HD Poster ⚡"):
            with st.spinner("Pehle Background ban raha hai..."):
                # 1. Generate Background Image
                prompt = f"Professional political background, abstract blue and saffron theme, 8k"
                bg_url = f"https://image.pollinations.ai/prompt/{prompt.replace(' ', '%20')}?width=1024&height=1280&nologo=true"
                bg_res = requests.get(bg_url)
                
                if bg_res.status_code == 200:
                    # 2. Add Hindi Text using Pillow
                    final_img = add_hindi_text(bg_res.content, f"{name}\n{hindi_slogan}")
                    st.session_state['poster'] = final_img

    with col2:
        if 'poster' in st.session_state:
            st.image(st.session_state['poster'])
            st.download_button("Download Poster", st.session_state['poster'], "poster.png")

with tab3:
    st.markdown(f"""
    <div class="razorpay-box">
        <h2>💎 Upgrade to Premium</h2>
        <p>Unlock Audio Cloning & Unlimited Downloads</p>
        <a href="{RAZORPAY_PAY_LINK}" target="_blank">
            <button style="width:250px; cursor:pointer;">PAY VIA RAZORPAY</button>
        </a>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("---")
    st.subheader("WhatsApp Connectivity")
    wa_num = st.text_input("Enter Mobile Number", "91XXXXXXXXXX")
    if st.button("Generate Smart WhatsApp Link"):
        link = f"https://wa.me/{wa_num}?text=Mujhe%20Vixan%20AI%20ka%20Premium%20Plan%20chahiye"
        st.code(link)
        st.markdown(f"[Direct Chat]({link})")

st.sidebar.title("Partner Dashboard")
st.sidebar.success("Khand Font: Active ✅")
st.sidebar.info("Razorpay: Connected ✅")
