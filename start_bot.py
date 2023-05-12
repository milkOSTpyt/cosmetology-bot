from aiogram.utils import executor
from loguru import logger

from bot.loader import dp
from bot import middlewares, filters, handlers


if __name__ == '__main__':
    # dp.loop.create_task(init_models())
    logger.success('Bot started')
    executor.start_polling(dp)
