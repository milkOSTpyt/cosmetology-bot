from aiogram.utils import executor

from bot.loader import dp
from bot import middlewares, filters, handlers
from bot.utils.misc import init_models


if __name__ == '__main__':
    dp.loop.create_task(init_models())
    executor.start_polling(dp)
