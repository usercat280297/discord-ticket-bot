# 📁 Project Structure

## Cây thư mục

```
discord-ticket-bot/
│
├── 📄 main.py                    # File chính - Entry point của bot
├── 📄 setup.py                   # Setup script - Thiết lập ban đầu
├── 📄 requirements.txt           # Dependencies (pip)
├── 📄 .env                       # Environment variables (Token, etc)
├── 📄 config.json                # Cấu hình bot
│
├── 📁 cogs/                      # Các tính năng modular (Cogs)
│   ├── 📄 __init__.py
│   ├── 📄 tickets.py             # ⭐ Ticket commands & button handlers
│   ├── 📄 events.py              # Discord event listeners
│   └── 📄 moderation.py          # Admin commands
│
├── 📁 utils/                     # Hàm tiện ích
│   ├── 📄 __init__.py
│   ├── 📄 database.py            # Hàm xử lý database (JSON)
│   ├── 📄 embed.py               # Tạo Discord embeds
│   └── 📄 checks.py              # Permission checks/decorators
│
├── 📁 data/                      # Dữ liệu bot
│   └── 📄 tickets.json           # Database tickets (lưu trữ dữ liệu)
│
├── 📄 README.md                  # Hướng dẫn cơ bản
├── 📄 GUIDE.md                   # Hướng dẫn chi tiết
├── 📄 COMMANDS.md                # Danh sách commands
├── 📄 .gitignore                 # Git ignore file
├── 📄 run.bat                    # Quick start (Windows)
└── 📄 run.sh                     # Quick start (Linux/Mac)
```

## Chi tiết các file

### 🔴 File chính (Main Files)

#### `main.py`
- **Mục đích**: Entry point của bot
- **Chức năng**:
  - Setup Discord bot intents
  - Load tất cả cogs
  - Handle events (on_ready, on_command_error, etc)
  - Start bot

#### `setup.py`
- **Mục đích**: Setup script tương tác
- **Chức năng**:
  - Tạo file .env
  - Tạo config.json
  - Tạo thư mục data

#### `config.json`
- **Mục đích**: Cấu hình bot (không cần code)
- **Chứa**:
  - Prefix commands
  - Tên roles (Staff, Admin)
  - Tên category/channel
  - Welcome message
  - Màu embeds

#### `.env`
- **Mục đích**: Lưu trữ token (bảo mật)
- **Chứa**:
  - Discord bot token
  - Prefix (optional)
- **⚠️ Quan trọng**: KHÔNG commit lên git!

### 🔵 Cogs (Tính năng)

#### `cogs/tickets.py` ⭐ MAIN COG
- **Chức năng chính**:
  - `TicketCreateButton` class - Button để mở ticket
  - `CloseTicketButton` class - Button để đóng ticket
  - `Tickets` cog với commands:
    - `!setup` - Tạo panel
    - `!close` - Đóng ticket
    - `!claim` - Claim ticket
    - `!add` - Thêm member
    - `!remove` - Xóa member
    - `!transfer` - Chuyển ticket
    - `!mytickets` - Xem tickets của mình

#### `cogs/events.py`
- **Chức năng**:
  - Event listeners (on_member_remove, on_message, etc)
  - Interaction handlers

#### `cogs/moderation.py`
- **Chức năng**:
  - `!ticketinfo` - Xem info ticket
  - `!tickets` - Xem tất cả tickets
  - `!panels` - Xem tất cả panels
  - `!setconfig` - Thay đổi config

### 🟡 Utils (Hàm tiện ích)

#### `utils/database.py`
- **Hàm chính**:
  - `load_data()` - Load tickets.json
  - `save_data()` - Lưu data
  - `create_ticket()` - Tạo ticket mới
  - `get_ticket()` - Lấy thông tin ticket
  - `update_ticket()` - Cập nhật ticket
  - `claim_ticket()` - Claim ticket
  - `close_ticket()` - Đóng ticket
  - `add_panel()` - Thêm panel
  - `add_ticket_member()` - Thêm member
  - `remove_ticket_member()` - Xóa member

