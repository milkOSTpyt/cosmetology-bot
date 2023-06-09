from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.middlewares import BaseMiddleware

from bot.loader import bot, storage
from bot.utils.config import ADMIN


class MessageFilter(BaseMiddleware):
    async def on_pre_process_message(self, message: types.Message, data: dict):
        state = FSMContext(storage=storage, chat=message.chat.id, user=message.from_user.id)
        if cur := await state.get_state():
            current_state = cur.split(':')[1]
            if any((current_state == 'CONTACT' and message.contact,
                    current_state == 'CONTACT' and message.text == 'Отмена',
                    current_state == 'INPUT_MESSAGE_STATE')):
                return
        if message.text == '/start' or (message.text == '/admin' and message.from_user.id == ADMIN):
            return
        await bot.delete_message(message.chat.id, message.message_id)
