# 🚀 Quick Deployment Guide

## Local Development (5 minutes)

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the app:**
   ```bash
   python main.py
   ```

3. **Open browser:**
   ```
   http://localhost:5001
   ```

## Deploy to Digital Ocean App Platform (15 minutes)

### Step 1: Push to GitHub

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial Gantt Chart app"

# Connect to your GitHub repo
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# Push
git push -u origin main
```

### Step 2: Create App on Digital Ocean

1. Go to https://cloud.digitalocean.com/apps
2. Click **"Create App"**
3. Choose **GitHub** as source
4. Select your repository
5. Click **Next**

### Step 3: Configure Build Settings

Digital Ocean should auto-detect Python. Verify these settings:

- **Build Command:** `pip install -r requirements.txt`
- **Run Command:** `python main.py`
- **HTTP Port:** `5001`

### Step 4: Configure Resources (Optional)

- Choose **Basic** plan ($5/month) for testing
- Can upgrade later if needed

### Step 5: Deploy!

- Click **"Create Resources"**
- Wait 3-5 minutes for deployment
- You'll get a URL like: `https://your-app-name.ondigitalocean.app`

## Important Notes

### ✅ What Gets Published (Public on GitHub)
- Source code (main.py, database.py)
- Requirements and configs
- README documentation

### ❌ What Stays Private
- **Your database file (gantt.db)** - stays on server only
- User data and tasks
- Environment variables (if you add any)

### 📝 License Compliance
- Frappe Gantt is MIT licensed (totally free, even commercial use)
- Your code should be public on GitHub
- Your **data** remains completely private

## Troubleshooting

### App won't start on Digital Ocean?
- Check the **Runtime Logs** in Digital Ocean dashboard
- Verify `runtime.txt` specifies Python 3.11
- Make sure all dependencies are in `requirements.txt`

### Database errors?
- Digital Ocean App Platform uses ephemeral storage
- For production, migrate to PostgreSQL managed database
- Tutorial in main README.md

### Need to update the app?
```bash
git add .
git commit -m "Update description"
git push
```
Digital Ocean auto-deploys on push!

## Quick Tips

1. **Test locally first** - always run `python main.py` before deploying
2. **Check logs** - Digital Ocean dashboard shows live logs
3. **Free tier** - Basic plan starts at $5/month with $200 credit for new users
4. **Auto-deploy** - Every git push triggers deployment
5. **Environment** - Add secrets in Digital Ocean dashboard under "App Settings"

## Next Steps After Deployment

- [ ] Add custom domain in Digital Ocean settings
- [ ] Set up PostgreSQL database for persistence
- [ ] Enable HTTPS (automatic with Digital Ocean)
- [ ] Add user authentication if needed
- [ ] Configure backups

---

Need help? Check the full README.md for detailed documentation!
