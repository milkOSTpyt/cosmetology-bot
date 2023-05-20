from asyncio import get_event_loop

from aiogram import Bot
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.dispatcher import Dispatcher

from bot.utils import config


bot = Bot(token=config.BOT_TOKEN)
storage = RedisStorage2(host=config.REDIS_HOST)

dp = Dispatcher(bot, storage=storage, loop=get_event_loop())
