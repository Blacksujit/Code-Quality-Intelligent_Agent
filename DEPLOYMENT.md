# 🚀 Deployment Guide - Code Quality Intelligence Agent

This guide provides step-by-step instructions for deploying the Code Quality Intelligence Agent to various free platforms.

## 🎯 Free Deployment Options

| Platform | Free Tier | Best For | Setup Time |
|----------|-----------|----------|------------|
| **☁️ Streamlit Cloud** | ✅ Unlimited | Quick demos | 5 minutes |
| **🚂 Railway** | ✅ 500 hours/month | Development | 10 minutes |
| **🎨 Render** | ✅ 750 hours/month | Production | 15 minutes |
| **🪰 Fly.io** | ✅ 3 apps, 256MB RAM | Scalable apps | 20 minutes |
| **▲ Vercel** | ✅ 100GB bandwidth | Static + API | 10 minutes |

---

## ☁️ Streamlit Cloud (Recommended for Demos)

**Best for**: Quick demos, sharing with others, zero configuration

### 📋 Prerequisites
- GitHub repository with your code
- Streamlit Cloud account (free)

### 🚀 Deployment Steps

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Connect your GitHub repository
   - Set main file path: `src/cq_agent/web/app.py`
   - Click "Deploy!"

3. **Configure Secrets (Optional)**
   - In Streamlit Cloud dashboard, go to "Settings" → "Secrets"
   - Add your API keys:
   ```toml
   DEEPSEEK_API_KEY = "your_key_here"
   HF_TOKEN = "your_token_here"
   ```

**✅ Done!** Your app will be live at `https://your-app-name.streamlit.app`

---

## 🚂 Railway (Great for Development)

**Best for**: Development, testing, continuous deployment

### 📋 Prerequisites
- GitHub repository
- Railway account (free)

### 🚀 Deployment Steps

1. **Install Railway CLI**
   ```bash
   npm install -g @railway/cli
   ```

2. **Deploy**
   ```bash
   railway login
   railway init
   railway up
   ```

3. **Set Environment Variables**
   ```bash
   railway variables set DEEPSEEK_API_KEY=your_key
   railway variables set HF_TOKEN=your_token
   ```

**✅ Done!** Your app will be live at `https://your-app-name.railway.app`

---

## 🎨 Render (Production Ready)

**Best for**: Production applications, reliable hosting

### 📋 Prerequisites
- GitHub repository
- Render account (free)

### 🚀 Deployment Steps

