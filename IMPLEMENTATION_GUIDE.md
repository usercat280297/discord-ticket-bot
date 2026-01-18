# 🎫 Discord Ticket Bot - Hướng Dẫn Triển Khai

## 📋 Cách Hoạt Động của Ticket Bot

### 1. **Tạo Ticket**
- User bấm nút **"Mở Ticket"** trong panel ticket
- Bot tự động tạo một channel riêng cho ticket
- Channel được đặt tên theo định dạng: `ticket-[ID_NGẪU_NHIÊN]`
- Chỉ user, staff, và admin mới có thể thấy channel này

### 2. **Welcome Message**
Khi ticket được tạo, bot gửi một embed chứa:
- 🎫 **Tiêu đề**: "Welcome to your ticket"
- 📋 **Danh mục**: Loại ticket đang được xử lý
- ⏱️ **Thời gian phản hồi**: Thông tin về thời gian đợi
- 📝 **Hướng dẫn**: Chi tiết cách sử dụng
- **Các nút (Buttons)**:
  - ✅ **It Works!** - User xác nhận vấn đề đã giải quyết
  - 🆘 **Need Help** - User yêu cầu trợ giúp thêm
  - 🔒 **Đóng Ticket** - Staff đóng ticket thủ công

### 3. **Xử Lý Ticket**

#### **Nút "It Works!"** ✅
- **Chức năng**: User bấm khi vấn đề đã được giải quyết
- **Quá trình**:
  1. Bot hiển thị embed xác nhận vấn đề đã giải quyết
  2. **Tự động đóng ticket** trong database
  3. **Xóa channel sau 5 giây**
  4. Log hành động vào file log

```
✅ Vấn đề Đã Giải Quyết
@User đã xác nhận rằng vấn đề đã được giải quyết.
💬 Cảm ơn bạn đã sử dụng dịch vụ của chúng tôi!
(Ticket sẽ được đóng trong 5 giây...)
```

#### **Nút "Need Help"** 🆘
- **Chức năng**: User vẫn cần trợ giúp thêm
- **Quá trình**:
  1. Bot gửi thông báo yêu cầu trợ giúp
  2. **Ping staff role** (nếu có)
  3. Cập nhật status ticket thành `"need_help"`
  4. Staff sẽ được thông báo và hỗ trợ

```
🆘 Yêu Cầu Trợ Giúp
@User vẫn cần trợ giúp thêm.
📞 Staff sẽ sớm hỗ trợ bạn!
```

#### **Nút "Đóng Ticket"** 🔒
- **Chức năng**: Staff/Admin đóng ticket thủ công
- **Quyền yêu cầu**: `@Staff` hoặc `@Admin` role
- **Quá trình**:
  1. Lưu thông tin về người đóng ticket
  2. Hiển thị embed xác nhận
  3. Xóa channel sau 5 giây

### 4. **Cơ Chế Lưu Trữ Dữ Liệu**

#### **Ticket Mở**
Lưu trong `data/tickets.json` với các trường:
```json
{
  "ticket_id": "abc123",
  "user_id": 123456789,
  "channel_id": 987654321,
  "guild_id": 111111111,
  "category": "General Support",
  "claimed_by": null,
  "claimed_at": null,
  "created_at": "2026-01-18T10:30:00.000000",
  "closed": false,
  "closed_at": null,
  "closed_by": null,
  "members": [123456789],
  "status": "open"
}
```

#### **Ticket Đóng**
Khi đóng ticket:
- `closed`: `true`
- `closed_at`: Timestamp của thời điểm đóng
- `closed_by`: User ID của người đóng
- **Chuyển vào danh sách `closed_tickets`**
- **Xóa khỏi danh sách `tickets`**

### 5. **Các Lệnh Quản Lý**

| Lệnh | Mô Tả | Quyền | Sử Dụng |
|------|-------|-------|--------|
| `!setup [category]` | Tạo panel ticket | Admin | `!setup "General Support"` |
| `/claim` | Claim ticket | Staff | Dùng trong channel ticket |
| `/add @user` | Thêm member | Staff | `/add @UserName` |
| `/remove @user` | Xóa member | Staff | `/remove @UserName` |
| `/transfer @user` | Chuyển ticket | Staff | `/transfer @UserName` |
| `!mytickets` | Xem tickets của bạn | User | `!mytickets` |

### 6. **Quy Trình Đóng Ticket Chi Tiết**

```
User mở ticket
    ↓
Bot tạo channel + gửi welcome message
    ↓
User bấm "It Works!" (hoặc Staff bấm "Close")
    ↓
Bot cập nhật status thành "closed" trong database
    ↓
Bot gửi embed xác nhận
    ↓
Chờ 5 giây (delay để user thấy message)
    ↓
🗑️ XÓA CHANNEL TICKET (tự động)
    ↓
✅ Ticket hoàn toàn đóng
```

