# Discord Ticket Bot
Một Discord bot quản lý ticket đầy đủ với hỗ trợ multi-panel, auto-reply, và quản lý tickets.

## Tính năng
- ✅ Multi-panel ticket system
- ✅ Tự động gửi message chào mừng khi ticket được mở
- ✅ Quản lý tickets (open, close, claim, transfer)
- ✅ Lưu trữ dữ liệu tickets
- ✅ Phân quyền (staff, admin)
- ✅ Transcript tickets

## Cài đặt

### 1. Clone/Download dự án
```bash
cd discord-ticket-bot
```

### 2. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 3. Tạo file .env
```
DISCORD_TOKEN=your_bot_token_here
PREFIX=!
```

### 4. Chạy bot
```bash
python main.py
```

## Lệnh chính

| Lệnh | Mô tả | Quyền |
|------|-------|-------|
| `!setup` | Tạo panel ticket | Admin |
| `!close` | Đóng ticket | Staff |
| `!claim` | Claim ticket | Staff |
| `!transfer` | Chuyển ticket | Staff |
| `!add` | Thêm người dùng vào ticket | Staff |
| `!remove` | Xóa người dùng khỏi ticket | Staff |

## Cấu trúc dự án
```
discord-ticket-bot/
├── main.py              # File chính
├── config.json          # Cấu hình
├── cogs/
│   ├── __init__.py
│   ├── tickets.py       # Ticket commands
│   ├── events.py        # Event handlers
│   └── moderation.py    # Moderation commands
├── data/
│   └── tickets.json     # Database
├── utils/
│   ├── __init__.py
│   ├── database.py      # Database functions
│   ├── embed.py         # Embed generators
│   └── checks.py        # Permission checks
├── requirements.txt
├── .env                 # Environment variables
└── README.md
```

## Thông tin
- **Python**: 3.8+
- **Discord.py**: 2.3.2
