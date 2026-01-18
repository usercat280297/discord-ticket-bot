# 🎮 Activation Panel Bot - Chi Tiết Quy Trình

## 📌 Giải Thích Hình Ảnh Bạn Cung Cấp

Từ các hình ảnh Discord ticket bot, đây là quy trình hoàn chỉnh:

---

## **PHASE 1: Tạo Ticket**

```
┌─────────────────────────────────────────┐
│  User bấm nút "Mở Ticket"                │
│  (ví dụ: "Demon Slayer -Kimetsu no Ya")  │
└─────────────────┬───────────────────────┘
                  ↓
        ┌─────────────────────┐
        │ Bot kiểm tra:       │
        │ ✅ Có ticket nào?   │
        │ ✅ Có quyền?        │
        │ ✅ Số lượng limit?  │
        └────────┬────────────┘
                 ↓ (Pass)
        ┌──────────────────────────┐
        │ Bot tạo channel ticket   │
        │ Tên: #ticket-abc123      │
        │ Category: "Tickets"      │
        └────────┬─────────────────┘
                 ↓
        ┌──────────────────────────┐
        │ Bot set permissions:     │
        │ ❌ @everyone - NO        │
        │ ✅ User - YES            │
        │ ✅ @Staff - YES          │
        │ ✅ @Admin - YES          │
        └────────┬─────────────────┘
                 ↓
        ┌──────────────────────────┐
        │ Bot gửi Welcome Message  │
        └────────┬─────────────────┘
```

---

## **PHASE 2: Welcome Message (Activation Instructions)**

```
┌──────────────────────────────────────────────────────────────┐
│                    🎫 Welcome to your ticket                │
│                                                              │
│                        @User                                │
│                                                              │
│  📋 Category: Demon Slayer -Kimetsu no Yaiba- 2             │
│                                                              │
│  ⏱️ Response Time:                                           │
│     Staff sẽ trả lời trong vài phút đến vài giờ             │
│                                                              │
│  📝 Hướng Dẫn:                                               │
│     • Vui lòng mô tả vấn đề chi tiết                        │
│     • Cung cấp ảnh chụp màn hình                            │
│     • Chờ staff trả lời                                     │
│     • Bấm ✅ It Works! khi giải quyết                       │
│                                                              │
│     [✅ It Works!] [🆘 Need Help] [🔒 Close Ticket]         │
└──────────────────────────────────────────────────────────────┘
```

### **Bot gửi thêm:**

1. **Panel Hướng Dẫn Activation** (từ hình ảnh)
   - Tiêu đề activation
   - Danh sách bước (Step 1, Step 2, 3...)
   - Ảnh chỉ dẫn
   - Token/Account info
   - Nút download, get activation file, etc.

2. **Thông Tin Ticket**
   - Ticket ID: `bbf03ded-cbcd-47f2-aa6e-577e50750e73`
   - Account ID: `275`

---

## **PHASE 3: User Tương Tác**

### **Scenario A: User hoàn tất hướng dẫn ✅**

```
User hoàn tất tất cả các bước
         ↓
   Bấm [✅ It Works!]
         ↓
   ┌──────────────────────────────┐
   │ Bot gửi embed:               │
   │                              │
   │ ✅ Vấn đề Đã Giải Quyết      │
   │                              │
   │ @User đã xác nhận rằng       │
   │ vấn đề đã được giải quyết.   │
   │                              │
   │ 💬 Cảm ơn bạn đã sử dụng     │
   │ dịch vụ của chúng tôi!       │
   │                              │
   │ Ticket sẽ được đóng          │
   │ trong 5 giây...              │
   └────────┬─────────────────────┘
            ↓ (Chờ 5 giây)
   ┌──────────────────────────────┐
   │ Bot xóa channel              │
   │ 🗑️ #ticket-abc123 DELETED   │
   └──────────────────────────────┘
            ↓
   ┌──────────────────────────────┐
   │ Database Update:             │
   │ • "closed": true             │
   │ • "closed_at": timestamp     │
   │ • "closed_by": User ID       │
   │ • Move to closed_tickets     │
   └──────────────────────────────┘
            ↓
      ✅ TICKET CLOSED
```

### **Scenario B: User gặp vấn đề 🆘**

```
User vẫn cần trợ giúp
       ↓
Bấm [🆘 Need Help]
       ↓
  ┌────────────────────────────┐
  │ Bot gửi embed:             │
  │                            │
  │ 🆘 Yêu Cầu Trợ Giúp       │
  │                            │
  │ @User vẫn cần trợ giúp    │
  │ thêm.                      │
  │                            │
  │ 📞 Staff sẽ sớm hỗ trợ    │
  │ bạn!                       │
  │                            │
  │ @Staff ← PING              │
  └────────┬───────────────────┘
           ↓
  ┌────────────────────────────┐
  │ Database Update:           │
  │ "status": "need_help"      │
  │ Ticket vẫn mở              │
  └────────┬───────────────────┘
           ↓
    Staff sẽ can thiệp
```

### **Scenario C: Staff quản lý ticket 🔒**

```
Staff muốn đóng ticket
         ↓
   Bấm [🔒 Close Ticket]
         ↓
   ┌──────────────────────────────┐
   │ Bot cập nhật:                │
   │ • "closed": true             │
   │ • "closed_by": Staff ID      │
   │ • Gửi close embed            │
   └────────┬─────────────────────┘
            ↓ (Chờ 5 giây)
   ┌──────────────────────────────┐
   │ Bot xóa channel              │
   └──────────────────────────────┘
            ↓
      ✅ TICKET CLOSED
```

---

## **CODE IMPLEMENTATION**

