import discord
from discord.ext import commands
from discord import app_commands
import random
import string
import logging
import asyncio
from bot import db, storage
import os

logger = logging.getLogger(__name__)


def _gen_ticket_id(length: int = 6) -> str:
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))


class OpenTicketButton(discord.ui.Button):
    def __init__(self):
        super().__init__(style=discord.ButtonStyle.primary, label="📩 Mở Ticket")

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        guild = interaction.guild
        user = interaction.user

        # basic rate limit by counting open tickets
        existing = await db.get_user_tickets(user.id, guild.id)
        if len(existing) >= 3:
            await interaction.followup.send(f"❌ Bạn đã có {len(existing)} ticket(s) mở. Hãy đóng bớt trước.", ephemeral=True)
            return

        # find or create category
        config_cat_name = "Tickets"
        category = discord.utils.get(guild.categories, name=config_cat_name)
        if not category:
            category = await guild.create_category(config_cat_name)

        ticket_id = _gen_ticket_id()
        channel_name = f"ticket-{ticket_id}"

        # create private channel
        channel = await guild.create_text_channel(
            name=channel_name,
            category=category,
            topic=f"Ticket của {user} | id={ticket_id}"
        )

        # permissions
        await channel.set_permissions(guild.default_role, view_channel=False)
        await channel.set_permissions(user, view_channel=True, send_messages=True, read_message_history=True)

        # save to DB
        await db.create_ticket(ticket_id=ticket_id, user_id=user.id, channel_id=channel.id, guild_id=guild.id, category=None)

        # prepare buttons similar to desired UI
        view = discord.ui.View(timeout=None)

        # Link button: Download Activation (presigned GET) — key assumed as activations/{ticket_id}.zip
        bucket = os.getenv('S3_BUCKET')
        key = f"activations/{ticket_id}.zip"
        presigned = None
        if bucket:
            presigned = storage.generate_presigned_get_url(bucket, key, expires_in=1200)

        if presigned:
            view.add_item(discord.ui.Button(style=discord.ButtonStyle.link, label="Download Activation", url=presigned))
        else:
            # fallback: provide a button that requests the file via bot (will attempt to generate/upload)
            class GetFileButton(discord.ui.Button):
                def __init__(self):
                    super().__init__(style=discord.ButtonStyle.secondary, label="Get Activation File via Bot")

                async def callback(self, inner_interaction: discord.Interaction):
                    await inner_interaction.response.defer(ephemeral=True)
                    bucket_local = os.getenv('S3_BUCKET')
                    if not bucket_local:
                        await inner_interaction.followup.send("S3_BUCKET not configured on server.", ephemeral=True)
                        return
                    url = storage.generate_presigned_get_url(bucket_local, key, expires_in=1200)
                    if not url:
                        await inner_interaction.followup.send("Không thể tạo link file. Liên hệ admin.", ephemeral=True)
                        return
                    await inner_interaction.followup.send(f"Your download link (expires soon): {url}", ephemeral=True)

            view.add_item(GetFileButton())

        # It Works + Need Help + Close (with callbacks)
        class ItWorksButton(discord.ui.Button):
            def __init__(self):
                super().__init__(style=discord.ButtonStyle.success, label="✅ It Works!")

            async def callback(self, btn_interaction: discord.Interaction):
                await btn_interaction.response.defer()
                ticket_row = await db.get_ticket(ticket_id)
                if ticket_row:
                    # try send DM
                    try:
                        user_obj = await btn_interaction.client.fetch_user(ticket_row['user_id'])
                        await user_obj.send(embed=discord.Embed(title='✅ Vấn đề đã được giải quyết', description=f'Ticket `{ticket_id}` đã được đóng.'))
                    except Exception:
                        pass
                await db.close_ticket(ticket_id, closed_by=btn_interaction.user.id)
                await btn_interaction.followup.send('✅ Ticket marked as resolved; closing channel...', ephemeral=True)
                await asyncio.sleep(2)
                try:
                    await channel.delete()
                except Exception:
                    pass

        class NeedHelpButton(discord.ui.Button):
            def __init__(self):
                super().__init__(style=discord.ButtonStyle.danger, label="🆘 Need Help")

            async def callback(self, btn_interaction: discord.Interaction):
                await btn_interaction.response.defer()
                staff_role = discord.utils.get(btn_interaction.guild.roles, name=os.getenv('STAFF_ROLE', 'Staff'))
                if staff_role:
                    await btn_interaction.followup.send(content=staff_role.mention, embed=discord.Embed(title='🆘 User requested help', description=f'User {user.mention} requested additional help for ticket `{ticket_id}`'))
                else:
                    await btn_interaction.followup.send(embed=discord.Embed(title='🆘 Help requested', description='Staff will assist shortly.'))
                await db.update_ticket(ticket_id, status='need_help')

        view.add_item(ItWorksButton())
        view.add_item(NeedHelpButton())
        view.add_item(CloseTicketButton())

        # styled embed similar to screenshots
        embed = discord.Embed(title=f"✨ Ticket {ticket_id} — Activation Processing", color=discord.Color.dark_grey())
        embed.description = (
            "Please download the file using the button below and run the activation immediately (within 20 mins) or token will expire.\n\n"
            "**Follow the steps in the correct order:**\n"
            "1. Extract the contents into the game folder.\n"
            "2. Replace all files.\n"
            "3. Launch the game using the .exe file.\n\n"
            f"⏳ This ticket will auto-close in 20 minutes if there's no button interaction.\n\nTicket ID: `{ticket_id}`"
        )

        await channel.send(content=user.mention, embed=embed, view=view)

        await interaction.followup.send(f"✅ Ticket đã được tạo: {channel.mention}", ephemeral=True)
        logger.info(f"Created ticket {ticket_id} for {user} in {guild}")

        # schedule auto-close task
        async def _auto_close():
            await asyncio.sleep(int(os.getenv('TICKET_AUTO_CLOSE_SECONDS', 1200)))
            ticket_row = await db.get_ticket(ticket_id)
            if not ticket_row:
                return
            if ticket_row['status'] != 'open':
                return
            try:
                await db.close_ticket(ticket_id)
                try:
                    await channel.send(embed=discord.Embed(title='⏲️ Auto-closed', description='Ticket closed due to inactivity.', color=discord.Color.red()))
                    await asyncio.sleep(3)
                    await channel.delete()
                except Exception:
                    pass
                logger.info(f"Auto-closed ticket {ticket_id}")
            except Exception:
                logger.exception('Failed to auto-close ticket %s', ticket_id)

        asyncio.create_task(_auto_close())


