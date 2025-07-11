#!/bin/bash

echo "⏰ Настройка cron для автоматического запуска бота..."

# Получаем полный путь к директории
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
BOT_SCRIPT="$SCRIPT_DIR/bot_service.py"

# Создаем cron задачу для проверки и перезапуска бота
(crontab -l 2>/dev/null; echo "*/5 * * * * pgrep -f bot_service.py > /dev/null || cd $SCRIPT_DIR && python3 bot_service.py > /dev/null 2>&1") | crontab -

echo "✅ Cron задача добавлена!"
echo "📋 Бот будет автоматически перезапускаться каждые 5 минут, если процесс упадет"
echo ""
echo "Для просмотра cron задач: crontab -l"
echo "Для удаления cron задач: crontab -r" 