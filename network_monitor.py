import asyncio
import aiohttp
import logging
from settings import settings
from typing import Dict, Tuple

class NetworkMonitor:
    def __init__(self):
        self._setup_logging()
        self.session = aiohttp.ClientSession()
        self.logger = logging.getLogger('network')

    def _setup_logging(self):
        """Настройка отдельного логгера для сетевых проверок"""
        handler = logging.FileHandler(settings.LOGS_DIR / 'network.log')
        handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        ))
        
        logger = logging.getLogger('network')
        logger.setLevel(settings.LOG_LEVEL)
        logger.addHandler(handler)

    async def _test_connection(self, name: str, url: str) -> Tuple[bool, str]:
        """Проверка соединения с одним сервисом"""
        try:
            async with self.session.get(
                url,
                timeout=settings.NETWORK_TIMEOUT
            ) as response:
                if response.status == 200:
                    return True, "OK"
                return False, f"HTTP {response.status}"
        except Exception as e:
            return False, str(e)

    async def check_connections(self) -> Dict[str, Tuple[bool, str]]:
        """Проверка всех критически важных соединений"""
        services = {
            "Google": "https://www.google.com",
            "Cloudflare": "https://www.cloudflare.com",
            "Telegram API": "https://api.telegram.org",
            "Local Server": f"http://localhost:{settings.INTERNAL_PORT}"
        }
        
        results = {}
        for name, url in services.items():
            status, message = await self._test_connection(name, url)
            results[name] = (status, message)
            if not status:
                self.logger.error(f"Connection failed to {name}: {message}")
        
        return results

    async def _monitoring_loop(self):
        """Цикл периодической проверки сети"""
        while True:
            results = await self.check_connections()
            report = "\n".join(
                f"{name}: {'✅' if status else '❌'} {details}"
                for name, (status, details) in results.items()
            )
            self.logger.info(f"Network status report:\n{report}")
            await asyncio.sleep(settings.NETWORK_CHECK_INTERVAL)

    async def start_monitoring(self):
        """Запуск фонового мониторинга сети"""
        asyncio.create_task(self._monitoring_loop())
        self.logger.info("Network monitoring started")

    async def close(self):
        """Корректное закрытие сессии"""
        await self.session.close()
