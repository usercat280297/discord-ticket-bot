import discord
from discord.ext import commands, tasks
import os
import json
from dotenv import load_dotenv
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment
load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
PREFIX = os.getenv('PREFIX', '!')

# Load config
def load_config():
    with open('config.json', 'r', encoding='utf-8') as f:
        return json.load(f)

CONFIG = load_config()

# Setup bot
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)

@bot.event
async def on_ready():
    """Bot sẵn sàng"""
    logger.info(f"✅ Bot đăng nhập thành công: {bot.user}")
    logger.info(f"📊 Bot đang phục vụ {len(bot.guilds)} server")
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name="Ticket Support")
    )

@bot.event
async def on_guild_join(guild):
    """Khi bot join vào server"""
    logger.info(f"✅ Bot đã join server: {guild.name} ({guild.id})")

# Load cogs
async def load_cogs():
    """Load tất cả cogs"""
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and not filename.startswith('__'):
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                logger.info(f"✅ Đã load cog: {filename}")
            except Exception as e:
                logger.error(f"❌ Lỗi load cog {filename}: {e}")

@bot.before_invoke
async def before_invoke(ctx):
    """Chạy trước khi invoke command"""
    logger.info(f"Command: {ctx.command} | User: {ctx.author} | Guild: {ctx.guild}")

# Error handler
@bot.event
async def on_command_error(ctx, error):
    """Xử lý lỗi command"""
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ Bạn không có quyền sử dụng lệnh này!")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"❌ Thiếu argument: {error.param.name}")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("❌ Lệnh không tồn tại!")
    else:
        logger.error(f"Command error: {error}")
        await ctx.send(f"❌ Có lỗi xảy ra: {error}")

async def main():
    """Main function"""
    async with bot:
        await load_cogs()
        await bot.start(TOKEN)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
