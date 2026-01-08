import yt_dlp
import os

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
        ydl_opts = {
            # 1. Format: Best video + Best Audio merged into MP4
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            
            # 2. Output template (Filename)
            'outtmpl': os.path.join(self.download_path, '%(title)s.%(ext)s'),
            
            # 3. Progress Hook
            'progress_hooks': [progress_hook] if progress_hook else [],
            'noplaylist': True,
            
            # 4. ANTI-BOT HEADERS (The Fix for 403)
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'nocheckcertificate': True,
            'force_ipv4': True,  # Often fixes 403 errors on IPv6 networks
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.download([url])
                return "Success"
            except Exception as e:
                return str(e)
