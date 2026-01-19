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
from utils.embed import create_panel_embed, create_panel_embed_single, create_ticket_embed, create_closed_embed, create_info_embed
import os
from utils.checks import is_admin, is_staff, is_ticket_channel

logger = logging.getLogger(__name__)

# Guard to prevent duplicate panel creation when commands fire twice
_panels_creation_in_progress = set()
_last_panel_notification = {}
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
    try:
        if not interaction.response.is_done():
            await interaction.response.defer()
    except Exception:
        # fallback: try to defer and ignore if already acknowledged
        try:
            await interaction.response.defer()
        except Exception:
            pass
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

    @commands.group(name='ticket', invoke_without_command=True)
    async def ticket_cmd(self, ctx):
        """Prefix group `!ticket` -> shows help if no subcommand"""
        try:
            embed = create_info_embed(
                title="📚 Ticket Help",
                description="Sử dụng `!ticket setup` để tạo panel hoặc `/ticket help` để xem hướng dẫn",
                Panel="Sử dụng `!ticket setup` để tạo panel ticket (dropdown) trong kênh hiện tại.",
                Commands="`!ticket setup`, `!ticket close`, `!ticket claim`, `!ticket add @user`, `!ticket remove @user`, `!ticket transfer @user`, `!ticket mytickets`",
            )
            await ctx.send(embed=embed)
        except Exception as e:
            logger.error(f"Error in prefix ticket help: {e}")
            await ctx.send(f"❌ Lỗi: {e}")

    @ticket_cmd.command(name='setup')
    async def ticket_cmd_setup(self, ctx):
        """Prefix `!ticket setup` - tạo panel ticket"""
        try:
            logger.debug("entering ticket_cmd_setup (prefix)")
            channel_id = ctx.channel.id
            # prevent concurrent duplicate creations
            if channel_id in _panels_creation_in_progress:
                try:
                    await ctx.author.send("❗ Panel đang được tạo — vui lòng chờ giây lát.")
                except Exception:
                    await ctx.send("❗ Panel đang được tạo — vui lòng chờ giây lát.", delete_after=6)
                return
            config = load_config()
            if config.get("panel_channel_id") == channel_id:
                # verify the panel message still exists (pinned by bot). If not, clear stale config and continue
                try:
                    pins = await ctx.channel.pins()
                    found = False
                    for m in pins:
                        if m.author == ctx.bot.user and (m.embeds and len(m.embeds) > 0):
                            # consider this the panel
                            found = True
                            break
                    if not found:
                        logger.info("stale panel_channel_id found in config for channel %s — clearing", channel_id)
                        config.pop("panel_channel_id", None)
                        with open('config.json', 'w', encoding='utf-8') as f:
                            json.dump(config, f, ensure_ascii=False, indent=2)
                    else:
                        # dedupe repeated notifications within short time window
                        import time
                        last = _last_panel_notification.get(channel_id)
                        now = time.time()
                        if last and now - last < 5:
                            logger.debug("suppressing duplicate panel-exists message for channel %s", channel_id)
                            return
                        _last_panel_notification[channel_id] = now
                        # Notify the command caller privately to avoid spamming the channel
                        try:
                            await ctx.author.send("❗ Panel đã tồn tại trong kênh này.")
                        except Exception:
                            await ctx.send("❗ Panel đã tồn tại trong kênh này.", delete_after=6)
                        return
                except Exception:
                    # If checking pins fails, just notify once
                    await ctx.send("❗ Panel đã tồn tại trong kênh này.")
                    return
            _panels_creation_in_progress.add(channel_id)
            # Prefer a local attachment if available (images/steam.png). Falls back to online embeds.
            local_image_path = os.path.join('images', 'steam.png')
            if os.path.exists(local_image_path):
                panel_payload = create_panel_embed_single('steam.png')
            else:
                panel_payload = create_panel_embed()
            view = PanelView()
            # try to find existing panel messages authored by the bot (avoid duplicates)
            existing = []
            try:
                async for m in ctx.channel.history(limit=200):
                    if m.author == ctx.bot.user and m.embeds:
                        title = m.embeds[0].title if m.embeds and len(m.embeds) > 0 else ''
                        if title in ("Self-Serve Activation", "🎫 Hệ Thống Ticket Hỗ Trợ", "🎫 Mở Ticket"):
                            existing.append(m)
            except Exception:
                existing = []

            if existing:
                # If using a local-attachment panel, replace all existing panels with a single new message
                if isinstance(panel_payload, tuple):
                    for m in existing:
                        try:
                            await m.delete()
                        except Exception:
                            pass
                    embed_obj, fname = panel_payload
                    file_path = os.path.join('images', fname) if fname else None
                    try:
                        if file_path and os.path.exists(file_path):
                            f = discord.File(file_path, filename=fname)
                            message = await ctx.channel.send(embed=embed_obj, file=f, view=view)
                        else:
                            message = await ctx.channel.send(embed=embed_obj, view=view)
                    except Exception:
                        message = existing[0]
                else:
                    # keep first, edit it and remove extras
                    message = existing[0]
                    try:
                        if isinstance(panel_payload, list):
                            await message.edit(embeds=panel_payload, view=view)
                        else:
                            await message.edit(embed=panel_payload, view=view)
                    except Exception:
                        pass
                    try:
                        await message.pin()
                    except Exception:
                        pass
                    for m in existing[1:]:
                        try:
                            await m.delete()
                        except Exception:
                            pass
            else:
                if isinstance(panel_payload, tuple):
                    embed_obj, fname = panel_payload
                    file_path = os.path.join('images', fname) if fname else None
                    if file_path and os.path.exists(file_path):
                        f = discord.File(file_path, filename=fname)
                        message = await ctx.channel.send(embed=embed_obj, file=f, view=view)
                    else:
                        message = await ctx.channel.send(embed=embed_obj, view=view)
                else:
                    if isinstance(panel_payload, list):
                        message = await ctx.channel.send(embeds=panel_payload, view=view)
                    else:
                        message = await ctx.channel.send(embed=panel_payload, view=view)
            try:
                await message.pin()
            except discord.errors.HTTPException:
                pass

            config = load_config()
            config["panel_channel_id"] = ctx.channel.id
            with open('config.json', 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)

            embed_success = discord.Embed(
                title="✅ Panel Ticket Đã Tạo",
                description=f"📍 Kênh: {ctx.channel.mention}\n\n"
                           f"✨ Người dùng có thể chọn loại ticket từ dropdown",
                color=discord.Color.green()
            )
            # Send success notice privately when possible to avoid cluttering channel
            try:
                await ctx.author.send(embed=embed_success)
                # react in channel as lightweight confirmation
                try:
                    await ctx.message.add_reaction("✅")
                except Exception:
                    pass
            except Exception:
                # fallback to a short public confirmation that auto-deletes
                await ctx.send(embed=embed_success, delete_after=8)
            logger.info(f"Panel created in {ctx.guild} | Channel: {ctx.channel.id}")
            # done
            _panels_creation_in_progress.discard(channel_id)
            _last_panel_notification.pop(channel_id, None)

        except Exception as e:
            logger.error(f"Error in prefix ticket setup: {e}")
            _panels_creation_in_progress.discard(getattr(ctx.channel, 'id', None))
            await ctx.send(f"❌ Lỗi: {e}")
    ticket = app_commands.Group(name="ticket", description="Ticket commands")

    @ticket.command(name='setup', description='Tạo panel ticket chính')
    async def ticket_setup(self, interaction: discord.Interaction):
        """Tạo panel ticket chính với dropdown (subcommand `/ticket setup`)"""
        try:
            logger.debug("entering ticket_setup (slash)")
            channel_id = interaction.channel.id if interaction.channel else None
            if channel_id in _panels_creation_in_progress:
                await interaction.response.send_message("❗ Panel đang được tạo — vui lòng chờ giây lát.", ephemeral=True)
                return
            config = load_config()
            if config.get("panel_channel_id") == channel_id:
                # verify pinned panel exists
                try:
                    pins = await interaction.channel.pins()
                    found = False
                    for m in pins:
                        if m.author == interaction.client.user and (m.embeds and len(m.embeds) > 0):
                            found = True
                            break
                    if not found:
                        logger.info("stale panel_channel_id found in config for channel %s (slash) — clearing", channel_id)
                        config.pop("panel_channel_id", None)
                        with open('config.json', 'w', encoding='utf-8') as f:
                            json.dump(config, f, ensure_ascii=False, indent=2)
                    else:
                        import time
                        last = _last_panel_notification.get(channel_id)
                        now = time.time()
                        if last and now - last < 5:
                            logger.debug("suppressing duplicate panel-exists message for channel %s (slash)", channel_id)
                            return
                        _last_panel_notification[channel_id] = now
                        await interaction.response.send_message("❗ Panel đã tồn tại trong kênh này.", ephemeral=True)
                        return
                except Exception:
                    await interaction.response.send_message("❗ Panel đã tồn tại trong kênh này.", ephemeral=True)
                    return
            _panels_creation_in_progress.add(channel_id)
            # Prefer a local attachment if available (images/steam.png). Falls back to online embeds.
            local_image_path = os.path.join('images', 'steam.png')
            if os.path.exists(local_image_path):
                panel_payload = create_panel_embed_single('steam.png')
            else:
                panel_payload = create_panel_embed()

            # Tạo view với dropdown
            view = PanelView()

            # try to find existing panel messages authored by the bot (avoid duplicates)
            existing = []
            try:
                async for m in interaction.channel.history(limit=200):
                    if m.author == interaction.client.user and m.embeds:
                        title = m.embeds[0].title if m.embeds and len(m.embeds) > 0 else ''
                        if title in ("Self-Serve Activation", "🎫 Hệ Thống Ticket Hỗ Trợ", "🎫 Mở Ticket"):
                            existing.append(m)
            except Exception:
                existing = []

            if existing:
                # If using a local-attachment panel, replace all existing panels with a single new message
                if isinstance(panel_payload, tuple):
                    for m in existing:
                        try:
                            await m.delete()
                        except Exception:
                            pass
                    embed_obj, fname = panel_payload
                    file_path = os.path.join('images', fname) if fname else None
                    try:
                        if file_path and os.path.exists(file_path):
                            f = discord.File(file_path, filename=fname)
                            message = await interaction.channel.send(embed=embed_obj, file=f, view=view)
                        else:
                            message = await interaction.channel.send(embed=embed_obj, view=view)
                    except Exception:
                        message = existing[0]
                else:
                    message = existing[0]
                    try:
                        if isinstance(panel_payload, list):
                            await message.edit(embeds=panel_payload, view=view)
                        else:
                            await message.edit(embed=panel_payload, view=view)
                    except Exception:
                        pass
                    try:
                        await message.pin()
                    except Exception:
                        pass
                    for m in existing[1:]:
                        try:
                            await m.delete()
                        except Exception:
                            pass
            else:
                if isinstance(panel_payload, tuple):
                    embed_obj, fname = panel_payload
                    file_path = os.path.join('images', fname) if fname else None
                    if file_path and os.path.exists(file_path):
                        f = discord.File(file_path, filename=fname)
                        message = await interaction.channel.send(embed=embed_obj, file=f, view=view)
                    else:
                        message = await interaction.channel.send(embed=embed_obj, view=view)
                else:
                    if isinstance(panel_payload, list):
                        message = await interaction.channel.send(embeds=panel_payload, view=view)
                    else:
                        message = await interaction.channel.send(embed=panel_payload, view=view)

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
            # Reply ephemerally to the command invoker to avoid public spam
            await interaction.response.send_message(embed=embed_success, ephemeral=True)
            logger.info(f"Panel created in {interaction.guild} | Channel: {interaction.channel.id}")
            _panels_creation_in_progress.discard(channel_id)
            _last_panel_notification.pop(channel_id, None)

        except Exception as e:
            logger.error(f"Error in /ticket setup: {e}")
            try:
                _panels_creation_in_progress.discard(channel_id if 'channel_id' in locals() else None)
            except Exception:
                pass
            await interaction.response.send_message(f"❌ Lỗi: {e}")

    @ticket.command(name='help', description='Hiển thị hướng dẫn sử dụng ticket')
    async def ticket_help(self, interaction: discord.Interaction):
        """Hiển thị thông tin và hướng dẫn sử dụng hệ thống ticket (subcommand `/ticket help`)"""
        try:
            embed = create_info_embed(
                title="📚 Hướng Dẫn Sử Dụng Ticket",
                description="Dưới đây là các lệnh và mô tả",
                Panel="Sử dụng `/ticket setup` để tạo panel ticket (dropdown) trong kênh hiện tại.",
                Commands="`/close`, `!claim`, `!add @user`, `!remove @user`, `!transfer @user`, `!mytickets`",
                Buttons="Người dùng có thể bấm ✅ It Works!, 🆘 Need Help, hoặc 🔒 Đóng Ticket trong channel ticket."
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            logger.error(f"Error in /ticket help: {e}")
            await interaction.response.send_message(f"❌ Lỗi: {e}")

    @ticket.command(name='close', description='Đóng ticket')
    async def ticket_close(self, interaction: discord.Interaction, reason: Optional[str] = "Không có lý do"):
        """Đóng ticket (subcommand `/ticket close`)"""
        try:
            config = load_config()
            if not interaction.channel or not interaction.guild:
                await interaction.response.send_message("❌ Lệnh chỉ dùng trong server.", ephemeral=True)
                return

            if not interaction.channel.name.startswith(config.get("ticket_prefix", "ticket")):
                await interaction.response.send_message("❌ Lệnh này chỉ có thể sử dụng trong ticket channel!", ephemeral=True)
                return

            # staff check
            staff_role = discord.utils.get(interaction.user.roles, name=config.get("staff_role", "Staff"))
            admin_role = discord.utils.get(interaction.user.roles, name=config.get("admin_role", "Admin"))
            if not staff_role and not admin_role:
                await interaction.response.send_message("❌ Bạn không có quyền sử dụng lệnh này!", ephemeral=True)
                return

            ticket_id = get_channel_ticket(interaction.channel.id)
            if not ticket_id:
                await interaction.response.send_message("❌ Không tìm thấy ticket này!", ephemeral=True)
                return

            ticket = get_ticket(ticket_id)
            if not ticket:
                await interaction.response.send_message("❌ Ticket không tồn tại!", ephemeral=True)
                return

            user = interaction.guild.get_member(ticket["user_id"]) or await self.bot.fetch_user(ticket["user_id"])
            embed = create_closed_embed(user, interaction.user, reason)
            await interaction.response.send_message(embed=embed)

            # Gửi DM cho user
            await send_ticket_closed_dm(user_id=ticket["user_id"], ticket_id=ticket_id, reason=f"🔒 {reason}", bot=self.bot)

            # Update DB
            close_ticket(ticket_id, interaction.user.id)

            # Xóa channel sau 5 giây
            await asyncio.sleep(5)
            try:
                await interaction.channel.delete()
            except Exception:
                pass

            logger.info(f"Ticket closed via /ticket close: {ticket_id} by {interaction.user}")

        except Exception as e:
            logger.error(f"Error in /ticket close: {e}")
            try:
                await interaction.response.send_message(f"❌ Lỗi: {e}")
            except Exception:
                pass

    @ticket.command(name='claim', description='Claim ticket')
    async def ticket_claim(self, interaction: discord.Interaction):
        """Claim ticket (subcommand `/ticket claim`)"""
        try:
            config = load_config()
            if not interaction.channel or not interaction.guild:
                await interaction.response.send_message("❌ Lệnh chỉ dùng trong server.", ephemeral=True)
                return

            staff_role = discord.utils.get(interaction.user.roles, name=config.get("staff_role", "Staff"))
            admin_role = discord.utils.get(interaction.user.roles, name=config.get("admin_role", "Admin"))
            if not staff_role and not admin_role:
                await interaction.response.send_message("❌ Bạn không có quyền sử dụng lệnh này!", ephemeral=True)
                return

            ticket_id = get_channel_ticket(interaction.channel.id)
            if not ticket_id:
                await interaction.response.send_message("❌ Không tìm thấy ticket này!", ephemeral=True)
                return

            ticket = get_ticket(ticket_id)
            if ticket and ticket.get("claimed_by"):
                claimer = interaction.guild.get_member(ticket["claimed_by"]) if interaction.guild else None
                await interaction.response.send_message(f"❌ Ticket đã được claim bởi {claimer.mention if claimer else 'someone'}", ephemeral=True)
                return

            claim_ticket(ticket_id, interaction.user.id)
            embed = discord.Embed(title="🎯 Ticket Claimed", description=f"{interaction.user.mention} đã claim ticket này", color=discord.Color.green())
            await interaction.response.send_message(embed=embed)
            logger.info(f"Ticket claimed via /ticket claim: {ticket_id} by {interaction.user}")

        except Exception as e:
            logger.error(f"Error in /ticket claim: {e}")
            await interaction.response.send_message(f"❌ Lỗi: {e}")

    @ticket.command(name='add', description='Thêm user vào ticket')
    async def ticket_add(self, interaction: discord.Interaction, user: discord.User):
        """Thêm user vào ticket (subcommand `/ticket add @user`)"""
        try:
            config = load_config()
            if not interaction.channel or not interaction.guild:
                await interaction.response.send_message("❌ Lệnh chỉ dùng trong server.", ephemeral=True)
                return

            staff_role = discord.utils.get(interaction.user.roles, name=config.get("staff_role", "Staff"))
            admin_role = discord.utils.get(interaction.user.roles, name=config.get("admin_role", "Admin"))
            if not staff_role and not admin_role:
                await interaction.response.send_message("❌ Bạn không có quyền sử dụng lệnh này!", ephemeral=True)
                return

            ticket_id = get_channel_ticket(interaction.channel.id)
            if not ticket_id:
                await interaction.response.send_message("❌ Không tìm thấy ticket này!", ephemeral=True)
                return

            member = interaction.guild.get_member(user.id)
            if not member:
                await interaction.response.send_message("❌ User không trong server!", ephemeral=True)
                return

            await interaction.channel.set_permissions(member, view_channel=True, send_messages=True, read_message_history=True)
            add_ticket_member(ticket_id, user.id)

            embed = discord.Embed(description=f"✅ {user.mention} đã được thêm vào ticket", color=discord.Color.green())
            await interaction.response.send_message(embed=embed)

        except Exception as e:
            logger.error(f"Error in /ticket add: {e}")
            await interaction.response.send_message(f"❌ Lỗi: {e}")

    @ticket.command(name='remove', description='Xóa user khỏi ticket')
    async def ticket_remove(self, interaction: discord.Interaction, user: discord.User):
        """Xóa user khỏi ticket (subcommand `/ticket remove @user`)"""
        try:
            config = load_config()
            if not interaction.channel or not interaction.guild:
                await interaction.response.send_message("❌ Lệnh chỉ dùng trong server.", ephemeral=True)
                return

            staff_role = discord.utils.get(interaction.user.roles, name=config.get("staff_role", "Staff"))
            admin_role = discord.utils.get(interaction.user.roles, name=config.get("admin_role", "Admin"))
            if not staff_role and not admin_role:
                await interaction.response.send_message("❌ Bạn không có quyền sử dụng lệnh này!", ephemeral=True)
                return

            ticket_id = get_channel_ticket(interaction.channel.id)
            if not ticket_id:
                await interaction.response.send_message("❌ Không tìm thấy ticket này!", ephemeral=True)
                return

            member = interaction.guild.get_member(user.id)
            if member:
                await interaction.channel.set_permissions(member, overwrite=None)

            remove_ticket_member(ticket_id, user.id)
            embed = discord.Embed(description=f"✅ {user.mention} đã bị xóa khỏi ticket", color=discord.Color.orange())
            await interaction.response.send_message(embed=embed)

        except Exception as e:
            logger.error(f"Error in /ticket remove: {e}")
            await interaction.response.send_message(f"❌ Lỗi: {e}")

    @ticket.command(name='transfer', description='Chuyển ticket cho user khác')
    async def ticket_transfer(self, interaction: discord.Interaction, user: discord.User):
        """Chuyển ticket cho user khác (subcommand `/ticket transfer @user`)"""
        try:
            config = load_config()
            if not interaction.channel or not interaction.guild:
                await interaction.response.send_message("❌ Lệnh chỉ dùng trong server.", ephemeral=True)
                return

            staff_role = discord.utils.get(interaction.user.roles, name=config.get("staff_role", "Staff"))
            admin_role = discord.utils.get(interaction.user.roles, name=config.get("admin_role", "Admin"))
            if not staff_role and not admin_role:
                await interaction.response.send_message("❌ Bạn không có quyền sử dụng lệnh này!", ephemeral=True)
                return

            ticket_id = get_channel_ticket(interaction.channel.id)
            if not ticket_id:
                await interaction.response.send_message("❌ Không tìm thấy ticket này!", ephemeral=True)
                return

            ticket = get_ticket(ticket_id)
            old_user = interaction.guild.get_member(ticket["user_id"]) if ticket else None
            if old_user:
                await interaction.channel.set_permissions(old_user, overwrite=None)

            member = interaction.guild.get_member(user.id)
            if not member:
                await interaction.response.send_message("❌ User không trong server!", ephemeral=True)
                return

            await interaction.channel.set_permissions(member, view_channel=True, send_messages=True, read_message_history=True)
            update_ticket(ticket_id, user_id=user.id)

            embed = discord.Embed(title="🔄 Ticket Transferred", description=f"Ticket đã được chuyển sang {user.mention}", color=discord.Color.blue())
            await interaction.response.send_message(embed=embed)

        except Exception as e:
            logger.error(f"Error in /ticket transfer: {e}")
            await interaction.response.send_message(f"❌ Lỗi: {e}")

    @ticket.command(name='mytickets', description='Xem tickets của bạn')
    async def ticket_mytickets(self, interaction: discord.Interaction):
        """Xem tất cả tickets của user (subcommand `/ticket mytickets`)"""
        try:
            if not interaction.guild:
                await interaction.response.send_message("❌ Lệnh chỉ dùng trong server.", ephemeral=True)
                return

            tickets = get_user_tickets(interaction.user.id, interaction.guild.id)
            if not tickets:
                await interaction.response.send_message("❌ Bạn không có ticket nào!", ephemeral=True)
                return

            embed = discord.Embed(title="🎫 Tickets Của Bạn", description=f"Bạn có **{len(tickets)}** ticket(s) đang mở", color=5814783)
            for ticket in tickets:
                channel = interaction.guild.get_channel(ticket["channel_id"])
                claimed = "✅ Claimed" if ticket.get("claimed_by") else "⏳ Waiting"
                embed.add_field(name=f"#{ticket['ticket_id']}", value=f"Channel: {channel.mention if channel else 'Deleted'}\nStatus: {claimed}", inline=False)

            await interaction.response.send_message(embed=embed, ephemeral=True)

        except Exception as e:
            logger.error(f"Error in /ticket mytickets: {e}")
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
