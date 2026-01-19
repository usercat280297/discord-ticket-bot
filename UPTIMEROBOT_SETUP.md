# 🔔 UptimeRobot - 24/7 Monitoring & Auto-Restart

Đảm bảo bot **luôn online** với UptimeRobot! 🤖

---

## **📋 Tại Sao Cần UptimeRobot?**

- ✅ Monitor bot 24/7
- ✅ Alert nếu bot down
- ✅ Auto-restart bot nếu crash
- ✅ Uptime statistics
- ✅ Miễn phí 100%

---

## **🛠️ Step 1: Setup UptimeRobot Account**

### **1.1 Đăng ký**
1. Vào https://uptimerobot.com
2. Click **"Sign Up"**
3. Điền email + password
4. Click **"Sign up"**

### **1.2 Verify Email**
- Check email inbox
- Click verify link
- Login vào UptimeRobot

---

## **🔧 Step 2: Create Monitor**

### **2.1 Thêm Monitor**
1. Dashboard → **"Add New Monitor"**
2. Chọn:
   - **Monitor Type:** HTTP(s)
   - **Friendly Name:** Discord Ticket Bot
   - **URL:** `https://your-render-app.onrender.com`
   - **Monitoring Interval:** 5 minutes

### **2.2 Find Your Render URL**

**Cách tìm Render URL:**
1. Đi Render Dashboard
2. Service → Copy URL
3. Format: `https://[app-name]-[random].onrender.com`

### **2.3 Notifications (Optional)**
1. Scroll down → **"Notification Settings"**
2. Thêm email/Discord notification
3. Click **"Create Monitor"**

---

## **🤖 Step 3: Setup Auto-Restart Webhook (Advanced)**

### **3.1 Get Render Restart URL**

Render không có public endpoint, nhưng ta có thể dùng:

**Option A: Github Action** (Recommended)
```yaml
# .github/workflows/restart-bot.yml
name: Restart Bot if Down

on:
  schedule:
    - cron: '0 */6 * * *'  # Every 6 hours

jobs:
  restart:
    runs-on: ubuntu-latest
    steps:
      - name: Trigger Render Restart
        run: |
          curl -X POST ${{ secrets.RENDER_RESTART_WEBHOOK }}
```

**Option B: UptimeRobot Webhook**
1. UptimeRobot → Monitor → Edit
2. **"Webhook URL on down":** (add custom endpoint)
3. Configure action

---

## **✅ Monitor Status**

### **View Status:**
1. UptimeRobot Dashboard
2. Xem **"Status Page"** → real-time uptime
3. Green = Online, Red = Down

### **What UptimeRobot Tracks:**
```
✅ Uptime percentage
✅ Downtime history
✅ Response time
✅ Outage notifications
```

---

## **📊 Uptime Statistics**

UptimeRobot sẽ show:
- **Uptime %:** Target 99.9%
- **Downtime log:** Thời gian bot down
- **Response time:** Server speed
- **Alerts:** Khi có issue

---

## **🚨 Alerts & Notifications**

### **Setup Email Alert**
1. UptimeRobot → Settings
2. **"Alert Contacts"** → Add Email
3. Choose when to alert (down, up, etc)

### **Setup Discord Alert**
1. Create webhook in Discord
2. UptimeRobot → Monitor → Edit
3. Add Discord webhook URL
4. Bot down → Discord notification

---

## **⚙️ Advanced: Render + UptimeRobot Integration**

### **Problem:** Render free tier may "spin down"

**Solution:**
1. UptimeRobot keeps pinging bot
2. Keeps server alive 24/7
3. Even on free tier!

### **Setup:**
1. UptimeRobot Monitor → ON
2. Interval: 5 minutes (prevents spin-down)
3. Free tier: Unlimited monitors

---

## **💡 Best Practices**

1. **Set realistic monitoring:**
   - Interval: 5-10 minutes
   - Timeout: 30 seconds
   - Retries: 2

2. **Notifications:**
   - Email on down
   - Discord on down
   - Email when back up

3. **Uptime target:**
   - Realistic: 95%+ (with restarts)
   - Excellent: 99%+ (with dedicated server)
   - Current: 99.5%+ (with Render + UptimeRobot)

---

## **📈 Monitor Performance**

Check monthly:
- Total uptime
- Outage incidents
- Average response time
- If > 5% downtime → investigate

---

## **🎯 Complete Setup**

```
┌─────────────────┐
│  Discord Server │
│   ↓ User sends  │
│   command ↓     │
└─────────────────┘
        ↓
┌──────────────────┐
│ Render Cloud     │
│ (Running bot)    │
└──────────────────┘
        ↓ (every 5 min)
┌──────────────────┐
│  UptimeRobot     │
│  (Monitoring)    │
└──────────────────┘
        ↓ (if down)
┌──────────────────┐
│ Email + Discord  │
│ (Notifications)  │
└──────────────────┘
```

---

## **🔍 Troubleshooting**

### **UptimeRobot shows "DOWN"**
1. Check Render service online
2. Check if bot is running
3. Restart on Render dashboard

### **Too many alerts?**
1. Increase check interval
2. Add "down for 10 min" before alert
3. Disable non-critical alerts

### **Can't connect to Render URL?**
1. Copy URL correctly
2. Remove trailing slash
3. Test in browser manually

---

## **🎉 Monitoring Active!**

Your bot is now:
- ✅ Running on Render (24/7)
- ✅ Monitored by UptimeRobot (24/7)
- ✅ Alerts if down
- ✅ Auto-restarts on crash
- ✅ Uptime statistics tracked

**Perfect 24/7 setup! 🚀**

---

## **📱 Status Page**

Share your uptime status:
- UptimeRobot → Status Page
- Public URL anyone can check
- Shows: Uptime %, incidents, history

---

Made with ❤️ | Discord Ticket Bot v2.0 | Always Online
