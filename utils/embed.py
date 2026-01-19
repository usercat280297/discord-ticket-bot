import discord
import json

def load_config() -> dict:
    """Load cấu hình từ file config.json"""
    with open('config.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def create_panel_embed() -> list:
    """Return two embeds: a banner embed (large image) and a content embed.

    The first embed is a full-width banner image to create a large visual header.
    The second embed contains the thumbnail, title, fields and explanatory text.
    Returns a list of `discord.Embed` objects.
    """
    config = load_config()
    large_gif = config.get(
        "panel_large_image",
        "https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExYms2ZXBpYnhlaXI3bmdsZnNxdHhyc3E2ejhjaTZkZGU1eDhseXg2ZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/EnrH0xdlmT5uBZ9BCe/giphy.gif",
    )
    thumb_gif = config.get(
        "panel_thumbnail",
        "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExMDBhc3htcDk3YnkwNTg2ZmptYjdrZnZ2djc0OW9ybXVoZWxpczV0MSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/6Eui7Hxv9mKWPt5iRG/giphy.gif",
    )

    color = config.get("ticket_color", 5814783)

    # Banner embed: large image only (no title) to create a wide visual
    banner = discord.Embed(color=color)
    try:
        banner.set_image(url=large_gif)
    except Exception:
        pass

    # Content embed: thumbnail + structured fields
    content = discord.Embed(
        title="Self-Serve Activation",
        description="You can use this panel to activate automatically.",
        color=color,
    )

    content.set_thumbnail(url=thumb_gif)

    content.add_field(
        name="✨ Today's Featured Activation",
        value="**Classic Hits Wave (Other Games + EA)**",
        inline=False,
    )

    content.add_field(
        name="Before You Start",
        value=(
            "• Read the #guide channel.\n"
            "• Download clean game files from resources or the downloader.\n\n"
            "**Follow the steps in the correct order:**\n"
            "1. Extract the contents of the file (use WinRAR or 7zip) into the game folder.\n"
            "2. Replace all files (ensure the folders match).\n"
            "3. Launch the game using the .exe file."
        ),
        inline=False,
    )

    content.add_field(
        name="How to Request",
        value=(
            "Once panels open, select your game from the menu below.\n\n"
            "• Use the dropdowns below to pick the correct game/section.\n"
            "• The panel will provide an activation link automatically after processing."
        ),
        inline=False,
    )

    content.add_field(
        name="Important",
        value=(
            "Make sure to read all notes above before proceeding.\n"
            "Tokens may expire; download and run the activation immediately (within the time limit)."
        ),
        inline=False,
    )

    content.set_footer(text="Self-Serve Activation | Follow instructions carefully")

    return [banner, content]

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
