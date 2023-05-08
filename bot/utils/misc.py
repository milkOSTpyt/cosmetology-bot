from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import MessageToDeleteNotFound

from bot.loader import bot


async def delete_old_message(message_obj: types.Message, state: FSMContext) -> None:
    state_data = await state.get_data()
    if message_del := state_data.get('message'):
        await bot.delete_message(message_obj.chat.id, message_del)


def error_handler(func: callable) -> callable:
    """ Decorator error handler """
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as error:
            print(f'ERROR: {error}')
    return wrapper


async def delete_message_from_chat(chat_id, message_id):
    try:
        await bot.delete_message(chat_id, message_id)
    except MessageToDeleteNotFound as error:
        print(f'ERROR: {error} \nchad_id: {chat_id}')
