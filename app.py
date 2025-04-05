import streamlit as st
import requests

st.title("⚽ Football Highlights Generator")
st.write("Upload a football match and get quick highlights!")

# 🔗 Replace with your Colab Ngrok link
colab_backend = "https://abc123.ngrok.io/process"  # change this!

video = st.file_uploader("Upload Match Video", type=["mp4", "mkv"])
duration = st.selectbox("Highlight Duration (minutes)", [3, 5, 8, 10])

if st.button("Generate Highlights"):
    if not video:
        st.warning("Please upload a video file.")
    else:
        with st.spinner("Processing..."):
            files = {'video': video}
            data = {'duration': duration * 60}
            res = requests.post(colab_backend, files=files, data=data)
            if res.status_code == 200:
                with open("highlights.mp4", "wb") as f:
                    f.write(res.content)
                st.success("Done! Download your highlights below 👇")
                st.video("highlights.mp4")
                with open("highlights.mp4", "rb") as f:
                    st.download_button("📥 Download", f, file_name="highlights.mp4")
            else:
                st.error("Processing failed. Check backend.")
