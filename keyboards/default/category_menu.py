from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from managers import Manager


async def get_category_menu() -> ReplyKeyboardMarkup:
    manager = Manager()
    categories_kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=7)
    for category in await manager.file_manager.get_categories():
        categories_kb.add(KeyboardButton(category))
    return categories_kb
