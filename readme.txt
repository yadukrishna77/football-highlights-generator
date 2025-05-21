1. Prepare Your USB Drive
Folder Structure:

FootballProject/
├── web_app.py             # Your working code
├── requirements.txt       # From below
├── temp_files/            # Leave empty
└── sample_video.mp4       # Short test video (1-2 mins)
requirements.txt Content:

txt
streamlit==1.35.0
librosa==0.10.1
numpy==1.26.4
pandas==2.2.2
moviepy==1.0.3
matplotlib==3.8.4
numba==0.59.1
soundfile==0.12.1
tqdm==4.66.2
2. On Your Friend's Laptop
A. Install Python
Go to python.org/downloads

Download Python 3.12.3 (same as your PC)

Run installer:

Check ✅ "Add Python to PATH"

Click "Install Now"

B. Install FFmpeg (Critical)
Open Command Prompt:

cmd
winget install Gyan.FFmpeg
If winget isn't available, download from ffmpeg.org

Extract to C:\FFmpeg\ and add to PATH:

cmd
setx PATH "%PATH%;C:\FFmpeg\bin"
C. Copy Project Files
Insert USB drive

Copy the entire FootballProject folder to:

C:\Users\{Friend'sUsername}\Desktop\FootballProject
3. Setup the Project
Open Command Prompt:

cmd
cd Desktop\FootballProject
Create Streamlit config:

cmd
mkdir %USERPROFILE%\.streamlit
echo [server] > %USERPROFILE%\.streamlit\config.toml
echo maxUploadSize = 2000 >> %USERPROFILE%\.streamlit\config.toml
Install dependencies:

cmd
pip install --upgrade pip
pip install -r requirements.txt
4. Run the App
In the same Command Prompt:

cmd
streamlit run web_app.py
The app will automatically open in Chrome/Firefox at:

http://localhost:8501
5. Demo Time
Test with Sample Video:

Click "Browse files" → Select sample_video.mp4

Choose duration (e.g., 10 mins)

Click "Generate Highlights"

Show Path Input:

Type C:\Users\{Friend'sUsername}\Desktop\FootballProject\sample_video.mp4

Click "Generate Highlights"

6. Post-Demo Cleanup
Close the app (Ctrl+C in Command Prompt)

Run cleanup:

cmd
rd /s /q %USERPROFILE%\.streamlit
rd /s /q C:\Users\{Friend'sUsername}\Desktop\FootballProject\temp_files
Troubleshooting Cheat Sheet
Issue: No module named 'numba'
Fix:

cmd
pip install numba==0.59.1
Issue: FFmpeg not found
Fix:

cmd
setx PATH "%PATH%;C:\FFmpeg\bin"
Issue: RuntimeError: Broken toolchain
Fix: Install Microsoft C++ Build Tools

Checklist Before Demo
Tested on your PC first

USB contains requirements.txt + web_app.py

Friend's laptop has 2GB+ free space

Python added to PATH confirmed

FFmpeg installed and PATH set

This guarantees a smooth demo without technical hiccups! 🚀