1. **Connect Repository**
   - Go to [render.com](https://render.com)
   - Click "New" → "Web Service"
   - Connect your GitHub repository

2. **Configure Service**
   - **Name**: `code-quality-agent`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -e . && pip install transformers torch --index-url https://download.pytorch.org/whl/cpu`
   - **Start Command**: `streamlit run src/cq_agent/web/app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true`

3. **Set Environment Variables**
   - `DEEPSEEK_API_KEY`: Your DeepSeek API key
   - `HF_TOKEN`: Your Hugging Face token

**✅ Done!** Your app will be live at `https://your-app-name.onrender.com`

---

## 🪰 Fly.io (Scalable)

**Best for**: Scalable applications, global deployment

### 📋 Prerequisites
- Fly.io account (free)
- Fly CLI installed

### 🚀 Deployment Steps

1. **Install Fly CLI**
   ```bash
   # macOS
   brew install flyctl
   
   # Windows
   iwr https://fly.io/install.ps1 -useb | iex
   
   # Linux
   curl -L https://fly.io/install.sh | sh
   ```

2. **Deploy**
   ```bash
   fly auth signup
   fly launch
   fly deploy
   ```

3. **Set Secrets**
   ```bash
   fly secrets set DEEPSEEK_API_KEY=your_key
   fly secrets set HF_TOKEN=your_token
   ```

**✅ Done!** Your app will be live at `https://your-app-name.fly.dev`

---

## ▲ Vercel (API + Static)

**Best for**: API endpoints, static sites with backend

### 📋 Prerequisites
- Vercel account (free)
- Vercel CLI (optional)

### 🚀 Deployment Steps

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Deploy**
   ```bash
   vercel login
   vercel --prod
   ```

3. **Set Environment Variables**
   - Go to Vercel dashboard
   - Project Settings → Environment Variables
   - Add your API keys

**✅ Done!** Your app will be live at `https://your-app-name.vercel.app`

---

## 🐳 Local Docker Deployment

**Best for**: Local development, testing, self-hosting

### 🚀 Quick Start

```bash
# Clone and build
git clone https://github.com/your-username/code-quality-agent.git
cd code-quality-agent

# Build and run
docker-compose up --build

# Access at http://localhost:8501
```

### 🔧 Production Setup

```bash
# Run with Redis for caching
docker-compose --profile production up --build -d

# Check logs
docker-compose logs -f

# Stop services
docker-compose down
```

---

## 🔧 Environment Variables

### Required for AI Features
```bash
DEEPSEEK_API_KEY=your_deepseek_api_key
HF_TOKEN=your_huggingface_token
HUGGINGFACEHUB_API_TOKEN=your_hf_inference_token
```

### Optional Performance Tuning
```bash
MAX_FILES=1000
WORKER_THREADS=4
CACHE_TTL=3600
```

---

## 🚨 Troubleshooting

### Common Issues

#### **Port Already in Use**
```bash
# Find process using port 8501
lsof -i :8501

# Kill process
kill -9 <PID>

# Or use different port
streamlit run src/cq_agent/web/app.py --server.port 8502
```

#### **Memory Issues**
```bash
# Reduce max files for large repos
export MAX_FILES=500

# Use fast mode
streamlit run src/cq_agent/web/app.py --server.port 8501
```

#### **AI Model Loading Issues**
```bash
# Clear model cache
rm -rf ~/.cache/huggingface/

# Use smaller model
export LOCAL_MODEL="microsoft/DialoGPT-small"
```

### Platform-Specific Issues

#### **Streamlit Cloud**
- **Issue**: App not loading
- **Solution**: Check main file path is correct
- **Issue**: Secrets not working
- **Solution**: Ensure secrets.toml format is correct

#### **Railway**
- **Issue**: Build failing
- **Solution**: Check Python version in railway.json
- **Issue**: App sleeping
- **Solution**: Upgrade to paid plan or use cron job

#### **Render**
- **Issue**: App sleeping after 15 minutes
- **Solution**: This is normal for free tier
- **Issue**: Build timeout
- **Solution**: Optimize dependencies, use smaller models

---

## 📊 Performance Optimization

### For Large Repositories

1. **Enable Fast Mode**
   ```bash
   # In web interface, check "Fast scan (large repos)"
   # Or CLI: --max-files 1000
   ```

2. **Use Incremental Caching**
   ```bash
   # Default behavior, files are cached based on modification time
   ```

3. **Optimize AI Models**
   ```bash
   # Use smaller models for faster inference
   export LOCAL_MODEL="microsoft/DialoGPT-small"
   ```

### For Production

1. **Use Redis Caching**
   ```bash
   docker-compose --profile production up
   ```

2. **Set Resource Limits**
   ```bash
   # In docker-compose.yml
   deploy:
     resources:
       limits:
         memory: 2G
         cpus: '1.0'
   ```

3. **Enable Health Checks**
   ```bash
   # Already configured in Dockerfile
   HEALTHCHECK --interval=30s --timeout=30s
   ```

---

## 🎯 Deployment Checklist

### Before Deployment
- [ ] Code pushed to GitHub
- [ ] All tests passing
- [ ] Environment variables documented
- [ ] README updated
- [ ] Dependencies optimized

### After Deployment
- [ ] App loads successfully
- [ ] AI features working (if configured)
- [ ] Performance acceptable
- [ ] Error monitoring set up
- [ ] Documentation updated with live URL

---

## 🆘 Getting Help

- **📖 Documentation**: Check this guide and README.md
- **🐛 Issues**: Create GitHub issue with deployment logs
- **💬 Discussions**: Use GitHub Discussions for questions
- **📧 Support**: Contact maintainers for urgent issues

---

**🚀 Happy Deploying!** Choose the platform that best fits your needs and get your Code Quality Intelligence Agent live in minutes!
