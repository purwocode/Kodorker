@echo off
REM 🚀 Run Both Scraper & Admin Panel Together (Windows)
REM This batch script starts the scraper and dashboard in separate windows

setlocal enabledelayedexpansion

cls
echo ╔════════════════════════════════════════════════════════════╗
echo ║  🚀 DuckDuckGo Scraper + Admin Panel                       ║
echo ║     Run Scraper ^& Monitor Dashboard                         ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Check if we're in the right directory
if not exist "ddg_scraper.py" (
    echo ❌ Error: ddg_scraper.py not found!
    echo 📍 Please run this batch file from the DORKER directory
    echo.
    pause
    exit /b 1
)

echo ✅ Starting services...
echo.

REM Start Python scraper in new window
echo 🔵 Starting Python Scraper...
start cmd /k "title Scraper & python run_infinite_search.py"
echo    Scraper window opened
echo.

REM Wait a bit for scraper to start
timeout /t 3 /nobreak

REM Start admin panel in new window
echo 🟢 Starting Admin Dashboard...
cd admin-panel
start cmd /k "title Admin Panel & npm run dev"
echo    Dashboard window opened
cd ..
echo.

echo ╔════════════════════════════════════════════════════════════╗
echo ║  ✨ Both services are running!                             ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo 📊 Dashboard URL:  http://localhost:3000
echo 🔵 Scraper:        Running in new window
echo 🟢 Dashboard:      Running in new window
echo.
echo 📋 Instructions:
echo    • Two new windows will open (Scraper + Dashboard)
echo    • Open http://localhost:3000 in your browser
echo    • Dashboard auto-refreshes every 30 seconds
echo    • Scraper saves results to Supabase automatically
echo.
echo 🎯 Tips:
echo    • Leave both windows open to monitor in real-time
echo    • Press Ctrl+C in scraper window to stop infinite search
echo    • You can close this window - services keep running
echo.
echo ✋ Keep this window open to see status...
pause
