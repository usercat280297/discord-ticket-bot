# 🚀 Deploy lên Render.com - 24/7 Hosting

Bot sẽ chạy **24/7** trên server Render! ☁️

---

## **📋 Prerequisites**

- ✅ GitHub account (repo của bot)
- ✅ Render.com account (miễn phí)
- ✅ Bot token (đã có)

---

## **🛠️ Step 1: Prepare Repository**

### **1.1 Create .env.example** (cho clone)
```bash
# Tạo file .env.example
# File này để hướng dẫn người khác setup
```

Tạo file [.env.example](.env.example):
```
DISCORD_BOT_TOKEN=your_bot_token_here
```

### **1.2 Commit & Push to GitHub**
```bash
git add .env.example
git commit -m "Add .env.example template"
git push origin main
```

---

## **☁️ Step 2: Setup Render.com**

### **2.1 Đăng ký Render**
1. Vào https://render.com
2. Click **"Sign up"**
3. Chọn **"Continue with GitHub"**
4. Authorize Render để truy cập GitHub repos

### **2.2 Tạo New Web Service**
1. Dashboard → **"New +"** → **"Web Service"**
2. Chọn repository: `discord-ticket-bot`
3. Click **"Connect"**

### **2.3 Configure Service**

| Field | Value |
|-------|-------|
| **Name** | discord-ticket-bot |
| **Environment** | Python 3 |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `python main.py` |
| **Instance Type** | Free (hoặc Starter nếu muốn stable) |

### **2.4 Add Environment Variables**
1. Scroll down → **"Environment"**
2. Click **"Add Environment Variable"**

Thêm:
| Key | Value |
|-----|-------|
| DISCORD_BOT_TOKEN | your_actual_bot_token_here |

**⚠️ QUAN TRỌNG:** Copy token từ `.env` file (local)

### **2.5 Deploy**
1. Click **"Deploy"**
2. Chờ ~2-3 phút
3. Check **"Logs"** tab - phải thấy "Bot logged in as ..."

---

## **✅ Verify Deployment**

### **Check Bot Status:**
```
Logs → Watch for "Bot logged in as [YourBotName]"
```

### **Test Bot on Discord:**
1. Mở Discord server
2. Tạo kênh `#ticket-panel`
3. Gõ: `!setup`
4. ✅ Dropdown phải hiển thị

---

## **🔄 Auto-Redeploy on GitHub Push**

Render sẽ **tự động redeploy** mỗi khi bạn push code:

```bash
# Make changes
git add .
git commit -m "Fix bug"
git push origin main

# Render automatically redeploys! 🤖
```

---

## **⚙️ Configure Auto-Restart (Optional)**

Nếu bot bị crash, Render có thể tự restart:

1. Dashboard → Your Service
2. **Settings** → **Restart Policy**
3. Chọn **"Always"**

---

## **📊 Monitor Bot Status**

### **Render Dashboard:**
- Green dot = Online ✅
- Red dot = Down ❌
- Yellow dot = Deploying 🟡

### **Check Logs:**
```
Service → Logs → Real-time logs
```

---

## **🆘 Troubleshooting**

### **Bot offline (Red indicator)?**
1. Check Logs tab
2. Look for error messages
3. Common issues:
   - Invalid token
   - Missing dependencies
   - Syntax error in code

### **Fix & Redeploy:**
```bash
# Fix error locally
git add .
git commit -m "Fix issue"
git push origin main
# Render tự động redeploy
```

### **Manual Restart:**
Dashboard → Service → **"Restart"** button

---

## **💰 Pricing**

| Plan | Price | Features |
|------|-------|----------|
| **Free** | $0 | 24/7 uptime, but may sleep |
| **Starter** | $7/mo | Full 24/7 guaranteed |
| **Standard** | $25/mo | Better performance |

**Recommend:** Free tier vừa đủ for ticket bot

---

## **🚨 Important Notes**

1. ✅ **Token Safety:** Token stored secure in Render (not in repo)
2. ✅ **Automatic Updates:** New pushes = auto deploy
3. ✅ **Logs Available:** Real-time logs in dashboard
4. ✅ **Custom Domain:** Optional (default: render-generated URL)

---

## **🎉 You're Live!**

Your bot is now:
- ✅ Running 24/7 on cloud
- ✅ Auto-redeploying on GitHub push
- ✅ Auto-restarting if it crashes
- ✅ Monitoring available in dashboard

**Chúc mừng! Bot của bạn giờ lên cloud! 🚀**

---

## **Next Step:** Setup UptimeRobot Monitoring

Xem file: `UPTIMEROBOT_SETUP.md`

Made with ❤️ | Discord Ticket Bot v2.0
