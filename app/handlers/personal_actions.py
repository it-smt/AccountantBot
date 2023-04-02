from aiogram import types, Dispatcher
import re

from app.database.sql import DB

BotDB = DB('accountant.db')


async def record(msg: types.Message):
    """Добавляет записи в БД."""
    cmd_variants = (('/expand', '/e'), ('/income', '/i'))
    operation = '-' if msg.text.split()[0] in cmd_variants[0] else '+'

    value = msg.text.strip().split()[1] if ' ' in msg.text else ''

    if len(value):
        x = re.findall(r'\d+(?:.\d+)?', value)

        if len(x):
            value = float(x[0].replace(',', '.'))

            BotDB.add_record(msg.from_user.id, operation, value)

            if operation == '-':
                await msg.reply('Запись о <u><b>расходе</b></u> успешно внесена!', parse_mode='HTML')
            else:
                await msg.reply('Запись о <u><b>доходе</b></u> успешно внесена!', parse_mode='HTML')
        else:
            await msg.reply('Не удалось определить сумму!')
    else:
        await msg.reply('Не введена сумма!')


async def history(msg: types.Message):
    """Выводит историю операций пользователя."""
    cmd_variants = ('/history', '/h')
    within_als = {
        'day': ('today', 'day', 'сегодня', 'день'),
        'month': ('month', 'месяц'),
        'year': ('year', 'год')
    }

    cmd = msg.text.split()[1] if ' ' in msg.text else msg.text

    within = 'day'  # По умолчанию.
    if len(cmd):
        for k in within_als:
            for als in within_als[k]:
                if als == cmd:
                    within = k

    records = BotDB.get_records(msg.from_user.id, within)  # Извлекаем все записи, которые соответствуют пользователю.

    if len(records):
        answer = f'История операций за {within_als[within][-1]}\n\n'

        result_i = 0
        result_e = 0

        for r in records:
            if not r[2]:
                result_e += r[3]
            else:
                result_i += r[3]
            answer += f'<b>{"Расход" if not r[2] else "Доход"}</b> - {r[3]} <i>({r[4]})</i>\n'

        answer += f'\n<i>В общем за {within_als[within][-1]} доход составил: {result_i}, а расход: {result_e}</i>'

        await msg.reply(answer, parse_mode='HTML')
    else:
        await msg.reply('Записей не обнаружено!')


def register_handlers_personal_actions(dp: Dispatcher):
    """Регистрирует хендлеры."""
    dp.register_message_handler(record, commands=['income', 'i', 'expend', 'e'], state='*')
    dp.register_message_handler(history, commands=['history', 'h'], state='*')
