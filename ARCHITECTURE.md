# 🎫 Bot Architecture & Flow Diagrams

## 📐 System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      DISCORD SERVER                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────────┐        ┌──────────────────────┐           │
│  │  #announcements  │        │   💬 PANEL CHANNEL   │           │
│  │   (etc)          │        │  (Ticket Creation)   │           │
│  └──────────────────┘        ├──────────────────────┤           │
│                              │ [Mở Ticket Button]   │           │
│  ┌──────────────────┐        │                      │           │
│  │ Category:        │        │ "General Support"    │           │
│  │ "Tickets"        │◄───────┤ "Activation"        │           │
│  │ (Auto-created)   │        │ "Support"           │           │
│  └────────┬─────────┘        └──────────────────────┘           │
│           │                                                       │
│           ├─ #ticket-abc123  (User 1)                          │
│           │  ├─ Welcome Message                                 │
│           │  ├─ [✅ It Works!] [🆘 Need Help] [🔒 Close]      │
│           │  └─ User message, Staff response                   │
│           │                                                     │
│           ├─ #ticket-def456  (User 2)                          │
│           │  └─ ...                                             │
│           │                                                     │
│           └─ #ticket-ghi789  (User 3)                          │
│              └─ ...                                             │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                              ▲
                              │
                    ┌─────────┴──────────┐
                    │                    │
              ┌─────┴─────┐        ┌────┴─────┐
              │ Discord   │        │  Discord  │
              │ User      │        │  Bot      │
              │ (Click)   │        │ (Listen)  │
              └───────────┘        └───────────┘
```

---

## 🔄 Button Interaction Flow

```
┌──────────────────────────────────────────────────────────────────┐
│                     BUTTON CLICKED                               │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌────────────────┐  ┌─────────────────┐  ┌──────────────────┐ │
│  │ ✅ It Works!   │  │ 🆘 Need Help    │  │ 🔒 Close Ticket  │ │
│  └────────┬───────┘  └────────┬────────┘  └────────┬─────────┘ │
│           │                   │                    │             │
│           ▼                   ▼                    ▼             │
│  ┌─────────────────┐  ┌──────────────┐  ┌─────────────────┐    │
│  │ • Get Ticket    │  │ • Get Ticket │  │ • Check Auth    │    │
│  │ • Verify        │  │ • Ping Staff │  │ • Verify Perms  │    │
│  │ • Close in DB   │  │ • Update DB  │  │ • Close in DB   │    │
│  │ • Send Embed    │  │ • Send Embed │  │ • Send Embed    │    │
│  │ • Sleep 5s      │  │ • Keep Open  │  │ • Sleep 5s      │    │
│  │ • Delete Ch     │  │              │  │ • Delete Ch     │    │
│  └────────┬────────┘  └──────┬───────┘  └────────┬────────┘    │
│           │                  │                   │              │
│           ▼                  ▼                   ▼              │
│  ✅ Closed      🕐 Open+Help          ✅ Closed             │
│                 (Staff in)                                    │
│                                                               │
└──────────────────────────────────────────────────────────────────┘
```

---

## 📊 Ticket Lifecycle

```
START
  │
  ├─── User clicks "Mở Ticket"
  │
  ▼
[CREATION PHASE]
  │
  ├─ Bot creates #ticket-abc123
  ├─ Set permissions (only user, staff, admin)
  ├─ Send Welcome Embed
  ├─ Add [✅ It Works!] [🆘 Need Help] [🔒 Close] buttons
  │
  ▼
[ACTIVE PHASE]
  │
  ├─ User & Staff discussion
  │
  ├─► BRANCH A: It Works! (User)
  │   │
  │   ├─ Update DB: closed=true, closed_by=user
  │   ├─ Send "✅ Vấn đề Đã Giải Quyết" embed
  │   ├─ Sleep 5 seconds
  │   ├─ Delete channel
  │   │
  │   ▼
  │   [CLOSED]
  │
  ├─► BRANCH B: Need Help (User)
  │   │
  │   ├─ Update DB: status=need_help
  │   ├─ Ping @Staff role
  │   ├─ Keep channel open
  │   │
  │   ▼
  │   Staff can claim, add members, etc.
  │   Then use Branch C to close
  │
  ├─► BRANCH C: Close Ticket (Staff/Admin)
  │   │
  │   ├─ Check permissions
  │   ├─ Update DB: closed=true, closed_by=staff
  │   ├─ Send "🔒 Ticket Đã Đóng" embed
  │   ├─ Sleep 5 seconds
  │   ├─ Delete channel
  │   │
  │   ▼
  │   [CLOSED]
  │
  ▼
