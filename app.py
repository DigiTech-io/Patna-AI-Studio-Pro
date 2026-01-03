import streamlit as st
import google.generativeai as genai
import requests
import tempfile
import os
from pydub import AudioSegment
from streamlit_option_menu import option_menu

# --- 1. सुरक्षा: Secrets से कीज़ लोड करना ---
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    ELEVENLABS_API_KEY = st.secrets["ELEVENLABS_API_KEY"]
except Exception:
    st.error("🚫 Secrets में API Key नहीं मिली! कृपया Streamlit Settings चेक करें।")
    st.stop()

# --- 2. मॉडर्न AI सेटअप (Log Fix) ---
genai.configure(api_key=GEMINI_API_KEY)

def get_model():
    # यह लिस्ट सबसे नए और स्थिर मॉडल्स को ट्राई करेगी
    for model_name in ['gemini-1.5-flash', 'gemini-1.5-flash-latest', 'gemini-pro']:
        try:
            m = genai.GenerativeModel(model_name)
            # छोटा सा टेस्ट
            m.generate_content("Hi", generation_config={"max_output_tokens": 1})
            return m
        except:
            continue
    return None

model = get_model()

# --- 3. UI और फीचर्स ---
st.set_page_config(page_title="Patna AI Studio Pro", layout="wide")

if not model:
    st.error("❌ Google AI कनेक्ट नहीं हो पा रहा है। कृपया अपनी API Key जांचें।")
else:
    with st.sidebar:
        selected = option_menu("Control Panel", ["Election Tool", "Ad Studio", "Dashboard"], 
                             icons=['mic', 'sparkles', 'graph-up'], menu_icon="cast")

    if selected == "Election Tool":
        st.header("🗳️ Election Campaign Generator")
        # आपका पुराना चुनाव वाला कोड यहाँ रहेगा...
        st.info("AI मॉडल सक्रिय है! अब आप ऑडियो बना सकते हैं।")


