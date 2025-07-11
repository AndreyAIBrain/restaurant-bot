# 🚀 Развертывание ресторанного бота

## Вариант 1: Systemd (Рекомендуется для VPS)

### Установка на Ubuntu/Debian:

1. **Установите зависимости:**
```bash
sudo apt update
sudo apt install python3 python3-pip
pip3 install -r requirements.txt
```

2. **Запустите установочный скрипт:**
```bash
chmod +x install_service.sh
./install_service.sh
```

3. **Проверьте статус:**
```bash
sudo systemctl status restaurant-bot
```

### Управление сервисом:
```bash
# Запуск
sudo systemctl start restaurant-bot

# Остановка
sudo systemctl stop restaurant-bot

# Перезапуск
sudo systemctl restart restaurant-bot

# Просмотр логов
sudo journalctl -u restaurant-bot -f

# Автозапуск при загрузке системы
sudo systemctl enable restaurant-bot
```

## Вариант 2: Docker

### Установка Docker:
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install docker.io docker-compose
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER
```

### Запуск бота:
```bash
# Сборка и запуск
docker-compose up -d

# Просмотр логов
docker-compose logs -f

# Остановка
docker-compose down
```

## Вариант 3: Облачные платформы

### Heroku:
1. Создайте аккаунт на Heroku
2. Установите Heroku CLI
3. Создайте `Procfile`:
```
worker: python bot_service.py
```
4. Разверните:
```bash
heroku create your-bot-name
git push heroku main
heroku ps:scale worker=1
```

### Railway:
1. Подключите GitHub репозиторий
2. Укажите команду запуска: `python bot_service.py`
3. Добавьте переменную окружения `TOKEN`

### Render:
1. Создайте новый Web Service
2. Подключите GitHub репозиторий
3. Укажите команду: `python bot_service.py`

## Вариант 4: VPS с screen/tmux

### Установка screen:
```bash
sudo apt install screen
```

### Запуск бота:
```bash
# Создаем новую сессию
screen -S restaurant-bot

# Запускаем бота
python3 bot_service.py

# Отключаемся от сессии (Ctrl+A, затем D)
# Для подключения обратно: screen -r restaurant-bot
```

## Мониторинг и логирование

### Просмотр логов:
```bash
# Systemd
sudo journalctl -u restaurant-bot -f

# Docker
docker-compose logs -f

# Файл логов
tail -f bot.log
```

### Автоматический перезапуск:
- Systemd: автоматически перезапускает при сбоях
- Docker: `restart: unless-stopped`
- Screen: можно добавить в cron для проверки

## Безопасность

1. **Смените токен бота** в `restaurant_bot.py`
2. **Ограничьте доступ** к серверу
3. **Настройте firewall**
4. **Регулярно обновляйте** систему

## Рекомендации

- **VPS с systemd** - лучший вариант для продакшена
- **Docker** - удобно для разработки и тестирования
- **Облачные платформы** - быстрое развертывание без настройки сервера 