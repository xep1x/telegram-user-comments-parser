import json
import logging
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetRepliesRequest
from telethon.errors import ChannelPrivateError, ChannelInvalidError
from telethon.tl.types import PeerUser

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Загрузка ключей API из файла api_keys.json
with open('api_keys.json', 'r') as f:
    api_keys = json.load(f)

api_id = api_keys['telegram_api_id']
api_hash = api_keys['telegram_api_hash']
phone = api_keys['telegram_phone_number']

# Инициализация клиента
client = TelegramClient(phone, api_id, api_hash)

# Функция для получения комментариев пользователя из всех постов канала
async def get_user_comments(channel_link, user_id):
    await client.start()
    try:
        channel = await client.get_entity(channel_link)
        logger.info(f"Канал найден: {channel_link}")
    except ValueError:
        logger.error(f"Не удалось найти канал по ссылке: {channel_link}")
        return []
    except ChannelPrivateError:
        logger.error(f"Канал {channel_link} является приватным.")
        return []
    except ChannelInvalidError:
        logger.error(f"Канал {channel_link} является недействительным.")
        return []

    if isinstance(user_id, str):
        try:
            user = await client.get_entity(user_id)
            user_id = user.id
            logger.info(f"Пользователь найден: {user_id}")
        except ValueError:
            logger.error(f"Не удалось найти пользователя: {user_id}")
            return []

    posts = await client.get_messages(channel, limit=100)  # Получаем 100 постов, можно изменить лимит
    logger.info(f"Получено {len(posts)} постов из канала {channel_link}")

    user_comments = []

    for post in posts:
        if not post.replies:
            continue

        discussion = await client(GetRepliesRequest(
            peer=channel,
            msg_id=post.id,
            offset_id=0,
            offset_date=None,
            add_offset=0,
            limit=100,
            max_id=0,
            min_id=0,
            hash=0
        ))

        messages = discussion.messages

        for message in messages:
            if isinstance(message.from_id, PeerUser) and message.from_id.user_id == user_id:
                comment_data = {
                    'post': post.message,
                    'comment': message.message,
                    'link': f'https://t.me/{channel_link}/{post.id}?comment={message.id}'
                }
                user_comments.append(comment_data)
                logger.info(f"Найден комментарий пользователя {user_id} к посту {post.id}")

    return user_comments

# Основная функция
async def main():
    channel_link = 'https://t.me/link'  # Вставьте ссылку на канал
    user_id = 'userlink_without_@'  # Замените на ID пользователя или ссылку

    comments = await get_user_comments(channel_link, user_id)

    with open('parsing.txt', 'w', encoding='utf-8') as f:
        for comment in comments:
            f.write(f"Post: {comment['post']}\n")
            f.write(f"Comment: {comment['comment']}\n")
            f.write(f"Link: {comment['link']}\n\n")

    for comment in comments:
        print(f"Post: {comment['post']}")
        print(f"Comment: {comment['comment']}")
        print(f"Link: {comment['link']}\n")

# Запуск клиента и основной функции
with client:
    client.loop.run_until_complete(main())