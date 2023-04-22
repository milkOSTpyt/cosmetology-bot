from aiogram import types
from aiogram.types import InlineKeyboardMarkup

from managers import Manager


async def get_services_inline(category: str) -> InlineKeyboardMarkup:
    manager = Manager()
    keyboard = types.InlineKeyboardMarkup()
    for service in await manager.file_manager.get_services_of_category(category):
        keyboard.add(types.InlineKeyboardButton(text=service, callback_data=service[:33]))
    return keyboard


async def get_detail_inline(link: str) -> InlineKeyboardMarkup:
    actions = ['Записаться', 'Онлайн-консультация']
    keyboard = InlineKeyboardMarkup(row_width=3)
    for action in actions:
        if action == 'Записаться':
            keyboard.add(types.InlineKeyboardButton(text=action, callback_data=action, url=link))
            continue
        keyboard.add(types.InlineKeyboardButton(text=action, callback_data='consulting'))
    keyboard.add(types.InlineKeyboardButton(text='↩ Назад', callback_data='back_to_services'))
    return keyboard


async def delete_ok() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=3)
    keyboard.add(types.InlineKeyboardButton(text='✅ Ok', callback_data='delete_ok'))
    return keyboard
