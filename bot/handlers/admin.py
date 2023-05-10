from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.db.managers import DbManager
from bot.filters import IsServicesExists
from bot import keyboards
from bot.loader import dp, bot
from bot.states.admin import AdminState


@dp.callback_query_handler(lambda c: c.data == 'list_services_by_discount', state=AdminState.PROMOTIONS_MENU)
async def list_services_by_discount_menu(callback: types.CallbackQuery, state: FSMContext):
    await AdminState.next()  # state PROMOTIONS_LIST_MENU
    await bot.edit_message_text('Список акций',
                                callback.message.chat.id,
                                callback.message.message_id,
                                reply_markup=await keyboards.get_list_services_by_discount_inline())


@dp.callback_query_handler(lambda c: c.data == 'back_to_discount_menu', state=AdminState.PROMOTIONS_LIST_MENU)
async def back_to_discount_menu(callback: types.CallbackQuery, state: FSMContext):
    await AdminState.previous()  # state PROMOTIONS_MENU
    await bot.edit_message_text('Меню акций',
                                callback.message.chat.id,
                                callback.message.message_id,
                                reply_markup=await keyboards.get_promotions_menu_inline())


@dp.callback_query_handler(lambda c: c.data == 'back_to_main_menu', state=AdminState.PROMOTIONS_MENU)
async def back_to_main_menu(callback: types.CallbackQuery, state: FSMContext):
    await AdminState.previous()  # state MAIN_MENU
    await bot.edit_message_text('Администрирование',
                                callback.message.chat.id,
                                callback.message.message_id,
                                reply_markup=await keyboards.get_admin_menu())


@dp.callback_query_handler(lambda c: c.data == 'promotions_menu', state=AdminState.MAIN_MENU)
async def promotions_menu(callback: types.CallbackQuery, state: FSMContext):
    await AdminState.next()  # state PROMOTIONS_MENU
    await bot.edit_message_text('Меню акций',
                                callback.message.chat.id,
                                callback.message.message_id,
                                reply_markup=await keyboards.get_promotions_menu_inline())


@dp.callback_query_handler(lambda c: c.data == 'back_to_list_discount_menu', state=AdminState.PROMOTIONS_DETAIL_MENU)
async def back_to_list_discount_menu(callback: types.CallbackQuery, state: FSMContext):
    await AdminState.previous()  # state PROMOTIONS_LIST_MENU
    await bot.edit_message_text('Список акций',
                                callback.message.chat.id,
                                callback.message.message_id,
                                reply_markup=await keyboards.get_list_services_by_discount_inline())


@dp.callback_query_handler(IsServicesExists(), state=AdminState.PROMOTIONS_LIST_MENU)
async def detail_discount(callback: types.CallbackQuery, state: FSMContext):
    await AdminState.next()  # state PROMOTIONS_DETAIL_MENU
    service_by_discount = await DbManager().service.get_service_by_id(service_id=int(callback.data))
    await bot.edit_message_text(service_by_discount.title,
                                callback.message.chat.id,
                                callback.message.message_id,
                                reply_markup=await keyboards.get_update_service_by_discount_inline(service_by_discount))
    await state.update_data(update_service_id=service_by_discount.id)


@dp.callback_query_handler(lambda c: c.data == 'update_discount', state=AdminState.PROMOTIONS_DETAIL_MENU)
async def update_discount(callback: types.CallbackQuery, state: FSMContext):
    await AdminState.previous()  # state PROMOTIONS_LIST_MENU
    state_data = await state.get_data()
    service_id = state_data.get('update_service_id')
    await DbManager().service.update_discount(service_id=service_id)
    await callback.answer(text='Обновлено', show_alert=True)
    await bot.edit_message_text('Список услуг с акцией',
                                callback.message.chat.id,
                                callback.message.message_id,
                                reply_markup=await keyboards.get_list_services_by_discount_inline())
