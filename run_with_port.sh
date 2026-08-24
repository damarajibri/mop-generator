#!/bin/bash
# MOP Generator - Port Launcher Script

echo "🚀 MOP Generator - Port Selection"
echo "================================="
echo ""
echo "Available port options:"
echo "1) Port 3000 (Development)"
echo "2) Port 5000 (Default Flask)"
echo "3) Port 8080 (Alternative)"
echo "4) Port 9000 (High port)"
echo "5) Custom port"
echo ""

read -p "Select option (1-5): " choice

case $choice in
    1)
        echo "🌐 Starting on port 3000..."
        PORT=3000 python3 app.py
        ;;
    2)
        echo "🌐 Starting on port 5000..."
        PORT=5000 python3 app.py
        ;;
    3)
        echo "🌐 Starting on port 8080..."
        PORT=8080 python3 app.py
        ;;
    4)
        echo "🌐 Starting on port 9000..."
        PORT=9000 python3 app.py
        ;;
    5)
        read -p "Enter custom port number: " custom_port
        if [[ $custom_port =~ ^[0-9]+$ ]] && [ $custom_port -ge 1024 ] && [ $custom_port -le 65535 ]; then
            echo "🌐 Starting on port $custom_port..."
            PORT=$custom_port python3 app.py
        else
            echo "❌ Invalid port number. Please use 1024-65535"
            exit 1
        fi
        ;;
    *)
        echo "❌ Invalid selection"
        exit 1
        ;;
esac