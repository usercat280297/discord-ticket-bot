# 🚀 Deploy Bot lên Render.com - Step by Step

**Estimated time: 15 minutes**

---

## 🎯 Tương Lai của Bot Sau Deploy

```
Your Computer              Render Server
    ↓                            ↓
 (Offline)              BOT RUNS 24/7 ✅
 (Sleep)                No need to keep PC on
 (Restart)              Auto-restart on error
                        Always available
```

---

## ✅ Pre-Deploy Checklist

- [x] Bot works locally? ✅ (tested)
- [x] Procfile created? ✅ (just created)
- [x] requirements.txt? ✅ (should have)
- [x] DISCORD_TOKEN ready? ✅ (in .env)
- [x] GitHub account? ✅ (create if not)

---

## 📝 Step 1: Prepare GitHub Repo (5 min)

### **1.1 Create GitHub Account** (if you don't have)
- Go to https://github.com
- Sign up (free)
- Verify email

### **1.2 Create New Repository**

1. Go to https://github.com/new
2. Fill in:
   - **Repository name:** `discord-ticket-bot`
   - **Description:** Discord Ticket Support Bot
   - **Public:** Yes (need for Render free tier)
   - **DO NOT initialize** (we have files already)
3. Click "Create repository"

### **1.3 Push Your Code to GitHub**

Open Terminal in your bot folder:

```bash
# Go to bot folder
cd e:\Steam\ panel\ denuvo\ activation\discord-ticket-bot

# Initialize git (if not already)
git init

# Add all files
git add .

# Commit
git commit -m "Discord Ticket Bot v2.0 - Ready for production"

# Add remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/discord-ticket-bot.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**Note:** GitHub will ask for token:
- Go to https://github.com/settings/tokens
- Click "Generate new token"
- Select scopes: `repo`
- Copy token
- Paste when asked in terminal

✅ **Code is now on GitHub!**

---

## 🌍 Step 2: Deploy on Render.com (10 min)

### **2.1 Create Render Account**

1. Go to https://render.com
2. Click "Get Started"
3. Sign up with GitHub ← **THIS IS KEY!**
4. Authorize Render to access GitHub

### **2.2 Create Web Service**

1. After login, click **"New +"**
2. Select **"Web Service"**
3. You'll see your GitHub repos
4. Click "Connect" next to `discord-ticket-bot`

### **2.3 Configure Service**

Fill in these fields:

```
Name:                      discord-ticket-bot
Environment:               Python 3
Region:                    Choose closest (Singapore OK)
Branch:                    main
Root Directory:            . (leave empty)

Build Command:             pip install -r requirements.txt
Start Command:             python main.py
```

### **2.4 Add Environment Variables**

Click **"Add Environment Variable"** button:

```
Name:  DISCORD_TOKEN
Value: [your_bot_token_here]

Name:  PREFIX
Value: !
```

**⚠️ DO NOT put token in code!**

### **2.5 Review & Deploy**

1. Scroll down
2. Click **"Create Web Service"**
3. Wait 2-3 minutes for build
4. See "Your service is live!" ✅

---

## ✅ Verification

### **Check if Bot is Online**

1. Go to Discord
2. Check bot profile
3. Should show **"Online"** or **"Do Not Disturb"**

### **Test Bot**

1. In Discord server, type:
   ```
   !setup Test Support
   ```
2. Bot should respond ✅

### **Check Logs**

In Render dashboard:
1. Click your service
2. Go to **"Logs"** tab
3. Should see:
   ```
   ✅ Bot đăng nhập thành công: [BotName]
   📊 Bot đang phục vụ X server
   ```

---

## 🔄 Update Bot Code

Whenever you want to update bot code:

```bash
# Make changes to files
# Then:
git add .
git commit -m "Update: [describe changes]"
git push origin main

# Render automatically deploys! (2-3 min)
```

---

## ⚠️ Important Notes

### **DO NOT Commit:**
```
.env                    ← Token file
data/tickets.json       ← User data
__pycache__/            ← Cache
```

Already in `.gitignore` ✅

### **Data Backup**

Render spins down free tier, but `data/tickets.json` is created on startup:

**To backup data:**
1. Download from Render
2. Or git-track it (but be careful with passwords)

---

## 🛠️ Troubleshooting

### **Build fails?**

Check these:
1. **requirements.txt**
   ```bash
   pip freeze > requirements.txt
   ```
   Make sure it includes: `discord.py`

2. **Procfile syntax**
   ```
   worker: python main.py
   ```
   (No extra spaces)

3. **Python version**
   - Render defaults to latest Python ✅
   - Should work fine

### **Bot crashes after deploy?**

Check Render logs:
1. Service → Logs tab
2. Look for error message
3. Fix locally
4. `git push` again

### **DISCORD_TOKEN not working?**

1. Verify token in Render environment variables
2. Check it's correct
3. Make sure `os.getenv('DISCORD_TOKEN')` in main.py
4. Restart service (Render → Logs → "Restart")

### **Bot offline after a while?**

Free tier behavior - auto spins down after 15min inactivity.

**Solutions:**
1. **Pay ($7/month)** - Always on
2. **Use UptimeRobot** - Add HTTP endpoint (complicated)
3. **Just accept it** - Reactivates when pinged

---

## 💰 Cost Comparison

| Tier | Cost | Benefits |
|------|------|----------|
| **Free** | $0 | Runs bot, cold starts OK |
| **Starter** | $7/month | Always warm, no cold starts |
| **Pro** | $12/month | Better performance |

**Recommendation:** Free tier is fine for starting, upgrade later if needed.

---

## 🎉 You're Live!

After deploy:

```
✅ Bot runs 24/7
✅ Auto-restarts on crash
✅ Data persists
✅ No PC needed
✅ Easy updates (just git push)
```

---

## 📚 Quick Reference

| Command | What it does |
|---------|-------------|
| `git init` | Start git repo |
| `git add .` | Stage all files |
| `git commit -m "msg"` | Commit changes |
| `git push origin main` | Push to GitHub |
| (auto) | Render deploys! |

---

## ❓ FAQs

**Q: Will my data be lost?**
A: No! `data/tickets.json` is persistent on Render.

**Q: Can I update bot without downtime?**
A: Almost instant! Just `git push` and Render redeploys in 2-3 min.

**Q: What if bot crashes?**
A: Render auto-restarts! You'll get notifications.

**Q: Can I use my own server?**
A: Yes! But Render is easier and free.

**Q: Do I need webhook?**
A: No! Your bot is event-driven. No webhook needed.

---

## 🚀 Next Steps

1. **Create GitHub account** (if you don't have)
2. **Push code to GitHub** (see Step 1)
3. **Deploy on Render** (see Step 2)
4. **Test in Discord** ✅
5. **Enjoy 24/7 bot!** 🎉

---

**Questions? Check the logs or re-read this guide!**

**Your bot will be online in 15 minutes!** ⏱️🚀