[ARCHIVE PHASE]
  │
  ├─ Move from "tickets" to "closed_tickets"
  ├─ Save: ticket_id, user_id, closed_at, closed_by
  ├─ Log to console/file
  │
  ▼
END ✅
```

---

## 💾 Database Schema

```
data/tickets.json
├── "panels": [
│   ├── {
│   │   "message_id": 123...,
│   │   "channel_id": 456...,
│   │   "guild_id": 789...,
│   │   "category": "General Support",
│   │   "created_at": "2026-01-18T10:30:00"
│   │ }
│   └── ...
├── "tickets": {
│   ├── "abc123": {
│   │   "ticket_id": "abc123",
│   │   "user_id": 123456789,
│   │   "channel_id": 987654321,
│   │   "guild_id": 111111111,
│   │   "category": "General Support",
│   │   "claimed_by": null,
│   │   "claimed_at": null,
│   │   "created_at": "2026-01-18T10:30:00",
│   │   "closed": false,
│   │   "closed_at": null,
│   │   "closed_by": null,
│   │   "members": [123456789, 987654321],
│   │   "status": "open"           ◄── NEW
│   │ },
│   └── ...
└── "closed_tickets": [
    ├── {
    │   "ticket_id": "old123",
    │   "user_id": 111111111,
    │   "closed": true,
    │   "closed_at": "2026-01-18T11:45:00",
    │   "closed_by": 222222222,
    │   ...
    │ }
    └── ...
  ]
```

---

## 🎯 User Journey

```
┌───────────┐
│ START     │
└─────┬─────┘
      │
      ▼
   [User sees panel with "Mở Ticket" button]
      │
      ▼
   [User clicks button]
      │
      ├─ Is user online? NO ──► [ERROR]
      │
      ├─ User already has tickets? YES ──► [ERROR: Max tickets]
      │
      ▼
   [Bot checks pass]
      │
      ▼
   [Bot creates channel]
      ├─ Channel name: #ticket-[RANDOM_6CHARS]
      ├─ Category: "Tickets"
      │
      ▼
   [Bot sends welcome message]
      ├─ Title: "🎫 Welcome to your ticket"
      ├─ Info: Category, Response time, Instructions
      ├─ Buttons: [✅ It Works!] [🆘 Need Help] [🔒 Close]
      │
      ▼
   [User reads message]
      │
      ├─► USER PATH A: Problem is solved
      │   │
      │   ├─ Clicks [✅ It Works!]
      │   │
      │   ├─ Bot checks: Is this user?
      │   │
      │   ├─ Bot updates DB: closed=true
      │   │
      │   ├─ Bot sends: "✅ Vấn đề Đã Giải Quyết"
      │   │
      │   ├─ User sees message ✓
      │   │
      │   ├─ Bot waits: 5 seconds
      │   │
      │   ├─ Bot deletes: #ticket-abc123
      │   │
      │   ▼
      │   [TICKET CLOSED] ✅
      │
      ├─► USER PATH B: Problem not solved
      │   │
      │   ├─ Clicks [🆘 Need Help]
      │   │
      │   ├─ Bot sends: "🆘 Yêu Cầu Trợ Giúp"
      │   │
      │   ├─ Bot mentions: @Staff ◄── PING!
      │   │
      │   ├─ Staff gets notified
      │   │
      │   ├─ Staff enters channel
      │   │
      │   ├─ Staff & User discuss
      │   │
      │   ├─ Issue resolved
      │   │
      │   ├─ Staff clicks [🔒 Close Ticket]
      │   │
      │   ├─ Bot checks: Is staff?
      │   │
      │   ├─ Bot updates DB: closed=true
      │   │
      │   ├─ Bot deletes channel (5s delay)
      │   │
      │   ▼
      │   [TICKET CLOSED] ✅
      │
      └─► ADMIN PATH C: Manual close
          │
          ├─ Admin clicks [🔒 Close Ticket]
          │
          ├─ Same as Path B
          │
          ▼
          [TICKET CLOSED] ✅

      ALL PATHS:
          ▼
      [Bot logs action]
      [Save to closed_tickets]
      [✅ DONE]
```

---

## 🔌 Integration Points

```
Bot ◄──► Discord Server
  │
  ├─ [Interaction] ◄──────► User Button Click
  │  └─ callback()
  │
  ├─ [Message] ◄──────────► Send Embed/Message
  │  └─ send()
  │
  ├─ [Channel] ◄──────────► Create/Delete/Modify
  │  └─ create_text_channel()
  │  └─ delete()
  │  └─ set_permissions()
  │
  ├─ [Role] ◄─────────────► Get/Mention Role
  │  └─ get_role()
  │
  └─ [Logging] ◄──────────► Command Execution
     └─ logger.info()

Bot ◄──► Database (JSON)
  │
  ├─ [Read] ◄────────────── Load tickets.json
  │  └─ load_data()
  │
  └─ [Write] ◄───────────── Save changes
     └─ save_data()
```

---

## ⏱️ Timing Diagram

```
Time   Action                          Status
────────────────────────────────────────────────────
0.0s   User clicks button              🟢 Button down
0.1s   Bot receives interaction        🟡 Processing
0.2s   Bot gets ticket from DB         🟡 Checking
0.3s   Bot verifies permissions        🟡 Validating
0.4s   Bot closes in DB                🟡 Updating
0.5s   Bot sends confirmation embed    🟡 Messaging
0.6s   User sees message               🟢 Visible
1.0s   ...                             🟡 Waiting
2.0s   ...                             🟡 Waiting
3.0s   ...                             🟡 Waiting
4.0s   ...                             🟡 Waiting
5.0s   ...                             🟡 Waiting
5.1s   Bot deletes channel             🔴 Deleting
5.2s   Channel is gone                 ⚪ Closed
5.3s   Log action                      ✅ Done

Duration: 5.3 seconds from click to complete closure
```

---

## 🎨 Embed Structure

```
┌─ WELCOME EMBED
│  ├─ Title: "🎫 Welcome to your ticket"
│  ├─ Description: "@User"
│  ├─ Field 1: "📋 Category" → "Demon Slayer"
│  ├─ Field 2: "⏱️ Response Time" → "Minutes to hours"
│  ├─ Field 3: "📝 Hướng Dẫn" → Step-by-step
│  ├─ Color: 5814783 (Custom)
│  └─ Footer: "Discord Ticket Bot"
│
├─ CONFIRMATION EMBED (It Works!)
│  ├─ Title: "✅ Vấn đề Đã Giải Quyết"
│  ├─ Description: "User confirmed solution"
│  ├─ Footer: "Ticket will close in 5 seconds"
│  ├─ Color: Green (discord.Color.green())
│  └─ Ephemeral: False
│
├─ HELP REQUEST EMBED (Need Help)
│  ├─ Title: "🆘 Yêu Cầu Trợ Giúp"
│  ├─ Description: "User needs more help"
│  ├─ Mention: @Staff
│  └─ Color: Orange
│
└─ CLOSE EMBED
   ├─ Title: "🔒 Ticket Đã Đóng"
   ├─ Description: "Closed by: Staff/Admin/User"
   └─ Color: Red
```

---

## 📈 Metrics Tracked

```
Ticket Metrics:
├─ Total Created
├─ Closed (It Works!)
├─ Closed (Need Help → Staff)
├─ Closed (Manual by Staff)
├─ Still Open
├─ Avg Resolution Time
└─ Avg Response Time

User Metrics:
├─ Tickets per User
├─ Most Common Category
├─ Resolution Rate
└─ Helper (Staff) Activity

System Metrics:
├─ Bot Uptime
├─ Commands Processed
├─ Database Size
└─ Error Rate
```

---

## ✨ Summary

- **Architecture**: Modular, event-driven
- **Database**: JSON-based persistence
- **Workflow**: 3 paths (It Works, Need Help, Manual Close)
- **Timing**: 5 seconds from action to channel deletion
- **Security**: Permission-based access control
- **Monitoring**: Full logging & metrics

**Result: Clean, maintainable, production-ready bot!**
