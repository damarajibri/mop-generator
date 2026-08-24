#!/bin/bash

# 🐳 MOP Generator - Docker Deployment Script
# Complete setup with database and web application

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "🐳 MOP Generator - Docker Deployment"
echo "===================================="
echo -e "${NC}"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not installed. Please install Docker first:${NC}"
    echo "   https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is available
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo -e "${RED}❌ Docker Compose is not available. Please install Docker Compose.${NC}"
    exit 1
fi

# Function to use docker-compose or docker compose
docker_compose_cmd() {
    if command -v docker-compose &> /dev/null; then
        docker-compose "$@"
    else
        docker compose "$@"
    fi
}

echo -e "${YELLOW}📋 Deployment Options:${NC}"
echo "1. 🚀 Full Stack (Web + Database + Redis)"
echo "2. 🌐 Web Only (External Database)"
echo "3. 🗄️ Database Only"
echo "4. 🛑 Stop All Services"
echo "5. 🧹 Clean Up (Remove containers and volumes)"
echo "6. 📊 View Logs"
echo ""
read -p "Choose an option (1-6): " choice

case $choice in
    1)
        echo -e "${GREEN}🚀 Starting Full Stack Deployment...${NC}"
        
        # Create .env file if it doesn't exist
        if [ ! -f .env ]; then
            echo -e "${YELLOW}📝 Creating .env file...${NC}"
            cp .env.example .env
        fi
        
        # Create necessary directories
        mkdir -p uploads generated_mops
        
        # Build and start services
        echo -e "${BLUE}🔨 Building containers...${NC}"
        docker_compose_cmd build --no-cache
        
        echo -e "${BLUE}🚀 Starting services...${NC}"
        docker_compose_cmd up -d
        
        # Wait for services to be ready
        echo -e "${YELLOW}⏳ Waiting for services to be ready...${NC}"
        sleep 10
        
        # Check service health
        if docker_compose_cmd ps | grep -q "Up"; then
            echo -e "${GREEN}✅ Services started successfully!${NC}"
            echo ""
            echo -e "${GREEN}🌐 MOP Generator is now running at:${NC}"
            echo -e "   ${BLUE}http://localhost:8080${NC}"
            echo ""
            echo -e "${YELLOW}📊 Service Status:${NC}"
            docker_compose_cmd ps
            echo ""
            echo -e "${YELLOW}📝 To view logs: ${NC}./docker-deploy.sh (option 6)"
            echo -e "${YELLOW}🛑 To stop: ${NC}./docker-deploy.sh (option 4)"
        else
            echo -e "${RED}❌ Some services failed to start. Check logs:${NC}"
            docker_compose_cmd logs
        fi
        ;;
        
    2)
        echo -e "${GREEN}🌐 Starting Web Application Only...${NC}"
        
        # Get database URL
        read -p "Enter DATABASE_URL (or press enter for file storage): " db_url
        
        if [ -n "$db_url" ]; then
            export DATABASE_URL="$db_url"
        fi
        
        # Build and run only web service
        docker build -t mop-generator .
        
        docker run -d \
            --name mop_generator_web \
            -p 8080:8080 \
            -e DATABASE_URL="$DATABASE_URL" \
            -e FLASK_SECRET_KEY="mop-generator-secret-$(date +%s)" \
            -v "$(pwd)/uploads:/app/uploads" \
            -v "$(pwd)/generated_mops:/app/generated_mops" \
            mop-generator
            
        echo -e "${GREEN}✅ Web application started!${NC}"
        echo -e "${BLUE}🌐 Access at: http://localhost:8080${NC}"
        ;;
        
    3)
        echo -e "${GREEN}🗄️ Starting Database Only...${NC}"
        docker_compose_cmd up -d postgres
        
        echo -e "${GREEN}✅ PostgreSQL database started!${NC}"
        echo -e "${BLUE}📍 Connection: postgresql://mop_user:mop_password_2026@localhost:5432/mop_generator${NC}"
        ;;
        
    4)
        echo -e "${YELLOW}🛑 Stopping all services...${NC}"
        docker_compose_cmd down
        
        # Also stop standalone containers
        docker stop mop_generator_web 2>/dev/null || true
        docker rm mop_generator_web 2>/dev/null || true
        
        echo -e "${GREEN}✅ All services stopped.${NC}"
        ;;
        
    5)
        echo -e "${YELLOW}🧹 Cleaning up containers and volumes...${NC}"
        
        read -p "⚠️  This will delete all data. Are you sure? (y/N): " confirm
        if [[ $confirm == [yY] || $confirm == [yY][eE][sS] ]]; then
            docker_compose_cmd down -v
            docker system prune -f
            docker volume prune -f
            
            # Remove standalone containers
            docker stop mop_generator_web 2>/dev/null || true
            docker rm mop_generator_web 2>/dev/null || true
            docker rmi mop-generator 2>/dev/null || true
            
            echo -e "${GREEN}✅ Cleanup completed.${NC}"
        else
            echo -e "${YELLOW}❌ Cleanup cancelled.${NC}"
        fi
        ;;
        
    6)
        echo -e "${BLUE}📊 Service Logs:${NC}"
        echo ""
        
        if docker_compose_cmd ps -q | wc -l | grep -q "0"; then
            echo -e "${RED}❌ No services are running.${NC}"
        else
            echo -e "${YELLOW}Choose logs to view:${NC}"
            echo "1. All services"
            echo "2. Web application only"
            echo "3. Database only"
            echo "4. Redis only"
            echo ""
            read -p "Choose (1-4): " log_choice
            
            case $log_choice in
                1) docker_compose_cmd logs -f ;;
                2) docker_compose_cmd logs -f web ;;
                3) docker_compose_cmd logs -f postgres ;;
                4) docker_compose_cmd logs -f redis ;;
                *) docker_compose_cmd logs -f ;;
            esac
        fi
        ;;
        
    *)
        echo -e "${RED}❌ Invalid choice. Please run the script again.${NC}"
        exit 1
        ;;
esac

echo ""
echo -e "${BLUE}📚 Need help?${NC}"
echo -e "   ${YELLOW}• Check logs: ${NC}docker-compose logs -f"
echo -e "   ${YELLOW}• Access database: ${NC}docker-compose exec postgres psql -U mop_user -d mop_generator"
echo -e "   ${YELLOW}• Restart services: ${NC}docker-compose restart"
echo -e "   ${YELLOW}• View containers: ${NC}docker-compose ps"