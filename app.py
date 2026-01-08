import streamlit as st
import os
from src.downloader import VideoDownloader

st.set_page_config(page_title="TubeFetch", page_icon="📺")

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
        if st.button("⬇️ Download High Quality MP4"):
            progress_bar = st.progress(0)
            status_text = st.empty()

            def progress_hook(d):
                if d['status'] == 'downloading':
                    try:
                        p = d.get('_percent_str', '0%').replace('%','')
                        progress_bar.progress(float(p) / 100)
                        status_text.text(f"Downloading: {d.get('_percent_str')} ...")
                    except:
                        pass
                if d['status'] == 'finished':
                    progress_bar.progress(1.0)
                    status_text.text("✅ Download Complete! Processing...")

            try:
                result = downloader.download_video(url, progress_hook)
                if result == "Success":
                    st.success(f"🎉 Video saved to: `{os.path.abspath('downloads')}`")
                    st.balloons()
                else:
                    st.error(f"Download Failed: {result}")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")

# ... (Previous code remains the same until the button) ...
        
        # 2. Download Button
        if st.button("⬇️ Download High Quality MP4"):
            progress_bar = st.progress(0)
            status_text = st.empty()

            # Define a callback to update the progress bar
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
                # Run the download logic
                result = downloader.download_video(url, progress_hook)
                
                if result == "Success":
                    # FIND THE FILE: Since we don't know the exact sanitized filename, 
                    # we look for the most recently created mp4 in the downloads folder.
                    files = [os.path.join("downloads", f) for f in os.listdir("downloads") if f.endswith(".mp4")]
                    if not files:
                        st.error("File not found on server.")
                    else:
                        latest_file = max(files, key=os.path.getctime)
                        file_name = os.path.basename(latest_file)
                        
                        # CREATE DOWNLOAD BUTTON
                        with open(latest_file, "rb") as f:
                            st.download_button(
                                label="⬇️ Click Here to Save to Your Computer",
                                data=f,
                                file_name=file_name,
                                mime="video/mp4"
                            )
                        st.success("Ready! Click the button above to save.")
                else:
                    st.error(f"Server Download Failed: {result}")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")
