from aiogram import types
from aiogram.types import InlineKeyboardMarkup

from bot.db.managers import DbManager


async def get_category_menu() -> InlineKeyboardMarkup:
    categories_kb = InlineKeyboardMarkup(row_width=1)
    for category in await DbManager().category.get_all_categories():
        categories_kb.add(types.InlineKeyboardButton(text=category.title, callback_data=category.id))
    return categories_kb


async def get_services_inline(category_id: str) -> InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup()
    for service in await DbManager().service.get_services_by_category(category_id=int(category_id)):
        keyboard.add(types.InlineKeyboardButton(text=service.title, callback_data=service.id))
    keyboard.add(types.InlineKeyboardButton(text='↩ Назад', callback_data='back_to_categories'))
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
