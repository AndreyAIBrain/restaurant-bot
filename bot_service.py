#!/usr/bin/env python3
import telebot
import time
import logging
import sys
import os
from datetime import datetime

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Импортируем бота из основного файла
from restaurant_bot import bot, TOKEN

# Импортируем веб-сервер
from web_server import run_web_server, update_bot_status

def run_bot():
    """Запуск бота с автоматическим перезапуском и веб-сервером"""
    
    # Запускаем веб-сервер для мониторинга
    web_thread = run_web_server()
    logger.info("🌐 Web server started for monitoring")
    
    while True:
        try:
            logger.info("🚀 Запускаем бота...")
            update_bot_status(started=True)
            
            # Очищаем webhook перед запуском
            try:
                bot.delete_webhook()
                logger.info("✅ Webhook очищен")
            except Exception as e:
                logger.error(f"❌ Ошибка при очистке webhook: {e}")
            
            # Запускаем бота
            bot.polling(none_stop=True, timeout=60)
            
        except KeyboardInterrupt:
            logger.info("🛑 Бот остановлен пользователем")
            break
        except Exception as e:
            error_msg = str(e)
            logger.error(f"❌ Ошибка: {error_msg}")
            logger.info("🔄 Перезапуск через 10 секунд...")
            time.sleep(10)

if __name__ == "__main__":
    run_bot() 