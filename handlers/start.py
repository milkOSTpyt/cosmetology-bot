from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart

from keyboards import get_category_menu
from loader import dp, bot
from managers import Manager
from utils.misc import delete_old_message


@dp.message_handler(CommandStart(), state='*')
async def start_command(message: types.Message, state: FSMContext):
    state_data = await state.get_data()
    if message_del := state_data.get('description_message'):
        await bot.delete_message(message.chat.id, message_del)
    await delete_old_message(message_obj=message, state=state)
    await state.reset_state()
    manager = Manager()
    description = await manager.file_manager.get_description()
    message_obj = await message.answer(text=description, reply_markup=await get_category_menu())
    await state.update_data(description_message=message_obj.message_id)
    await bot.delete_message(message.chat.id, message.message_id)  # delete /start message
