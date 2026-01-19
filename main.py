import discord
from discord.ext import commands, tasks
from aiohttp import web
import os
import json
from dotenv import load_dotenv
import logging
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
from bot import db

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
    # Use BOT_ACTIVITY env var to set the activity name; default to 'Ticket Support'
    activity_name = os.getenv('BOT_ACTIVITY', 'Ticket Support')
    # Use ActivityType from env (playing/listening/watching/competing/streaming)
    atype = os.getenv('BOT_ACTIVITY_TYPE', 'playing').lower()
    if atype == 'listening':
        act = discord.Activity(type=discord.ActivityType.listening, name=activity_name)
    elif atype == 'watching':
        act = discord.Activity(type=discord.ActivityType.watching, name=activity_name)
    elif atype == 'streaming':
        act = discord.Streaming(name=activity_name, url=os.getenv('BOT_STREAM_URL', 'https://twitch.tv'))
    elif atype == 'competing':
        act = discord.Activity(type=discord.ActivityType.competing, name=activity_name)
    else:
        act = discord.Activity(type=discord.ActivityType.playing, name=activity_name)

    try:
        await bot.change_presence(activity=act)
    except Exception:
        logger.exception('Failed to set bot presence')

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
            # Add interactions endpoint for Discord Interaction HTTP
            PUBLIC_KEY = os.getenv('PUBLIC_KEY')
            APP_ID = os.getenv('APPLICATION_ID') or os.getenv('APP_ID')

            async def verify_request(request):
                sig = request.headers.get('X-Signature-Ed25519', '')
                ts = request.headers.get('X-Signature-Timestamp', '')
                body = await request.read()
                if not PUBLIC_KEY:
                    logger.warning('PUBLIC_KEY not set; rejecting interaction')
                    return False
                try:
                    vk = VerifyKey(bytes.fromhex(PUBLIC_KEY))
                    vk.verify(ts.encode() + body, bytes.fromhex(sig))
                    return True
                except BadSignatureError:
                    return False

            async def interactions_handler(request):
                if not await verify_request(request):
                    return web.Response(status=401, text='invalid request signature')
                payload = await request.json()
                # PING
                if payload.get('type') == 1:
                    return web.json_response({'type': 1})
                # Handle a simple /setup command
                data = payload.get('data', {})
                name = data.get('name')
                if name == 'setup':
                    return web.json_response({
                        'type': 4,
                        'data': {'content': 'Đã setup (via interactions HTTP)'}
                    })
                return web.json_response({'type': 4, 'data': {'content': 'OK'}})

            app.router.add_post('/interactions', interactions_handler)

        # Start health server as a background task
        import asyncio as _asyncio
        _asyncio.create_task(run_health_server())

        await load_cogs()
        # Connect to database if available
        try:
            await db.connect()
            # create tables for dev if using sqlite/local (no-op on postgres if tables exist)
            try:
                db.create_tables()
            except Exception:
                pass
            logger.info("Database connected")
        except Exception as e:
            logger.warning(f"Could not connect to database: {e}")

        # Sync application commands to guilds for faster availability during development
        try:
            for g in bot.guilds:
                try:
                    await bot.tree.sync(guild=discord.Object(id=g.id))
                    logger.info(f"Synced app commands to guild: {g.id}")
                except Exception:
                    logger.exception("Failed to sync commands to guild %s", g.id)
        except Exception:
            logger.exception("Error while syncing app commands")

        await bot.start(TOKEN)
        # On shutdown disconnect DB
        try:
            await db.disconnect()
        except Exception:
            pass

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
