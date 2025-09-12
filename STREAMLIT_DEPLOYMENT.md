# ☁️ Streamlit Cloud Deployment Guide

## 🚀 Quick Deployment Steps

### 1. **Prepare Your Repository**
```bash
# Ensure your code is pushed to GitHub
git add .
git commit -m "Ready for Streamlit Cloud deployment"
git push origin main
```

### 2. **Deploy on Streamlit Cloud**
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click **"New app"**
3. Connect your GitHub repository
4. Set **Main file path**: `src/cq_agent/web/app.py`
5. Click **"Deploy!"**

### 3. **Configure Secrets (Optional)**
In the Streamlit Cloud dashboard:

1. Go to **"Settings"** → **"Secrets"**
2. Paste the configuration below
3. Replace placeholder values with your actual keys
4. Click **"Save"**

---

## 🔐 Secrets Configuration

Copy this content to Streamlit Cloud's **"Secrets"** section:

```toml
# 🤖 AI API Keys (Optional)
DEEPSEEK_API_KEY = "your_deepseek_api_key_here"
HF_TOKEN = "your_huggingface_token_here"
HUGGINGFACEHUB_API_TOKEN = "your_hf_hub_token_here"

# 🚀 Performance Settings
MAX_FILES = 1000
WORKER_THREADS = 4
CACHE_TTL = 3600

# 🎯 Feature Flags
ENABLE_AI = true
ENABLE_LOCAL_LLM = true
ENABLE_CACHING = true
ENABLE_PARALLEL = true

# 🔧 Configuration
DEBUG = false
LOG_LEVEL = "INFO"
ENVIRONMENT = "production"
```

---

## 🎯 Minimal Configuration (No AI)

If you don't have API keys, use this minimal configuration:

```toml
# 🚀 Basic Performance Settings
MAX_FILES = 1000
WORKER_THREADS = 4

# 🎯 Feature Flags
ENABLE_AI = false
ENABLE_LOCAL_LLM = false
ENABLE_CACHING = true
ENABLE_PARALLEL = true

# 🔧 Configuration
DEBUG = false
ENVIRONMENT = "production"
```

---

## 🔑 Getting API Keys

### **DeepSeek API Key**
1. Go to [platform.deepseek.com](https://platform.deepseek.com/)
2. Sign up/Login
3. Go to API Keys section
4. Create new API key
5. Copy the key (starts with `sk-`)

### **Hugging Face Token**
1. Go to [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
2. Sign up/Login
3. Create new token
4. Copy the token (starts with `hf_`)

---

## 🚨 Troubleshooting

### **App Not Loading**
- ✅ Check main file path: `src/cq_agent/web/app.py`
- ✅ Ensure all dependencies are in `pyproject.toml`
- ✅ Check build logs for errors

### **AI Features Not Working**
- ✅ Verify API keys are correct
- ✅ Check secrets are saved (takes ~1 minute to propagate)
- ✅ Ensure keys have proper permissions

### **Performance Issues**
- ✅ Reduce `MAX_FILES` for large repositories
- ✅ Increase `WORKER_THREADS` for faster processing
- ✅ Enable `ENABLE_CACHING` for repeated analysis

### **Build Failures**
- ✅ Check Python version compatibility
- ✅ Verify all imports are available
- ✅ Review build logs for missing dependencies

---

## 📊 Performance Optimization

### **For Large Repositories**
```toml
# Optimize for large codebases
MAX_FILES = 500
WORKER_THREADS = 8
CACHE_TTL = 7200
ENABLE_CACHING = true
ENABLE_PARALLEL = true
```

### **For Fast Analysis**
```toml
# Optimize for speed
MAX_FILES = 200
WORKER_THREADS = 4
CACHE_TTL = 1800
ENABLE_CACHING = true
ENABLE_PARALLEL = true
```

### **For AI Features**
```toml
# Enable all AI features
ENABLE_AI = true
ENABLE_LOCAL_LLM = true
DEEPSEEK_API_KEY = "your_key"
HF_TOKEN = "your_token"
```

---

## 🔧 Advanced Configuration

### **Custom Model Configuration**
```toml
# Use specific AI models
LOCAL_MODEL = "microsoft/DialoGPT-small"
HF_MODEL = "HuggingFaceH4/zephyr-7b-beta"
```

### **Security Settings**
```toml
# Security configuration
SECRET_KEY = "your_random_secret_key"
ALLOWED_HOSTS = "your-app-name.streamlit.app"
```

### **Debug Mode**
```toml
# Enable debug mode (development only)
DEBUG = true
LOG_LEVEL = "DEBUG"
```

---

## 📱 App URL

After deployment, your app will be available at:
```
https://your-app-name.streamlit.app
```

---

## 🆘 Support

### **Common Issues**
- **Build timeout**: Reduce dependencies or use smaller models
- **Memory issues**: Lower `MAX_FILES` or `WORKER_THREADS`
- **API errors**: Check API key validity and permissions

### **Getting Help**
- 📖 Check [Streamlit Cloud docs](https://docs.streamlit.io/streamlit-community-cloud)
- 🐛 Create GitHub issue with deployment logs
- 💬 Use GitHub Discussions for questions

---

**🚀 Happy Deploying!** Your Code Quality Intelligence Agent will be live in minutes!
