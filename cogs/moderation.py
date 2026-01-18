import discord
from discord.ext import commands
import json
import logging
from utils.database import get_user_tickets, get_panels
from utils.checks import is_admin, is_staff

logger = logging.getLogger(__name__)

def load_config():
    with open('config.json', 'r', encoding='utf-8') as f:
        return json.load(f)

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='ticketinfo', description='Xem thông tin ticket')
    @is_staff()
    async def ticketinfo(self, ctx, ticket_id: str = None):
        """Xem thông tin chi tiết ticket"""
        try:
            from utils.database import get_ticket, get_channel_ticket
            
            if not ticket_id:
                # Nếu không có ID, lấy từ channel hiện tại
                ticket_id = get_channel_ticket(ctx.channel.id)
                if not ticket_id:
                    await ctx.send("❌ Vui lòng nhập ticket ID hoặc dùng lệnh này trong ticket channel!")
                    return
            
            ticket = get_ticket(ticket_id)
            if not ticket:
                await ctx.send("❌ Ticket không tồn tại!")
                return
            
            user = ctx.guild.get_member(ticket["user_id"])
            user_name = user.mention if user else f"<@{ticket['user_id']}>"
            
            claimed_by = ticket.get("claimed_by")
            if claimed_by:
                claimer = ctx.guild.get_member(claimed_by)
                claimed_text = claimer.mention if claimer else f"<@{claimed_by}>"
            else:
                claimed_text = "Chưa claim"
            
            embed = discord.Embed(
                title=f"🎫 Thông Tin Ticket #{ticket_id}",
                color=5814783
            )
            
            embed.add_field(name="Người mở", value=user_name, inline=True)
            embed.add_field(name="Danh mục", value=ticket["category"], inline=True)
            embed.add_field(name="Trạng thái", value="✅ Mở" if not ticket["closed"] else "🔒 Đóng", inline=True)
            embed.add_field(name="Claim bởi", value=claimed_text, inline=True)
            embed.add_field(name="Tạo lúc", value=ticket["created_at"][:10], inline=True)
            embed.add_field(name="Members", value=f"{len(ticket['members'])} người", inline=True)
            
            await ctx.send(embed=embed)
            
        except Exception as e:
            logger.error(f"Error in ticketinfo: {e}")
            await ctx.send(f"❌ Lỗi: {e}")
    
    @commands.command(name='tickets', description='Xem tất cả tickets')
    @is_admin()
    async def tickets(self, ctx, status: str = "open"):
        """Xem tất cả tickets trong server"""
        try:
            from utils.database import load_data
            
            data = load_data()
            all_tickets = list(data["tickets"].values())
            
            # Filter
            all_tickets = [t for t in all_tickets if t["guild_id"] == ctx.guild.id]
            
            if not all_tickets:
                await ctx.send("❌ Không có ticket nào!")
                return
            
            embed = discord.Embed(
                title=f"🎫 Tất Cả Tickets ({len(all_tickets)})",
                color=5814783
            )
            
            for ticket in all_tickets[:25]:  # Max 25 fields
                user = ctx.guild.get_member(ticket["user_id"])
                user_name = user.display_name if user else f"ID:{ticket['user_id']}"
                status_emoji = "⏳" if not ticket["claimed_by"] else "✅"
                
                embed.add_field(
                    name=f"{status_emoji} #{ticket['ticket_id']}",
                    value=f"User: {user_name}\nCategory: {ticket['category']}",
                    inline=True
                )
            
            await ctx.send(embed=embed)
            
        except Exception as e:
            logger.error(f"Error in tickets: {e}")
            await ctx.send(f"❌ Lỗi: {e}")
    
    @commands.command(name='panels', description='Xem tất cả panels')
    @is_admin()
    async def panels(self, ctx):
        """Xem tất cả ticket panels trong server"""
        try:
            panels = get_panels(ctx.guild.id)
            
            if not panels:
                await ctx.send("❌ Không có panel nào!")
                return
            
            embed = discord.Embed(
                title=f"📋 Ticket Panels ({len(panels)})",
                color=5814783
            )
            
            for panel in panels:
                channel = ctx.guild.get_channel(panel["channel_id"])
                channel_name = channel.mention if channel else "Deleted"
                
                embed.add_field(
                    name=panel["category"],
                    value=f"Channel: {channel_name}\nMessage ID: {panel['message_id']}",
                    inline=False
                )
            
            await ctx.send(embed=embed)
            
        except Exception as e:
            logger.error(f"Error in panels: {e}")
            await ctx.send(f"❌ Lỗi: {e}")
    
    @commands.command(name='setconfig', description='Cấu hình bot')
    @is_admin()
    async def setconfig(self, ctx, key: str, *, value: str):
        """Thay đổi cấu hình"""
        try:
            config = load_config()
            
            # Validate key
            valid_keys = ["staff_role", "admin_role", "ticket_category", "ticket_prefix", "prefix"]
            if key not in valid_keys:
                await ctx.send(f"❌ Config không hợp lệ! Hợp lệ: {', '.join(valid_keys)}")
                return
            
            config[key] = value
            
            with open('config.json', 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            await ctx.send(f"✅ Đã cấu hình `{key}` = `{value}`")
            logger.info(f"Config changed: {key} = {value}")
            
        except Exception as e:
            logger.error(f"Error in setconfig: {e}")
            await ctx.send(f"❌ Lỗi: {e}")

async def setup(bot):
    await bot.add_cog(Moderation(bot))
