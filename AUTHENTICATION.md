# 🔐 Authentication Guide - Sauce Recipe RAG API

## Overview

Your sauce recipe API is now protected with **HTTP Basic Authentication**. This means users need to provide a username and password to access protected endpoints.

## Required Environment Variables

**⚠️ IMPORTANT: You MUST set these environment variables!**

- **API_USERNAME**: Your chosen username
- **API_PASSWORD**: Your chosen password

**No default credentials are provided for security reasons.**

## Setting Custom Credentials

### For Railway Deployment:

1. **Go to Railway Dashboard**:

   - Open your project
   - Navigate to "Variables" tab

2. **Add Environment Variables**:

   ```
   API_USERNAME=your_custom_username
   API_PASSWORD=your_secure_password
   ```

3. **Redeploy** (Railway will automatically redeploy)

### For Local Development:

Add to your `.env` file:

```bash
API_USERNAME=your_custom_username
API_PASSWORD=your_secure_password
```

## Protected vs Public Endpoints

### 🔒 **Protected Endpoints** (Require Authentication):

- `GET /query` - Query sauce recipes
- `GET /test` - Debug information
- `GET /docs` - Interactive API documentation
- `GET /redoc` - Alternative API documentation

### 🌐 **Public Endpoints** (No Authentication):

- `GET /` - API information
- `GET /health` - Health check

## How to Use Authentication

### 1. **Browser Access**:

When you visit protected endpoints in your browser, you'll see a login popup:

- Enter your username and password
- Browser will remember credentials for the session

### 2. **cURL Requests**:

```bash
# With authentication (replace with your actual credentials)
curl -u "your_username:your_password" "https://your-app.railway.app/query?q=Jak zrobić sos czosnkowy?"

# Test endpoint
curl -u "your_username:your_password" "https://your-app.railway.app/test"

# Public endpoint (no auth needed)
curl "https://your-app.railway.app/health"
```

### 3. **Python Requests**:

```python
import requests
from requests.auth import HTTPBasicAuth

# Protected endpoint
response = requests.get(
    "https://your-app.railway.app/query?q=Jak zrobić sos czosnkowy?",
    auth=HTTPBasicAuth("your_username", "your_password")
)

# Public endpoint
response = requests.get("https://your-app.railway.app/health")
```

### 4. **JavaScript/Fetch**:

```javascript
// Protected endpoint
const username = "your_username";
const password = "your_password";
const credentials = btoa(`${username}:${password}`);

fetch("https://your-app.railway.app/query?q=Jak zrobić sos czosnkowy?", {
  headers: {
    Authorization: `Basic ${credentials}`,
  },
})
  .then((response) => response.json())
  .then((data) => console.log(data));
```

## Interactive API Documentation

The `/docs` endpoint (Swagger UI) now requires authentication:

1. Visit: `https://your-app.railway.app/docs`
2. Click the "Authorize" button (🔒 icon)
3. Enter your username and password
4. Test all endpoints interactively!

## Security Best Practices

### 🔒 **For Production Use**:

1. **Use Strong Credentials**:

   ```bash
   API_USERNAME=mycompany_api_user
   API_PASSWORD=verySecurePassword123!@#
   ```

2. **Use HTTPS Only**: Railway provides HTTPS by default ✅

3. **Consider Advanced Auth**: For production, consider:
   - JWT tokens
   - OAuth2
   - API keys
   - Rate limiting

### 🔧 **Environment Variables Summary**:

```bash
# Required for OpenAI
OPENAI_API_KEY=your_openai_api_key

# Optional for custom authentication (defaults to admin/sauce123)
API_USERNAME=your_username
API_PASSWORD=your_password
```

## Testing Authentication

### Quick Test Commands:

```bash
# Test public endpoint (should work)
curl "https://your-app.railway.app/"

# Test protected endpoint without auth (should fail with 401)
curl "https://your-app.railway.app/test"

# Test protected endpoint with auth (should work)
curl -u "your_username:your_password" "https://your-app.railway.app/test"
```

Your API is now secure! 🎉 Only users with valid credentials can access your sauce recipe queries.
