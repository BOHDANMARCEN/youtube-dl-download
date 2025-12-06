import gradio as gr
import yt_dlp
import os
import re
from urllib.parse import urlparse, parse_qs

# Створюємо папку для завантажень, якщо її немає
DOWNLOAD_DIR = "downloads"
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

def clean_youtube_url(url):
    """Очищає YouTube URL від параметрів плейлисту та інших параметрів."""
    if not url:
        return url
    
    # Видаляємо параметри плейлисту та інші непотрібні параметри
    if 'youtube.com' in url or 'youtu.be' in url:
        # Для youtube.com/watch?v=VIDEO_ID&list=...
        if 'watch?v=' in url:
            video_id = url.split('watch?v=')[1].split('&')[0]
            return f"https://www.youtube.com/watch?v={video_id}"
        
        # Для youtu.be/VIDEO_ID?list=...
        elif 'youtu.be/' in url:
            video_id = url.split('youtu.be/')[1].split('?')[0]
            return f"https://www.youtube.com/watch?v={video_id}"
    
    return url

# Створюємо папку для завантажень, якщо її немає
DOWNLOAD_DIR = "downloads"
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

def get_quality_options(url):
    """Повертає список опцій якості без довгої обробки."""
    if not url or not url.strip():
        return [
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(value="Будь ласка, введіть URL відео")
        ]
    
    # Очищаємо URL від параметрів плейлисту
    clean_url = clean_youtube_url(url.strip())
    
    # Пропонуємо заздалегідь визначені, надійні варіанти якості
    quality_choices = [
        ("Найкраща якість (Відео+Аудіо, може вимагати ffmpeg)", "bestvideo+bestaudio/best"),
        ("Найкраща MP4 (до 1080p)", "bestvideo[ext=mp4][height<=1080]+bestaudio[ext=m4a]/best[ext=mp4]"),
        ("720p", "bestvideo[height<=720]+bestaudio/best"),
        ("480p", "bestvideo[height<=480]+bestaudio/best"),
        ("360p", "bestvideo[height<=360]+bestaudio/best"),
        ("Найкраще аудіо (m4a)", "bestaudio[ext=m4a]/bestaudio"),
        ("Найкраще аудіо (mp3)", "bestaudio/best")
    ]
    
    return [
        gr.update(choices=quality_choices, value=quality_choices[0][1], visible=True),
        gr.update(visible=True),
        gr.update(value=f"Формати готові. Виберіть якість і натисніть 'Завантажити'.\nОчищений URL: {clean_url}")
    ]


def download_video(url, quality_selector):
    """Завантажує відео, використовуючи селектор якості."""
    if not quality_selector or not url:
        yield "Помилка: URL або якість не вибрано."
        return
    
    # Очищаємо URL від параметрів плейлисту
    clean_url = clean_youtube_url(url.strip())
    
    yield f"Завантаження розпочато...\nОчищений URL: {clean_url}"
    
    try:
        # Налаштування для yt-dlp
        ydl_opts = {
            'format': quality_selector,
            'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'),
            'merge_output_format': 'mp4',
            'postprocessor_args': [],
            'progress_hooks': [lambda d: print(f">>> {d.get('_percent_str', '0%')} of ~{d.get('_total_bytes_str', 'unknown')} at {d.get('_speed_str', 'unknown')}", end="\r") if d.get('status') == 'downloading' else None],
            # Важливо: обмежуємо завантаження тільки одним відео
            'playlistend': 1,
            'noplaylist': True,
        }

        # Якщо користувач хоче mp3, додаємо відповідний пост-процесор
        if "mp3" in quality_selector:
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(clean_url, download=True)
            filename = ydl.prepare_filename(info)
            
        yield f"✅ Завантаження завершено! Файл збережено як: {os.path.basename(filename)}"

    except Exception as e:
        error_msg = str(e)
        if "Video unavailable" in error_msg:
            yield "❌ Помилка: Відео недоступне або приватне"
        elif "Private video" in error_msg:
            yield "❌ Помилка: Приватне відео"
        elif "Video unavailable" in error_msg:
            yield "❌ Помилка: Відео видалено або недоступне"
        else:
            yield f"❌ Помилка під час завантаження: {error_msg}"

# Створення інтерфейсу Gradio
with gr.Blocks(theme=gr.themes.Soft(), title="YouTube Downloader") as demo:
    gr.Markdown("# 🎥 YouTube Downloader v2")
    gr.Markdown("""
    ### Як користуватися:
    1. **Вставте URL** відео (YouTube, Vimeo, TikTok тощо)
    2. **Натисніть "Отримати варіанти"** - це відбудеться миттєво
    3. **Виберіть якість** з випадаючого списку
    4. **Натисніть "Завантажити"** для початку завантаження
    
    **💡 Порада:** Для найкращої якості встановіть [ffmpeg](https://ffmpeg.org/download.html)
    **🔧 Автоматично:** Програма автоматично очищає URL від параметрів плейлисту
    """)

    with gr.Row():
        with gr.Column(scale=3):
            url_input = gr.Textbox(
                label="🔗 URL відео", 
                placeholder="https://www.youtube.com/watch?v=...",
                lines=1
            )
            fetch_button = gr.Button("📋 Отримати варіанти", variant="secondary")
            
        with gr.Column(scale=2):
            quality_dropdown = gr.Dropdown(
                label="🎯 Виберіть якість", 
                visible=False,
                interactive=True
            )
            download_button = gr.Button("⬇️ Завантажити", variant="primary", visible=False)
    
    status_output = gr.Textbox(
        label="📊 Статус", 
        interactive=False,
        lines=3,
        value="Введіть URL відео та натисніть 'Отримати варіанти'"
    )

    fetch_button.click(
        fn=get_quality_options,
        inputs=url_input,
        outputs=[quality_dropdown, download_button, status_output]
    )
    
    download_button.click(
        fn=download_video,
        inputs=[url_input, quality_dropdown],
        outputs=status_output
    )

if __name__ == "__main__":
    demo.launch()