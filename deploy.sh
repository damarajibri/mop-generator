#!/bin/bash

# 🚀 MOP Generator - Quick Deploy Script
# Choose your preferred hosting platform

echo "🚀 MOP Generator - Quick Deploy"
echo "================================"
echo ""
echo "Choose your hosting platform:"
echo "1. Railway (Recommended - Easiest)"
echo "2. Heroku (Traditional & Reliable)" 
echo "3. Render (Modern Alternative)"
echo "4. Docker (Local/Custom)"
echo ""
read -p "Enter your choice (1-4): " choice

case $choice in
    1)
        echo "🚂 Deploying to Railway..."
        echo ""
        echo "Steps:"
        echo "1. Go to https://railway.app"
        echo "2. Click 'Start a New Project'"
        echo "3. Select 'Deploy from GitHub repo'"
        echo "4. Choose 'damarajibri/mop-generator'"
        echo "5. Add PostgreSQL service"
        echo "6. Your app will be live in ~2 minutes!"
        echo ""
        echo "🌐 Your app will be available at: https://your-app-name.railway.app"
        ;;
    2)
        echo "🌿 Deploying to Heroku..."
        if command -v heroku &> /dev/null; then
            echo "Creating Heroku app..."
            read -p "Enter app name (or press enter for auto-generated): " app_name
            
            if [ -z "$app_name" ]; then
                heroku create
            else
                heroku create $app_name
            fi
            
            echo "Adding PostgreSQL database..."
            heroku addons:create heroku-postgresql:mini
            
            echo "Deploying to Heroku..."
            git push heroku main
            
            echo "Initializing database..."
            heroku run python init_db.py
            
            echo "✅ Deployment complete!"
            heroku open
        else
            echo "❌ Heroku CLI not found. Install it first:"
            echo "brew install heroku/brew/heroku"
            echo ""
            echo "Then run this script again."
        fi
        ;;
    3)
        echo "🎨 Deploying to Render..."
        echo ""
        echo "Steps:"
        echo "1. Go to https://render.com"
        echo "2. Connect your GitHub account"
        echo "3. Create new Web Service"
        echo "4. Select 'damarajibri/mop-generator'"
        echo "5. Create PostgreSQL database"
        echo "6. Set DATABASE_URL environment variable"
        echo "7. Deploy!"
        echo ""
        echo "Environment Variables needed:"
        echo "DATABASE_URL=postgresql://... (from database)"
        echo "PYTHON_VERSION=3.11.5"
        ;;
    4)
        echo "🐳 Building Docker container..."
        if command -v docker &> /dev/null; then
            echo "Building image..."
            docker build -t mop-generator .
            
            echo "Running container..."
            docker run -p 8080:8080 -e DATABASE_URL=sqlite:///mop.db mop-generator
            
            echo "✅ Container running!"
            echo "🌐 Access at: http://localhost:8080"
        else
            echo "❌ Docker not found. Install Docker first:"
            echo "https://docs.docker.com/get-docker/"
        fi
        ;;
    *)
        echo "❌ Invalid choice. Please run the script again."
        exit 1
        ;;
esac

echo ""
echo "📚 Need help? Check DEPLOYMENT.md for detailed instructions"
echo "🐛 Issues? Visit: https://github.com/damarajibri/mop-generator/issues"