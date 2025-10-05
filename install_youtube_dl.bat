@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ===============================================
echo    YouTube-DL Auto Installer
echo ===============================================
echo.

:: Перевірка чи запущено від імені адміністратора
net session >nul 2>&1
if %errorLevel% == 0 (
    echo [INFO] Запущено від імені адміністратора
) else (
    echo [ERROR] Потрібні права адміністратора для встановлення
    echo Запустіть бат-файл від імені адміністратора
    echo.
    echo Натисніть будь-яку клавішу для виходу...
    pause >nul
    exit /b 1
)

:: Встановлення директорії проекту
set "PROJECT_DIR=C:\youtube-dl"
set "GITHUB_REPO=https://github.com/BOHDANMARCEN/youtube-dl-download.git"

echo [INFO] Встановлення директорії проекту: %PROJECT_DIR%

:: Перевірка наявності Python
echo [INFO] Перевірка наявності Python...
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERROR] Python не знайдено в системі
    echo Будь ласка, встановіть Python з https://python.org
    pause
    exit /b 1
) else (
    echo [OK] Python знайдено
    python --version
)

:: Перевірка наявності Git
echo [INFO] Перевірка наявності Git...
git --version >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERROR] Git не знайдено в системі
    echo Будь ласка, встановіть Git з https://git-scm.com
    pause
    exit /b 1
) else (
    echo [OK] Git знайдено
    git --version
)

:: Створення директорії проекту
echo [INFO] Створення директорії проекту...
if exist "%PROJECT_DIR%" (
    echo [INFO] Директорія вже існує, видаляємо стару версію...
    rmdir /s /q "%PROJECT_DIR%"
)

mkdir "%PROJECT_DIR%"
if %errorLevel% neq 0 (
    echo [ERROR] Не вдалося створити директорію проекту
    pause
    exit /b 1
)

:: Клонування репозиторію
echo [INFO] Завантаження проекту з GitHub...
cd /d "%PROJECT_DIR%"
git clone %GITHUB_REPO% .
if %errorLevel% neq 0 (
    echo [ERROR] Не вдалося завантажити проект з GitHub
    pause
    exit /b 1
)
echo [OK] Проект успішно завантажено

:: Встановлення залежностей Python
echo [INFO] Встановлення залежностей Python...
if exist "requirements.txt" (
    echo [INFO] Знайдено requirements.txt, встановлюємо залежності...
    pip install -r requirements.txt
    if %errorLevel% neq 0 (
        echo [WARNING] Деякі залежності не вдалося встановити
        echo [INFO] Спробуємо встановити основні залежності окремо...
        pip install yt-dlp gradio
    ) else (
        echo [OK] Залежності успішно встановлено
    )
) else (
    echo [INFO] requirements.txt не знайдено, встановлюємо базові залежності...
    pip install yt-dlp gradio requests urllib3
    echo [OK] Базові залежності встановлено
)

:: Створення бат-файлу для запуску
echo [INFO] Створення бат-файлу для запуску...
echo @echo off > "%PROJECT_DIR%\youtube-dl.bat"
echo python "%PROJECT_DIR%\youtube_downloader.py" %%* >> "%PROJECT_DIR%\youtube-dl.bat"

:: Додавання до PATH
echo [INFO] Додавання проекту до системного PATH...
set "PATH_VALUE=%PROJECT_DIR%"

:: Отримання поточного PATH
for /f "tokens=2*" %%a in ('reg query "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v PATH 2^>nul') do set "CURRENT_PATH=%%b"

:: Перевірка чи вже є в PATH
if defined CURRENT_PATH (
    echo %CURRENT_PATH% | find /i "%PROJECT_DIR%" >nul
    if %errorLevel% == 0 (
        echo [INFO] Проект вже додано до PATH
    ) else (
        echo [INFO] Додавання проекту до PATH...
        set "NEW_PATH=%CURRENT_PATH%;%PROJECT_DIR%"
        reg add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v PATH /t REG_EXPAND_SZ /d "%NEW_PATH%" /f >nul 2>&1
        if %errorLevel% neq 0 (
            echo [WARNING] Не вдалося додати до системного PATH
            echo [INFO] Проект буде працювати з повним шляхом
        ) else (
            echo [OK] Проект додано до PATH
        )
    )
) else (
    echo [WARNING] Не вдалося отримати поточний PATH
    echo [INFO] Проект буде працювати з повним шляхом
)

:: Створення ярлика на робочому столі
echo [INFO] Створення ярлика на робочому столі...
set "DESKTOP=%USERPROFILE%\Desktop"
echo [InternetShortcut] > "%DESKTOP%\YouTube-DL.url"
echo URL=file:///%PROJECT_DIR%\youtube-dl.bat >> "%DESKTOP%\YouTube-DL.url"
echo IconFile=%PROJECT_DIR%\youtube-dl.bat >> "%DESKTOP%\YouTube-DL.url"
echo IconIndex=0 >> "%DESKTOP%\YouTube-DL.url"

:: Тестування встановлення
echo [INFO] Тестування встановлення...
cd /d "%PROJECT_DIR%"
python youtube_downloader.py --version >nul 2>&1
if %errorLevel% neq 0 (
    echo [WARNING] Тест не пройшов, але встановлення завершено
) else (
    echo [OK] Тест пройшов успішно
)

echo.
echo ===============================================
echo    Встановлення завершено!
echo ===============================================
echo.
echo Проект встановлено в: %PROJECT_DIR%
echo Ярлик створено на робочому столі
echo Проект додано до системного PATH
echo.
echo Для використання:
echo   python youtube_downloader.py
echo   або запустіть ярлик з робочого столу
echo.
echo Проект включає веб-інтерфейс Gradio для зручного завантаження
echo Для оновлення проекту запустіть цей бат-файл знову
echo.

echo Натисніть будь-яку клавішу для завершення...
pause >nul
