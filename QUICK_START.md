# 🎫 Hướng Dẫn Nhanh - Discord Ticket Bot v2.0

## 🚀 Start Bot (Nhanh Nhất)

### 1. Cài Package
```bash
pip install -r requirements.txt
```

### 2. Tạo `.env`
```
DISCORD_TOKEN=your_bot_token_here
PREFIX=!
```

### 3. Run Bot
```bash
python main.py
```

✅ Bot sẵn sàng!

---

## 🎮 Dùng Bot Trong Discord

### Step 1: Tạo Panel Ticket
Gõ lệnh này trong bất kỳ channel nào:
```
!setup General Support
```

Bot sẽ gửi message với nút **"Mở Ticket"**

### Step 2: User Mở Ticket
- Bấm nút **"Mở Ticket (General Support)"**
- Bot tự động tạo channel: `#ticket-abc123`
- Bot gửi welcome message với hướng dẫn

### Step 3: Xử Lý Ticket

**User hoàn tất (It Works!):**
```
Bấm [✅ It Works!]
  ↓
Channel tự động đóng + xóa sau 5 giây
```

**User cần help thêm:**
```
Bấm [🆘 Need Help]
  ↓
Bot ping @Staff role
  ↓
Staff vào channel hỗ trợ
```

**Staff đóng ticket:**
```
Bấm [🔒 Close Ticket]
  ↓
Channel tự động đóng + xóa
```

---

## 📋 Lệnh Chính

| Lệnh | Dùng Cho | Ví Dụ |
|------|----------|-------|
| `!setup` | Tạo panel | `!setup General Support` |
| `/claim` | Claim ticket | Dùng trong channel ticket |
| `/add @user` | Thêm member | `/add @UserName` |
| `/remove @user` | Xóa member | `/remove @UserName` |
| `/transfer @user` | Chuyển ticket | `/transfer @UserName` |
| `!mytickets` | Xem tickets | Gõ bất kỳ đâu |

---

## 🎯 Quy Trình Hoàn Chỉnh

```
1️⃣  User bấm "Mở Ticket"
    ↓
2️⃣  Bot tạo channel + gửi welcome
    ↓
3️⃣  User làm theo hướng dẫn
    ↓
4️⃣  User bấm "✅ It Works!" (hoặc "🆘 Need Help")
    ↓
5️⃣  Bot tự động xóa channel sau 5 giây
    ↓
6️⃣  ✅ Ticket hoàn toàn closed!
```

---

## ⚙️ Cấu Hình

Edit `config.json`:

```json
{
  "prefix": "!",                    // Command prefix
  "staff_role": "Staff",            // Role name để ping
  "admin_role": "Admin",            // Admin role
  "ticket_category": "Tickets",     // Category để tạo ticket
  "ticket_prefix": "ticket",        // Prefix tên channel
  "auto_close_delay": 5,            // Giây trước xóa channel
  "max_user_tickets": 3             // Tối đa ticket/user
}
```

---

## 🔐 Permissions

### Bot Cần Quyền
- ✅ Send Messages
- ✅ Embed Links
- ✅ Manage Channels
- ✅ Manage Permissions
- ✅ View Channels
- ✅ Read Message History

### Role Setup
**Tạo 2 roles trong Discord:**
1. `Staff` - Người xử lý ticket
2. `Admin` - Quản lý toàn bộ

---

## 📊 Database

Bot lưu trữ tất cả ticket vào `data/tickets.json`:

```json
{
  "panels": [...],           // Danh sách panels
  "tickets": {...},          // Ticket đang mở
  "closed_tickets": [...]    // Ticket đã đóng
}
```

---

## 🆘 Có Lỗi?

### Bot không phản hồi button
- [ ] Kiểm tra bot online
- [ ] Kiểm tra intents enabled
- [ ] Kiểm tra bot role cao hơn

### Channel không xóa
- [ ] Kiểm tra bot có quyền delete
- [ ] Kiểm tra `auto_close_delay`

### Staff không nhận ping
- [ ] Kiểm tra role name đúng
- [ ] Kiểm tra `@Staff` role tồn tại

**Chạy test:**
```bash
python test_bot.py
```

---

## 📚 Tài Liệu Chi Tiết

- **`DEPLOYMENT_SUMMARY.md`** - Tóm tắt toàn bộ thay đổi
- **`IMPLEMENTATION_GUIDE.md`** - Hướng dẫn chi tiết
- **`ACTIVATION_FLOW.md`** - Giải thích workflow
- **`test_bot.py`** - Test suite

---

## 💡 Ví Dụ Flow

### Ví Dụ 1: Game Activation

```
User: Mở ticket → Category "Demon Slayer"
Bot: Gửi hướng dẫn + token + ảnh
User: Làm theo steps
User: Bấm ✅ It Works!
Bot: "Vấn đề Đã Giải Quyết" embed
Bot: Chờ 5 giây
Bot: 🗑️ Xóa channel
✅ Done!
```

### Ví Dụ 2: Support Ticket

```
User: Mở ticket → Category "Support"
User: Mô tả vấn đề
Bot: Gửi welcome message
User: "Vẫn cần help" → Bấm 🆘
Bot: Ping @Staff
Staff: Trả lời trong channel
User: Giải quyết được → Bấm ✅ It Works!
Bot: Xóa channel tự động
✅ Done!
```

---

## 🎉 Ready!

Bot của bạn đã:
- ✅ Tạo ticket tự động
- ✅ Nút "It Works!" → Tự động đóng
- ✅ Nút "Need Help" → Ping staff
- ✅ Xóa channel tự động
- ✅ Lưu trữ đầy đủ

**🚀 Sẵn sàng deployment!**

---

**Cần giúp? Xem chi tiết trong `IMPLEMENTATION_GUIDE.md`**
