from bot.filters.category_exists import IsCategoryExists
from bot.filters.admin import IsAdmin
from bot.loader import dp


dp.filters_factory.bind(IsCategoryExists)
dp.filters_factory.bind(IsAdmin)
