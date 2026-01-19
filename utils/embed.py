import discord
import json

def load_config() -> dict:
    """Load cấu hình từ file config.json"""
    with open('config.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def create_panel_embed() -> discord.Embed:
    """Tạo embed panel ticket chính"""
    config = load_config()
    embed = discord.Embed(
        title="🎫 Hệ Thống Ticket Hỗ Trợ",
        description="Chào mừng đến với hệ thống hỗ trợ của chúng tôi!\n\n**Hãy chọn loại vấn đề của bạn từ dropdown bên dưới:**",
        color=config.get("ticket_color", 5814783)
    )
    embed.add_field(
        name="📞 Thời Gian Phản Hồi",
        value="• 🎮 Hỗ trợ Game: 10-30 phút\n• 💳 Hỗ trợ Account: 5-15 phút\n• 🐛 Báo Bug: 15-60 phút",
        inline=False
    )
    embed.add_field(
        name="💡 Lưu Ý",
        value="• Hãy mô tả vấn đề chi tiết để staff hỗ trợ nhanh hơn\n• Cung cấp ảnh chụp màn hình nếu cần thiết\n• Chỉ mở 1 ticket cho mỗi vấn đề",
        inline=False
    )
    embed.set_footer(text="Discord Ticket Bot | Luôn sẵn sàng hỗ trợ bạn ✨")
    return embed

def create_ticket_embed(user: discord.User, category: str) -> discord.Embed:
    """Tạo embed ticket welcome"""
    config = load_config()
    embed = discord.Embed(
        title="🎫 Welcome to your ticket",
        description=f"{user.mention}",
        color=config.get("ticket_color", 5814783)
    )
    
    # Thêm thông tin chi tiết
    embed.add_field(
        name="📋 Category",
        value=category,
        inline=False
    )
    
    embed.add_field(
        name="⏱️ Response Time",
        value="Staff sẽ trả lời trong vài phút đến vài giờ tùy vào tình hình",
        inline=False
    )
    
    embed.add_field(
        name="📝 Hướng Dẫn",
        value="• Vui lòng mô tả vấn đề của bạn một cách chi tiết\n"
              "• Cung cấp ảnh chụp màn hình nếu cần thiết\n"
              "• Chờ staff phản hồi của bạn\n"
              "• Bấm **✅ It Works!** khi vấn đề được giải quyết",
        inline=False
    )
    
    embed.set_footer(text="Discord Ticket Bot")
    return embed

def create_closed_embed(user: discord.User, closed_by: discord.User, reason: str = "Không có lý do") -> discord.Embed:
    """Tạo embed khi đóng ticket"""
    config = load_config()
    embed = discord.Embed(
        title="🔒 Ticket Đã Đóng",
        description=f"**Lý do:** {reason}",
        color=discord.Color.red()
    )
    embed.add_field(name="Người mở", value=user.mention, inline=True)
    embed.add_field(name="Người đóng", value=closed_by.mention, inline=True)
    embed.set_footer(text="Ticket Bot")
    return embed

def create_info_embed(title: str, description: str, **fields) -> discord.Embed:
    """Tạo embed thông tin chung"""
    config = load_config()
    embed = discord.Embed(
        title=title,
        description=description,
        color=config.get("ticket_color", 5814783)
    )
    for name, value in fields.items():
        embed.add_field(name=name, value=value, inline=False)
    return embed
