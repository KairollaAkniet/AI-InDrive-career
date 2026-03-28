# inVision U Selector - AI Assistant for inDrive

## Описание
Интеллектуальная система для первичного отбора кандидатов в университет inVision U. Бот анализирует текстовые заявки абитуриентов на предмет лидерского потенциала и мотивации.

## Технологии
- **Язык:** Python 3.14
- **Библиотека:** aiogram 3.x (Telegram Bot API)
- **AI Core:** Alem Score API (Reranker model `bge-reranker-v2-m3`)

## Как запустить
1. Склонируйте репозиторий.
2. Создайте файл `.env` и добавьте `BOT_TOKEN` и `INDRIVE_API_KEY`.
3. Установите зависимости: `pip install -r requirements.txt`.
4. Запустите бота: `python main.py`.