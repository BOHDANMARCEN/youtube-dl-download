@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ===============================================
echo    YouTube-DL Updater
echo ===============================================
echo.

set "PROJECT_DIR=C:\youtube-dl"

:: Перевірка чи існує директорія проекту
if not exist "%PROJECT_DIR%" (
    echo [ERROR] Проект не знайдено в %PROJECT_DIR%
    echo Спочатку запустіть install_youtube_dl.bat
    pause
    exit /b 1
)

echo [INFO] Оновлення проекту з GitHub...
cd /d "%PROJECT_DIR%"

:: Оновлення з GitHub
git pull origin main
if %errorLevel% neq 0 (
    echo [ERROR] Не вдалося оновити проект
    pause
    exit /b 1
)

echo [OK] Проект успішно оновлено

:: Оновлення залежностей
echo [INFO] Оновлення залежностей...
if exist "requirements.txt" (
    pip install -r requirements.txt --upgrade
    echo [OK] Залежності оновлено
)

echo.
echo ===============================================
echo    Оновлення завершено!
echo ===============================================
echo.

echo Натисніть будь-яку клавішу для завершення...
pause >nul
