from asyncio import sleep

from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.filters import IsCategoryExists
from bot.filters.category_exists import IsServicesExists
from bot.keyboards import get_services_inline, get_detail_inline, get_contact_button, delete_ok, get_category_menu
from bot.loader import dp, bot
from bot.managers import Manager
from bot.states import ServicesState
from bot.utils import config


@dp.message_handler(text=['Отмена'], state=ServicesState.CONTACT)
async def back_contact(message: types.Message, state: FSMContext):
    state_data = await state.get_data()
    await ServicesState.DETAIL.set()
    await bot.delete_message(message.chat.id, state_data.get('consulting_message'))
    await bot.delete_message(message.chat.id, message.message_id)


@dp.message_handler(content_types=types.ContentTypes.CONTACT, state=ServicesState.CONTACT)
async def get_contact(message: types.Message, state: FSMContext):
    state_data = await state.get_data()
    service = state_data.get('service')
    await bot.delete_message(message.chat.id, state_data.get('consulting_message'))
    await bot.delete_message(message.chat.id, message.message_id)

    # send notify to admin
    await bot.send_message(config.ADMIN,
                           config.NOTIFY_CONSULTING.format(service, f'+{message.contact.phone_number}'),
                           reply_markup=await delete_ok())

    message_obj = await message.answer(text=config.ALERT_CONSULTING_SUCCESS)
    await sleep(1.2)
    await bot.delete_message(message.chat.id, message_obj.message_id)
    await ServicesState.DETAIL.set()


@dp.callback_query_handler(lambda c: c.data == 'consulting', state=ServicesState.DETAIL)
async def consulting(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer(cache_time=5)
    state_data = await state.get_data()
    service = state_data.get('service')
    if username := callback.from_user.username:
        await bot.send_message(config.ADMIN,
                               config.NOTIFY_CONSULTING.format(service, f'@{username}'),
                               reply_markup=await delete_ok())
        await callback.answer(text=config.ALERT_CONSULTING_SUCCESS, show_alert=True)
        return

    await ServicesState.CONTACT.set()
    message_obj = await callback.message.answer(
        'Нажмите кнопку ниже, чтобы отправить контакт',
        reply_markup=await get_contact_button()
    )
    await state.update_data(consulting_message=message_obj.message_id)


@dp.callback_query_handler(lambda c: c.data == 'delete_ok', state='*')
async def delete_consulting_message(callback: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)


@dp.callback_query_handler(lambda c: c.data == 'back_to_services', state=ServicesState.DETAIL)
async def back_to_services(callback: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    category = state_data.get('category')
    await ServicesState.previous()
    await bot.edit_message_text(category, callback.message.chat.id,
                                callback.message.message_id,
                                reply_markup=await get_services_inline(category))


@dp.callback_query_handler(lambda c: c.data == 'back_to_categories', state=ServicesState.SERVICES)
async def back_to_categories(callback: types.CallbackQuery, state: FSMContext):
    manager = Manager()
    description = await manager.file_manager.get_description()
    await ServicesState.previous()
    await bot.edit_message_text(description, callback.message.chat.id,
                                callback.message.message_id,
                                reply_markup=await get_category_menu())


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


@dp.callback_query_handler(IsCategoryExists(), state='*')
async def services_of_category(callback: types.CallbackQuery, state: FSMContext):
    await bot.edit_message_text(
        callback.data,
        callback.message.chat.id,
        callback.message.message_id,
        reply_markup=await get_services_inline(callback.data)
    )
    await ServicesState.SERVICES.set()
    await state.update_data(category=callback.data)
