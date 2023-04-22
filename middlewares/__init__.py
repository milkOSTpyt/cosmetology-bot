from loader import dp
from middlewares.delete_messages import MessageFilter


dp.middleware.setup(MessageFilter())
