#!/bin/bash

# Скрипт установки бота как системной службы

echo "🍽️ Установка ресторанного бота как системной службы..."

# Получаем текущую директорию
CURRENT_DIR=$(pwd)
PYTHON_PATH=$(which python3)

echo "📁 Текущая директория: $CURRENT_DIR"
echo "🐍 Python путь: $PYTHON_PATH"

# Создаем systemd сервис
sudo tee /etc/systemd/system/restaurant-bot.service > /dev/null <<EOF
[Unit]
Description=Restaurant Telegram Bot
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$CURRENT_DIR
Environment=PATH=$PYTHON_PATH
ExecStart=$PYTHON_PATH $CURRENT_DIR/bot_service.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

# Перезагружаем systemd
sudo systemctl daemon-reload

# Включаем автозапуск
sudo systemctl enable restaurant-bot.service

echo "✅ Сервис установлен!"
echo "📋 Команды для управления:"
echo "   Запуск: sudo systemctl start restaurant-bot"
echo "   Остановка: sudo systemctl stop restaurant-bot"
echo "   Статус: sudo systemctl status restaurant-bot"
echo "   Логи: sudo journalctl -u restaurant-bot -f"
echo ""
echo "🚀 Запускаем бота..."
sudo systemctl start restaurant-bot

echo "✅ Бот запущен! Проверьте статус: sudo systemctl status restaurant-bot" 