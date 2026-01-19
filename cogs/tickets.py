import discord
from discord.ext import commands
from discord import app_commands
import json
import random
import string
import logging
import asyncio
from typing import Optional
from utils.database import (
    create_ticket, get_ticket, update_ticket, claim_ticket, close_ticket,
    add_panel, get_panels, add_ticket_member, remove_ticket_member,
    get_user_tickets, get_channel_ticket
)
from utils.embed import create_panel_embed, create_ticket_embed, create_closed_embed, create_info_embed
from utils.checks import is_admin, is_staff, is_ticket_channel

logger = logging.getLogger(__name__)

def load_config():
    with open('config.json', 'r', encoding='utf-8') as f:
        return json.load(f)

# =============== AUTO DM FEATURE ===============

async def send_ticket_closed_dm(user_id: int, ticket_id: str, reason: str = "Ticket đã được đóng", bot=None):
    """Gửi DM cho user khi ticket đóng"""
    try:
        if not bot:
            return
        
        user = await bot.fetch_user(user_id)
        if not user:
            return
        
        embed = discord.Embed(
            title="🔒 Ticket Của Bạn Đã Đóng",
            description=f"**Ticket ID:** `{ticket_id}`\n\n**Lý do:** {reason}",
            color=discord.Color.red()
        )
        embed.add_field(
            name="📝 Tiếp Theo?",
            value="Nếu bạn có vấn đề mới, hãy mở ticket mới trong server!\n\nCảm ơn bạn đã sử dụng dịch vụ của chúng tôi! ✨",
            inline=False
        )
        embed.set_footer(text="Discord Ticket Bot")
        
        await user.send(embed=embed)
        logger.info(f"DM sent to {user_id} for ticket {ticket_id}")
    except Exception as e:
        logger.warning(f"Could not send DM to {user_id}: {e}")

# =============== DROPDOWN & VIEWS ===============

class TicketCategorySelect(discord.ui.Select):
    """Dropdown để chọn loại ticket"""
    def __init__(self):
        config = load_config()
        categories = config.get("panel_categories", [
            "🎮 Hỗ trợ Game",
            "💳 Hỗ trợ Account",
            "🐛 Báo Bug",
            "💬 Khác"
        ])
        
        options = []
        for cat in categories:
            options.append(
                discord.SelectOption(
                    label=cat,
                    value=cat,
                    description=f"Mở ticket cho {cat}"
                )
            )
        
        super().__init__(
            placeholder="🎫 Chọn loại ticket...",
            min_values=1,
            max_values=1,
            options=options,
            custom_id="ticket_category_select"
        )
    
    async def callback(self, interaction: discord.Interaction):
        category = self.values[0]
        await create_ticket_from_select(interaction, category)

class PanelView(discord.ui.View):
    """View chứa dropdown cho panel"""
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketCategorySelect())

# =============== TICKET CREATION ===============

async def create_ticket_from_select(interaction: discord.Interaction, category: str):
    """Tạo ticket từ dropdown selection"""
    await interaction.response.defer()
    config = load_config()
    guild = interaction.guild
    user = interaction.user
    
    # Kiểm tra user đã mở ticket chưa
    existing = get_user_tickets(user.id, guild.id)
    if len(existing) >= config.get("max_user_tickets", 3):
        await interaction.followup.send(
            f"❌ Bạn đã có {len(existing)} ticket(s) đang mở! (Giới hạn: {config.get('max_user_tickets', 3)})",
            ephemeral=True
        )
        return
    
    try:
        # Tìm hoặc tạo category
        category_obj = discord.utils.get(guild.categories, name=config.get("ticket_category", "Tickets"))
        if not category_obj:
            category_obj = await guild.create_category(config.get("ticket_category", "Tickets"))
        
        # Tạo ID ticket
        ticket_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        channel_name = f"{config.get('ticket_prefix', 'ticket')}-{ticket_id}"
        
        # Tạo channel ticket
        channel = await guild.create_text_channel(
            name=channel_name,
            category=category_obj,
            topic=f"Ticket của {user} | Category: {category}"
        )
        
        # Tạo overwrites - PRIVATE
        await channel.set_permissions(guild.default_role, view_channel=False)
        await channel.set_permissions(user, view_channel=True, send_messages=True, read_message_history=True)
        
        # Thêm staff roles
        staff_role = discord.utils.get(guild.roles, name=config.get("staff_role", "Staff"))
        if staff_role:
            await channel.set_permissions(staff_role, view_channel=True, send_messages=True, read_message_history=True)
        
        admin_role = discord.utils.get(guild.roles, name=config.get("admin_role", "Admin"))
        if admin_role:
            await channel.set_permissions(admin_role, view_channel=True, send_messages=True, read_message_history=True)
        
        # Lưu ticket vào database
        create_ticket(
            ticket_id=ticket_id,
            user_id=user.id,
            channel_id=channel.id,
            guild_id=guild.id,
            category=category
        )
        
        # Gửi welcome message - PIN IT
        embed = create_ticket_embed(user, category)
        
        # Tạo view với buttons
        view = discord.ui.View(timeout=None)
        it_works_button = ItWorksButton()
        need_help_button = NeedHelpButton()
        close_button = CloseTicketButton()
        
        view.add_item(it_works_button)
        view.add_item(need_help_button)
        view.add_item(close_button)
        
        welcome_msg = await channel.send(embed=embed, view=view)
        
        # PIN message
        try:
            await welcome_msg.pin()
        except discord.errors.HTTPException:
            pass
        
        # Thêm footer message
        footer_embed = discord.Embed(
            description="**📋 Lệnh Có Sẵn:**\n"
                       "`/close [reason]` - Đóng ticket\n"
                       "`/claim` - Claim ticket\n"
                       "`/add @user` - Thêm member\n"
                       "`/remove @user` - Xóa member\n"
                       "`/transfer @user` - Chuyển ticket",
            color=discord.Color.greyple()
        )
        await channel.send(embed=footer_embed)
        
        await interaction.followup.send(
            f"✅ Ticket đã được mở: {channel.mention}",
            ephemeral=True
        )
        logger.info(f"Ticket created: {ticket_id} by {user} | Category: {category}")
        
    except Exception as e:
        logger.error(f"Error creating ticket: {e}")
        await interaction.followup.send(f"❌ Lỗi tạo ticket: {e}", ephemeral=True)