#### `utils/embed.py`
- **Hàm chính**:
  - `create_panel_embed()` - Tạo embed panel
  - `create_ticket_embed()` - Tạo embed welcome
  - `create_closed_embed()` - Tạo embed đóng
  - `create_info_embed()` - Tạo embed info

#### `utils/checks.py`
- **Decorators**:
  - `@is_staff()` - Check staff role
  - `@is_admin()` - Check admin role
  - `@is_ticket_channel()` - Check ticket channel

### 🟢 Data

#### `data/tickets.json`
```json
{
  "panels": [...],        // Danh sách panels
  "tickets": {...},       // Tickets đang mở
  "closed_tickets": [...]  // Tickets đã đóng (lịch sử)
}
```

---

## Flow Diagram

### User mở Ticket
```
1. User nhấn button "Mở Ticket" 
   └─> `TicketCreateButton.callback()`
   
2. Bot kiểm tra user đã có ticket không
   
3. Bot tạo channel trong category "Tickets"
   
4. Bot set permissions:
   - User: view + send
   - Staff role: view + send
   - Others: can't view
   
5. Bot lưu vào database
   
6. Bot gửi welcome message
   └─> Embed + Close button
```

### Staff xử lý Ticket
```
1. Staff nhấn !claim
   └─> `Tickets.claim()`
   
2. Bot cập nhật database
   └─> claimed_by = staff_id
   
3. Staff chat với user
   
4. Staff nhấn !close [reason]
   └─> `Tickets.close()`
   
5. Bot tạo closed embed
   
6. Bot di chuyển từ "tickets" → "closed_tickets"
   
7. Bot xóa channel sau 5 giây
```

---

## Database Schema

### Panel Object
```javascript
{
  message_id: 123456,              // ID tin nhắn embed
  channel_id: 789012,              // Channel của panel
  guild_id: 345678,                // Server ID
  category: "General Support",     // Tên danh mục
  created_at: "2024-01-18T10:..."  // Thời tạo
}
```

### Ticket Object
```javascript
{
  ticket_id: "abc123",             // ID ticket (6 ký tự)
  user_id: 111111,                 // ID người mở
  channel_id: 222222,              // Channel ticket
  guild_id: 333333,                // Server ID
  category: "General Support",     // Danh mục
  claimed_by: 444444,              // ID người claim (null nếu chưa)
  claimed_at: "2024-01-18T10:...", // Thời claim
  created_at: "2024-01-18T10:...", // Thời tạo
  closed: false,                   // Trạng thái
  closed_at: null,                 // Thời đóng
  closed_by: null,                 // ID người đóng
  members: [111111, 444444]        // Danh sách members
}
```

---

## Cách bot hoạt động

### Startup (`main.py`)
1. Load environment (.env)
2. Load config (config.json)
3. Setup Discord intents
4. Load tất cả cogs (cogs/*.py)
5. Connect tới Discord
6. Emit `on_ready` event

### Command Flow
```
User types: !setup "Support"
         ↓
Bot receives message
         ↓
Process command: "setup"
         ↓
Check permissions (@is_admin)
         ↓
Execute Tickets.setup()
         ↓
Create embed + button
         ↓
Send message
         ↓
Add panel to database
```

### Button Flow
```
User clicks button
         ↓
Discord sends Interaction
         ↓
Button.callback() executed
         ↓
Create channel
         ↓
Save to database
         ↓
Send welcome message
         ↓
Send response
```

---

## Dependency Tree

```
main.py
├─ discord.py (library)
├─ python-dotenv
└─ cogs/
   ├─ tickets.py
   │  ├─ utils/database.py
   │  ├─ utils/embed.py
   │  └─ utils/checks.py
   ├─ events.py
   └─ moderation.py
```

---

**Version**: 1.0.0  
**Last Updated**: 18/01/2024
