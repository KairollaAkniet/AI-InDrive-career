import os
# ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←
# Отключаем Xet Storage ДО ВСЕХ импортов
os.environ["HF_HUB_DISABLE_XET"] = "1"
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
# ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←

import asyncio
import os  # можно оставить, дубликат не мешает
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from indrive_api import analyze_candidate_score

load_dotenv()

# ... весь остальной код main.py без изменений ...

load_dotenv()

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()

# Идеальный профиль из ТЗ inVision U (теперь используется!)
IDEAL_PROFILE = (
    "Leadership potential, social projects, motivation to grow, "
    "integrity, and proactive mindset."
)


@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        f"Привет, {message.from_user.first_name}! 👋\n\n"
        "Я — бот inVision U от inDrive. Расскажи подробнее о себе:\n"
        "• лидерские проекты / социальные инициативы\n"
        "• мотивация расти в IT\n"
        "• опыт и навыки\n\n"
        "Чем подробнее — тем точнее я оценю твой потенциал через Alem Score Engine!"
    )



@dp.message(F.text)
async def handle_application(message: types.Message):
    if len(message.text) < 10:
        await message.answer("Расскажи чуть подробнее!")
        return

    await message.answer("⏳ Нейросеть inVision U изучает твой профиль...")

    score, feedback = analyze_candidate_score(message.text)

    if score:
        status = "✅ Рекомендован" if score > 0.7 else "🔄 В лист ожидания"
        response = (
            f" **Твой Score:** `{score}`\n"
            f" **Статус:** {status}\n\n"
            f" **Анализ ИИ:**\n{feedback}"
        )
        await message.answer(response, parse_mode="Markdown")
    else:
        await message.answer("Ошибка связи с ИИ. Попробуй позже.")


async def main():
    print("Бот с интеллектом inVision U запущен!")
    await dp.start_polling(bot)



if __name__ == "__main__":
    asyncio.run(main())