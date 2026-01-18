# 🎮 Command Reference

## Admin Commands

### Setup
```
!setup [category_name]
```
- **Mô tả**: Tạo panel ticket mới
- **Ví dụ**: `!setup General Support`
- **Kết quả**: Bot gửi embed với button "Mở Ticket"

**Quyền**: `Admin`

---

### Panels
```
!panels
```
- **Mô tả**: Xem tất cả panels trong server
- **Kết quả**: Danh sách tất cả ticket panels

**Quyền**: `Admin`

---

### Tickets
```
!tickets
```
- **Mô tả**: Xem tất cả tickets đang mở
- **Kết quả**: Danh sách tất cả active tickets

**Quyền**: `Admin`

---

### Set Config
```
!setconfig [key] [value]
```
- **Mô tả**: Thay đổi cấu hình bot
- **Keys hợp lệ**:
  - `staff_role` - Tên role staff
  - `admin_role` - Tên role admin
  - `ticket_category` - Tên category tickets
  - `ticket_prefix` - Prefix tên channel (mặc định: ticket)
  - `prefix` - Prefix commands (mặc định: !)

**Ví dụ**:
```
!setconfig staff_role Moderator
!setconfig ticket_prefix support
!setconfig prefix !!
```

**Quyền**: `Admin`

---

## Staff Commands (Chỉ trong Ticket Channel)

### Close
```
!close [reason]
```
- **Mô tả**: Đóng ticket
- **Ví dụ**: `!close Vấn đề đã được giải quyết`
- **Kết quả**: Ticket được đóng, channel được xóa sau 5 giây

**Quyền**: `Staff` hoặc `Admin`

---

### Claim
```
!claim
```
- **Mô tả**: Claim ticket (nhận việc xử lý)
- **Kết quả**: Ticket được gán cho staff
- **Lưu ý**: Một ticket chỉ có thể claim bởi 1 staff

**Quyền**: `Staff` hoặc `Admin`

---

### Add Member
```
!add [@user]
```
- **Mô tả**: Thêm user vào ticket
- **Ví dụ**: `!add @John`
- **Kết quả**: User được thêm vào channel

**Quyền**: `Staff` hoặc `Admin`

---

### Remove Member
```
!remove [@user]
```
- **Mô tả**: Xóa user khỏi ticket
- **Ví dụ**: `!remove @John`
- **Kết quả**: User bị xóa khỏi channel

**Quyền**: `Staff` hoặc `Admin`

---

### Transfer Ticket
```
!transfer [@user]
```
- **Mô tả**: Chuyển ownership ticket cho user khác
- **Ví dụ**: `!transfer @Moderator2`
- **Kết quả**: User khác trở thành chủ ticket

**Quyền**: `Staff` hoặc `Admin`

---

### Ticket Info
```
!ticketinfo [ticket_id]
```
- **Mô tả**: Xem thông tin chi tiết ticket
- **Ví dụ**: `!ticketinfo abc123`
- **Thông tin hiển thị**:
  - Người mở
  - Danh mục
  - Trạng thái (mở/đóng)
  - Người claim
  - Ngày tạo
  - Số members

**Quyền**: `Staff` hoặc `Admin`

---

## User Commands

### My Tickets
```
!mytickets
```
- **Mô tả**: Xem tất cả tickets của mình
- **Kết quả**: Danh sách tickets người dùng đã mở

**Quyền**: Bất kỳ user nào

---

## Button Interactions

### Mở Ticket (Button)
- **Nơi**: Trong panel embed
- **Cách dùng**: Nhấn button "Mở Ticket [Category]"
- **Kết quả**: 
  - Tạo channel ticket mới
  - Gửi welcome message
  - Thêm permissions cho user

---

### Đóng Ticket (Button)
- **Nơi**: Trong ticket channel (welcome message)
- **Cách dùng**: Nhấn button "🔒 Đóng Ticket"
- **Kết quả**: Đóng ticket tương tự như `!close`

---

## Command Examples

### Quy trình bình thường

1. **Admin tạo panel**:
```
!setup Technical Support
```

2. **User mở ticket**:
- Nhấn button "Mở Ticket (Technical Support)"

3. **Staff claim ticket**:
```
!claim
```

4. **Staff xử lý vấn đề**:
- Trò chuyện với user
- Thêm staff khác nếu cần: `!add @helper`

5. **Staff đóng ticket**:
```
!close Vấn đề đã xong
```

---

## Lưu ý quan trọng

⚠️ **Cần Role**: Staff hoặc Admin  
⚠️ **Quyền Bot**: Manage Channels, Manage Roles  
⚠️ **Channel**: Một số command chỉ dùng trong ticket channel  
✅ **Button**: Không cần command prefix, chỉ nhấn button

---

## Troubleshooting

### Command không hoạt động
- Kiểm tra role Staff/Admin
- Kiểm tra bot có quyền không
- Kiểm tra tên command chính xác

### Button không hiển thị
- Kiểm tra bot có quyền Embed Links
- Restart bot

### Ticket không được tạo
- Kiểm tra bot quyền tạo channel
- Kiểm tra category tồn tại/được tạo

---

**Last Updated**: 18/01/2024  
**Version**: 1.0.0
