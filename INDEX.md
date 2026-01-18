# 📚 Discord Ticket Bot - Tài liệu & Hướng dẫn

## 🚀 Bắt đầu nhanh

1. **Cài đặt lần đầu**:
   ```bash
   python setup.py
   pip install -r requirements.txt
   python main.py
   ```

2. **Chạy lần sau**:
   - **Windows**: Chạy `run.bat`
   - **Linux/Mac**: Chạy `run.sh` hoặc `python main.py`

3. **Tạo panel ticket**:
   ```
   !setup General Support
   ```

---

## 📖 Tài liệu (Đọc theo thứ tự)

### 📄 1. [README.md](README.md) - Tổng quan
- Tính năng chính
- Cài đặt cơ bản
- Link tài liệu

### 📋 2. [GUIDE.md](GUIDE.md) - Hướng dẫn chi tiết
- Cài đặt từng bước
- Cấu hình
- Lệnh chính
- Xử lý sự cố cơ bản

### 🎮 3. [COMMANDS.md](COMMANDS.md) - Danh sách commands
- Tất cả commands
- Quyền cần thiết
- Ví dụ sử dụng
- Troubleshooting commands

### 📁 4. [STRUCTURE.md](STRUCTURE.md) - Cấu trúc dự án
- Chi tiết từng file
- Flow diagram
- Database schema
- Dependency tree

### 📋 5. [WORKFLOW.md](WORKFLOW.md) - Quy trình làm việc
- Flow từng phase
- State diagram
- Edge cases
- Deployment checklist

### ❓ 6. [FAQ.md](FAQ.md) - Câu hỏi thường gặp
- Setup issues
- Command issues
- Permission issues
- Advanced features

---

## 🗂️ Cấu trúc thư mục

```
discord-ticket-bot/
│
├── 📄 main.py              ⭐ Chạy cái này để start bot
├── 📄 setup.py             Thiết lập lần đầu
├── 📄 .env                 Token bot (BẢO MẬT!)
├── 📄 config.json          Cấu hình bot
│
├── 📁 cogs/                Các tính năng
│   ├── tickets.py          ⭐ Main feature
│   ├── events.py           Event listeners
│   └── moderation.py       Admin commands
│
├── 📁 utils/               Hàm tiện ích
│   ├── database.py         Lưu/load data
│   ├── embed.py            Tạo embeds
│   └── checks.py           Permission checks
│
├── 📁 data/                Dữ liệu
│   └── tickets.json        Database tickets
│
├── 📄 requirements.txt      Dependencies
├── 📄 run.bat              Quick start (Windows)
├── 📄 run.sh               Quick start (Linux/Mac)
│
└── 📖 DOCUMENTATION
    ├── README.md           Overview
    ├── GUIDE.md            Detailed guide
    ├── COMMANDS.md         All commands
    ├── STRUCTURE.md        Project structure
    ├── WORKFLOW.md         Ticket workflow
    ├── FAQ.md              Q&A
    └── INDEX.md            This file
```

---

## 🎯 Tính năng chính

### ✅ Ticket Management
- ✓ Multi-panel ticket system
- ✓ Auto-create channels
- ✓ Permission management
- ✓ Member management (add/remove)
- ✓ Ticket claiming
- ✓ Ticket transfer

### ✅ Database
- ✓ JSON-based storage
- ✓ Ticket history
- ✓ Panel tracking
- ✓ Member tracking

### ✅ Customization
- ✓ Custom welcome message
- ✓ Custom colors
- ✓ Custom prefix
- ✓ Role-based permissions

### ✅ Admin Features
- ✓ Panel management
- ✓ Ticket overview
- ✓ Config management
- ✓ Ticket info lookup

---

## 🔑 Key Commands

| Lệnh | Mô tả | Quyền |
|------|-------|-------|
| `!setup [category]` | Tạo panel ticket | Admin |
| `!claim` | Claim ticket | Staff |
| `!close [reason]` | Đóng ticket | Staff |
| `!add @user` | Thêm member | Staff |
| `!remove @user` | Xóa member | Staff |
| `!transfer @user` | Chuyển ticket | Staff |
| `!mytickets` | Xem tickets của mình | User |
| `!tickets` | Xem tất cả tickets | Admin |
| `!panels` | Xem tất cả panels | Admin |

Xem [COMMANDS.md](COMMANDS.md) để xem đầy đủ!

---

## 🛠️ Tech Stack

- **Language**: Python 3.8+
- **Framework**: discord.py 2.3.2
- **Database**: JSON (local file)
- **Dependencies**: python-dotenv

