import asyncio
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import BotCommand

from cfg import API_TOKEN
from app.handlers.common import register_handlers_common
from app.handlers.drinks import register_handlers_drinks
from app.handlers.food import register_handlers_food


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command='/start', description='команда для начала работы с ботом.'),
        BotCommand(command='/help', description='команда для знакомства со всеми возможностями бота.'),
        # BotCommand(command='/income 1000', description='команда для добавления дохода (1000 руб.).'),
        # BotCommand(command='/expand 1000', description='команда для добавления расхода (1000 руб.).'),
        BotCommand(command='/gi', description='команда для получения дохода за все время.'),
        # BotCommand(command='/gi day', description='команда для получения дохода за день.'),
        # BotCommand(command='/gi month', description='команда для получения дохода за месяц.'),
        # BotCommand(command='/gi year', description='команда для получения дохода за год.'),
        BotCommand(command='/ge', description='команда для получения расхода за все время.'),
        # BotCommand(command='/ge day', description='команда для получения расхода за день.'),
        # BotCommand(command='/ge year', description='команда для получения расхода за месяц.'),
        # BotCommand(command='/ge month', description='команда для получения расхода за год.')
    ]
    await bot.set_my_commands(commands)


async def main():
    # Объявление и инициализация объектов бота и диспетчера.
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher(bot, storage=MemoryStorage())

    # Регистрация хендлеров.
    register_handlers_common(dp)
    register_handlers_food(dp)
    register_handlers_drinks(dp)

    # Установка команд бота.
    await set_commands(bot)

    # Запуск поллинга.
    await dp.skip_updates()  # пропуск накопившихся апдейтов (необязательно).
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
