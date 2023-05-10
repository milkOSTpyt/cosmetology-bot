from bot.loader import dp
from bot.middlewares.message_filter import MessageFilter


dp.middleware.setup(MessageFilter())