---

## 📝 Setup Checklist

- [ ] Python 3.8+ cài đặt
- [ ] Clone/download dự án
- [ ] Chạy `python setup.py`
- [ ] Cài `pip install -r requirements.txt`
- [ ] Tạo roles (Staff, Admin) trong Discord server
- [ ] Invite bot vào server
- [ ] Chạy `python main.py`
- [ ] Dùng `!setup` để tạo panel
- [ ] Test ticket creation + close

---

## 📊 Database

### Lưu trữ dữ liệu
```json
{
  "panels": [
    {
      "message_id": 123...,
      "channel_id": 456...,
      "category": "General Support"
    }
  ],
  "tickets": {
    "abc123": {
      "user_id": 111...,
      "channel_id": 222...,
      "claimed_by": null,
      "status": "open"
    }
  },
  "closed_tickets": [...]
}
```

Lưu ở: `data/tickets.json`

---

## 🐛 Troubleshooting Quick Links

- **Bot không chạy**: Xem [GUIDE.md #Cài đặt](GUIDE.md#cài-đặt)
- **Command không hoạt động**: Xem [COMMANDS.md](COMMANDS.md) & [FAQ.md #Q4](FAQ.md#q4-command-không-hoạt-động)
- **Ticket không tạo được**: Xem [FAQ.md #Q5](FAQ.md#q5-sao-không-thể-tạo-ticket)
- **Permission error**: Xem [FAQ.md #Q11](FAQ.md#q11-sao-lệnh-admin-không-hoạt-động)
- **Database issue**: Xem [FAQ.md #Q15](FAQ.md#q15-làm-sao-xóa-ticket-từ-database)

---

## 🎓 Học thêm

### Hiểu cách hoạt động
1. Đọc [WORKFLOW.md](WORKFLOW.md) - Quy trình chi tiết
2. Xem [STRUCTURE.md](STRUCTURE.md) - Code organization
3. Tìm hiểu [discord.py docs](https://discordpy.readthedocs.io/)

### Tùy chỉnh bot
1. Edit `config.json` - Thay đổi cấu hình
2. Edit `cogs/tickets.py` - Thêm commands/features
3. Edit `utils/embed.py` - Thay đổi giao diện

### Mở rộng chức năng
1. Thêm transcripts trong `cogs/tickets.py`
2. Thêm reactions trong `utils/embed.py`
3. Thêm logging trong `utils/database.py`

---

## 📞 Support & Help

### Các bước debug
1. Kiểm tra logs chi tiết
2. Xem lỗi message
3. Tìm trong [FAQ.md](FAQ.md)
4. Xem [TROUBLESHOOTING](GUIDE.md#xử-lý-sự-cố) section
5. Restart bot: `Ctrl+C` then `python main.py`

### Tìm thêm thông tin
- 📖 Đọc comments trong code
- 🔍 Tìm error message trên Google
- 💬 Xem [discord.py docs](https://discordpy.readthedocs.io/)
- 📚 Xem toàn bộ [GUIDE.md](GUIDE.md)

---

## 📄 File List

| File | Mô tả |
|------|-------|
| `main.py` | Entry point, bot initialization |
| `setup.py` | Interactive setup script |
| `.env` | Token & config (bảo mật) |
| `config.json` | Bot settings |
| `requirements.txt` | Python packages |
| `cogs/tickets.py` | Main ticket commands |
| `cogs/events.py` | Discord event listeners |
| `cogs/moderation.py` | Admin commands |
| `utils/database.py` | Database functions |
| `utils/embed.py` | Embed creators |
| `utils/checks.py` | Permission decorators |
| `data/tickets.json` | Ticket database |
| `README.md` | Project overview |
| `GUIDE.md` | Detailed setup guide |
| `COMMANDS.md` | Command reference |
| `STRUCTURE.md` | Project structure |
| `WORKFLOW.md` | Ticket workflow |
| `FAQ.md` | Common questions |
| `INDEX.md` | This file |

---

## 🎉 Xong!

Bot của bạn đã sẵn sàng! 

**Bước tiếp theo**:
1. Chạy `python main.py`
2. Dùng `!setup` để tạo panel
3. Test mở/close ticket
4. Tùy chỉnh theo nhu cầu

**Cần giúp?** Xem tài liệu hoặc [FAQ.md](FAQ.md)

---

**Version**: 1.0.0  
**Last Updated**: 18/01/2024  
**Created**: A Comprehensive Discord Ticket Bot
