#!/bin/bash

# 🐳 Docker Health Check and Setup Script

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🐳 Docker Environment Check${NC}"
echo "=========================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not installed${NC}"
    echo ""
    echo -e "${YELLOW}📥 Install Docker:${NC}"
    echo "  • macOS: Download Docker Desktop from https://docker.com/products/docker-desktop"
    echo "  • Linux: sudo apt install docker.io docker-compose"
    echo "  • Windows: Download Docker Desktop"
    exit 1
fi

echo -e "${GREEN}✅ Docker is installed${NC}"

# Check if Docker daemon is running
if ! docker info >/dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  Docker daemon is not running${NC}"
    echo ""
    echo -e "${YELLOW}🚀 Starting Docker:${NC}"
    
    # Try to start Docker on macOS
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "  Starting Docker Desktop on macOS..."
        open -a Docker
        echo "  Please wait for Docker Desktop to start, then run this script again."
        echo "  You'll see the Docker icon in your menu bar when it's ready."
        exit 1
    fi
    
    # Try to start Docker on Linux
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "  Attempting to start Docker service..."
        sudo systemctl start docker
        sudo systemctl enable docker
    fi
    
    # Wait a bit and check again
    sleep 5
    if ! docker info >/dev/null 2>&1; then
        echo -e "${RED}❌ Could not start Docker daemon${NC}"
        echo "  Please start Docker manually and try again."
        exit 1
    fi
fi

echo -e "${GREEN}✅ Docker daemon is running${NC}"

# Check Docker Compose
if command -v docker-compose &> /dev/null; then
    echo -e "${GREEN}✅ Docker Compose is available${NC}"
    COMPOSE_CMD="docker-compose"
elif docker compose version >/dev/null 2>&1; then
    echo -e "${GREEN}✅ Docker Compose (v2) is available${NC}"
    COMPOSE_CMD="docker compose"
else
    echo -e "${RED}❌ Docker Compose is not available${NC}"
    echo "  Please install Docker Compose"
    exit 1
fi

echo ""
echo -e "${GREEN}🎉 Docker environment is ready!${NC}"
echo ""

# Show current Docker info
echo -e "${BLUE}📊 Docker Information:${NC}"
docker --version
$COMPOSE_CMD --version
echo "Docker Root Dir: $(docker info --format '{{.DockerRootDir}}')"
echo "Available Memory: $(docker system df --format 'table {{.Type}}\t{{.TotalCount}}\t{{.Size}}')"

echo ""
echo -e "${YELLOW}🚀 Ready to deploy MOP Generator!${NC}"
echo ""
echo "Next steps:"
echo "  1. Run: ./docker-deploy.sh"
echo "  2. Choose option 1 for full stack"
echo "  3. Access at: http://localhost:8080"

# Optional: Test build
read -p "Test Docker build now? (y/N): " test_build
if [[ $test_build == [yY] ]]; then
    echo ""
    echo -e "${BLUE}🔨 Testing Docker build...${NC}"
    if docker build -t mop-generator-test . >/dev/null 2>&1; then
        echo -e "${GREEN}✅ Docker build successful!${NC}"
        docker rmi mop-generator-test >/dev/null 2>&1
    else
        echo -e "${RED}❌ Docker build failed${NC}"
        echo "Check Dockerfile and requirements.txt"
    fi
fi