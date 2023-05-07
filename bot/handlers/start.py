from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart

from bot.db.managers import DbManager
from bot.keyboards import get_category_menu
from bot.loader import dp, bot
from bot.utils.misc import delete_old_message


@dp.message_handler(CommandStart(), state='*')
async def start_command(message: types.Message, state: FSMContext):
    await DbManager().client.update_or_create(
        telegram_id=message.from_user.id,
        name=message.from_user.full_name,
        telegram_username=message.from_user.username,
        phone_number=message.contact.phone_number if message.contact else None
    )  # Add or update client in database

    state_data = await state.get_data()
    if message_del := state_data.get('description_message'):
        await bot.delete_message(message.chat.id, message_del)
    await delete_old_message(message_obj=message, state=state)
    await state.reset_state()
    owner = await DbManager().owner.get_owner()
    message_obj = await message.answer(text=owner.description, reply_markup=await get_category_menu())
    await state.update_data(description_message=message_obj.message_id)
    await bot.delete_message(message.chat.id, message.message_id)  # delete /start message
