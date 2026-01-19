# 🎫 Setup Ticket Panel - Hướng Dẫn Chuyên Nghiệp

Hệ thống ticket bot của bạn giờ đã được upgrade với **Dropdown menu** chuyên nghiệp! 🚀

---

## 📋 Cấu Trúc Hệ Thống

```
📌 Kênh #ticket-panel
├── Pinned Message: "Hệ Thống Ticket Hỗ Trợ"
├── Dropdown Menu:
│   ├── 🎮 Hỗ trợ Game
│   ├── 💳 Hỗ trợ Account
│   ├── 🐛 Báo Bug
│   └── 💬 Khác
└── 

↓ User bấm dropdown ↓

📌 Kênh #ticket-xxxxx (Riêng tư)
├── Pinned Message: Welcome + Instructions
├── Buttons: [✅ It Works!] [🆘 Need Help] [🔒 Close Ticket]
└── Footer: Lệnh hỗ trợ (/close, /claim, /add, /remove, /transfer)
```

---

## 🚀 Cách Setup

### **Bước 1: Tạo Kênh Panel**
1. Mở Discord server
2. Tạo kênh mới: `#ticket-panel`
3. Mô tả: "Kênh mở ticket hỗ trợ"

### **Bước 2: Chạy Bot & Setup Command**
```bash
# 1. Cài dependencies
pip install -r requirements.txt

# 2. Chạy bot
python main.py
```

### **Bước 3: Chạy Setup Command**
Trong kênh `#ticket-panel`, gõ:
```
!setup
```

Bot sẽ:
- ✅ Tạo **Dropdown menu** 
- ✅ **Pin message** panel trong kênh
- ✅ Lưu cấu hình vào `config.json`

### **Bước 4: User Sử Dụng**
- Nhấn vào dropdown `🎫 Chọn loại ticket...`
- Chọn loại vấn đề (🎮 Game, 💳 Account, 🐛 Bug, 💬 Khác)
- Bot tự động tạo kênh private + pinned message
- Nhấn buttons: [✅ It Works!] [🆘 Need Help] [🔒 Close Ticket]

---

## ⚙️ Cấu Hình (config.json)

```json
{
  "prefix": "!",
  "staff_role": "Staff",
  "admin_role": "Admin",
  "ticket_category": "Tickets",
  "ticket_prefix": "ticket",
  "panel_channel_id": null,
  "panel_categories": [
    "🎮 Hỗ trợ Game",
    "💳 Hỗ trợ Account",
    "🐛 Báo Bug",
    "💬 Khác"
  ],
  "ticket_color": 5814783,
  "auto_close_delay": 5,
  "auto_close_inactive": 1800,
  "max_user_tickets": 3
}
```

**Giải thích:**
- `panel_categories`: Danh sách loại ticket (tùy chỉnh được)
- `max_user_tickets`: Tối đa ticket/user (mặc định: 3)
- `auto_close_delay`: Thời gian trước khi xóa channel (5 giây)
- `ticket_color`: Màu embed (5814783 = xanh dương)

---

## 🎯 Các Tính Năng

### **Dropdown Menu**
- Chọn loại ticket từ menu
- Tạo kênh riêng tư ngay lập tức
- Tự động pin welcome message

### **Buttons trong Ticket**
| Button | Tác Dụng |
|--------|----------|
| ✅ **It Works!** | Xác nhận giải quyết → Đóng ticket tự động |
| 🆘 **Need Help** | Yêu cầu trợ giúp → Ping Staff role |
| 🔒 **Close Ticket** | Đóng ticket thủ công |

### **Commands Staff**
```
/close [reason]        - Đóng ticket với lý do
/claim                 - Claim ticket (xác nhận đang xử lý)
/add @user             - Thêm user vào ticket
/remove @user          - Xóa user khỏi ticket
/transfer @user        - Chuyển ticket cho user khác
```

### **Commands User**
```
/mytickets             - Xem ticket của bạn
```

---

## 🔒 Bảo Mật & Permissions

✅ **Ticket Channel (Riêng tư):**
- ❌ Mọi người: KHÔNG thấy
- ✅ User tạo: Xem + Viết tin nhắn
- ✅ Staff role: Xem + Viết tin nhắn
- ✅ Admin role: Xem + Viết tin nhắn

✅ **Panel Channel (Công khai):**
- ✅ Mọi người: Xem + Dùng dropdown

---

## 📝 Ví Dụ Workflow

```
1. User: Vào #ticket-panel
   ↓
2. User: Bấm dropdown → Chọn "🎮 Hỗ trợ Game"
   ↓
3. Bot: Tạo #ticket-a7x2k1 (riêng tư)
   ↓
4. Bot: Gửi pinned message welcome + buttons
   ↓
5. User: Mô tả vấn đề
   ↓
6. Staff: Claim + xử lý vấn đề
   ↓
7. User: Bấm "✅ It Works!" 
   ↓
8. Bot: Đóng channel (5 giây sau)
```

---

## 🛠️ Troubleshooting

### ❌ **Dropdown không hiển thị**
- Đảm bảo bot đã được updated (file mới)
- Restart bot: `python main.py`
- Chạy lại `!setup` command

### ❌ **Bot không tạo channel**
- Kiểm tra bot permissions (Manage Channels, Create Channels)
- Kiểm tra role Staff/Admin tồn tại trong server

### ❌ **Message không pin được**
- Kiểm tra bot permissions (Manage Messages)
- Kênh có đủ slot pin (50 message limit)

---

## 📚 Tài Liệu Thêm

- `README.md` - Tổng quan dự án
- `COMMANDS.md` - Danh sách lệnh
- `GUIDE.md` - Hướng dẫn chi tiết

---

## ✨ Lợi Ích Upgrade

✅ **Dropdown menu** - Giao diện chuyên nghiệp hơn  
✅ **Pinned messages** - Dễ tìm thấy thông tin quan trọng  
✅ **Categories tùy chỉnh** - Thêm/bớt loại ticket dễ dàng  
✅ **Permissions tự động** - Kênh ticket riêng tư 100%  
✅ **Better UX** - Người dùng mới dễ sử dụng  

---

**Made with ❤️ by Ticket Bot v2.0**

Chúc bạn thành công! 🚀
