from aiogram import types


def start_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add('/i 1000', '/e 1000').add('/history').add('/help')
    return keyboard
