from aiogram.utils import executor

from bot.loader import dp
from bot import middlewares, filters, handlers


if __name__ == '__main__':
    # dp.loop.create_task(init_models())
    executor.start_polling(dp)
