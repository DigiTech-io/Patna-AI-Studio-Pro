# ================= MODULE: TEXT TO IMAGE =================
elif selected == "Text to Image":
    st.header("🖼️ AI Imagine Engine")
    prompt = st.text_area("Aap kya banana chahte hain? (Describe in detail)")
    
    if st.button("🚀 Generate High-Res Image"):
        with st.spinner("Vixan AI image render kar raha hai..."):
            # Segmind Flux API Call
            url = "https://api.segmind.com/v1/flux-1.0-schnell"
            payload = {"prompt": prompt, "base64": True, "aspect_ratio": "1:1"}
            headers = {"x-api-key": SEGMIND_KEY}
            
            response = requests.post(url, json=payload, headers=headers)
            data = response.json()
            
            if "image" in data:
                st.image(f"data:image/png;base64,{data['image']}", use_column_width=True)
                st.success("✨ Image ready!")
            else:
                st.error("API Error: Key check karein.")

# ================= MODULE: IMAGE TO VIDEO =================
elif selected == "Image to Video":
    st.header("🎬 Motion AI Studio")
    st.info("Photo upload karein aur use video mein badlein.")
    
    uploaded_file = st.file_uploader("Upload Image", type=['jpg', 'png', 'jpeg'])
    
    if uploaded_file:
        st.image(uploaded_file, width=300, caption="Original Photo")
        if st.button("🎥 Create 4-Second Video"):
            with st.spinner("AI motion analysis kar raha hai... isme 1-2 min lag sakte hain."):
                # Yahan Segmind SVD (Stable Video Diffusion) API call aayegi
                st.warning("Video Generation engine is connecting... (SVD API integration required)")
                # Demo placeholder
                st.video("https://samplelib.com/lib/preview/mp4/sample-5s.mp4")
