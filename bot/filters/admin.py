from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from bot.utils.config import ADMIN


class IsAdmin(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        if str(message.from_user.id) == str(ADMIN):
            return True
        return False
