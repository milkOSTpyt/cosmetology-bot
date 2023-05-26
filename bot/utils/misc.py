from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import MessageToDeleteNotFound, MessageIdentifierNotSpecified, MessageCantBeDeleted
from loguru import logger

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
            logger.exception(f"{error}")
    return wrapper


async def delete_message_from_chat(chat_id, message_id):
    try:
        await bot.delete_message(chat_id, message_id)
    except (MessageToDeleteNotFound, MessageIdentifierNotSpecified, MessageCantBeDeleted) as error:
        logger.debug(f'DEBUG: {error} chad_id: {chat_id}')
