from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart, Command

from bot.db.managers import DbManager
from bot.filters import IsAdmin
from bot.keyboards import get_category_menu, get_admin_menu
from bot.loader import dp
from bot.states import ServicesState
from bot.states.admin import AdminState
from bot.utils.misc import delete_old_message, delete_message_from_chat


async def _prepare_chat_before_command(state, message):
    state_data = await state.get_data()
    await delete_message_from_chat(message.chat.id, state_data.get("description_message"))
    await delete_message_from_chat(message.chat.id, state_data.get("consulting_message"))
    await delete_message_from_chat(message.chat.id, state_data.get("admin_message"))
    await state.reset_state()


@dp.message_handler(CommandStart(), state="*")
async def start_command(message: types.Message, state: FSMContext):
    await DbManager().client.update_or_create(
        telegram_id=message.from_user.id,
        chat_id=message.chat.id,
        name=message.from_user.full_name,
        telegram_username=message.from_user.username,
        phone_number=message.contact.phone_number if message.contact else None
    )  # Add or update client in database
    await _prepare_chat_before_command(state, message)
    await delete_old_message(message_obj=message, state=state)
    await state.reset_state()
    owner = await DbManager().owner.get_owner()
    message_obj = await message.answer(text=owner.description, reply_markup=await get_category_menu())
    await state.update_data(description_message=message_obj.message_id)
    await delete_message_from_chat(message.chat.id, message.message_id)  # delete /start message
    await ServicesState.CATEGORIES.set()


@dp.message_handler(Command("admin"), IsAdmin(), state="*")
async def admin_command(message: types.Message, state: FSMContext):
    message_obj = await message.answer(text="Администрирование", reply_markup=await get_admin_menu())
    await _prepare_chat_before_command(state, message)
    await AdminState.MAIN_MENU.set()
    await delete_message_from_chat(message.chat.id, message.message_id)  # delete /admin message
    await state.update_data(admin_message=message_obj.message_id)
