from aiogram import types
from aiogram.types import InlineKeyboardMarkup

from bot.db.managers import DbManager


async def get_back_button(callback_data: str):
    return types.InlineKeyboardButton(text='↩ Назад', callback_data=callback_data)


async def get_admin_menu() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=5)
    keyboard.add(types.InlineKeyboardButton(text='Акции 🔥', callback_data='promotions_menu'))
    keyboard.add(types.InlineKeyboardButton(text='Рассылка ✉', callback_data='send_messages'))
    return keyboard


async def get_promotions_menu_inline() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=5)
    keyboard.add(
        types.InlineKeyboardButton(
            text='Список акций',
            callback_data='list_services_by_discount'
        )
    )
    keyboard.add(await get_back_button(callback_data="back_to_main_menu"))
    return keyboard


async def get_list_services_by_discount_inline() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=5)
    for service in await DbManager().service.get_all_services_by_discount():
        text = f'✅ {service.title}' if service.is_active else f'❌ {service.title}'
        keyboard.add(types.InlineKeyboardButton(text=text, callback_data=service.id))
    keyboard.add(await get_back_button(callback_data="back_to_discount_menu"))
    return keyboard


async def get_update_service_by_discount_inline(service_obj) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)
    if service_obj.is_active:
        keyboard.add(types.InlineKeyboardButton(text='❌ Снять акцию', callback_data='update_discount'))
    else:
        keyboard.add(types.InlineKeyboardButton(text='✅ Запустить акцию', callback_data='update_discount'))
    keyboard.add(await get_back_button(callback_data="back_to_list_discount_menu"))
    return keyboard


async def get_back_to_main_menu_button():
    keyboard = InlineKeyboardMarkup(row_width=5)
    keyboard.add(await get_back_button(callback_data="back_to_main_menu"))
    return keyboard


async def get_approved_send_message():
    keyboard = InlineKeyboardMarkup(row_width=5)
    keyboard.add(types.InlineKeyboardButton(text='✅ Да', callback_data='approved_send_message'))
    keyboard.add(types.InlineKeyboardButton(text='❌ Отмена', callback_data='back_to_main_menu'))
    return keyboard
