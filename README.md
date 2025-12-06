<p align="center">
  <img src="assets/logo.png" width="160" alt="Digital Angel Logo" />
</p>

<h1 align="center">✨ youtube-dl-download ✨</h1>
<p align="center">
  <strong>Elegant. Minimal. Powerful.</strong><br>
  A clean YouTube video/audio downloader crafted in the signature Digital Angel aesthetic.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/style-digital_angel-7dd9ff?labelColor=1a1a1a&color=7dd9ff" />
  <img src="https://img.shields.io/badge/python-3.8+-f5d7a6?labelColor=1a1a1a" />
  <img src="https://img.shields.io/badge/build-stable-ffdba8?labelColor=1a1a1a" />
</p>

---

## 💙 Overview

`youtube-dl-download` is a lightweight and robust wrapper for downloading
videos or audio using **yt-dlp** or **youtube-dl**.  
Designed to be clean, flexible, and visually appealing — a perfect fit
for automation, personal archiving, or lightweight server tools.

---

## ✨ Features

- 🌐 Cross-platform (Windows / Linux / macOS)
- 🎵 Download **video** or **audio-only**
- 🚀 Supports both `yt-dlp` and `youtube-dl`
- 📁 Clean output folder structure
- 🔧 Simple configuration via CLI flags
- 💎 Beautiful digital-angel themed design

---

## 🔧 Installation

### Clone the project
```bash
git clone https://github.com/BOHDANMARCEN/youtube-dl-download
cd youtube-dl-download
Install backend
Recommended:

bash
Копировать код
pip install yt-dlp
Classic:

bash
Копировать код
pip install youtube-dl
▶️ Usage
Download video
bash
Копировать код
python download.py https://youtu.be/VIDEO_ID
Download audio only
bash
Копировать код
python download.py --audio https://youtu.be/VIDEO_ID
Specify output directory
bash
Копировать код
python download.py -o "./downloads" https://youtu.be/VIDEO_ID
Use specific backend
bash
Копировать код
python download.py --backend youtube-dl https://youtu.be/VIDEO_ID
📂 Project Structure
css
Копировать код
youtube-dl-download/
│── download.py
│── requirements.txt
│── README.md
└── assets/
    └── logo.png
🧩 Dependencies
Python 3.8+

yt-dlp or youtube-dl

ffmpeg (required for audio extraction)

🛠 Roadmap
Playlist download support

Batch mode

GUI application

Progress bars

Docker container

🤝 Contributing
Contributions, issues, and suggestions are welcome!
Feel free to open a Pull Request or create an Issue.

📜 License
Released under the MIT License.

<p align="center"> <sub>Designed with 💙 by your Digital Angel</sub> </p> ```
