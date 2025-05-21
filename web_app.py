# web_app.py
import streamlit as st
import librosa
import numpy as np
import pandas as pd
import os
import shutil
from moviepy.editor import VideoFileClip, concatenate_videoclips
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from math import ceil

# Configuration
st.set_page_config(page_title="Sports Highlights Generator", layout="wide")
st.title("⚽ Sports Video Highlights Generator")
TEMP_DIR = "temp_files"
os.makedirs(TEMP_DIR, exist_ok=True)

def save_large_file(uploaded_file):
    """Save large files in 100MB chunks"""
    chunk_size = 1024 * 1024 * 100
    video_path = os.path.join(TEMP_DIR, uploaded_file.name)
    
    with st.spinner(f"Saving {uploaded_file.name}..."):
        with open(video_path, "wb") as f:
            for chunk in iter(lambda: uploaded_file.read(chunk_size), b""):
                f.write(chunk)
    return video_path

def generate_highlights(mul, video_path):
    try:
        # Load video and extract audio
        video = VideoFileClip(video_path)
        audio = video.audio
        audio_path = os.path.join(TEMP_DIR, "audio_temp.mp3")
        audio.write_audiofile(audio_path, codec='mp3')

        # Audio processing
        audio_data, sample_rate = librosa.load(audio_path)
        chunk_size = 5
        window_length = chunk_size * sample_rate

        # ====== FINAL FIXED ENERGY CALCULATION ======
        energy = np.array([
            (np.abs(audio_data[i:i+window_length] ** 2)).mean()  # Simplified and fixed
            for i in range(0, len(audio_data), window_length)
        ])
        # ============================================

        # Threshold calculation
        inc = 0.2 if ceil(np.mean(energy)*1000) > 2 else 0
        thresh = np.mean(energy) * mul + inc

        # Create time intervals DataFrame
        df = pd.DataFrame(columns=['energy', 'start', 'end'])
        row_index = 0
        
        for i in range(len(energy)):
            value = energy[i]
            if value >= thresh:
                df.loc[row_index] = [value, i*5, (i+1)*5]
                row_index += 1

        # Sort and merge intervals
        df = df.sort_values('start').reset_index(drop=True)
        i = 0
        while i < len(df)-1:
            if df.loc[i, 'end'] >= df.loc[i+1, 'start']:
                df.loc[i, 'end'] = max(df.loc[i, 'end'], df.loc[i+1, 'end'])
                df = df.drop(i+1).reset_index(drop=True)
            else:
                i += 1

        # Video processing
        sub_folder = os.path.join(TEMP_DIR, "subclips")
        if os.path.exists(sub_folder):
            shutil.rmtree(sub_folder)
        os.makedirs(sub_folder)

        clips = []
        for idx, row in df.iterrows():
            start_lim = max(0, row['start'] - 5)
            end_lim = row['end']
            duration = end_lim - start_lim
            
            filename = f"highlight_{idx:04d}.mp4"
            target_path = os.path.join(sub_folder, filename)

            if duration > 20:
                ffmpeg_extract_subclip(video_path, start_lim+5, start_lim+20, targetname=target_path)
            elif duration > 10:
                ffmpeg_extract_subclip(video_path, start_lim, start_lim+15, targetname=target_path)
            else:
                ffmpeg_extract_subclip(video_path, start_lim, end_lim, targetname=target_path)
            
            if os.path.exists(target_path):
                clips.append(VideoFileClip(target_path))

        # Combine clips
        if clips:
            final_clip = concatenate_videoclips(clips)
            output_path = os.path.join(TEMP_DIR, "highlights_output.mp4")
            final_clip.write_videofile(output_path, audio_codec='mp3')
            for clip in clips:
                clip.close()
            return output_path
        return None

    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

# Streamlit UI
uploaded_file = st.file_uploader("Upload video", type=["mp4", "avi", "mkv"])
file_path = st.text_input("OR Enter file path:", placeholder="C:/FootballProject/video.mp4")
duration_option = st.selectbox("Highlight duration (minutes)", ("10", "15", "20", "30"), index=2)

if st.button("Generate Highlights"):
    video_path = None
    
    if uploaded_file:
        video_path = save_large_file(uploaded_file)
    elif file_path and os.path.exists(file_path):
        video_path = file_path
    else:
        st.error("Please upload a file or provide valid path")
        st.stop()
    
    mul_map = {"10": 3, "15": 2.4, "20": 1.8, "30": 1.2}
    mul = mul_map[duration_option]

    with st.spinner("Generating highlights..."):
        result_path = generate_highlights(mul, video_path)
    
    if result_path:
        st.success("Highlights generated!")
        st.video(result_path)
        with open(result_path, "rb") as f:
            st.download_button("Download", f, file_name="highlights.mp4")
        
        # Cleanup
        if uploaded_file:
            os.remove(video_path)
        os.remove(result_path)
        shutil.rmtree(os.path.join(TEMP_DIR, "subclips"), ignore_errors=True)