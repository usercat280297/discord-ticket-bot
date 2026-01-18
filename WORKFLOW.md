# 📋 Ticket Workflow Documentation

## 🎯 Tổng quan quy trình

```
┌─────────────────────────────────────────────────────────────┐
│                   DISCORD TICKET BOT FLOW                   │
└─────────────────────────────────────────────────────────────┘

1. SETUP PHASE
   ├─ Admin tạo roles (Staff, Admin)
   ├─ Bot tạo ticket panels (!setup)
   └─ Panels ready

2. USER PHASE
   ├─ User nhấn button "Mở Ticket"
   ├─ Bot tạo ticket channel
   └─ Bot gửi welcome message

3. STAFF PHASE
   ├─ Staff claim ticket (!claim)
   ├─ Staff chat với user
   ├─ Staff add/remove members
   └─ Ticket đang xử lý

4. CLOSE PHASE
   ├─ Staff đóng ticket (!close)
   ├─ Bot lưu lịch sử
   └─ Bot xóa channel
```

---

## Phase 1: Setup

### 1.1 Chuẩn bị Server

**Bước 1**: Tạo Roles
```
Settings → Roles
┌─────────────────────────────────┐
│ Role Name    │ Color    │ Perms │
├──────────────┼──────────┼───────┤
│ Admin        │ Red      │ All   │
│ Staff        │ Blue     │ View  │
│ User         │ Default  │ View  │
└─────────────────────────────────┘
```

**Bước 2**: Gán Roles
- Admin → Bot Owner, Senior Mods
- Staff → Moderators, Helpers
- User → Everyone

**Bước 3**: Tạo Channels
```
Channels cần thiết:
├─ #general
├─ #announcements
├─ #support (Panel sẽ ở đây)
└─ #tickets-logs (Optional - để lưu logs)
```

### 1.2 Bot Setup

**Bước 1**: Invite Bot
```
Quyền cần:
✓ View Channels
✓ Send Messages
✓ Embed Links
✓ Manage Channels
✓ Manage Roles
✓ Read Message History
```

**Bước 2**: Cấu hình
```bash
python setup.py  # Tạo .env
python main.py   # Chạy bot
```

**Bước 3**: Tạo Panels
```
!setup General Support
!setup Technical Support
!setup Billing
```

---

## Phase 2: User mở Ticket

### Flow Chi tiết

```
USER ACTION
    │
    ├─ 1. Nhấn button "Mở Ticket (Category)"
    │
BOT RESPONSE (TicketCreateButton.callback)
    │
    ├─ 2. Kiểm tra user đã có ticket chưa
    │     └─ YES → Từ chối (ephemeral message)
    │     └─ NO  → Tiếp tục
    │
    ├─ 3. Tạo channel ticket
    │     ├─ Channel name: "ticket-[6 ký tự]"
    │     ├─ Category: "Tickets"
    │     └─ Topic: "Ticket của {user} | Category: {category}"
    │
    ├─ 4. Set permissions
    │     ├─ @everyone: ❌ Không thể view
    │     ├─ User: ✅ View + Send + Read History
    │     ├─ Staff: ✅ View + Send + Read History
    │     └─ Admin: ✅ View + Send + Read History
    │
    ├─ 5. Lưu ticket vào database
    │     └─ tickets.json → tickets[ticket_id]
    │
    ├─ 6. Gửi welcome message
    │     ├─ Embed chào mừng (TicketCreateButton embed)
    │     ├─ Close button
    │     └─ Hướng dẫn lệnh
    │
    └─ 7. Phản hồi user
          └─ ✅ "Ticket đã được mở: #ticket-[id]"

DATABASE UPDATE
{
  "ticket_id": "abc123",
  "user_id": 111111,
  "channel_id": 222222,
  "status": "open",
  "claimed_by": null,
  ...
}
```

### Dữ liệu lưu trữ
```json
{
  "tickets": {
    "abc123": {
      "ticket_id": "abc123",
      "user_id": 111111,
      "channel_id": 222222,
      "guild_id": 333333,
      "category": "General Support",
      "claimed_by": null,
      "claimed_at": null,
      "created_at": "2024-01-18T10:30:00.000",
      "closed": false,
      "closed_at": null,
      "closed_by": null,
      "members": [111111]
    }
  }
}
```

---

## Phase 3: Staff xử lý

### 3.1 Staff Claim Ticket

```
STAFF ACTION: !claim

BOT PROCESS
    │
    ├─ 1. Kiểm tra staff có role?
    │     └─ NO → Từ chối + lỗi
    │
    ├─ 2. Kiểm tra có phải ticket channel?
    │     └─ NO → Từ chối
    │
    ├─ 3. Kiểm tra ticket đã claim chưa?
    │     └─ YES → Từ chối + thông báo
    │
    ├─ 4. Claim ticket
    │     └─ claimed_by = staff_id
    │     └─ claimed_at = now
    │
    └─ 5. Gửi thông báo
          └─ "✅ Ticket claimed by @Staff"

DATABASE UPDATE
{
  "ticket_id": "abc123",
  "claimed_by": 444444,
  "claimed_at": "2024-01-18T10:35:00.000"
}
```

### 3.2 Staff Thêm Members

```
STAFF ACTION: !add @user

BOT PROCESS
    │
    ├─ 1. Kiểm tra user hợp lệ
    │     └─ NO → Từ chối
    │
    ├─ 2. Add permissions trong channel
    │     └─ View + Send + Read History
    │
    ├─ 3. Cập nhật database
    │     └─ Add user ID vào members list
    │
    └─ 4. Thông báo
          └─ "✅ @user added to ticket"

DATABASE UPDATE
{
  "ticket_id": "abc123",
  "members": [111111, 555555]  // Added new member
}
```

