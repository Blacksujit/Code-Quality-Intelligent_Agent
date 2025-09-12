#!/bin/bash

# 🚀 Code Quality Intelligence Agent - Deployment Script
# This script provides multiple deployment options for the application

set -e

echo "🚀 Code Quality Intelligence Agent - Deployment Script"
echo "=================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is installed
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    print_success "Docker is available"
}

# Check if Docker Compose is installed
check_docker_compose() {
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    print_success "Docker Compose is available"
}

# Local Docker deployment
deploy_local_docker() {
    print_status "Deploying locally with Docker..."
    
    check_docker
    check_docker_compose
    
    # Build and run with docker-compose
    docker-compose up --build -d
    
    print_success "Application deployed locally!"
    print_status "Access the application at: http://localhost:8501"
    print_status "To stop: docker-compose down"
}

# Production Docker deployment
deploy_production_docker() {
    print_status "Deploying production Docker setup..."
    
    check_docker
    check_docker_compose
    
    # Build and run with production profile
    docker-compose --profile production up --build -d
    
    print_success "Production application deployed!"
    print_status "Access the application at: http://localhost:8501"
    print_status "Redis cache available at: http://localhost:6379"
    print_status "To stop: docker-compose --profile production down"
}

# Streamlit Cloud deployment
deploy_streamlit_cloud() {
    print_status "Preparing for Streamlit Cloud deployment..."
    
    # Check if .streamlit/secrets.toml exists
    if [ ! -f ".streamlit/secrets.toml" ]; then
        print_warning "Creating .streamlit/secrets.toml template..."
        mkdir -p .streamlit
        cat > .streamlit/secrets.toml << EOF
# Streamlit Cloud Secrets
# Add your API keys here for production deployment

# DeepSeek API Key (optional)
DEEPSEEK_API_KEY = "your_deepseek_api_key_here"

# Hugging Face Token (optional)
HF_TOKEN = "your_huggingface_token_here"

# Hugging Face Inference API Token (optional)
HUGGINGFACEHUB_API_TOKEN = "your_hf_inference_token_here"
EOF
        print_warning "Please update .streamlit/secrets.toml with your actual API keys"
    fi
    
    print_success "Ready for Streamlit Cloud deployment!"
    print_status "1. Push your code to GitHub"
    print_status "2. Go to https://share.streamlit.io"
    print_status "3. Connect your GitHub repository"
    print_status "4. Deploy with the following settings:"
    print_status "   - Main file path: src/cq_agent/web/app.py"
    print_status "   - Python version: 3.11"
}

# Railway deployment
deploy_railway() {
    print_status "Preparing for Railway deployment..."
    
    # Check if Railway CLI is installed
    if ! command -v railway &> /dev/null; then
        print_warning "Railway CLI not found. Installing..."
        npm install -g @railway/cli
    fi
    
    print_success "Ready for Railway deployment!"
    print_status "1. Run: railway login"
    print_status "2. Run: railway init"
    print_status "3. Run: railway up"
    print_status "4. Set environment variables in Railway dashboard"
}

# Render deployment
deploy_render() {
    print_status "Preparing for Render deployment..."
    
    print_success "Ready for Render deployment!"
    print_status "1. Push your code to GitHub"
    print_status "2. Go to https://render.com"
    print_status "3. Create a new Web Service"
    print_status "4. Connect your GitHub repository"
    print_status "5. Use the following settings:"
    print_status "   - Build Command: pip install -e . && pip install transformers torch --index-url https://download.pytorch.org/whl/cpu"
    print_status "   - Start Command: streamlit run src/cq_agent/web/app.py --server.port=\$PORT --server.address=0.0.0.0 --server.headless=true"
    print_status "   - Python Version: 3.11"
}

# Fly.io deployment (Free tier available)
deploy_fly() {
    print_status "Preparing for Fly.io deployment..."
    
    # Check if Fly CLI is installed
    if ! command -v fly &> /dev/null; then
        print_warning "Fly CLI not found. Installing..."
        print_status "Visit: https://fly.io/docs/hands-on/install-flyctl/"
    fi
    
    print_success "Ready for Fly.io deployment!"
    print_status "1. Run: fly auth signup"
    print_status "2. Run: fly launch"
    print_status "3. Run: fly secrets set DEEPSEEK_API_KEY=your_key"
    print_status "4. Run: fly secrets set HF_TOKEN=your_token"
    print_status "5. Run: fly deploy"
}

# Vercel deployment (Free tier)
deploy_vercel() {
    print_status "Preparing for Vercel deployment..."
    
    # Check if Vercel CLI is installed
    if ! command -v vercel &> /dev/null; then
        print_warning "Vercel CLI not found. Installing..."
        npm install -g vercel
    fi
    
    print_success "Ready for Vercel deployment!"
    print_status "1. Run: vercel login"
    print_status "2. Run: vercel --prod"
    print_status "3. Set environment variables in Vercel dashboard"
}

# Show deployment options
show_options() {
    echo ""
    echo "🎯 Available Deployment Options:"
    echo "================================"
    echo "1. 🐳 Local Docker (Development)"
    echo "2. 🏭 Production Docker (with Redis)"
    echo "3. ☁️  Streamlit Cloud (Free)"
    echo "4. 🚂 Railway (Free tier)"
    echo "5. 🎨 Render (Free tier)"
    echo "6. 🪰 Fly.io (Free tier)"
    echo "7. ▲ Vercel (Free tier)"
    echo "8. 📋 Show all options"
    echo ""
}

# Main deployment function
main() {
    case "${1:-}" in
        "local")
            deploy_local_docker
            ;;
        "production")
            deploy_production_docker
            ;;
        "streamlit")
            deploy_streamlit_cloud
            ;;
        "railway")
            deploy_railway
            ;;
        "render")
            deploy_render
            ;;
        "fly")
            deploy_fly
            ;;
        "vercel")
            deploy_vercel
            ;;
        "help"|"-h"|"--help")
            show_options
            ;;
        *)
            show_options
            echo "Usage: $0 [local|production|streamlit|railway|render|fly|vercel|help]"
            echo ""
            echo "Examples:"
            echo "  $0 local          # Deploy locally with Docker"
            echo "  $0 streamlit      # Prepare for Streamlit Cloud"
            echo "  $0 railway        # Deploy to Railway"
            ;;
    esac
}

# Run main function
main "$@"
