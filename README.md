# 🍽️ Ресторанный Telegram Бот

Бот для заказа еды в ресторане с красивым меню, корзиной и оформлением заказов.

## 🚀 Быстрый запуск

### Локальный запуск:
```bash
# Установка зависимостей
pip install -r requirements.txt

# Запуск бота
python restaurant_bot.py
```

### Автоматический запуск:
```bash
# Используйте скрипт для автоматической установки зависимостей
./run_bot.sh
```

## 📋 Функции

- 🍽️ **Интерактивное меню** с категориями блюд
- 📸 **Фотографии блюд** с описанием и ценами
- 🛒 **Корзина** с возможностью добавления нескольких позиций
- 📍 **Геолокация** для доставки
- 📱 **Современный интерфейс** с inline-кнопками
- 👨‍💼 **Уведомления администраторам** о новых заказах

## 🏗️ Структура проекта

```
images/
├── drinks/          # Напитки
├── hot/             # Горячие блюда (супы)
├── main/            # Основные блюда
├── salads/          # Салаты
├── sauces/          # Соусы
├── snacks/          # Закуски
└── restaurant_bot.py # Основной файл бота
```

## 🔧 Развертывание для постоянной работы

### Вариант 1: Systemd (Рекомендуется для VPS)

```bash
# Установка как системной службы
./install_service.sh

# Управление
sudo systemctl start restaurant-bot
sudo systemctl status restaurant-bot
sudo journalctl -u restaurant-bot -f
```

### Вариант 2: Docker

```bash
# Запуск в контейнере
docker-compose up -d

# Просмотр логов
docker-compose logs -f
```

### Вариант 3: Облачные платформы

- **Heroku**: `heroku ps:scale worker=1`
- **Railway**: Подключите GitHub репозиторий
- **Render**: Создайте Web Service

### Вариант 4: Cron (простой)

```bash
# Настройка автоматического перезапуска
./cron_setup.sh
```

## 📁 Файлы развертывания

- `bot_service.py` - Сервис с автоматическим перезапуском
- `install_service.sh` - Установка как systemd службы
- `docker-compose.yml` - Docker конфигурация
- `Dockerfile` - Docker образ
- `Procfile` - Для облачных платформ
- `run_bot.sh` - Простой запуск
- `cron_setup.sh` - Настройка cron

## 🔐 Безопасность

1. **Смените токен бота** в `restaurant_bot.py`
2. **Настройте переменные окружения**:
   ```bash
   export TOKEN="ваш_токен_бота"
   ```
3. **Ограничьте доступ** к серверу
4. **Регулярно обновляйте** систему

## 📊 Мониторинг

### Логи:
- Systemd: `sudo journalctl -u restaurant-bot -f`
- Docker: `docker-compose logs -f`
- Файл: `tail -f bot.log`

### Статус:
- Systemd: `sudo systemctl status restaurant-bot`
- Docker: `docker-compose ps`

## 🛠️ Настройка

### Изменение меню:
Отредактируйте словарь `CATEGORIES` в `restaurant_bot.py`

### Добавление блюд:
1. Добавьте фото в соответствующую папку
2. Добавьте информацию в `CATEGORIES`
3. Перезапустите бота

### Изменение админов:
Измените список `admin_ids` в функции обработки заказов

## 📞 Поддержка

При возникновении проблем:
1. Проверьте логи: `tail -f bot.log`
2. Убедитесь, что токен бота правильный
3. Проверьте подключение к интернету
4. Перезапустите бота

## 📄 Лицензия

MIT License 

---

## Как исправить:

### 1. Убедитесь, что web_server.py запускается вместе с ботом

В файле `bot_service.py` уже есть импорт и запуск web-сервера через Flask.  
**Важно:** Railway должен знать, какой порт слушать.

### 2. Проверьте Procfile

В Procfile должна быть команда:
```
worker: python bot_service.py
```
(или, если вы хотите явно запускать web_server.py, используйте `python web_server.py`)

### 3. Проверьте, что Flask-сервер слушает порт, который задаёт Railway

Railway обычно передаёт порт через переменную окружения `PORT`.  
В файле `web_server.py` замените запуск сервера на:

```python
def run_web_server():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
```

---

## Итоговые шаги:

1. **Обновите функцию запуска Flask-сервера в `web_server.py`:**
   ```python
   def run_web_server():
       port = int(os.environ.get("PORT", 5000))
       app.run(host="0.0.0.0", port=port, debug=False)
   ```
2. **Сделайте коммит и отправьте изменения на GitHub:**
   ```sh
   git add web_server.py
   git commit -m "Fix Flask server to use Railway PORT env"
   git push origin main
   ```
3. **Redeploy на Railway.**

---

**Если после этого снова будет ошибка — пришлите новые логи!**  
Если всё получится — бот будет работать, и healthcheck пройдёт успешно! 

---

## 1. Откройте файл `web_server.py` в вашем проекте

Найдите функцию, которая запускает Flask-сервер. Она выглядит примерно так:
```python
def run_web_server(host='0.0.0.0', port=5000):
    def run():
        app.run(host=host, port=port, debug=False)
    thread = threading.Thread(target=run, daemon=True)
    thread.start()
    return thread
```

---

## 2. Измените запуск сервера, чтобы он использовал переменную окружения PORT

Замените функцию на этот вариант:
```python
<code_block_to_apply_changes_from>
```
**(Главное отличие — порт берётся из переменной окружения PORT, которую Railway задаёт автоматически.)**

---

## 3. Сохраните изменения

---

## 4. Откройте Терминал и выполните команды:

```sh
cd ~/Desktop/images
git add web_server.py
git commit -m "Исправил запуск Flask-сервера для Railway"
git push origin main
```

---

## 5. Вернитесь на Railway и сделайте Redeploy

- Перейдите в ваш проект на Railway.
- Нажмите **Deploy** или **Redeploy**.
- Дождитесь завершения деплоя.

---

## 6. Проверьте результат

- Если деплой прошёл успешно — бот должен заработать, а healthcheck пройти.
- Если появится ошибка — пришлите скриншот или текст ошибки, я помогу!

---

Если что-то не получается на каком-то шаге — напишите, где возник вопрос, я объясню подробнее! 