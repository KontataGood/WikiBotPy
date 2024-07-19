#wikipedia bot aiogram
import logging
from aiogram import Bot, F, Dispatcher
import wikipedia
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
import asyncio

# Установка уровня логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token="")
dp = Dispatcher()

# Обработчик команды /start
@dp.message(CommandStart())
async def start(message: Message):
    await message.reply("Привет! Я бот, который поможет тебе искать информацию на Википедии. Просто отправь мне запрос.")

#подробный помощник меню
@dp.message(Command('help'))
async def help_about(message: Message):
   await message.reply("Здесь вы сможете рассказать про свою проблему")

@dp.message(Command('about'))
async def about(message: Message):
   await message.reply("Данный бот является аналогом популярного сайта Wikipedia, но в виде чат-бота")

# Обработчик текстовых сообщений
@dp.message()
async def search_wikipedia(message: Message):
    query = message.text.strip()
    language = 'ru'
    wikipedia.set_lang(language)

    # Поиск информации на Википедии
    try:
        result = await asyncio.to_thread(wikipedia.summary, query, sentences=3)  # Получаем краткое описание
        await message.reply(result)
    except wikipedia.exceptions.DisambiguationError as e:
        options = "\n".join(e.options)
        await message.reply(f"Уточните ваш запрос. Возможно вы имели в виду:\n{options}")
    except wikipedia.exceptions.PageError:
        await message.reply("По вашему запросу ничего не найдено.")
    except Exception as e:
        await message.reply("При обработке вашего запроса произошла ошибка.")

async def main():
    await dp.start_polling(bot)

# Запуск бота
if __name__ == '__main__':
    asyncio.run(main())