### 3.3 Staff Chat & Support

```
Trong ticket channel:
┌─────────────────────────────────────┐
│ 👤 User: Giúp mình cái này được không?
│ 👨‍💼 Staff: Chắc chắn! Bạn có thể mô tả...
│ 👤 User: ...
│ 👨‍💼 Staff: Vậy tôi xử lý cho bạn
└─────────────────────────────────────┘

Các action có thể:
├─ !add @helper     - Thêm staff khác
├─ !remove @user    - Xóa member
├─ !transfer @staff - Chuyển cho staff khác
└─ !claim           - Xác nhận claim
```

---

## Phase 4: Đóng Ticket

### 4.1 Staff Đóng

```
STAFF ACTION: !close Vấn đề đã giải quyết

BOT PROCESS
    │
    ├─ 1. Kiểm tra quyền staff
    │     └─ NO → Từ chối
    │
    ├─ 2. Lấy thông tin ticket
    │     └─ ticket_id, user, reason
    │
    ├─ 3. Tạo closed embed
    │     ├─ Title: "🔒 Ticket Đã Đóng"
    │     ├─ Content: "Lý do: {reason}"
    │     ├─ Người mở: @user
    │     └─ Người đóng: @staff
    │
    ├─ 4. Gửi closed embed
    │     └─ Display 5 giây
    │
    ├─ 5. Update database
    │     ├─ closed = true
    │     ├─ closed_at = now
    │     ├─ closed_by = staff_id
    │     └─ Move từ "tickets" → "closed_tickets"
    │
    ├─ 6. Lưu transcript (optional)
    │     └─ Lưu tin nhắn để lịch sử
    │
    └─ 7. Xóa channel
          └─ Sau 5 giây, xóa channel

DATABASE UPDATE
{
  // Xóa từ "tickets"
  // Thêm vào "closed_tickets":
  {
    "ticket_id": "abc123",
    "user_id": 111111,
    "channel_id": 222222,
    "category": "General Support",
    "claimed_by": 444444,
    "created_at": "2024-01-18T10:30:00.000",
    "closed": true,
    "closed_at": "2024-01-18T10:45:00.000",
    "closed_by": 444444,
    "reason": "Vấn đề đã giải quyết"
  }
}
```

### 4.2 Button Đóng (Alternative)

```
USER ACTION: Nhấn button "🔒 Đóng Ticket"

BOT PROCESS
    │
    ├─ 1. Kiểm tra (tương tự !close)
    │
    └─ 2. Xử lý (tương tự !close)

Kết quả: Same as !close command
```

---

## 📊 Các trạng thái Ticket

```
┌──────────────────────────────────────┐
│        TICKET STATE DIAGRAM          │
└──────────────────────────────────────┘

    CREATED (open, not claimed)
        │
        ├─ !claim
        │    │
        │    v
        CLAIMED (open, claimed by staff)
        │
        ├─ !add / !remove (members thay đổi)
        │
        ├─ !transfer (change owner)
        │
        └─ !close
             │
             v
        CLOSED (archived)
             │
             └─ Lưu vào closed_tickets


Timeout (optional feature):
    ├─ Auto-close sau X ngày
    ├─ Archive channel
    └─ Notify user
```

---

## 📈 Thống kê & Báo cáo

### Metrics có thể track

```
Total tickets:
├─ Mở: 5
├─ Claim: 3
├─ Chưa claim: 2
└─ Đóng: 127

By category:
├─ General Support: 45
├─ Technical: 56
├─ Billing: 26

Response time:
├─ Avg: 15 phút
├─ Min: 2 phút
├─ Max: 4 giờ

Staff stats:
├─ @Staff1: 45 tickets claim
├─ @Staff2: 38 tickets claim
└─ @Staff3: 22 tickets claim
```

---

## 🔄 Alternative Workflows

### Workflow A: Fast Support
```
User: !mytickets
      → Xem ticket đang mở
      → Trò chuyện tiếp
      → !close (tự đóng)
```

### Workflow B: Multi-staff
```
Staff1: !claim
        ├─ !add @Staff2
        └─ Chat với user

Staff2: Hỗ trợ Staff1
        └─ Xử lý vấn đề

Staff1: !close
        └─ Ticket đóng
```

### Workflow C: Escalation
```
Staff1: Chat với user
        → Vấn đề phức tạp
        └─ !transfer @Manager

Manager: Xử lý vấn đề
         └─ !close
```

---

## ⚠️ Edge Cases

### Case 1: User rời server
```
Ticket vẫn mở
└─ Bot sẽ keep permissions
└─ Ticket có thể đóng thủ công

Fix:
├─ on_member_remove event
├─ Auto-close tickets
└─ Notify staff
```

### Case 2: Bot bị kick
```
Tickets mất permissions
└─ Channels vẫn tồn tại

Fix:
├─ Invite bot lại
├─ Recover từ database
└─ Restore permissions
```

### Case 3: Category bị xóa
```
Ticket channels mở hiu
└─ Vẫn hoạt động nhưng xấu

Fix:
├─ Tạo category "Tickets" mới
├─ Move channels
└─ Update database
```

---

## 📝 Checklist Deployment

- [ ] Roles tạo (Staff, Admin)
- [ ] Bot invited + permissions
- [ ] `.env` có token
- [ ] `config.json` cấu hình đúng
- [ ] Chạy `python main.py`
- [ ] Bot online (status change)
- [ ] Test `!setup General Support`
- [ ] Panel hiển thị + button hoạt động
- [ ] User mở ticket thành công
- [ ] Staff claim + close hoạt động
- [ ] Database lưu dữ liệu
- [ ] Channel được xóa sau close

---

**Version**: 1.0.0  
**Last Updated**: 18/01/2024
