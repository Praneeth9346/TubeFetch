import streamlit as st
import yt_dlp
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="TubeFetch", page_icon="📺")

# --- CORE LOGIC (Formerly downloader.py) ---
class VideoDownloader:
    def __init__(self, download_path="downloads"):
        self.download_path = download_path
        if not os.path.exists(download_path):
            os.makedirs(download_path)

    def get_info(self, url):
        """Fetches video title and thumbnail without downloading"""
        # We add 'user_agent' to mimic a real browser
        ydl_opts = {
            'quiet': True,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(url, download=False)
                return {
                    "title": info.get('title', 'Unknown'),
                    "thumbnail": info.get('thumbnail', None),
                    "duration": info.get('duration', 0),
                    "views": info.get('view_count', 0)
                }
            except Exception as e:
                return {"error": str(e)}

    def download_video(self, url, progress_hook=None):
        """Downloads the video in Best Quality (MP4)"""
        
        # Check for cookies (Optional cloud bypass)
        cookie_file = "cookies.txt"
        
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': os.path.join(self.download_path, '%(title)s.%(ext)s'),
            'progress_hooks': [progress_hook] if progress_hook else [],
            'noplaylist': True,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        }

        # If cookies exist, use them
        if os.path.exists(cookie_file):
            ydl_opts['cookiefile'] = cookie_file

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.download([url])
                return "Success"
            except Exception as e:
                return str(e)

# --- USER INTERFACE (UI) ---
st.title("📺 TubeFetch: YouTube Downloader")
st.write("Paste a YouTube link below to save it directly to your machine.")

# Initialize Downloader
downloader = VideoDownloader()

# Input
url = st.text_input("YouTube URL:", placeholder="https://www.youtube.com/watch?v=...")

if url:
    # 1. Fetch Info first (Show thumbnail)
    with st.spinner("Fetching video details..."):
        info = downloader.get_info(url)
    
    if "error" in info:
        st.error(f"Error finding video: {info['error']}")
    else:
        # Show Video Metadata
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image(info['thumbnail'], use_container_width=True)
        with col2:
            st.subheader(info['title'])
            st.caption(f"👀 Views: {info['views']:,} | ⏳ Duration: {info['duration']}s")
            
        # 2. Download Button
        if st.button("⬇️ Download High Quality MP4", key="dl_main"):
            progress_bar = st.progress(0)
            status_text = st.empty()

            def progress_hook(d):
                if d['status'] == 'downloading':
                    try:
                        p = d.get('_percent_str', '0%').replace('%','')
                        progress_bar.progress(float(p) / 100)
                        status_text.text(f"Processing on Server: {d.get('_percent_str')} ...")
                    except:
                        pass
                if d['status'] == 'finished':
                    progress_bar.progress(1.0)
                    status_text.text("✅ Server Download Complete! Preparing file for you...")

            try:
                result = downloader.download_video(url, progress_hook)
                
                if result == "Success":
                    # FIND THE FILE
                    if os.path.exists("downloads"):
                        files = [os.path.join("downloads", f) for f in os.listdir("downloads") if f.endswith(".mp4")]
                        if not files:
                            st.error("File not found on server.")
                        else:
                            latest_file = max(files, key=os.path.getctime)
                            file_name = os.path.basename(latest_file)
                            
                            # CREATE BROWSER DOWNLOAD BUTTON
                            with open(latest_file, "rb") as f:
                                st.download_button(
                                    label="⬇️ Click Here to Save to Your Computer",
                                    data=f,
                                    file_name=file_name,
                                    mime="video/mp4",
                                    key="dl_browser"
                                )
                            st.success("Ready! Click the button above to save.")
                    else:
                         st.error("Download folder missing.")
                else:
                    st.error(f"Server Download Failed: {result}")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")
