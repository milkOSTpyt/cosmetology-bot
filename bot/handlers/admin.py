from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.db.managers import DbManager
from bot.filters import IsServicesExists
from bot import keyboards
from bot.loader import dp, bot
from bot.states.admin import AdminState, DiscountState, SendMessageState
from bot.utils.misc import SendMessage, delete_message_from_chat


@dp.callback_query_handler(lambda c: c.data == "list_services_by_discount", state=DiscountState.PROMOTIONS_MENU)
async def list_services_by_discount_menu(callback: types.CallbackQuery, state: FSMContext):
    await DiscountState.next()  # state PROMOTIONS_LIST_MENU
    await bot.edit_message_text("Список акций",
                                callback.message.chat.id,
                                callback.message.message_id,
                                reply_markup=await keyboards.get_list_services_by_discount_inline())


@dp.callback_query_handler(lambda c: c.data == "back_to_discount_menu", state=DiscountState.PROMOTIONS_LIST_MENU)
async def back_to_discount_menu(callback: types.CallbackQuery, state: FSMContext):
    await DiscountState.previous()  # state PROMOTIONS_MENU
    await bot.edit_message_text("Меню акций",
                                callback.message.chat.id,
                                callback.message.message_id,
                                reply_markup=await keyboards.get_promotions_menu_inline())


@dp.callback_query_handler(
    lambda c: c.data == "back_to_main_menu",
    state=(
            DiscountState.PROMOTIONS_MENU,
            SendMessageState.INPUT_MESSAGE_STATE,
            SendMessageState.CHECKING_MESSAGE_STATE,
    )
)
async def back_to_main_menu(callback: types.CallbackQuery, state: FSMContext):
    await AdminState.MAIN_MENU.set()  # state MAIN_MENU
    await bot.edit_message_text("Администрирование",
                                callback.message.chat.id,
                                callback.message.message_id,
                                reply_markup=await keyboards.get_admin_menu())


@dp.callback_query_handler(lambda c: c.data == "promotions_menu", state=AdminState.MAIN_MENU)
async def promotions_menu(callback: types.CallbackQuery, state: FSMContext):
    await DiscountState.PROMOTIONS_MENU.set()  # state PROMOTIONS_MENU
    await bot.edit_message_text("Меню акций",
                                callback.message.chat.id,
                                callback.message.message_id,
                                reply_markup=await keyboards.get_promotions_menu_inline())


@dp.callback_query_handler(lambda c: c.data == "back_to_list_discount_menu", state=DiscountState.PROMOTIONS_DETAIL_MENU)
async def back_to_list_discount_menu(callback: types.CallbackQuery, state: FSMContext):
    await DiscountState.previous()  # state PROMOTIONS_LIST_MENU
    await bot.edit_message_text("Список акций",
                                callback.message.chat.id,
                                callback.message.message_id,
                                reply_markup=await keyboards.get_list_services_by_discount_inline())


@dp.callback_query_handler(IsServicesExists(), state=DiscountState.PROMOTIONS_LIST_MENU)
async def detail_discount(callback: types.CallbackQuery, state: FSMContext):
    await DiscountState.next()  # state PROMOTIONS_DETAIL_MENU
    service_by_discount = await DbManager().service.get_service_by_id(service_id=int(callback.data))
    await bot.edit_message_text(service_by_discount.title,
                                callback.message.chat.id,
                                callback.message.message_id,
                                reply_markup=await keyboards.get_update_service_by_discount_inline(service_by_discount))
    await state.update_data(update_service_id=service_by_discount.id)


@dp.callback_query_handler(lambda c: c.data == "update_discount", state=DiscountState.PROMOTIONS_DETAIL_MENU)
async def update_discount(callback: types.CallbackQuery, state: FSMContext):
    await DiscountState.previous()  # state PROMOTIONS_LIST_MENU
    state_data = await state.get_data()
    service_id = state_data.get("update_service_id")
    await DbManager().service.update_discount(service_id=service_id)
    await callback.answer(text="Обновлено", show_alert=True)
    await bot.edit_message_text("Список услуг с акцией",
                                callback.message.chat.id,
                                callback.message.message_id,
                                reply_markup=await keyboards.get_list_services_by_discount_inline())


@dp.callback_query_handler(lambda c: c.data == "approved_send_message", state=SendMessageState.CHECKING_MESSAGE_STATE)
async def approved_message(callback: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    message_to_send = state_data.get("message_to_send")
    await SendMessage().run_task_mailing(message=message_to_send)
    await callback.answer(text="Сообщения клиентам отправлены", show_alert=True)
    await back_to_main_menu(callback, state)


@dp.message_handler(state=SendMessageState.INPUT_MESSAGE_STATE)
async def checking_message(message: types.Message, state: FSMContext):
    state_data = await state.get_data()
    main_message_id = state_data.get("main_message_id")
    await SendMessageState.next()  # state CHECKING_MESSAGE_STATE
    my_message = f"Отправить это сообщение?\n\n{message.text}"
    await bot.edit_message_text(my_message,
                                message.chat.id,
                                main_message_id,
                                reply_markup=await keyboards.get_approved_send_message())
    await state.update_data(message_to_send=message.text)
    await delete_message_from_chat(chat_id=message.chat.id, message_id=message.message_id)


@dp.callback_query_handler(lambda c: c.data == "send_messages", state=AdminState.MAIN_MENU)
async def send_messages_menu(callback: types.CallbackQuery, state: FSMContext):
    await SendMessageState.first()  # state INPUT_MESSAGE_STATE
    await bot.edit_message_text("Введите сообщение:",
                                callback.message.chat.id,
                                callback.message.message_id,
                                reply_markup=await keyboards.get_back_to_main_menu_button())
    await state.update_data(main_message_id=callback.message.message_id)
