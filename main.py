import discord
from discord.ext import commands, tasks
from aiohttp import web
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
    async def safe_send(content: str):
        try:
            await ctx.send(content)
        except discord.Forbidden:
            logger.warning(f"Missing permissions to send message in channel {getattr(ctx.channel, 'id', 'unknown')}")
        except discord.HTTPException as e:
            logger.error(f"Failed to send message: {e}")

    if isinstance(error, commands.MissingPermissions):
        await safe_send("❌ Bạn không có quyền sử dụng lệnh này!")
    elif isinstance(error, commands.MissingRequiredArgument):
        await safe_send(f"❌ Thiếu argument: {error.param.name}")
    elif isinstance(error, commands.CommandNotFound):
        await safe_send("❌ Lệnh không tồn tại!")
    else:
        logger.error(f"Command error: {error}")
        await safe_send(f"❌ Có lỗi xảy ra: {error}")

async def main():
    """Main function"""
    async with bot:
        # Start a minimal web server bound to the PORT Render provides so the platform
        # detects an open port. If no PORT is set, skip starting the server.
        async def run_health_server():
            port = os.getenv('PORT')
            if not port:
                logger.info("No PORT env var set, skipping web server start")
                return
            try:
                port_int = int(port)
            except ValueError:
                logger.warning(f"Invalid PORT value: {port}")
                return

            app = web.Application()
            async def handle_root(request):
                return web.Response(text="OK")

            app.router.add_get('/', handle_root)
            runner = web.AppRunner(app)
            await runner.setup()
            site = web.TCPSite(runner, '0.0.0.0', port_int)
            await site.start()
            logger.info(f"Health web server running on port {port_int}")

        # Start health server as a background task
        import asyncio as _asyncio
        _asyncio.create_task(run_health_server())

        await load_cogs()
        await bot.start(TOKEN)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
