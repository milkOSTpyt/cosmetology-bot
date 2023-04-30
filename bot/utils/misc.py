from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.loader import bot


async def delete_old_message(message_obj: types.Message, state: FSMContext):
    state_data = await state.get_data()
    if message_del := state_data.get('message'):
        await bot.delete_message(message_obj.chat.id, message_del)
