from aiogram import types, Dispatcher

from app.database.sql import DB
from app.keyboards.base_keyboards import start_keyboard

BotDB = DB('accountant.db')


async def start(msg: types.Message):
    """Функция старта и регистрации/аутентификации пользователя."""
    if not BotDB.user_exists(msg.from_user.id):
        BotDB.add_user(msg.from_user.id, msg.from_user.username)

    await msg.bot.send_message(msg.from_user.id, 'Добро пожаловать!\n\nЧтобы посмотреть, что я умею, введите /help',
                               reply_markup=start_keyboard())


async def help(msg: types.Message):
    """Функция, которая выводит пользователю команды бота."""
    await msg.bot.send_message(msg.from_user.id,
                               'Вот команды, которые у меня есть:\n'
                               '<b><i>/start</i></b> - команда для начала работы с ботом.\n'
                               '<b><i>/help</i></b> - команда для знакомства со всеми возможностями бота.\n'
                               '<b><i>/income сумма, /i сумма</i></b> - команда для добавления дохода.\n'
                               '<b><i>/expend сумма, /e сумма</i></b> - команда для добавления расхода.\n'
                               '<b><i>/history, /h</i></b> - команда для получения дохода за день. '
                               'В качестве аргумента можно передать период например <b><i>/history месяц</i></b> '
                               'или <b><i>/history year</i></b>',
                               parse_mode='HTML')


def register_handlers_base(dp: Dispatcher):
    """Регистрирует хендлеры."""
    dp.register_message_handler(start, commands='start', state='*')
    dp.register_message_handler(help, commands='help', state='*')
