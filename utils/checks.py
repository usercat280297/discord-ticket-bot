import discord
from discord.ext import commands
import json

def load_config() -> dict:
    """Load cấu hình"""
    with open('config.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def is_staff():
    """Check user có role Staff"""
    async def predicate(ctx):
        config = load_config()
        staff_role = discord.utils.get(ctx.author.roles, name=config.get("staff_role", "Staff"))
        admin_role = discord.utils.get(ctx.author.roles, name=config.get("admin_role", "Admin"))
        
        if not staff_role and not admin_role:
            await ctx.send("❌ Bạn không có quyền sử dụng lệnh này!")
            return False
        return True
    return commands.check(predicate)

def is_admin():
    """Check user có role Admin"""
    async def predicate(ctx):
        config = load_config()
        admin_role = discord.utils.get(ctx.author.roles, name=config.get("admin_role", "Admin"))
        
        if not admin_role:
            await ctx.send("❌ Bạn không có quyền sử dụng lệnh này!")
            return False
        return True
    return commands.check(predicate)

def is_ticket_channel():
    """Check xem có phải ticket channel"""
    async def predicate(ctx):
        config = load_config()
        if not ctx.channel.name.startswith(config.get("ticket_prefix", "ticket")):
            await ctx.send("❌ Lệnh này chỉ có thể sử dụng trong ticket channel!")
            return False
        return True
    return commands.check(predicate)