### 7. **Cấu Hình (`config.json`)**

```json
{
  "prefix": "!",
  "staff_role": "Staff",
  "admin_role": "Admin",
  "ticket_category": "Tickets",
  "ticket_prefix": "ticket",
  "welcome_message": "Cảm ơn bạn đã mở ticket!...",
  "ticket_color": 5814783,
  "auto_close_delay": 5,
  "auto_close_inactive": 1800,
  "max_user_tickets": 3
}
```

**Giải thích cấu hình**:
- `auto_close_delay`: **5 giây** - Thời gian chờ trước khi xóa channel
- `auto_close_inactive`: **1800 giây** (30 phút) - Thời gian không hoạt động trước khi đóng tự động
- `max_user_tickets`: **3** - Số ticket tối đa mỗi user có thể mở cùng lúc

### 8. **Bảo Mật & Quyền Hạn**

**Channel Permissions**:
- ❌ `@everyone` - Không thể xem
- ✅ **User tạo ticket** - Xem, gửi tin nhắn, đọc lịch sử
- ✅ **@Staff role** - Xem, gửi tin nhắn, đọc lịch sử, quản lý
- ✅ **@Admin role** - Toàn quyền

**Kiểm tra quyền trong code**:
```python
@is_admin()  # Chỉ Admin
@is_staff()  # Staff hoặc Admin
@is_ticket_channel()  # Chỉ dùng trong channel ticket
```

### 9. **Quy Trình Activation Panel (Như Ảnh)**

Từ hình ảnh bạn cung cấp, đây là workflow:

```
1️⃣ User mở ticket
   ↓
2️⃣ Bot gửi hướng dẫn (steps, images, token)
   ↓
3️⃣ User thực hiện từng bước
   ↓
4️⃣ User bấm "✅ It Works!" khi hoàn tất
   ↓
5️⃣ Bot đóng ticket + xóa channel sau 5s
   ↓
6️⃣ ✅ Hoàn tất!
```

Hoặc nếu có vấn đề:
```
4️⃣ User bấm "🆘 Need Help"
   ↓
5️⃣ Bot ping @Staff
   ↓
6️⃣ Staff giúp đỡ
   ↓
7️⃣ User bấm "✅ It Works!" hoặc Staff bấm "🔒 Close"
```

### 10. **Logging & Debugging**

Bot ghi lại tất cả hành động quan trọng:
```
✅ Bot đăng nhập thành công
📊 Bot đang phục vụ X server
✅ Đã load cog: tickets.py
Ticket created: abc123 by User
Ticket closed via 'It Works': abc123 by User
Help requested for ticket: abc123 by User
```

---

## 🚀 Cách Sử Dụng Bot

### **Bước 1: Tạo Panel Ticket**
```
!setup General Support
```
Admin gõ lệnh này trong channel nào đó, bot sẽ gửi message với nút để user bấm mở ticket.

### **Bước 2: User Mở Ticket**
- Bấm nút **"Mở Ticket (General Support)"**
- Bot tạo channel tự động
- Bot gửi welcome message

### **Bước 3: Xử Lý Ticket**
- **User giải quyết**: Bấm ✅ **It Works!** → Channel auto-delete
- **User cần help**: Bấm 🆘 **Need Help** → Ping staff
- **Staff can thiệp**: Bấm 🔒 **Close** → Close + auto-delete

### **Bước 4: Kiểm Tra Tickets**
```
!mytickets
```
User hoặc staff có thể xem tất cả ticket đang mở.

---

## ⚙️ Thay Đổi Gần Đây

✅ **Thêm nút "It Works!"** - Tự động đóng ticket khi user bấm
✅ **Thêm nút "Need Help"** - Ping staff khi user cần trợ giúp
✅ **Auto-delete channel** - Xóa sau 5 giây
✅ **Cấu hình linh hoạt** - Tất cả có thể thay đổi trong `config.json`
✅ **Lưu trữ status** - Theo dõi trạng thái ticket

---

## 🐛 Troubleshooting

### **Bot không phản hồi button**
- Kiểm tra bot có `intents.message_content = True` không
- Kiểm tra bot có message content intent trong Discord Developer Portal

### **Channel không xóa**
- Kiểm tra bot có quyền delete channel không
- Kiểm tra `auto_close_delay` trong config

### **Staff không nhận ping**
- Kiểm tra role name đúng là "Staff" không
- Kiểm tra staff role có cao hơn bot role không

---

**✅ Bot ticket đã sẵn sàng hoạt động!**
