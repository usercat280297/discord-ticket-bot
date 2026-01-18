# ❓ FAQ - Câu hỏi thường gặp

## 🚀 Cài đặt & Chạy

### Q1: Bot không hoạt động sau khi chạy
**A**: Kiểm tra:
1. Token trong `.env` có đúng?
   ```
   DISCORD_TOKEN=your_actual_token_here
   ```
2. Python >= 3.8?
   ```bash
   python --version
   ```
3. Các packages đã cài?
   ```bash
   pip install -r requirements.txt
   ```
4. Xem log lỗi chi tiết

---

### Q2: Làm sao để lấy Discord Bot Token?
**A**: Làm theo các bước:
1. Vào [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application"
3. Đặt tên, click "Create"
4. Tab "Bot" → "Add Bot"
5. Copy token ở phần "TOKEN"
6. Paste vào `.env`

---

### Q3: Bot không join được server
**A**: 
1. Kiểm tra bot đã được invite chưa:
   - [Discord OAuth2 URL Generator](https://discordapi.com/permissions.html#0)
   - Chọn scopes: `bot`
   - Chọn permissions:
     - Send Messages
     - Embed Links
     - Manage Channels
     - Manage Roles
2. Copy URL và dán vào browser

---

## 🎮 Lệnh & Commands

### Q4: Command không hoạt động
**A**: Kiểm tra:
1. Prefix đúng? (Default: `!`)
   - Xem config.json
   - Hoặc dùng `!setconfig prefix !!`
2. User có role cần thiết?
   - Staff command → cần role "Staff"
   - Admin command → cần role "Admin"
3. Bot có quyền không?
   - Check Server Settings → Roles

---

### Q5: Sao không thể tạo ticket?
**A**: 
1. User đã có ticket mở rồi?
   - Chỉ có thể mở 1 ticket cùng lúc
   - Dùng `!close` để đóng cái cũ
2. Bot quyền tạo channel?
3. Category "Tickets" tồn tại?
   - Bot sẽ tự tạo nếu không có

---

### Q6: Button "Mở Ticket" không hiển thị
**A**:
1. Bot quyền "Embed Links"?
2. Restart bot
3. Panel được tạo bởi `!setup` chính xác?

---

## 👥 Quản lý Tickets

### Q7: Làm sao để claim ticket?
**A**: 
1. Vào ticket channel
2. Dùng lệnh:
   ```
   !claim
   ```
3. Hoặc có thể tạo button claim custom

---

### Q8: Sao không thể thêm member vào ticket?
**A**:
1. User phải trong server
2. Dùng mention: `!add @username`
3. Không phải `!add username`

---

### Q9: Làm sao xem tất cả tickets?
**A**: Dùng:
```
!tickets
```
Chỉ admin mới thấy được

---

## 🔒 Quyền & Roles

### Q10: Làm sao tạo role Staff/Admin?
**A**:
1. Server Settings → Roles
2. Click "Create Role"
3. Tên: `Staff` hoặc `Admin`
4. Gán cho users muốn
5. Đảm bảo role cao hơn bot role

---

### Q11: Sao lệnh admin không hoạt động?
**A**:
1. User có role "Admin" không?
2. Role "Admin" được đặt cao hơn bot role?
   - Server Settings → Roles → Kéo role "Admin" lên cao hơn bot
3. Kiểm tra role name trong config.json chính xác

---

### Q12: Làm sao phân quyền cho staff?
**A**:
1. Tạo role "Staff"
2. Gán role cho các user muốn
3. Staff tự động có quyền:
   - !claim
   - !close
   - !add / !remove
   - !transfer

---

## 📊 Database & Dữ liệu

### Q13: Dữ liệu tickets lưu ở đâu?
**A**: File `data/tickets.json`
```
Cấu trúc:
{
  "panels": [...],        // Panels đã tạo
  "tickets": {...},       // Tickets đang mở
  "closed_tickets": [...]  // Lịch sử tickets
}
```

---

### Q14: Làm sao backup tickets?
**A**:
1. Copy file `data/tickets.json`
2. Lưu ở nơi an toàn
3. Nếu mất, paste lại file

---

### Q15: Làm sao xóa ticket từ database?
**A**:
1. Đóng ticket bình thường: `!close`
2. Bot tự động lưu vào "closed_tickets"
3. Hoặc edit `data/tickets.json` trực tiếp

---

## 🛠️ Cấu hình & Tùy chỉnh

### Q16: Làm sao đổi welcome message?
**A**:
1. Mở `config.json`
2. Tìm `"welcome_message"`
3. Sửa thành:
   ```json
   "welcome_message": "Chào bạn! Vui lòng mô tả vấn đề..."
   ```

---

### Q17: Làm sao đổi màu embed?
**A**:
1. Tìm RGB color từ [Color Picker](https://htmlcolorcodes.com/)
2. Convert sang decimal
3. Sửa trong `config.json`:
   ```json
   "ticket_color": 3447003
   ```

---

### Q18: Làm sao đổi prefix?
**A**:
```
!setconfig prefix !!
```
Hoặc sửa `config.json`:
```json
"prefix": "!!"
```

---

## 🐛 Lỗi & Xử lý sự cố

### Q19: "Command not found" error
**A**:
1. Kiểm tra command chính xác
2. Prefix đúng?
3. Restart bot
4. Xem COMMANDS.md

---

### Q20: "You don't have permission" error
**A**:
1. Bot không đủ quyền
2. Kiểm tra Server Settings → Roles
3. Bot role phải cao hơn hoặc bằng cấp target

---

### Q21: Channel không được xóa sau đóng ticket
**A**:
1. Bot không có quyền delete channel?
2. Xóa thủ công hoặc:
3. Chạy lại bot

---

### Q22: Database bị lỗi/corrupt
**A**:
1. Backup lại data
2. Xóa `data/tickets.json`
3. Chạy bot
4. Bot tự tạo file mới

---

## 💬 Tính năng Advanced

### Q23: Làm sao thêm log/transcript?
**A**: 
Có thể custom trong `cogs/tickets.py`:
```python
# Thêm vào close_ticket() function
# Save transcript trước xóa channel
```

---

### Q24: Làm sao gửi thông báo khi ticket mở?
**A**:
Edit `cogs/tickets.py` - `TicketCreateButton.callback()`:
```python
# Thêm sau khi tạo channel
notification_channel = bot.get_channel(NOTIFICATION_CHANNEL_ID)
await notification_channel.send(f"New ticket: {channel.mention}")
```

---

### Q25: Làm sao custom button/emoji?
**A**:
Edit `utils/embed.py` hoặc `cogs/tickets.py`:
```python
# Thay đổi label, emoji, style
button = TicketCreateButton(category)
button.label = "🎟️ Support Ticket"
button.style = discord.ButtonStyle.green
```

---

## 📞 Support

### Q26: Gặp lỗi mà không biết fix?
**A**:
1. Kiểm tra logs chi tiết
2. Xem error message
3. Google error message
4. Kiểm tra quyền bot
5. Restart bot

---

### Q27: Bot hoạt động lạ?
**A**:
1. Kiểm tra version discord.py: `pip show discord.py`
2. Update: `pip install --upgrade discord.py`
3. Xem file logs

---

### Q28: Cần thêm tính năng gì?
**A**:
Có thể custom trong:
- `cogs/tickets.py` - Thêm commands/buttons
- `utils/embed.py` - Thay đổi embed style
- `utils/database.py` - Thay đổi data structure

---

## 📚 Tài liệu thêm

### Xem thêm:
- [README.md](README.md) - Hướng dẫn cơ bản
- [GUIDE.md](GUIDE.md) - Hướng dẫn chi tiết
- [COMMANDS.md](COMMANDS.md) - Danh sách commands
- [STRUCTURE.md](STRUCTURE.md) - Cấu trúc dự án

### Link hữu ích:
- [discord.py Docs](https://discordpy.readthedocs.io/)
- [Discord Developer Portal](https://discord.com/developers)
- [Discord.py GitHub](https://github.com/Rapptz/discord.py)

---

**Version**: 1.0.0  
**Last Updated**: 18/01/2024

Có câu hỏi khác? Hãy kiểm tra lại tài liệu hoặc xem logs để tìm lỗi! 🎯
