import configparser
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

config = configparser.ConfigParser()
#config.read('config.ini') 
encodings_to_try = [
    'utf-8',        # Стандартная UTF-8
    'utf-8-sig',    # UTF-8 с BOM
    'ascii',        # Базовый ASCII
    'cp1251',       # Windows-1251 (кириллица)
    'cp866',        # Альтернативная кириллица (DOS)
    'iso-8859-1',   # Latin-1
    'iso-8859-5'    # Кириллица
]

config_read = False
for encoding in encodings_to_try:
    try:
        config.read('config.ini', encoding=encoding)
        print(f"Файл успешно прочитан в кодировке {encoding}")
        config_read = True
        break
    except UnicodeDecodeError as e:
        print(f"Ошибка декодирования в {encoding}: {str(e)}")
        continue
    except Exception as e:
        print(f"Другая ошибка при чтении в {encoding}: {str(e)}")
        continue

if not config_read:
    raise ValueError("Не удалось прочитать config.ini ни в одной из поддерживаемых кодировок")

def clean_config_value(value):
    if ';' in value:
        return value.split(';')[0].strip()
    return value.strip()

class Settings:
    # Bot
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    MODE = config.get('bot', 'mode', fallback='polling')
    LOG_LEVEL = config.get('bot', 'log_level', fallback='INFO')
    INTERNAL_PORT = config.getint('bot', 'internal_port', fallback=8443)
    WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET')

    # Ngrok
    NGROK_AUTH_TOKEN = os.getenv('NGROK_AUTH_TOKEN')
    NGROK_REGION = config.get('ngrok', 'region', fallback='us')

    # Cloudflare
    CF_API_TOKEN = os.getenv('CF_API_TOKEN')
    CF_ACCOUNT_ID = os.getenv('CF_ACCOUNT_ID')
    CF_ZONE_ID = os.getenv('CF_ZONE_ID')
    CF_DNS_RECORD = config.get('cloudflare', 'dns_record')
    CF_PROXY = config.getboolean('cloudflare', 'proxy', fallback=True)
    CLOUDFLARED_PATH = config.get('cloudflare', 'cloudflared_path', fallback='cloudflared')

    # SSH
    SSH_HOST = config.get('ssh_tunnel', 'host', fallback='')
    SSH_PORT = config.getint('ssh_tunnel', 'port', fallback=22)
    SSH_USER = config.get('ssh_tunnel', 'user', fallback='')
    SSH_KEY_PATH = os.getenv('SSH_KEY_PATH')

    # Network
    NETWORK_CHECK_INTERVAL = config.getint('network', 'check_interval', fallback=300)
    NETWORK_TIMEOUT = config.getint('network', 'timeout', fallback=10)

    # Paths
    LOGS_DIR = Path('logs')
    LOGS_DIR.mkdir(exist_ok=True)

settings = Settings()
