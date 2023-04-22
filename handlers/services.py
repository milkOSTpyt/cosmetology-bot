from aiogram import types
from aiogram.dispatcher import FSMContext

from filters import IsCategoryExists
from filters.category_exists import IsServicesExists
from keyboards import get_services_inline, get_detail_inline
from keyboards.inline.services import delete_ok
from loader import dp, bot
from managers import Manager
from states import ServicesState
from utils import config
from utils.misc import delete_old_message


@dp.callback_query_handler(lambda c: c.data == 'delete_ok', state='*')
async def delete_consulting_message(callback: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)


@dp.callback_query_handler(lambda c: c.data == 'consulting', state=ServicesState.DETAIL)
async def get_details(callback: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    service = state_data.get('service')
    client_username = callback.message.chat.username

    if client_username:
        # send notify to admin if username is not empty
        await bot.send_message(config.ADMIN,
                               config.NOTIFY_CONSULTING.format(service, client_username),
                               reply_markup=await delete_ok())
        await callback.answer(config.ALERT_CONSULTING_SUCCESS, show_alert=True)
        return

    await callback.answer(config.ALERT_NOT_USERNAME, show_alert=True)


@dp.callback_query_handler(lambda c: c.data == 'back_to_services', state=ServicesState.DETAIL)
async def back_to_services(callback: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    category = state_data.get('category')
    await ServicesState.previous()
    await bot.edit_message_text(category, callback.message.chat.id,
                                callback.message.message_id,
                                reply_markup=await get_services_inline(category))


@dp.callback_query_handler(IsServicesExists(), state=ServicesState.SERVICES)
async def get_more_details(callback: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()

    manager = Manager()
    service = None
    category = state_data.get('category')

    await callback.answer(cache_time=5)
    inlines = callback.message.reply_markup.values

    for inline in inlines.get('inline_keyboard'):
        if callback.data == inline[0].callback_data:
            service = inline[0].text
            break

    data = await manager.file_manager.get_data_on_service(category, service)

    await bot.edit_message_text(data['description'],
                                callback.message.chat.id, callback.message.message_id,
                                reply_markup=await get_detail_inline(data['link']))

    await ServicesState.DETAIL.set()
    await state.update_data(category=category, service=service)


@dp.message_handler(IsCategoryExists(), state='*')
async def services_of_category(message: types.Message, state: FSMContext):
    await delete_old_message(message_obj=message, state=state)
    await bot.delete_message(message.chat.id, message.message_id)
    message_delete = await message.answer(
        message.text,
        reply_markup=await get_services_inline(message.text)
    )
    await ServicesState.SERVICES.set()
    await state.update_data(category=message.text, message=message_delete.message_id)
