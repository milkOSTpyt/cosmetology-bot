from asyncio import sleep

from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.db.managers import DbManager
from bot.filters import IsCategoryExists
from bot.filters.category_exists import IsServicesExists
from bot import keyboards
from bot.loader import dp, bot
from bot.states import ServicesState
from bot.utils import config
from bot.utils.misc import delete_message_from_chat


@dp.message_handler(text=['Отмена'], state=ServicesState.CONTACT)
async def back_from_sending_contact(message: types.Message, state: FSMContext):
    state_data = await state.get_data()
    await ServicesState.DETAIL.set()
    await delete_message_from_chat(message.chat.id, state_data.get('consulting_message'))
    await delete_message_from_chat(message.chat.id, message.message_id)


@dp.message_handler(content_types=types.ContentTypes.CONTACT, state=ServicesState.CONTACT)
async def get_contact(message: types.Message, state: FSMContext):
    state_data = await state.get_data()
    service_title = state_data.get('service_title')
    await delete_message_from_chat(message.chat.id, state_data.get('consulting_message'))
    await delete_message_from_chat(message.chat.id, message.message_id)

    # send notify to admin_2
    await bot.send_message(config.ADMIN,
                           config.NOTIFY_CONSULTING.format(
                               service_title, f'+{message.contact.phone_number}'
                           ),
                           reply_markup=await keyboards.delete_ok())

    message_obj = await message.answer(text=config.ALERT_CONSULTING_SUCCESS)
    await sleep(3)
    await delete_message_from_chat(message.chat.id, message_obj.message_id)
    await ServicesState.DETAIL.set()


@dp.callback_query_handler(lambda c: c.data == 'consulting', state=ServicesState.DETAIL)
async def consulting(callback: types.CallbackQuery, state: FSMContext):
    # TODO: разделить логику
    state_data = await state.get_data()
    service_title = state_data.get('service_title')
    if username := callback.from_user.username:
        await bot.send_message(config.ADMIN,
                               config.NOTIFY_CONSULTING.format(service_title, f'@{username}'),
                               reply_markup=await keyboards.delete_ok())
        await callback.answer(text=config.ALERT_CONSULTING_SUCCESS, show_alert=True)
        return

    await ServicesState.CONTACT.set()
    message_obj = await callback.message.answer(
        'Нажмите кнопку ниже, чтобы отправить контакт',
        reply_markup=await keyboards.get_contact_button()
    )
    await state.update_data(consulting_message=message_obj.message_id)


@dp.callback_query_handler(lambda c: c.data == 'delete_ok', state='*')
async def delete_consulting_message(callback: types.CallbackQuery, state: FSMContext):
    await delete_message_from_chat(callback.message.chat.id, callback.message.message_id)


@dp.callback_query_handler(lambda c: c.data == 'back_to_services', state=ServicesState.DETAIL)
async def back_to_services(callback: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    category_title, category_id = state_data.get('category_title'), state_data.get('category_id')
    await ServicesState.previous()
    if state_data.get('discount_services') is True:
        await bot.edit_message_text('Акции 🔥',
                                    callback.message.chat.id,
                                    callback.message.message_id,
                                    reply_markup=await keyboards.get_services_inline())
        await state.update_data(discount_services=False)
    else:
        await bot.edit_message_text(category_title,
                                    callback.message.chat.id,
                                    callback.message.message_id,
                                    reply_markup=await keyboards.get_services_inline(category_id))


@dp.callback_query_handler(lambda c: c.data == 'back_to_categories', state=ServicesState.SERVICES)
async def back_to_categories(callback: types.CallbackQuery, state: FSMContext):
    owner = await DbManager().owner.get_owner()
    await ServicesState.previous()
    await bot.edit_message_text(owner.description,
                                callback.message.chat.id,
                                callback.message.message_id,
                                reply_markup=await keyboards.get_category_menu())


@dp.callback_query_handler(IsServicesExists(), state=ServicesState.SERVICES)
async def send_service_detail(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer(cache_time=5)
    service = await DbManager().service.get_service_by_id(service_id=int(callback.data))
    await bot.edit_message_text(service.description,
                                callback.message.chat.id,
                                callback.message.message_id,
                                reply_markup=await keyboards.get_detail_inline(service.link))
    await state.update_data(service_id=service.id, service_title=service.title)
    await ServicesState.DETAIL.set()


@dp.callback_query_handler(lambda c: c.data == 'services_by_discount', state=ServicesState.CATEGORIES)
async def send_services_by_discount(callback: types.CallbackQuery, state: FSMContext):
    await ServicesState.SERVICES.set()
    await bot.edit_message_text('Акции 🔥',
                                callback.message.chat.id,
                                callback.message.message_id,
                                reply_markup=await keyboards.get_services_inline())
    await state.update_data(discount_services=True)


@dp.callback_query_handler(IsCategoryExists(), state=ServicesState.CATEGORIES)
async def send_services_of_category(callback: types.CallbackQuery, state: FSMContext):
    category = await DbManager().category.get_category_by_id(category_id=int(callback.data))
    await bot.edit_message_text(category.title,
                                callback.message.chat.id,
                                callback.message.message_id,
                                reply_markup=await keyboards.get_services_inline(category.id))
    await ServicesState.SERVICES.set()
    await state.update_data(category_id=category.id, category_title=category.title)