### **1. ItWorksButton - Nút Xác Nhận**

```python
class ItWorksButton(discord.ui.Button):
    """Nút ✅ It Works!"""
    def __init__(self):
        super().__init__(
            style=discord.ButtonStyle.success,
            label="✅ It Works!",
            emoji="✅"
        )
    
    async def callback(self, interaction: discord.Interaction):
        # 1. Lấy ticket ID từ channel
        ticket_id = get_channel_ticket(interaction.channel.id)
        
        # 2. Kiểm tra ticket có tồn tại
        ticket = get_ticket(ticket_id)
        
        # 3. Cập nhật database
        close_ticket(ticket_id, interaction.user.id)
        
        # 4. Gửi embed xác nhận
        embed = discord.Embed(
            title="✅ Vấn đề Đã Giải Quyết",
            description=f"{interaction.user.mention} đã xác nhận...",
            color=discord.Color.green()
        )
        await interaction.followup.send(embed=embed)
        
        # 5. Chờ 5 giây
        await asyncio.sleep(5)
        
        # 6. XÓA CHANNEL
        await interaction.channel.delete()
```

### **2. NeedHelpButton - Nút Yêu Cầu Trợ Giúp**

```python
class NeedHelpButton(discord.ui.Button):
    """Nút 🆘 Need Help"""
    def __init__(self):
        super().__init__(
            style=discord.ButtonStyle.danger,
            label="🆘 Need Help",
            emoji="🆘"
        )
    
    async def callback(self, interaction: discord.Interaction):
        # 1. Lấy staff role
        staff_role = discord.utils.get(
            interaction.guild.roles,
            name="Staff"
        )
        
        # 2. Gửi embed + ping staff
        embed = discord.Embed(
            title="🆘 Yêu Cầu Trợ Giúp",
            description="...",
            color=discord.Color.orange()
        )
        
        await interaction.followup.send(
            content=staff_role.mention,
            embed=embed
        )
        
        # 3. Cập nhật status
        update_ticket(ticket_id, status="need_help")
```

### **3. Database Changes**

```python
# Data structure cho mỗi ticket:
{
    "ticket_id": "abc123",
    "user_id": 123456789,
    "channel_id": 987654321,
    "guild_id": 111111111,
    "category": "Demon Slayer -Kimetsu no Yaiba- 2",
    "claimed_by": null,
    "claimed_at": null,
    "created_at": "2026-01-18T10:30:00.000000",
    "closed": false,              # ← IMPORTANT
    "closed_at": null,            # ← Timestamp khi đóng
    "closed_by": null,            # ← User/Staff ID
    "members": [123456789],
    "status": "open"              # ← "open", "need_help"
}

# Khi đóng ticket:
# 1. Set "closed": true
# 2. Set "closed_at": datetime.now()
# 3. Set "closed_by": user.id
# 4. Chuyển từ "tickets" → "closed_tickets"
```

---

## **TIMING & DELAYS**

```
┌─────────────────────────────────────────┐
│ User bấm button (0s)                    │
├─────────────────────────────────────────┤
│ Bot gửi confirmation embed (0.1s)       │
├─────────────────────────────────────────┤
│ User thấy message (0.5s)                │
├─────────────────────────────────────────┤
│ 🕐 DELAY 5 GIÂY (user có thể chụp ảnh)  │
├─────────────────────────────────────────┤
│ Bot delete channel (5s)                 │
├─────────────────────────────────────────┤
│ ✅ Ticket hoàn toàn closed (5.5s)       │
└─────────────────────────────────────────┘
```

**Tại sao 5 giây?**
- ✅ Đủ thời gian user thấy confirmation
- ✅ Không quá lâu khiến user bối rối
- ✅ Có thể screenshot/ghi lại info
- ✅ Config có thể tùy chỉnh: `auto_close_delay`

---

## **PERMISSIONS & SECURITY**

```
┌────────────────────────────────────────┐
│ Channel Permissions                    │
├────────────────────────────────────────┤
│ @everyone: ❌ NO ACCESS                │
│ User: ✅ Full                          │
│ @Staff: ✅ Full                        │
│ @Admin: ✅ Full                        │
│ Bot: ✅ Manage Messages, Delete        │
└────────────────────────────────────────┘
```

---

## **COMPLETE WORKFLOW (All Scenarios)**

```
START
  ↓
[1] User clicks "Mở Ticket"
  ↓
[2] Bot creates #ticket-[ID]
  ↓
[3] Bot sends Welcome Embed + Buttons
  ├─→ [4A] It Works! → Close + Delete (5s)
  ├─→ [4B] Need Help → Ping Staff (Keep Open)
  └─→ [4C] Close Ticket → Close + Delete (5s)
  ↓
[5] Ticket status in DB updated
  ├─→ "closed": true
  ├─→ "closed_at": timestamp
  └─→ "closed_by": user_id
  ↓
[6] Channel deleted
  ↓
END ✅
```

---

## **KẾT LUẬN**

Ticket bot hoạt động theo quy trình:

1. **Tạo**: User bấm button → Bot tạo channel
2. **Ghi đón**: Bot gửi hướng dẫn + buttons
3. **Xử lý**: 
   - ✅ It Works! → Tự động đóng
   - 🆘 Need Help → Ping staff
   - 🔒 Close → Manual close (staff)
4. **Đóng**: Update database + Xóa channel (5s delay)
5. **Xong**: Ticket hoàn toàn closed ✅

**Điều quan trọng nhất: Sau khi bấm "It Works!" → Ticket TỰ ĐỘNG ĐÓNG + XÓA CHANNEL**

---

**✅ Bot đã sẵn sàng hoạt động đúng như hình ảnh bạn cung cấp!**
