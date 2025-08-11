# 🚀 Railway Deployment Guide - Sauce Recipe RAG API

## 🥇 Railway Deployment (2-Minute Setup)

**Why Railway?** Perfect for FastAPI + ChromaDB with persistent storage

### Quick Steps:

1. **Push to GitHub** (if not already done):

   ```bash
   git add .
   git commit -m "Add FastAPI sauce recipe RAG"
   git push origin main
   ```

2. **Deploy on Railway**:

   - Go to [railway.app](https://railway.app)
   - Click "Deploy from GitHub repo"
   - Connect your repository
   - Railway will auto-detect it's a Python project

3. **Add Environment Variable**:

   - In Railway dashboard → Variables
   - Add: `OPENAI_API_KEY` = `your_openai_api_key_here`

4. **Deploy!**
   - Railway will automatically build and deploy
   - Your API will be live at: `https://your-app.railway.app`

### ✅ Benefits:

- **Persistent storage** (ChromaDB survives restarts)
- **Automatic deployments** from GitHub
- **500 hours free/month** + $5 credit
- **Zero configuration** needed
- **Custom domains** available

### 🔧 Environment Variables Needed:

- `OPENAI_API_KEY`: Your OpenAI API key

### 📁 Files for Railway:

- `railway.json` - Railway configuration
- `requirements.txt` - Python dependencies
- `api.py` - Your FastAPI application

### 🧪 Test Your Deployed API:

```bash
# Replace with your Railway URL
curl "https://your-app.railway.app/health"
curl "https://your-app.railway.app/query?q=Jak zrobić sos czosnkowy?"
```

### 📖 Access Points:

- **API**: `https://your-app.railway.app`
- **Interactive Docs**: `https://your-app.railway.app/docs`
- **Health Check**: `https://your-app.railway.app/health`

### 🐛 Troubleshooting:

**Common Issues:**

1. **"Module not found"**:

   - Check `requirements.txt` includes all dependencies
   - Ensure Python version compatibility

2. **"OpenAI API quota exceeded"**:

   - Check your OpenAI billing and usage
   - Add credits to your OpenAI account

3. **Build fails**:
   - Check Railway logs in dashboard
   - Ensure all files are committed to GitHub

### 💡 Tips:

- **First deployment** takes 2-3 minutes (building ChromaDB)
- **Subsequent deployments** are faster (persistent storage)
- **Cold starts** may take 10-15 seconds on free tier
- **Auto-deploy** on every GitHub push

### 🆘 Getting Help:

- Railway Docs: [docs.railway.app](https://docs.railway.app)
- Railway Discord: Active community support