# =============== BUTTON HANDLERS ===============

class ItWorksButton(discord.ui.Button):
    """Button 'It Works!' - Xác nhận vấn đề đã giải quyết"""
    def __init__(self):
        super().__init__(style=discord.ButtonStyle.success, label="✅ It Works!", emoji="✅")
    
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        channel = interaction.channel
        ticket_id = get_channel_ticket(channel.id)
        
        if not ticket_id:
            await interaction.followup.send("❌ Không tìm thấy ticket này!", ephemeral=True)
            return
        
        ticket = get_ticket(ticket_id)
        if not ticket:
            await interaction.followup.send("❌ Ticket không tồn tại!", ephemeral=True)
            return
        
        # Tạo embed thông báo
        embed = discord.Embed(
            title="✅ Vấn Đề Đã Giải Quyết",
            description=f"{interaction.user.mention} đã xác nhận rằng vấn đề đã được giải quyết.\n\n💬 Cảm ơn bạn đã sử dụng dịch vụ của chúng tôi!",
            color=discord.Color.green()
        )
        embed.set_footer(text="Ticket sẽ được đóng trong 5 giây...")
        
        await interaction.followup.send(embed=embed)
        
        # Gửi DM cho user
        await send_ticket_closed_dm(
            user_id=ticket["user_id"],
            ticket_id=ticket_id,
            reason="✅ Vấn đề đã được giải quyết!",
            bot=self.bot if hasattr(self, 'bot') else interaction.client
        )
        
        # Cập nhật status ticket
        close_ticket(ticket_id, interaction.user.id)
        
        # Đóng channel sau 5 giây
        await asyncio.sleep(5)
        try:
            await channel.delete()
            logger.info(f"Ticket closed via 'It Works': {ticket_id} by {interaction.user}")
        except Exception as e:
            logger.error(f"Error deleting ticket channel: {e}")


class NeedHelpButton(discord.ui.Button):
    """Button 'Need Help' - Yêu cầu trợ giúp thêm"""
    def __init__(self):
        super().__init__(style=discord.ButtonStyle.danger, label="🆘 Need Help", emoji="🆘")
    
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        
        ticket_id = get_channel_ticket(interaction.channel.id)
        if not ticket_id:
            await interaction.followup.send("❌ Không tìm thấy ticket này!", ephemeral=True)
            return
        
        # Tạo embed thông báo
        embed = discord.Embed(
            title="🆘 Yêu Cầu Trợ Giúp",
            description=f"{interaction.user.mention} vẫn cần trợ giúp thêm.\n\n📞 Staff sẽ sớm hỗ trợ bạn!",
            color=discord.Color.orange()
        )
        
        # Ping staff role nếu có
        staff_role = discord.utils.get(interaction.guild.roles, name="Staff")
        if staff_role:
            await interaction.followup.send(content=staff_role.mention, embed=embed)
        else:
            await interaction.followup.send(embed=embed)
        
        # Cập nhật trạng thái ticket
        ticket = get_ticket(ticket_id)
        if ticket and not ticket["claimed_by"]:
            update_ticket(ticket_id, status="need_help")
        
        logger.info(f"Help requested for ticket: {ticket_id} by {interaction.user}")


