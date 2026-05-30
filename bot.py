"""
AI Slayd Generator Bot - Main Entry Point
Professional presentation, essay, and academic content generator
"""
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import BOT_TOKEN, STORAGE_CHANNEL_ID
from handlers import start, slide_creator, essay_creator, test_creator, referat_creator
from handlers import mustaqil_ish, kurs_ishi, maqola, tezis
from utils import tg_db, ram_cache

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize bot and dispatcher
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


async def on_startup():
    """Actions on bot startup"""
    logger.info("🚀 Bot ishga tushmoqda...")
    
    # Initialize database
    await tg_db.init(bot, STORAGE_CHANNEL_ID)
    logger.info("✅ Database ulandi (Telegram kanal)")
    
    # Start background tasks
    asyncio.create_task(ram_cache.cleanup_loop())
    asyncio.create_task(ram_cache.midnight_flush_loop(bot))
    asyncio.create_task(tg_db.auto_flush_loop())
    logger.info("✅ Background tasklar boshlandi")
    
    logger.info("✅ Bot tayyor!")


async def on_shutdown():
    """Actions on bot shutdown"""
    logger.info("🛑 Bot to'xtatilmoqda...")
    
    # Save all cached data
    await tg_db.flush_all()
    logger.info("✅ Ma'lumotlar saqlandi")
    
    await bot.session.close()
    logger.info("✅ Bot to'xtatildi")


async def main():
    """Main function to run the bot"""
    
    # Register handlers
    dp.include_router(start.router)
    dp.include_router(slide_creator.router)
    dp.include_router(essay_creator.router)
    dp.include_router(test_creator.router)
    dp.include_router(referat_creator.router)
    dp.include_router(mustaqil_ish.router)
    dp.include_router(kurs_ishi.router)
    dp.include_router(maqola.router)
    dp.include_router(tezis.router)
    
    # Startup actions
    await on_startup()
    
    try:
        # Start polling
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        # Shutdown actions
        await on_shutdown()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot foydalanuvchi tomonidan to'xtatildi")
    except Exception as e:
        logger.error(f"Xatolik: {e}")
