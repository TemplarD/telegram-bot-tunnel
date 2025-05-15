import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.webhook.aiohttp_server import SimpleRequestHandler
from aiogram.fsm.storage.memory import MemoryStorage
from aiohttp import web
from settings import settings
from network_monitor import NetworkMonitor
from tunnel_manager import TunnelManager

class TelegramBot:
    def __init__(self):
        self._setup_logging()
        self.bot = Bot(token=settings.BOT_TOKEN)
        self.dp = Dispatcher(storage=MemoryStorage())
        self.network = NetworkMonitor()
        self.tunnel = TunnelManager()
        self.logger = logging.getLogger(__name__)

    def _setup_logging(self):
        """Настройка системы логирования"""
        file_handler = logging.FileHandler(settings.LOGS_DIR / 'bot.log')
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ))
        
        logging.basicConfig(
            level=settings.LOG_LEVEL,
            handlers=[
                file_handler,
                logging.StreamHandler()
            ]
        )

    async def _setup_handlers(self):
        """Регистрация обработчиков сообщений"""
        @self.dp.message()
        async def handle_message(message: types.Message):
            self.logger.info(f"New message from {message.from_user.id}")
            await message.answer("✅ Bot is working!")
            
    async def start_polling(self):
        """Запуск в режиме polling"""
        self.logger.info("Starting in polling mode")
        await self.dp.start_polling(self.bot)

    async def start_webhook(self, public_url: str):
        """Запуск в режиме webhook"""
        app = web.Application()
        webhook_path = f"/webhook/{settings.WEBHOOK_SECRET}"
        
        # Настройка вебхука
        await self.bot.set_webhook(
            url=f"{public_url}{webhook_path}",
            secret_token=settings.WEBHOOK_SECRET
        )

        # Регистрация обработчика
        handler = SimpleRequestHandler(
            dispatcher=self.dp,
            bot=self.bot,
            secret_token=settings.WEBHOOK_SECRET
        )
        handler.register(app, path=webhook_path)

        # Запуск сервера
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(
            runner,
            '0.0.0.0',
            settings.INTERNAL_PORT
        )
        
        self.logger.info(f"Webhook started on {public_url}")
        await site.start()

    async def run(self):
        """Основной метод запуска бота"""
        try:
            await self._setup_handlers()
            await self.network.start_monitoring()

            if settings.MODE == 'polling':
                await self.start_polling()
            else:
                public_url = await self.tunnel.setup_tunnel()
                await self.start_webhook(public_url)
                await asyncio.Event().wait()  # Бесконечное ожидание

        except Exception as e:
            self.logger.critical(f"Bot failed: {e}", exc_info=True)
            raise

async def main():
    bot = TelegramBot()
    await bot.run()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Bot stopped by user")
    except Exception as e:
        logging.critical(f"Fatal error: {e}", exc_info=True)
