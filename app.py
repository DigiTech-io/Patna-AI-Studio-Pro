import streamlit as st
import os

# --- 1. सुरक्षा: Secrets लोड करना ---
# Ye code dono naam (GOOGLE ya GEMINI) check karega
api_key = st.secrets.get("GOOGLE_API_KEY") or st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("🚫 Secrets में API Key नहीं मिली! कृपया Streamlit Settings में 'GOOGLE_API_KEY' नाम से Key डालें।")
    st.stop()

# --- 2. Library Import (Error Checking के साथ) ---
try:
    import google.generativeai as genai
    from streamlit_option_menu import option_menu
    genai.configure(api_key=api_key)
except ModuleNotFoundError as e:
    st.error(f"❌ Library missing: {e}. कृपया requirements.txt चेक करें।")
    st.stop()

st.title("🚩 Patna AI Studio Pro")
st.success("✅ Connection Successful! Ready for Design.")

# --- 3. Design Selection (PDF Styles) ---
selected = option_menu(
    menu_title=None,
    options=["Style 1 (Circle)", "Style 2 (Banner)", "Style 3 (Mukhiya)"],
    icons=["image", "brush", "person"],
    orientation="horizontal",
)
