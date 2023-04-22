from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from managers import Manager


class IsCategoryExists(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        manager = Manager()
        return message.text in await manager.file_manager.get_categories()


class IsServicesExists(BoundFilter):
    async def check(self, callback: types.CallbackQuery) -> bool:
        inlines = callback.message.reply_markup.values
        service = False
        for inline in inlines.get('inline_keyboard'):
            if callback.data == inline[0].callback_data:
                service = True
                break
        return service
