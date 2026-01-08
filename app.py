import streamlit as st
import yt_dlp
import os
import re

# --- PAGE CONFIG ---
st.set_page_config(page_title="TubeFetch", page_icon="📺")

# --- CORE LOGIC ---
class VideoDownloader:
    def __init__(self, download_path="downloads"):
        self.download_path = download_path
        if not os.path.exists(download_path):
            os.makedirs(download_path)

    def get_info(self, url):
        """Fetches video title and thumbnail without downloading"""
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
        
        cookie_file = "cookies.txt"
        
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': os.path.join(self.download_path, '%(title)s.%(ext)s'),
            'progress_hooks': [progress_hook] if progress_hook else [],
            'noplaylist': True,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        }

        if os.path.exists(cookie_file):
            ydl_opts['cookiefile'] = cookie_file

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.download([url])
                return "Success"
            except Exception as e:
                return str(e)

# --- USER INTERFACE ---
st.title("📺 TubeFetch: YouTube Downloader")
st.write("Paste a YouTube link below to save it directly to your machine.")

# Initialize Downloader
downloader = VideoDownloader()

# Input
url = st.text_input("YouTube URL:", placeholder="https://www.youtube.com/watch?v=...")

if url:
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
            
        st.divider()

        # 2. Server Processing Button
        if st.button("🚀 Process & Prepare Download", key="process_btn", type="primary"):
            
            # --- PROGRESS BAR LOGIC ---
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            def progress_hook(d):
                if d['status'] == 'downloading':
                    try:
                        # Calculate percentage
                        p = d.get('_percent_str', '0%').replace('%','')
                        clean_p = float(re.sub(r'\x1b\[[0-9;]*m', '', p)) / 100  # Remove ANSI colors if any
                        
                        # Update bar
                        progress_bar.progress(clean_p)
                        
                        # Descriptive Text to explain "Jumps"
                        # We guess the stream type by file extension in the temp filename
                        filename = d.get('filename', '')
                        if 'video' in filename or '.f' in filename and '.mp4' not in filename:
                             status_text.info(f"📥 Downloading Video Track: {d.get('_percent_str')}...")
                        elif 'audio' in filename or '.m4a' in filename:
                             status_text.info(f"🎵 Downloading Audio Track: {d.get('_percent_str')}...")
                        else:
                             status_text.info(f"📥 Downloading Stream: {d.get('_percent_str')}...")

                    except:
                        pass
                        
                elif d['status'] == 'finished':
                    progress_bar.progress(1.0)
                    status_text.success("✅ Stream Downloaded. Merging files...")

            try:
                result = downloader.download_video(url, progress_hook)
                
                if result == "Success":
                    status_text.empty() # Clear status
                    progress_bar.empty() # Clear bar
                    
                    # Find the file
                    if os.path.exists("downloads"):
                        files = [os.path.join("downloads", f) for f in os.listdir("downloads") if f.endswith(".mp4")]
                        if not files:
                            st.error("File processed but not found on server.")
                        else:
                            latest_file = max(files, key=os.path.getctime)
                            file_name = os.path.basename(latest_file)
                            file_size = os.path.getsize(latest_file) / (1024 * 1024) # MB

                            st.success(f"🎉 Processing Complete! ({file_size:.1f} MB)")
                            
                            # --- FINAL DOWNLOAD BUTTON ---
                            with open(latest_file, "rb") as f:
                                st.download_button(
                                    label=f"⬇️ Save '{file_name}' to Device",
                                    data=f,
                                    file_name=file_name,
                                    mime="video/mp4",
                                    key="final_download_btn"
                                )
                    else:
                         st.error("Download folder missing.")
                else:
                    st.error(f"Processing Failed: {result}")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")
