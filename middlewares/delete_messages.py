from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from loader import bot
from managers import Manager


class MessageFilter(BaseMiddleware):
    async def on_pre_process_message(self, message: types.Message, data: dict):
        manager = Manager()
        if any((message.text in await manager.file_manager.get_categories(),
                message.text == '/start')):
            return
        await bot.delete_message(message.chat.id, message.message_id)
