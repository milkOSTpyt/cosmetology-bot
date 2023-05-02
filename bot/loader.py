from asyncio import get_event_loop

from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from bot.utils.config import BOT_TOKEN


bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()

dp = Dispatcher(bot, storage=storage, loop=get_event_loop())
