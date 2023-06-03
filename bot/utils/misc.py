import asyncio
from asyncio import sleep

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import MessageToDeleteNotFound, MessageIdentifierNotSpecified, MessageCantBeDeleted
from loguru import logger

from bot import keyboards
from bot.db.managers import DbManager
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
            logger.exception(f"TEST: {error}")
    return wrapper


async def delete_message_from_chat(chat_id, message_id):
    try:
        await bot.delete_message(chat_id, message_id)
    except (MessageToDeleteNotFound, MessageIdentifierNotSpecified, MessageCantBeDeleted) as error:
        logger.debug(f'DEBUG: {error} chad_id: {chat_id}')


class SendMessage:
    def __init__(self):
        self._time_sleep = 1

    async def _get_inline_keyboards(self):
        return await keyboards.delete_ok()

    async def _get_clients(self):
        clients = await DbManager().client.get_all_clients()
        return [client for client in clients if client.chat_id]

    async def _send_message(self, chat_id, message):
        await bot.send_message(
            chat_id=chat_id,
            text=message,
            reply_markup=await self._get_inline_keyboards()
        )

    @error_handler
    async def _mailing(self, message: str):
        for client in await self._get_clients():
            await sleep(self._time_sleep)
            await self._send_message(chat_id=client.chat_id, message=message)

    async def run_task_mailing(self, message):
        asyncio.create_task(self._mailing(message))
