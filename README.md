# 📺 TubeFetch: High-Performance YouTube Downloader

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Framework-Streamlit-red)
![yt-dlp](https://img.shields.io/badge/Engine-yt--dlp-green)
![Status](https://img.shields.io/badge/Status-Active-success)

**TubeFetch** is a robust video downloading application built with Python. Unlike basic downloaders that break frequently, TubeFetch uses the industry-standard `yt-dlp` engine to fetch high-quality video (1080p/4k) and audio, merging them automatically into a ready-to-watch MP4 file.

## 🚀 Features

* **Best Quality Auto-Merge:** Automatically downloads the highest resolution video stream and highest quality audio stream, then merges them using FFmpeg.
* **Instant Metadata:** Fetches video thumbnails, view counts, and duration before downloading.
* **Browser-Based Download:** After the server processes the video, it provides a direct download link to save the file to your local device.
* **Anti-Bot Evasion:** Includes custom User-Agent headers and cookie support to bypass basic YouTube restrictions.

## 🛠️ Tech Stack

* **Frontend:** Streamlit (Python)
* **Core Engine:** yt-dlp
* **Processing:** FFmpeg (Multimedia framework)

## 📂 Project Structure

```text
TubeFetch/
├── app.py               # The complete application (UI + Logic)
├── requirements.txt     # Python dependencies
├── packages.txt         # System dependencies (FFmpeg for Cloud)
├── cookies.txt          # (Optional) For bypassing 403 errors
└── README.md            # Documentation

```
💻 Installation & Local Usage
```
This app works best locally because YouTube aggressively blocks Data Center IPs (like AWS/Google Cloud).

1. Clone the Repository
Bash

git clone [https://github.com/](https://github.com/)[YourUsername]/TubeFetch.git
cd TubeFetch
2. Install FFmpeg (Crucial)
Windows: Download ffmpeg-release-essentials.zip from gyan.dev. Extract it and add the bin folder to your System PATH.

Mac: brew install ffmpeg

Linux: sudo apt install ffmpeg

3. Install Python Libraries
Bash

pip install -r requirements.txt
4. Run the App
Bash

streamlit run app.py
```
☁️ Cloud Deployment Notes (Important)

If you deploy this to Streamlit Cloud, Heroku, or AWS, you may encounter HTTP Error 403: Forbidden.

Why? YouTube blocks download requests coming from known Data Center IP addresses to prevent server-side scraping.

The Fix (included in code): The application supports a cookies.txt file. By exporting your local browser cookies and uploading them to the server, you can authenticate requests as a real user, often bypassing this block.

Note: For a guaranteed experience, run this application locally.

⚠️ Disclaimer
This project is for educational purposes only. Please respect YouTube's Terms of Service and copyright laws. Do not download copyrighted content without permission.

🤝 Contributing
Contributions are welcome! Please fork the repository and submit a pull request for any enhancements.

📝 License
Distributed under the MIT License.
