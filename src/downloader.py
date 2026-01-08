import yt_dlp
import os

class VideoDownloader:
    def __init__(self, download_path="downloads"):
        self.download_path = download_path
        if not os.path.exists(download_path):
            os.makedirs(download_path)

    def get_info(self, url):
        """Fetches video title and thumbnail without downloading"""
        ydl_opts = {'quiet': True}
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
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': os.path.join(self.download_path, '%(title)s.%(ext)s'),
            'progress_hooks': [progress_hook] if progress_hook else [],
            'noplaylist': True
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.download([url])
                return "Success"
            except Exception as e:
                return str(e)
