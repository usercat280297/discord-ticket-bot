# 📋 Quick Reference Card

## 🚀 Start Bot
```bash
python main.py
```

## 🎮 Essential Commands

### Create Panel
```
!setup General Support
```

### Claim Ticket
```
!claim
```

### Close Ticket
```
!close Vấn đề đã giải quyết
```

### Add Member
```
!add @username
```

### View My Tickets
```
!mytickets
```

## 📁 File Locations

- **Bot**: `main.py`
- **Config**: `config.json`
- **Token**: `.env`
- **Database**: `data/tickets.json`
- **Tickets Code**: `cogs/tickets.py`
- **Database Functions**: `utils/database.py`

## 🔧 Configuration

### Edit Welcome Message
```
config.json → "welcome_message"
```

### Change Prefix
```
!setconfig prefix !!
```

### Change Color
```
config.json → "ticket_color": 3447003
```

## 🔐 Permissions

- **Admin**: All commands
- **Staff**: Claim, close, add/remove
- **User**: Create tickets, view own

## 🐛 Quick Troubleshooting

| Issue | Fix |
|-------|-----|
| Bot won't start | Check `.env` token |
| Commands fail | Check roles exist |
| Buttons invisible | Check bot permissions |
| Can't claim | Must be in ticket |

## 📚 Quick Links

- 📖 [Full Guide](GUIDE.md)
- 🎮 [All Commands](COMMANDS.md)
- ❓ [FAQ](FAQ.md)
- 🗺️ [Structure](STRUCTURE.md)

---

**Keep this handy for quick reference!**
