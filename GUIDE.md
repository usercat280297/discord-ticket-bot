# 📖 Hướng dẫn Chi Tiết Discord Ticket Bot

## 📋 Mục lục
1. [Cài đặt](#cài-đặt)
2. [Cấu hình](#cấu-hình)
3. [Lệnh của Bot](#lệnh-của-bot)
4. [Cách hoạt động](#cách-hoạt-động)
5. [Xử lý sự cố](#xử-lý-sự-cố)

---

## 🚀 Cài đặt

### Yêu cầu
- Python 3.8 trở lên
- Discord Bot Token
- Server Discord để test

### Bước 1: Clone/Download dự án
```bash
cd discord-ticket-bot
```

### Bước 2: Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### Bước 3: Tạo file .env
```bash
# .env
DISCORD_TOKEN=your_bot_token_here
PREFIX=!
```

### Bước 4: Tạo roles trong Discord (quan trọng!)
1. Vào Server Settings → Roles
2. Tạo role `Staff` (cho nhân viên hỗ trợ)
3. Tạo role `Admin` (cho quản trị viên)

### Bước 5: Chạy bot
```bash
python main.py
```

---

## ⚙️ Cấu hình

### File config.json
```json
{
  "prefix": "!",           // Prefix command
  "staff_role": "Staff",   // Tên role staff
  "admin_role": "Admin",   // Tên role admin
  "ticket_category": "Tickets",  // Tên category ticket
  "ticket_prefix": "ticket",     // Prefix tên channel ticket
  "welcome_message": "...",      // Tin nhắn chào mừng
  "ticket_color": 5814783        // Màu embed (RGB)
}
```

### Thay đổi cấu hình bằng lệnh
```
!setconfig staff_role Moderator
!setconfig ticket_prefix support
```

---

## 🎮 Lệnh của Bot

### Admin Commands

#### `!setup [category]`
Tạo panel ticket mới
```
!setup General Support
!setup Technical Issues
!setup Billing
```
**Kết quả**: Bot sẽ gửi 1 embed với button "Mở Ticket"

#### `!panels`
Xem tất cả panels trong server
```
!panels
```

#### `!tickets`
Xem tất cả tickets đang mở
```
!tickets
```

### Staff Commands (Trong Ticket Channel)

#### `!close [reason]`
Đóng ticket
```
!close Vấn đề đã được giải quyết
```

#### `!claim`
Claim ticket (nhận ticket để xử lý)
```
!claim
```

#### `!add @user`
Thêm user vào ticket
```
!add @John
```

#### `!remove @user`
Xóa user khỏi ticket
```
!remove @John
```

#### `!transfer @user`
Chuyển ticket cho user khác
```
!transfer @Moderator1
```

#### `!ticketinfo [ticket_id]`
Xem thông tin chi tiết ticket
```
!ticketinfo abc123
```

### User Commands

#### `!mytickets`
Xem tất cả tickets của mình
```
!mytickets
```

---

## 🎯 Cách Hoạt Động

### 1️⃣ Người dùng mở Ticket
```
1. User nhấn button "Mở Ticket" trong panel
2. Bot tự động tạo channel ticket mới
3. Bot gửi welcome message vào ticket
```

### 2️⃣ Staff Xử Lý
```
1. Staff thấy thông báo trong #general hoặc nơi có panel
2. Staff vào ticket channel
3. Staff dùng !claim để claim ticket
4. Staff trò chuyện với user
5. Staff dùng !close để đóng ticket khi xong
6. Bot tự động xóa channel ticket
```

### 3️⃣ Database Lưu Trữ
- Tất cả thông tin tickets được lưu trong `data/tickets.json`
- Ticket đóng được chuyển vào `closed_tickets` để lưu lịch sử

---

## 🔧 Cấu Trúc Thư Mục

```
discord-ticket-bot/
│
├── main.py                   # File chính - chạy bot
├── config.json               # Cấu hình bot
├── requirements.txt          # Dependencies
├── README.md                 # Hướng dẫn cơ bản
│
├── cogs/                     # Các tính năng (cogs)
│   ├── __init__.py
│   ├── tickets.py            # Ticket commands & events
│   ├── events.py             # Discord events
│   └── moderation.py         # Moderation commands
│
├── utils/                    # Tiện ích
│   ├── __init__.py
│   ├── database.py           # Hàm database
│   ├── embed.py              # Tạo embeds
│   └── checks.py             # Permission checks
│
├── data/                     # Dữ liệu
│   └── tickets.json          # Database tickets
│
└── .env                      # Environment variables
```

---

## 📊 Database Structure

### tickets.json
```json
{
  "panels": [
    {
      "message_id": 123456,
      "channel_id": 789012,
      "guild_id": 345678,
      "category": "General Support",
      "created_at": "2024-01-18T10:30:00"
    }
  ],
  
  "tickets": {
    "abc123": {
      "ticket_id": "abc123",
      "user_id": 111111,
      "channel_id": 222222,
      "guild_id": 333333,
      "category": "General Support",
      "claimed_by": 444444,
      "claimed_at": "2024-01-18T10:35:00",
      "created_at": "2024-01-18T10:30:00",
      "closed": false,
      "closed_at": null,
      "closed_by": null,
      "members": [111111, 444444]
    }
  },
  
  "closed_tickets": [...]
}
```

---

## 🐛 Xử Lý Sự Cố

### Bot không startup
- Kiểm tra token trong `.env` có đúng không
- Kiểm tra bot có được thêm vào server không
- Kiểm tra Python version >= 3.8

### Ticket channel không được tạo
- Kiểm tra bot có quyền tạo channel không
- Kiểm tra category "Tickets" tồn tại không (bot sẽ tạo nếu không có)
- Xem logs để biết lỗi chi tiết

### Buttons không hoạt động
- Kiểm tra bot có quyền tương tác (Embed Links, etc.)
- Restart bot để reload cogs

### Staff/Admin commands không hoạt động
- Kiểm tra user có role "Staff" hoặc "Admin" không
- Kiểm tra tên role trong config.json chính xác

---

## 📝 Ghi chú

### Quyền cần cho Bot
- View Channels
- Send Messages
- Embed Links
- Manage Channels (tạo channel ticket)
- Manage Roles (set permissions)
- Read Message History
- Add Reactions

### Mẹo
- Đặt role Staff/Admin cao hơn bot role
- Tạo category riêng cho tickets để dễ quản lý
- Dùng `!setup` trước để tạo panel, sau đó test

---

## 💡 Tùy chỉnh

### Thay đổi welcome message
Sửa trong `config.json`:
```json
"welcome_message": "Chào mừng bạn! Vui lòng mô tả vấn đề..."
```

### Thay đổi màu embed
Sử dụng RGB color picker để tìm màu mong muốn, sau đó sửa:
```json
"ticket_color": 3447003  // Xanh
"ticket_color": 15158332 // Đỏ
"ticket_color": 3066993  // Xanh lá
```

### Thêm reactions/emoji
Có thể chỉnh sửa embeds trong `utils/embed.py`

---

**Tạo ngày:** 18/01/2024  
**Version:** 1.0.0  
**Author:** Ticket Bot Team
