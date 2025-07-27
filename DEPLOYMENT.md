# SmartSpark Deployment Guide

This guide provides step-by-step instructions for deploying the SmartSpark application to production.

## 🚀 Frontend Deployment (Vercel)

### Prerequisites
- GitHub account
- Vercel account (free tier available)

### Steps

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Connect to Vercel**
   - Go to [vercel.com](https://vercel.com)
   - Sign in with GitHub
   - Click "New Project"
   - Import your SmartSpark repository

3. **Configure Environment Variables**
   In the Vercel dashboard, add these environment variables:
   ```
   REACT_APP_BACKEND_URL=https://your-backend-url.com
   ```

4. **Deploy**
   - Vercel will automatically detect it's a React app
   - Click "Deploy"
   - Your app will be available at `https://your-project.vercel.app`

## 🔧 Backend Deployment

### Option 1: Railway (Recommended)

1. **Create Railway Account**
   - Go to [railway.app](https://railway.app)
   - Sign in with GitHub

2. **Deploy Backend**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your SmartSpark repository
   - Set the source directory to `Smartspark/backend`

3. **Configure Environment Variables**
   ```
   OPENAI_API_KEY=your_openai_api_key
   MONGO_URL=your_mongodb_connection_string
   DB_NAME=smartspark
   ```

4. **Deploy**
   - Railway will automatically detect it's a Python app
   - Click "Deploy"
   - Get your backend URL from the deployment

### Option 2: Render

1. **Create Render Account**
   - Go to [render.com](https://render.com)
   - Sign up with GitHub

2. **Create Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Set build command: `pip install -r requirements.txt`
   - Set start command: `uvicorn server:app --host 0.0.0.0 --port $PORT`

3. **Configure Environment Variables**
   ```
   OPENAI_API_KEY=your_openai_api_key
   MONGO_URL=your_mongodb_connection_string
   DB_NAME=smartspark
   ```

### Option 3: Heroku

1. **Install Heroku CLI**
   ```bash
   # macOS
   brew install heroku/brew/heroku
   ```

2. **Create Heroku App**
   ```bash
   heroku create your-smartspark-app
   ```

3. **Deploy**
   ```bash
   cd Smartspark/backend
   git init
   git add .
   git commit -m "Initial commit"
   heroku git:remote -a your-smartspark-app
   git push heroku main
   ```

4. **Set Environment Variables**
   ```bash
   heroku config:set OPENAI_API_KEY=your_openai_api_key
   heroku config:set MONGO_URL=your_mongodb_connection_string
   heroku config:set DB_NAME=smartspark
   ```

## 🗄️ Database Setup

### MongoDB Atlas (Recommended)

1. **Create MongoDB Atlas Account**
   - Go to [mongodb.com/atlas](https://mongodb.com/atlas)
   - Sign up for free tier

2. **Create Cluster**
   - Click "Build a Database"
   - Choose "FREE" tier
   - Select your preferred region
   - Click "Create"

3. **Configure Network Access**
   - Go to "Network Access"
   - Click "Add IP Address"
   - Click "Allow Access from Anywhere" (for development)
   - Click "Confirm"

4. **Create Database User**
   - Go to "Database Access"
   - Click "Add New Database User"
   - Create username and password
   - Select "Read and write to any database"
   - Click "Add User"

5. **Get Connection String**
   - Go to "Database"
   - Click "Connect"
   - Choose "Connect your application"
   - Copy the connection string
   - Replace `<password>` with your database user password

## 🔑 API Keys Setup

### OpenAI API Key

1. **Get OpenAI API Key**
   - Go to [platform.openai.com](https://platform.openai.com)
   - Sign in or create account
   - Go to "API Keys"
   - Click "Create new secret key"
   - Copy the key (starts with `sk-`)

2. **Add to Environment Variables**
   ```
   OPENAI_API_KEY=sk-your-api-key-here
   ```

## 🔗 Update Frontend Configuration

After deploying the backend, update your frontend environment variable:

1. **In Vercel Dashboard**
   - Go to your project settings
   - Navigate to "Environment Variables"
   - Update `REACT_APP_BACKEND_URL` with your backend URL

2. **Redeploy Frontend**
   - Vercel will automatically redeploy when you update environment variables

## 🧪 Testing Deployment

1. **Test Backend**
   ```bash
   curl https://your-backend-url.com/
   # Should return: {"message": "SmartSpark API is running!"}
   ```

2. **Test Frontend**
   - Open your frontend URL
   - Try sending a message
   - Check browser console for any errors

## 🔒 Security Considerations

1. **Environment Variables**
   - Never commit API keys to Git
   - Use environment variables for all sensitive data

2. **CORS Configuration**
   - Update CORS origins in `server.py` to only allow your frontend domain
   - Remove `"*"` from `allow_origins` in production

3. **Database Security**
   - Use strong passwords for database users
   - Restrict network access to your application servers only

## 📊 Monitoring

1. **Vercel Analytics**
   - Enable Vercel Analytics in your project settings
   - Monitor frontend performance

2. **Backend Logs**
   - Check your hosting platform's logs
   - Monitor API response times and errors

## 🚨 Troubleshooting

### Common Issues

1. **CORS Errors**
   - Ensure backend CORS is configured correctly
   - Check that frontend URL is in allowed origins

2. **API Key Issues**
   - Verify OpenAI API key is correct
   - Check API key has sufficient credits

3. **Database Connection**
   - Verify MongoDB connection string
   - Check network access settings

4. **Build Failures**
   - Check all dependencies are installed
   - Verify Node.js and Python versions

### Support

- Check hosting platform documentation
- Review application logs
- Test locally before deploying

---

**Your SmartSpark application should now be live and ready for use! 🎉** 