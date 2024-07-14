# Telegram User Comments Parser

Этот проект представляет собой скрипт для извлечения комментариев конкретного пользователя из всех постов в указанном Telegram-канале. Скрипт сохраняет комментарии в файл `parsing.txt`.

## Требования

- Python 3.7+
- Телеграм-аккаунт с API ключами

## Установка

1. Клонируйте репозиторий:

   ```bash
   git clone https://github.com/your_username/telegram-user-comments-parser.git
   cd telegram-user-comments-parser
   ```
2. Установите зависимости:

   ```bash
   pip install -r requirements.txt
   ```
3. Создайте файл api_keys.json в корневой директории проекта со следующим содержимым:

   ```bash
   {
    "telegram_api_id": "YOUR_TELEGRAM_API_ID_HERE",
    "telegram_api_hash": "YOUR_TELEGRAM_API_HASH_HERE",
    "telegram_phone_number": "YOUR_TELEGRAM_PHONE_NUMBER_HERE"
    }
   ```
## Использование

1. Откройте файл bot.py и измените переменные channel_link и user_id на соответствующие значения:

   ```bash
   channel_link = 'https://t.me/your_channel_link'  # Вставьте ссылку на канал
   user_id = 'user_id_to_search'  # Замените на ID пользователя или ссылку
   ```
2. Запустите скрипт:

   ```bash
   python bot.py
   ```
3. После выполнения скрипта откройте файл parsing.txt, чтобы увидеть результаты.

