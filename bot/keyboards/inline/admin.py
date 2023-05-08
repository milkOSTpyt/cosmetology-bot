from aiogram import types
from aiogram.types import InlineKeyboardMarkup


async def get_admin_menu() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton(text='Акции', callback_data='promotions_menu'))
    return keyboard


async def get_promotions_menu_inline() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        types.InlineKeyboardButton(
            text='Список акций',
            callback_data='list_promotions'
        )
    )
    keyboard.add(
        types.InlineKeyboardButton(
            text='Добавить акцию',
            callback_data='add_promotion'
        )
    )
    keyboard.add(types.InlineKeyboardButton(text='↩ Назад', callback_data='back_to_main_menu'))
    return keyboard
