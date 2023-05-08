from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.keyboards import get_promotions_menu_inline, get_admin_menu
from bot.loader import dp, bot
from bot.states.admin import AdminState


@dp.callback_query_handler(lambda c: c.data == 'back_to_main_menu', state=AdminState.PROMOTIONS)
async def back_to_main_menu(callback: types.CallbackQuery, state: FSMContext):
    await AdminState.previous()
    await bot.edit_message_text('Администрирование',
                                callback.message.chat.id,
                                callback.message.message_id,
                                reply_markup=await get_admin_menu())


@dp.callback_query_handler(lambda c: c.data == 'promotions_menu', state=AdminState.MAIN_MENU)
async def send_promotions_menu(callback: types.CallbackQuery, state: FSMContext):
    await bot.edit_message_text('Меню акций',
                                callback.message.chat.id,
                                callback.message.message_id,
                                reply_markup=await get_promotions_menu_inline())
    await AdminState.PROMOTIONS.set()
