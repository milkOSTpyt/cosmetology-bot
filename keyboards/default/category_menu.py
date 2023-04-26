from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


async def get_contact_button() -> ReplyKeyboardMarkup:
    contact_kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=7)
    contact_kb.add(KeyboardButton('Отправить контакт', request_contact=True))
    contact_kb.add(KeyboardButton('Отмена'))
    return contact_kb
