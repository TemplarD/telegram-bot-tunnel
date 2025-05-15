from pyngrok import ngrok, conf
from sshtunnel import SSHTunnelForwarder
import logging
from settings import settings
import asyncio
import aiohttp

logger = logging.getLogger(__name__)

class TunnelManager:
    @staticmethod
    async def setup_tunnel():
        if settings.MODE == 'ngrok':
            return await TunnelManager._start_ngrok()
        elif settings.MODE == 'ssh_tunnel':
            return await TunnelManager._start_ssh_tunnel()
        elif settings.MODE == 'cloudflare':
            return await TunnelManager._start_cloudflare_tunnel()
        else:
            raise ValueError(f"Unsupported mode: {settings.MODE}")

    @staticmethod
    async def _start_ngrok():
        if not settings.NGROK_AUTH_TOKEN:
            raise ValueError("Ngrok auth token is missing in .env")

        conf.get_default().auth_token = settings.NGROK_AUTH_TOKEN
        conf.get_default().region = settings.NGROK_REGION

        tunnel = ngrok.connect(
            addr=settings.INTERNAL_PORT,
            proto="http",
            bind_tls=True
        )
        logger.info(f"Ngrok tunnel established: {tunnel.public_url}")
        return tunnel.public_url

    @staticmethod
    async def _start_ssh_tunnel():
        server = SSHTunnelForwarder(
            (settings.SSH_HOST, settings.SSH_PORT),
            ssh_username=settings.SSH_USER,
            ssh_pkey=settings.SSH_KEY_PATH,
            remote_bind_address=('127.0.0.1', settings.INTERNAL_PORT)
        )
        server.start()
        logger.info(f"SSH tunnel established on port {server.local_bind_port}")
        return f"https://{settings.SSH_HOST}"

   @staticmethod
async def _start_cloudflare_tunnel():
    if not all([settings.CF_API_TOKEN, settings.CF_ACCOUNT_ID]):
        raise ValueError("Missing Cloudflare credentials in .env")

    headers = {
        "Authorization": f"Bearer {settings.CF_API_TOKEN}",
        "Content-Type": "application/json"
    }

    async with aiohttp.ClientSession(headers=headers) as session:
        # 1. Создаем туннель и получаем токен для подключения
        tunnel_data = {
            "name": "telegram-bot-tunnel",
            "tunnel_secret": os.urandom(32).hex()  # Генерируем секрет
        }

        async with session.post(
            f"https://api.cloudflare.com/client/v4/accounts/{settings.CF_ACCOUNT_ID}/tunnels",
            json=tunnel_data
        ) as resp:
            result = await resp.json()
            if not resp.ok:
                error = result.get('errors', [{}])[0].get('message', 'Unknown error')
                raise ValueError(f"Cloudflare API error: {error}")
            
            tunnel_id = result['result']['id']
            tunnel_token = result['result']['token']  # Ключевой токен!

        logger.info(f"Tunnel created. ID: {tunnel_id}")
        logger.info(f"Tunnel token (save this): {tunnel_token}")

        # 2. Конфигурация ingress (обязателен catch-all rule)
        config = {
            "ingress": [
                {
                    "hostname": settings.CF_DNS_RECORD,
                    "service": f"http://localhost:{settings.INTERNAL_PORT}"
                },
                {
                    "service": "http_status:404"  # Для всех остальных запросов
                }
            ]
        }

        async with session.put(
            f"https://api.cloudflare.com/client/v4/accounts/{settings.CF_ACCOUNT_ID}/tunnels/{tunnel_id}/configurations",
            json={"config": config}
        ) as resp:
            if not resp.ok:
                error = await resp.json()
                logger.error(f"Failed to configure tunnel: {error}")

        # 3. Запускаем cloudflared (пример для Windows)
        try:
            subprocess.Popen([
                "cloudflared", "tunnel",
                "--token", tunnel_token,
                "run"
            ], creationflags=subprocess.CREATE_NEW_CONSOLE)
        except Exception as e:
            logger.error(f"Failed to start cloudflared: {e}")
            raise

        return f"https://{settings.CF_DNS_RECORD}"