class CloseTicketButton(discord.ui.Button):
    """Button để đóng ticket"""
    def __init__(self):
        super().__init__(style=discord.ButtonStyle.danger, label="🔒 Đóng Ticket")
    
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        channel = interaction.channel
        ticket_id = get_channel_ticket(channel.id)
        
        if not ticket_id:
            await interaction.followup.send("❌ Không tìm thấy ticket này!")
            return
        
        ticket = get_ticket(ticket_id)
        if not ticket:
            await interaction.followup.send("❌ Ticket không tồn tại!")
            return
        
        # Đóng ticket
        close_ticket(ticket_id, interaction.user.id)
        
        # Gửi DM cho user
        await send_ticket_closed_dm(
            user_id=ticket["user_id"],
            ticket_id=ticket_id,
            reason="🔒 Ticket đã được đóng bởi staff",
            bot=interaction.client
        )
        
        embed = discord.Embed(
            title="🔒 Ticket Đã Đóng",
            description=f"Đóng bởi: {interaction.user.mention}",
            color=discord.Color.red()
        )
        await interaction.followup.send(embed=embed)
        
        # Xóa channel sau 5 giây
        await asyncio.sleep(5)
        await channel.delete()
        logger.info(f"Ticket closed: {ticket_id}")

# =============== COG COMMANDS ===============

