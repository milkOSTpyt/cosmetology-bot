from aiogram import types
from aiogram.types import InlineKeyboardMarkup

from bot.db.managers import DbManager


async def get_category_menu() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)
    for category in await DbManager().category.get_all_categories():
        keyboard.add(types.InlineKeyboardButton(text=category.title, callback_data=category.id))
    keyboard.add(types.InlineKeyboardButton(text='Акции 🔥', callback_data='services_by_discount'))
    keyboard.add(types.InlineKeyboardButton(text='Месторасположение 📍', callback_data='location'))
    return keyboard


async def get_services_inline(category_id: str = None) -> InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup()
    if category_id:
        for service in await DbManager().service.get_active_services_by_category(category_id=int(category_id)):
            keyboard.add(types.InlineKeyboardButton(text=service.title, callback_data=service.id))
    else:
        for service in await DbManager().service.get_active_services_by_discount():
            keyboard.add(types.InlineKeyboardButton(text=service.title, callback_data=service.id))
    keyboard.add(types.InlineKeyboardButton(text='↩ Назад', callback_data='back_to_categories'))
    return keyboard


async def get_detail_inline(link: str) -> InlineKeyboardMarkup:
    actions = {
        "Онлайн-консультация": "consulting",
        "Стоимость": "price",
        "Записаться": "note",
        "↩ Назад": "back_to_services"
    }
    keyboard = InlineKeyboardMarkup(row_width=3)
    for action in list(actions.keys()):
        if action == 'Записаться':
            keyboard.add(types.InlineKeyboardButton(text=action, callback_data=action, url=link))
            continue
        keyboard.add(types.InlineKeyboardButton(text=action, callback_data=actions[action]))
    return keyboard


async def delete_ok() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=3)
    keyboard.add(types.InlineKeyboardButton(text='✅ Ok', callback_data='delete_ok'))
    return keyboard
