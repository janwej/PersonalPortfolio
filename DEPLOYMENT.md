# Deployment Guide

This guide will help you deploy your portfolio to a public URL with a custom domain.

## Recommended Platforms

### Option 1: Render (Recommended - Easy & Free Tier)
**Best for:** Quick deployment with free tier

1. **Sign up** at [render.com](https://render.com)
2. **Create a new Web Service:**
   - Connect your GitHub repository
   - Select "Web Service"
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn app:app`
   - Environment: Python 3
3. **Custom Domain:**
   - Go to your service settings
   - Click "Custom Domains"
   - Add your domain
   - Follow DNS configuration instructions

### Option 2: Railway
**Best for:** Modern platform with great developer experience

1. **Sign up** at [railway.app](https://railway.app)
2. **Deploy:**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Select your repository
   - Railway auto-detects Flask and deploys
3. **Custom Domain:**
   - Go to Settings → Domains
   - Add your custom domain
   - Update DNS records as instructed

### Option 3: Heroku
**Best for:** Well-documented, established platform

1. **Sign up** at [heroku.com](https://heroku.com)
2. **Install Heroku CLI:**
   ```bash
   brew install heroku/brew/heroku  # macOS
   ```
3. **Deploy:**
   ```bash
   heroku login
   heroku create your-app-name
   git push heroku main
   ```
4. **Custom Domain:**
   ```bash
   heroku domains:add www.yourdomain.com
   heroku domains:add yourdomain.com
   ```

### Option 4: DigitalOcean App Platform
**Best for:** Production-ready with good pricing

1. **Sign up** at [digitalocean.com](https://digitalocean.com)
2. **Create App:**
   - Go to App Platform
   - Connect GitHub repository
   - Select Python as runtime
   - Build command: `pip install -r requirements.txt`
   - Run command: `gunicorn app:app`
3. **Custom Domain:**
   - Go to Settings → Domains
   - Add your domain
   - Configure DNS records

## Custom Domain Setup

### Step 1: Purchase a Domain
- **Namecheap** (recommended): [namecheap.com](https://namecheap.com)
- **Google Domains**: [domains.google](https://domains.google)
- **Cloudflare**: [cloudflare.com](https://cloudflare.com) (includes free SSL)

### Step 2: Configure DNS
Once you have your deployment URL (e.g., `your-app.onrender.com`):

1. **For www subdomain:**
   - Type: `CNAME`
   - Name: `www`
   - Value: `your-app.onrender.com`

2. **For root domain (apex):**
   - Type: `ALIAS` or `ANAME` (if supported)
   - OR use `A` record pointing to platform's IP
   - Check your platform's documentation for exact values

3. **SSL Certificate:**
   - Most platforms (Render, Railway, Heroku) provide free SSL
   - Enable HTTPS in your platform settings

### Step 3: Update Your Platform
- Add your custom domain in platform settings
- Wait for DNS propagation (can take up to 48 hours, usually 1-2 hours)

## Pre-Deployment Checklist

- [x] `requirements.txt` created
- [x] `Procfile` created
- [x] `.gitignore` created
- [x] App configured to use `PORT` environment variable
- [ ] Test locally with: `gunicorn app:app`
- [ ] Push code to GitHub
- [ ] Deploy to chosen platform
- [ ] Test deployed site
- [ ] Add custom domain
- [ ] Test custom domain

## Testing Locally

Before deploying, test with production server:
```bash
pip install -r requirements.txt
gunicorn app:app
```

Visit `http://localhost:8000` to verify everything works.

## Environment Variables

If you need to add environment variables later:
- **Render**: Settings → Environment Variables
- **Railway**: Variables tab
- **Heroku**: `heroku config:set KEY=value`

## Troubleshooting

### Common Issues:

1. **App crashes on startup:**
   - Check logs in your platform's dashboard
   - Verify `requirements.txt` has all dependencies
   - Ensure `Procfile` has correct command

2. **Static files not loading:**
   - Verify files are in `static/` folder
   - Check file paths in code
   - Ensure files are committed to git

3. **Custom domain not working:**
   - Wait for DNS propagation (up to 48 hours)
   - Verify DNS records are correct
   - Check platform's domain settings

## Next Steps

1. Choose a deployment platform
2. Push your code to GitHub
3. Deploy using platform's instructions
4. Purchase and configure custom domain
5. Share your portfolio!

