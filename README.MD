# Многорежимный Telegram Бот / Multi-Mode Telegram Bot

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Aiogram](https://img.shields.io/badge/aiogram-3.x-green)
![License](https://img.shields.io/badge/license-MIT-yellow)

## 🇷🇺 Русская версия

### О проекте
Этот бот представляет собой универсальное решение для развертывания Telegram-бота с поддержкой 4 режимов подключения. Основные возможности:

### 🌟 Функционал
1. **Гибкое подключение**:
   - ☎️ Polling (простое подключение)
   - 🚀 Ngrok (быстрый временный туннель)
   - 🔐 SSH (через ваш VPS)
   - 🌐 Cloudflare (стабильный туннель с доменом)

2. **Мониторинг сети**:
   - Регулярная проверка доступности критических сервисов
   - Логирование состояния сети
   - Автоматическое обнаружение проблем

3. **Управление туннелями**:
   - Автоматическая настройка выбранного режима
   - Генерация публичных URL
   - Поддержка аутентификации

4. **Логирование**:
   - Подробные логи работы бота
   - Отдельные логи сетевых проверок
   - Ротация логов

### Технологический стек
- **Python 3.10+** - основной язык
- **Aiogram 3.x** - работа с Telegram API
- **Cloudflare Tunnel** - для режима Cloudflare
- **Ngrok/SSH** - альтернативные туннели
- **Aiohttp** - асинхронные HTTP-запросы

### 📋 Требования
- Python 3.10 или новее
- Аккаунт Telegram с @BotFather
- (Для Cloudflare) Зарегистрированный домен
- (Для SSH) Доступ к VPS

## 🇬🇧 English Version

### About Project
This bot is a universal solution for deploying Telegram bots with 4 connection modes support.

### 🌟 Features
1. **Flexible Connection**:
   - ☎️ Polling (simple connection)
   - 🚀 Ngrok (quick temporary tunnel)
   - 🔐 SSH (via your VPS)
   - 🌐 Cloudflare (stable tunnel with domain)

2. **Network Monitoring**:
   - Regular critical services checks
   - Network status logging
   - Automatic issue detection

3. **Tunnel Management**:
   - Automatic mode configuration
   - Public URL generation
   - Authentication support

4. **Logging**:
   - Detailed operation logs
   - Separate network monitoring logs
   - Log rotation

### Tech Stack
- **Python 3.10+** - core language
- **Aiogram 3.x** - Telegram API
- **Cloudflare Tunnel** - for Cloudflare mode
- **Ngrok/SSH** - alternative tunnels
- **Aiohttp** - async HTTP requests

### 📋 Requirements
- Python 3.10 or newer
- Telegram account with @BotFather
- (For Cloudflare) Registered domain
- (For SSH) VPS access

---
