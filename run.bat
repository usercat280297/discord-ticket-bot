@echo off
REM Quick Start Script cho Discord Ticket Bot (Windows)

echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║          🎫 Discord Ticket Bot - Quick Start             ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python không được cài đặt! Vui lòng cài đặt Python 3.8+
    pause
    exit /b 1
)

echo ✅ Python đã được phát hiện

REM Check requirements
if not exist "requirements.txt" (
    echo ❌ Không tìm thấy requirements.txt
    pause
    exit /b 1
)

REM Install dependencies
echo.
echo 📦 Cài đặt dependencies...
pip install -r requirements.txt

REM Setup
echo.
echo ⚙️ Chạy setup...
python setup.py

REM Run bot
echo.
echo 🚀 Khởi động bot...
echo.
python main.py

pause
