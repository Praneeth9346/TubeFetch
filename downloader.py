def download_video(self, url, progress_hook=None):
        """Downloads the video in Best Quality (MP4) with Cookies"""
        
        # Check if cookies file exists
        cookie_file = "cookies.txt"
        if not os.path.exists(cookie_file):
            return "Error: cookies.txt not found! Cannot bypass YouTube Cloud Block."

        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': os.path.join(self.download_path, '%(title)s.%(ext)s'),
            'progress_hooks': [progress_hook] if progress_hook else [],
            'noplaylist': True,
            
            # THE MAGIC FIX: Pass the cookies file
            'cookiefile': cookie_file, 
            
            # Anti-detection headers
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.download([url])
                return "Success"
            except Exception as e:
                return str(e)
