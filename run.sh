#!/bin/bash
# Quick Start Script cho Discord Ticket Bot (Linux/Mac)

echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║          🎫 Discord Ticket Bot - Quick Start             ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python không được cài đặt! Vui lòng cài đặt Python 3.8+"
    exit 1
fi

echo "✅ Python đã được phát hiện"

# Check requirements
if [ ! -f "requirements.txt" ]; then
    echo "❌ Không tìm thấy requirements.txt"
    exit 1
fi

# Install dependencies
echo ""
echo "📦 Cài đặt dependencies..."
pip install -r requirements.txt

# Setup
echo ""
echo "⚙️ Chạy setup..."
python3 setup.py

# Run bot
echo ""
echo "🚀 Khởi động bot..."
echo ""
python3 main.py
