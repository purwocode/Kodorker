#!/bin/bash
# 🚀 Run Both Scraper & Admin Panel Together
# This script starts the scraper and dashboard in separate processes

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  🚀 DuckDuckGo Scraper + Admin Panel                       ║"
echo "║     Run Scraper & Monitor Dashboard                        ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Check if we're in the right directory
if [ ! -f "ddg_scraper.py" ]; then
    echo "❌ Error: ddg_scraper.py not found!"
    echo "📍 Please run this from the DORKER directory"
    exit 1
fi

echo "✅ Starting services..."
echo ""

# Start Python scraper in background
echo "🔵 Starting Python Scraper..."
python run_infinite_search.py &
SCRAPER_PID=$!
echo "   PID: $SCRAPER_PID"
echo ""

# Wait a bit for scraper to start
sleep 3

# Start admin panel
echo "🟢 Starting Admin Dashboard..."
cd admin-panel
npm run dev &
DASHBOARD_PID=$!
echo "   PID: $DASHBOARD_PID"
echo ""

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  ✨ Both services are running!                             ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "📊 Dashboard URL:  http://localhost:3000"
echo "🔍 Scraper:        Running (PID: $SCRAPER_PID)"
echo "🔴 Dashboard:      Running (PID: $DASHBOARD_PID)"
echo ""
echo "📋 Commands:"
echo "   • Press Ctrl+C to stop services"
echo "   • Dashboard auto-refreshes every 30 seconds"
echo "   • Scraper saves results to Supabase automatically"
echo ""
echo "🎯 Tips:"
echo "   • Leave this running to monitor scraper in real-time"
echo "   • Open http://localhost:3000 in your browser"
echo "   • Press Ctrl+C in scraper terminal to stop infinite search"
echo ""

# Keep the script running
wait
