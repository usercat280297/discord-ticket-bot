import discord
from discord.ext import commands
from utils.database import get_channel_ticket, get_ticket
import logging

logger = logging.getLogger(__name__)

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """Khi member rời server"""
        logger.info(f"Member rời: {member} ({member.id})")
    
    @commands.Cog.listener()
    async def on_message(self, message):
        """Xử lý tin nhắn"""
        # Không process bot messages
        if message.author.bot:
            return
        
        # Thêm xử lý custom cho ticket channels nếu cần
        await self.bot.process_commands(message)
    
    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
        """Xử lý interactions (buttons, selects)"""
        # Logging interactions
        if interaction.type == discord.InteractionType.component:
            logger.info(f"Component interaction: {interaction.custom_id} from {interaction.user}")

async def setup(bot):
    await bot.add_cog(Events(bot))
