# 🐳 Docker Setup for MOP Generator

Complete Docker configuration for running MOP Generator with PostgreSQL database, including development and production environments.

## 🚀 Quick Start

### **Option 1: One-Command Full Stack**
```bash
# Make script executable and run
chmod +x docker-deploy.sh
./docker-deploy.sh
# Choose option 1 for full stack deployment
```

### **Option 2: Manual Docker Compose**
```bash
# Production environment
docker-compose up -d

# Development environment  
docker-compose -f docker-compose.dev.yml up -d
```

### **Option 3: Simple Docker Run**
```bash
# Build and run web app only
docker build -t mop-generator .
docker run -p 8080:8080 mop-generator
```

---

## 📁 Docker Files Overview

| File | Purpose |
|------|---------|
| `Dockerfile` | Production container with security & optimization |
| `Dockerfile.dev` | Development container with hot reload |
| `docker-compose.yml` | Full production stack (Web + DB + Redis) |
| `docker-compose.dev.yml` | Development stack with hot reload |
| `docker-deploy.sh` | Interactive deployment script |
| `.env.example` | Environment variables template |

---

## 🏗️ Architecture

```
┌─────────────────────┐    ┌─────────────────────┐    ┌─────────────────────┐
│   Load Balancer     │    │    Web Container    │    │  Database Container │
│   (nginx/traefik)   │───▶│   MOP Generator     │───▶│    PostgreSQL 15    │
│   Port: 80/443      │    │   Port: 8080        │    │    Port: 5432       │
└─────────────────────┘    └─────────────────────┘    └─────────────────────┘
                                      │
                           ┌─────────────────────┐
                           │   Cache Container   │
                           │     Redis 7         │
                           │   Port: 6379        │
                           └─────────────────────┘
```

---

## 🛠️ Production Deployment

### **Full Stack with Database**
```bash
# Clone and navigate
git clone https://github.com/damarajibri/mop-generator.git
cd mop-generator

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Deploy full stack
docker-compose up -d

# Check status
docker-compose ps
```

### **Environment Variables**
```bash
# Required
DATABASE_URL=postgresql://mop_user:mop_password_2026@postgres:5432/mop_generator
FLASK_SECRET_KEY=your-production-secret-key

# Optional
PORT=8080
MAX_CONTENT_LENGTH=16777216
REDIS_URL=redis://redis:6379/0
```

---

## 🔧 Development Setup

### **Hot Reload Development**
```bash
# Start development stack
docker-compose -f docker-compose.dev.yml up -d

# Access at http://localhost:5000
# Code changes auto-reload
```

### **Local Development with External DB**
```bash
# Start only database
docker-compose up -d postgres

# Run app locally
export DATABASE_URL="postgresql://mop_user:mop_password_2026@localhost:5432/mop_generator"
python app.py
```

---

## 📊 Management Commands

### **Service Management**
```bash
# View all services
docker-compose ps

# View logs
docker-compose logs -f web          # Web app logs
docker-compose logs -f postgres     # Database logs
docker-compose logs -f              # All logs

# Restart services
docker-compose restart web
docker-compose restart postgres

# Scale web services
docker-compose up -d --scale web=3
```

### **Database Management**
```bash
# Connect to database
docker-compose exec postgres psql -U mop_user -d mop_generator

# Backup database
docker-compose exec postgres pg_dump -U mop_user mop_generator > backup.sql

# Restore database
docker-compose exec -T postgres psql -U mop_user -d mop_generator < backup.sql

# Reset database
docker-compose down -v
docker-compose up -d
```

### **File Management**
```bash
# Access web container
docker-compose exec web bash

# Copy files from container
docker cp mop_generator:/app/generated_mops ./local_backup

# View uploaded files
docker-compose exec web ls -la /app/uploads
```

---

## 🔒 Production Security

### **Security Features**
- ✅ Non-root user in container
- ✅ Read-only filesystem where possible  
- ✅ Health checks for all services
- ✅ Resource limits configured
- ✅ Secrets via environment variables
- ✅ PostgreSQL with authentication

### **Recommended Production Setup**
```bash
# Use production secrets
export FLASK_SECRET_KEY=$(openssl rand -base64 32)
export POSTGRES_PASSWORD=$(openssl rand -base64 32)

# Run with resource limits
docker-compose up -d --memory=512m --cpus=1.0
```

---

## 🚀 Scaling & Performance

### **Horizontal Scaling**
```bash
# Multiple web containers behind load balancer
docker-compose up -d --scale web=4

# Use nginx for load balancing
# See nginx.conf example below
```

### **Performance Optimization**
```yaml
# In docker-compose.yml
services:
  web:
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: '1.0'
        reservations:
          memory: 256M
          cpus: '0.5'
```

---

## 🔍 Troubleshooting

### **Common Issues**

**Port already in use:**
```bash
# Kill process using port
sudo lsof -ti:8080 | xargs kill -9

# Or change port in docker-compose.yml
ports:
  - "8081:8080"  # Use port 8081 instead
```

**Database connection failed:**
```bash
# Check database status
docker-compose logs postgres

# Ensure database is ready
docker-compose exec postgres pg_isready -U mop_user
```

**Container won't start:**
```bash
# Check container logs
docker-compose logs web

# Rebuild containers
docker-compose build --no-cache
docker-compose up -d
```

### **Health Checks**
```bash
# Check application health
curl http://localhost:8080/

# Check database health
docker-compose exec postgres pg_isready -U mop_user -d mop_generator

# Check all container health
docker ps --format "table {{.Names}}\t{{.Status}}"
```

---

## 🌐 Load Balancer Setup (nginx)

```nginx
# nginx.conf for production load balancing
upstream mop_generator {
    server localhost:8080;
    server localhost:8081;
    server localhost:8082;
}

server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://mop_generator;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

---

## 📈 Monitoring & Logs

### **Container Monitoring**
```bash
# Resource usage
docker stats

# System events
docker system events

# Container inspection
docker-compose exec web docker inspect mop_generator
```

### **Log Aggregation**
```yaml
# Add to docker-compose.yml for centralized logging
logging:
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"
```

---

## 🎯 Quick Commands Reference

```bash
# 🚀 Start everything
./docker-deploy.sh  # Interactive
docker-compose up -d  # Direct

# 🔍 Check status  
docker-compose ps
docker-compose logs -f

# 🛑 Stop everything
docker-compose down
./docker-deploy.sh  # Option 4

# 🧹 Clean up
docker-compose down -v
docker system prune -f

# 📊 Access services
# Web: http://localhost:8080
# DB:  postgresql://mop_user:mop_password_2026@localhost:5432/mop_generator
```

**🎊 Your MOP Generator is now fully containerized and production-ready!**