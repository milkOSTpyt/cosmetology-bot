from bot.loader import dp
from bot.middlewares.delete_messages import MessageFilter


dp.middleware.setup(MessageFilter())
