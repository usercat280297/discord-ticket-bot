#!/usr/bin/env python3
"""
🎫 Discord Ticket Bot v2.0 - Quick Start Guide
Professional Edition with Dropdown Menu & Pinned Messages
"""

print("""
╔════════════════════════════════════════════════════════════════╗
║       🎫 DISCORD TICKET BOT v2.0 - QUICK START GUIDE          ║
║              Professional Edition with Dropdown                ║
╚════════════════════════════════════════════════════════════════╝

✨ WHAT'S NEW:
   ✅ Dropdown menu cho phép chọn loại ticket
   ✅ Panel message được ghim (pinned) tự động
   ✅ Welcome message được ghim trong ticket channel
   ✅ Professional embed messages
   ✅ Configurable categories
   ✅ Ready for 24/7 deployment

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 SETUP CHECKLIST:

   1️⃣ BOT TOKEN
      • Discord Developer Portal: https://discord.com/developers/applications
      • Create Application → Bot → Copy Token
      • Paste vào .env file:
        DISCORD_BOT_TOKEN=your_token_here

   2️⃣ INSTALL DEPENDENCIES
      $ pip install -r requirements.txt

   3️⃣ TEST BOT LOCALLY
      $ python main.py
      • Check console cho "Bot logged in as ..."
      • Bot should be online trên Discord

   4️⃣ CREATE PANEL KÊNH
      • Tạo kênh mới: #ticket-panel
      • Trong kênh đó, chạy: !setup
      • Bot sẽ tạo dropdown + pin message

   5️⃣ TEST DROPDOWN
      • Bấm dropdown: 🎫 Chọn loại ticket...
      • Chọn: 🎮 Hỗ trợ Game
      • Bot tạo #ticket-xxxxx channel
      • Kiểm tra nó có pinned welcome message

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📚 FILES OVERVIEW:

   Core Files:
   • main.py                - Bot entry point
   • cogs/tickets.py        - Dropdown + ticket commands
   • config.json            - Settings (categories, roles, etc)
   
   Documentation:
   • SETUP_PANEL.md         - Detailed panel setup
   • GITHUB_SETUP.md        - Git & GitHub guide
   • UPGRADE_SUMMARY.md     - What's changed
   • COMMANDS.md            - All commands
   • README.md              - Project overview

   Security:
   • .env                   - Your bot token (NEVER push to GitHub)
   • .gitignore             - Protects sensitive files

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎮 DROPDOWN MENU CATEGORIES:

   Default categories (editable in config.json):
   • 🎮 Hỗ trợ Game
   • 💳 Hỗ trợ Account
   • 🐛 Báo Bug
   • 💬 Khác

   To add more: Edit config.json → panel_categories

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 COMMANDS:

   ADMIN:
   • !setup                 - Create panel with dropdown

   STAFF:
   • /claim                 - Claim ticket
   • /close [reason]        - Close ticket
   • /add @user             - Add user to ticket
   • /remove @user          - Remove user from ticket
   • /transfer @user        - Transfer ticket ownership

   USERS:
   • /mytickets             - View your tickets

   BUTTONS:
   • ✅ It Works!           - Auto-close ticket
   • 🆘 Need Help           - Ping staff
   • 🔒 Close Ticket        - Manual close

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚀 DEPLOYMENT (Render.com):

   Step 1: Push to GitHub
   $ git add .
   $ git commit -m "🎉 v2.0: Professional edition"
   $ git branch -M main
   $ git push -u origin main

   Step 2: Connect to Render
   • Go to render.com
   • New Web Service
   • Connect GitHub repo
   • Add DISCORD_BOT_TOKEN env variable
   • Deploy!

   Step 3: Verify
   • Bot should be online 24/7
   • Try the dropdown menu
   • It should work perfectly!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ IMPORTANT SECURITY:

   NEVER push these to GitHub:
   ❌ .env (contains your bot token)
   ❌ config.json (may contain sensitive info)
   ❌ data/ (user data)

   They're protected by .gitignore ✅

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❓ TROUBLESHOOTING:

   Bot doesn't appear online?
   → Check .env file has valid token
   → Restart bot: python main.py

   Dropdown doesn't work?
   → Check bot has Manage Channels permission
   → Run !setup command again

   Messages not pinning?
   → Check bot has Manage Messages permission
   → Check channel pin limit (50 max)

   See SETUP_PANEL.md for more troubleshooting

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎉 YOU'RE ALL SET!

   Your Discord Ticket Bot is now:
   ✅ Professional (Dropdown menu)
   ✅ User-friendly (Pinned messages)
   ✅ Well-documented
   ✅ Ready for production
   ✅ Ready to deploy 24/7

   Next: Read SETUP_PANEL.md for detailed instructions!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Made with ❤️  | Discord Ticket Bot v2.0 | Professional Edition
""")
