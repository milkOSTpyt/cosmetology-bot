from asyncio import get_event_loop

from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.dispatcher import Dispatcher

from bot.utils import config


bot = Bot(token=config.BOT_TOKEN)


def get_storage():
    if config.DEBUG:
        return MemoryStorage()
    return RedisStorage2(host=config.REDIS_HOST)


storage = get_storage()

dp = Dispatcher(bot, storage=get_storage(), loop=get_event_loop())
