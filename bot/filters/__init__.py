from bot.filters.category_exists import IsCategoryExists
from bot.loader import dp


dp.filters_factory.bind(IsCategoryExists)
