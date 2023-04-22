from filters.category_exists import IsCategoryExists
from loader import dp


dp.filters_factory.bind(IsCategoryExists)
