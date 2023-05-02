from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.db.models import Base
from bot.loader import bot
from bot.utils.config import engine


async def init_models() -> None:
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


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
