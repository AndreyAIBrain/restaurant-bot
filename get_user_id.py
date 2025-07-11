#!/usr/bin/env python3
"""
Скрипт для получения ID пользователя в Telegram
"""
import telebot
import os

# Используем токен из переменной окружения или из основного файла
TOKEN = os.getenv('TOKEN', "7634334499:AAFeR7PB0KTQHR74mPvehZlKaKFmRfk1fIM")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['myid'])
def get_user_id(message):
    """Отправляет ID пользователя"""
    user_id = message.from_user.id
    username = message.from_user.username or "Не указан"
    first_name = message.from_user.first_name or "Не указано"
    
    response = f"""
🆔 Ваш ID в Telegram:
ID: {user_id}
Имя: {first_name}
Username: @{username}

Скопируйте этот ID для настройки переменной ADMIN_IDS в Railway.
"""
    
    bot.reply_to(message, response)

@bot.message_handler(commands=['start'])
def start(message):
    """Приветственное сообщение"""
    bot.reply_to(message, "Привет! Отправьте /myid чтобы получить ваш ID в Telegram.")

if __name__ == "__main__":
    print("🤖 Бот запущен для получения ID")
    print("📱 Отправьте /myid вашему боту в Telegram")
    print("🛑 Для остановки нажмите Ctrl+C")
    
    try:
        bot.polling(none_stop=True)
    except KeyboardInterrupt:
        print("\n�� Бот остановлен") 