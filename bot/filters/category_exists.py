from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class IsCategoryExists(BoundFilter):
    async def check(self, callback: types.CallbackQuery) -> bool:
        inlines = callback.message.reply_markup.values
        category = False
        for inline in inlines.get('inline_keyboard'):
            if callback.data == inline[0].callback_data:
                category = True
                break
        return category


class IsServicesExists(BoundFilter):
    async def check(self, callback: types.CallbackQuery) -> bool:
        inlines = callback.message.reply_markup.values
        service = False
        for inline in inlines.get('inline_keyboard'):
            if callback.data == inline[0].callback_data:
                service = True
                break
        return service