class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name='setup', description='Tạo panel ticket chính')
    @is_admin()
    async def setup(self, interaction: discord.Interaction):
        """
        Tạo panel ticket chính với dropdown
        """
        try:
            embed = create_panel_embed()
            
            # Tạo view với dropdown
            view = PanelView()
            
            message = await interaction.channel.send(embed=embed, view=view)
            
            # PIN message
            try:
                await message.pin()
            except discord.errors.HTTPException:
                pass
            
            # Lưu panel ID vào config
            config = load_config()
            config["panel_channel_id"] = interaction.channel.id
            with open('config.json', 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            
            embed_success = discord.Embed(
                title="✅ Panel Ticket Đã Tạo",
                description=f"📍 Kênh: {interaction.channel.mention}\n\n"
                           f"✨ Người dùng có thể chọn loại ticket từ dropdown",
                color=discord.Color.green()
            )
            await interaction.response.send_message(embed=embed_success)
            logger.info(f"Panel created in {interaction.guild} | Channel: {interaction.channel.id}")
            
        except Exception as e:
            logger.error(f"Error in setup: {e}")
            await interaction.response.send_message(f"❌ Lỗi: {e}")
    
    @commands.command(name='close', description='Đóng ticket')
    @is_ticket_channel()
    @is_staff()
    async def close(self, ctx, *, reason: str = "Không có lý do"):
        """Đóng ticket"""
        try:
            ticket_id = get_channel_ticket(ctx.channel.id)
            if not ticket_id:
                await ctx.send("❌ Không tìm thấy ticket này!")
                return
            
            ticket = get_ticket(ticket_id)
            if not ticket:
                await ctx.send("❌ Ticket không tồn tại!")
                return
            
            user = ctx.guild.get_member(ticket["user_id"])
            
            # Tạo embed
            embed = create_closed_embed(user or await self.bot.fetch_user(ticket["user_id"]), ctx.author, reason)
            await ctx.send(embed=embed)
            
            # Gửi DM cho user
            await send_ticket_closed_dm(
                user_id=ticket["user_id"],
                ticket_id=ticket_id,
                reason=f"🔒 {reason}",
                bot=self.bot
            )
            
            # Đóng ticket
            close_ticket(ticket_id, ctx.author.id)
            
            # Xóa channel sau 5 giây
            await asyncio.sleep(5)
            await ctx.channel.delete()
            
            logger.info(f"Ticket closed: {ticket_id} by {ctx.author}")
            
        except Exception as e:
            logger.error(f"Error in close: {e}")
            await ctx.send(f"❌ Lỗi: {e}")
    
    @commands.command(name='claim', description='Claim ticket')
    @is_ticket_channel()
    @is_staff()
    async def claim(self, ctx):
        """Claim ticket"""
        try:
            ticket_id = get_channel_ticket(ctx.channel.id)
            if not ticket_id:
                await ctx.send("❌ Không tìm thấy ticket này!")
                return
            
            ticket = get_ticket(ticket_id)
            if ticket["claimed_by"]:
                claimer = ctx.guild.get_member(ticket["claimed_by"])
                await ctx.send(f"❌ Ticket đã được claim bởi {claimer.mention}")
                return
            
            claim_ticket(ticket_id, ctx.author.id)
            
            embed = discord.Embed(
                title="🎯 Ticket Claimed",
                description=f"{ctx.author.mention} đã claim ticket này",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
            
            logger.info(f"Ticket claimed: {ticket_id} by {ctx.author}")
            
        except Exception as e:
            logger.error(f"Error in claim: {e}")
            await ctx.send(f"❌ Lỗi: {e}")
    
    @commands.command(name='add', description='Thêm user vào ticket')
    @is_ticket_channel()
    @is_staff()
    async def add(self, ctx, user: discord.User):
        """Thêm user vào ticket"""
        try:
            ticket_id = get_channel_ticket(ctx.channel.id)
            if not ticket_id:
                await ctx.send("❌ Không tìm thấy ticket này!")
                return
            
            member = ctx.guild.get_member(user.id)
            if not member:
                await ctx.send("❌ User không trong server!")
                return
            
            await ctx.channel.set_permissions(member, view_channel=True, send_messages=True, read_message_history=True)
            add_ticket_member(ticket_id, user.id)
            
            embed = discord.Embed(
                description=f"✅ {user.mention} đã được thêm vào ticket",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
            
        except Exception as e:
            logger.error(f"Error in add: {e}")
            await ctx.send(f"❌ Lỗi: {e}")
    
    @commands.command(name='remove', description='Xóa user khỏi ticket')
    @is_ticket_channel()
    @is_staff()
    async def remove(self, ctx, user: discord.User):
        """Xóa user khỏi ticket"""
        try:
            ticket_id = get_channel_ticket(ctx.channel.id)
            if not ticket_id:
                await ctx.send("❌ Không tìm thấy ticket này!")
                return
            
            member = ctx.guild.get_member(user.id)
            if member:
                await ctx.channel.set_permissions(member, overwrite=None)
            
            remove_ticket_member(ticket_id, user.id)
            
            embed = discord.Embed(
                description=f"✅ {user.mention} đã bị xóa khỏi ticket",
                color=discord.Color.orange()
            )
            await ctx.send(embed=embed)
            
        except Exception as e:
            logger.error(f"Error in remove: {e}")
            await ctx.send(f"❌ Lỗi: {e}")
    
    @commands.command(name='transfer', description='Chuyển ticket cho user khác')
    @is_ticket_channel()
    @is_staff()
    async def transfer(self, ctx, user: discord.User):
        """Chuyển ticket cho user khác"""
        try:
            ticket_id = get_channel_ticket(ctx.channel.id)
            if not ticket_id:
                await ctx.send("❌ Không tìm thấy ticket này!")
                return
            
            ticket = get_ticket(ticket_id)
            
            # Xóa permissions cũ
            old_user = ctx.guild.get_member(ticket["user_id"])
            if old_user:
                await ctx.channel.set_permissions(old_user, overwrite=None)
            
            # Thêm permissions mới
            member = ctx.guild.get_member(user.id)
            if not member:
                await ctx.send("❌ User không trong server!")
                return
            
            await ctx.channel.set_permissions(member, view_channel=True, send_messages=True, read_message_history=True)
            
            # Update database
            update_ticket(ticket_id, user_id=user.id)
            
            embed = discord.Embed(
                title="🔄 Ticket Transferred",
                description=f"Ticket đã được chuyển từ {old_user.mention} sang {user.mention}",
                color=discord.Color.blue()
            )
            await ctx.send(embed=embed)
            
        except Exception as e:
            logger.error(f"Error in transfer: {e}")
            await ctx.send(f"❌ Lỗi: {e}")
    
    @commands.command(name='mytickets', description='Xem tickets của bạn')
    async def mytickets(self, ctx):
        """Xem tất cả tickets của user"""
        try:
            tickets = get_user_tickets(ctx.author.id, ctx.guild.id)
            
            if not tickets:
                await ctx.send("❌ Bạn không có ticket nào!")
                return
            
            embed = discord.Embed(
                title="🎫 Tickets Của Bạn",
                description=f"Bạn có **{len(tickets)}** ticket(s) đang mở",
                color=5814783
            )
            
            for ticket in tickets:
                channel = ctx.guild.get_channel(ticket["channel_id"])
                claimed = "✅ Claimed" if ticket["claimed_by"] else "⏳ Waiting"
                embed.add_field(
                    name=f"#{ticket['ticket_id']}",
                    value=f"Channel: {channel.mention if channel else 'Deleted'}\nStatus: {claimed}",
                    inline=False
                )
            
            await ctx.send(embed=embed)
            
        except Exception as e:
            logger.error(f"Error in mytickets: {e}")
            await ctx.send(f"❌ Lỗi: {e}")

async def setup(bot):
    await bot.add_cog(Tickets(bot))