class CloseTicketButton(discord.ui.Button):
    def __init__(self):
        super().__init__(style=discord.ButtonStyle.danger, label="🔒 Đóng Ticket")

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        channel = interaction.channel

        # get ticket id from DB
        ticket_id = await db.get_channel_ticket(channel.id)
        if not ticket_id:
            await interaction.followup.send("❌ Không tìm thấy ticket liên kết.")
            return

        # update DB
        await db.close_ticket(ticket_id, closed_by=interaction.user.id)

        embed = discord.Embed(title="🔒 Ticket Đã Đóng", description=f"Đóng bởi: {interaction.user.mention}", color=discord.Color.red())
        await interaction.followup.send(embed=embed)

        # delete channel after short delay
        await asyncio.sleep(3)
        try:
            await channel.delete()
        except Exception as e:
            logger.exception("Failed to delete ticket channel: %s", e)


class PanelView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(OpenTicketButton())


class TicketsV2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='create_panel', description='Tạo panel ticket (mới, v2)')
    async def create_panel(self, interaction: discord.Interaction):
        embed = discord.Embed(title="🎫 Mở Ticket", description="Nhấn nút bên dưới để mở ticket.", color=discord.Color.green())
        view = PanelView()
        await interaction.response.send_message(embed=embed, view=view)


async def setup(bot):
    await bot.add_cog(TicketsV2(bot))
