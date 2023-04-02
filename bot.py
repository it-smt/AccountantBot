import asyncio
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import BotCommand

from app.handlers.base import register_handlers_base
from app.handlers.personal_actions import register_handlers_personal_actions
from cfg import API_TOKEN


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command='/start', description='команда для начала работы с ботом.'),
        BotCommand(command='/help', description='команда для знакомства со всеми возможностями бота.'),
        BotCommand(command='/history', description='команда для просмотра истории ваших доходов и расходов.'),
        BotCommand(command='/h', description='команда для просмотра истории ваших доходов и расходов.'),
        BotCommand(command='/income', description='команда для записи дохода.'),
        BotCommand(command='/i', description='команда для записи дохода.'),
        BotCommand(command='/expand', description='команда для записи расхода.'),
        BotCommand(command='/e', description='команда для записи расхода.'),
    ]
    await bot.set_my_commands(commands)


async def main():
    """Точка входа."""
    # Объявление и инициализация объектов бота и диспетчера.
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher(bot, storage=MemoryStorage())

    # Регистрация хендлеров.
    register_handlers_base(dp)
    register_handlers_personal_actions(dp)

    # Установка команд бота.
    await set_commands(bot)

    # Запуск поллинга.
    await dp.skip_updates()  # пропуск накопившихся апдейтов (необязательно).
    await dp.start_polling()


if __name__ == '__main__':
    """Запускаем основной цикл программы."""
    asyncio.run(main())

