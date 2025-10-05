import gradio as gr
import yt_dlp
import os

# Створюємо папку для завантажень, якщо її немає
DOWNLOAD_DIR = "downloads"
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

def get_quality_options(url):
    """Повертає список опцій якості, а не всі формати."""
    try:
        # Просто перевіряємо, чи URL дійсний, щоб уникнути помилок
        ydl_opts = {'quiet': True, 'skip_download': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.extract_info(url, download=False)

        # Пропонуємо заздалегідь визначені, надійні варіанти якості
        quality_choices = [
            ("Найкраща якість (Відео+Аудіо, може вимагати ffmpeg)", "bestvideo+bestaudio/best"),
            ("Найкраща MP4 (до 1080p)", "bestvideo[ext=mp4][height<=1080]+bestaudio[ext=m4a]/best[ext=mp4]"),
            ("720p", "bestvideo[height<=720]+bestaudio/best"),
            ("480p", "bestvideo[height<=480]+bestaudio/best"),
            ("Найкраще аудіо (m4a)", "bestaudio[ext=m4a]/bestaudio"),
            ("Найкраще аудіо (mp3)", "bestaudio/best") # ffmpeg буде конвертувати в mp3
        ]
        
        return {
            quality_dropdown: gr.update(choices=quality_choices, value=quality_choices[0][1], visible=True),
            download_button: gr.update(visible=True),
            status_output: gr.update(value="Формати отримано. Виберіть якість і натисніть 'Завантажити'.")
        }
    except Exception as e:
        return {
            quality_dropdown: gr.update(visible=False),
            download_button: gr.update(visible=False),
            status_output: gr.update(value=f"Помилка отримання інформації: {str(e)}")
        }


def download_video(url, quality_selector):
    """Завантажує відео, використовуючи селектор якості."""
    if not quality_selector or not url:
        return "Помилка: URL або якість не вибрано."
    
    yield "Завантаження розпочато... Це може зайняти деякий час. Прогрес дивіться в консолі."

    try:
        # Налаштування для yt-dlp
        ydl_opts = {
            'format': quality_selector,
            'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'),
            'merge_output_format': 'mp4', # Об'єднує в mp4, якщо є окремі потоки
            'postprocessor_args': [],
            'progress_hooks': [lambda d: print(f">>> {d['_percent_str']} of ~{d['_total_bytes_str']} at {d['_speed_str']}", end="\r") if d['status'] == 'downloading' else None],
        }

        # Якщо користувач хоче mp3, додаємо відповідний пост-процесор
        if quality_selector == "bestaudio/best":
             ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
        yield f"Завантаження завершено! Файл збережено як: {filename}"

    except Exception as e:
        yield f"Помилка під час завантаження: {str(e)}"

# Створення інтерфейсу Gradio
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# YouTube Downloader v2")
    gr.Markdown("Вставте посилання, натисніть 'Отримати варіанти', виберіть якість та натисніть 'Завантажити'.\n**Увага:** Для найкращої якості може знадобитися [ffmpeg](https://ffmpeg.org/download.html).")

    with gr.Column():
        url_input = gr.Textbox(label="URL відео на YouTube")
        fetch_button = gr.Button("Отримати варіанти")
        
        quality_dropdown = gr.Dropdown(label="Виберіть якість", visible=False)
        download_button = gr.Button("Завантажити", variant="primary", visible=False)
        
        status_output = gr.Textbox(label="Статус", interactive=False)

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