from aiogram.dispatcher.filters.state import StatesGroup, State


class ServicesState(StatesGroup):
    CATEGORIES = State()
    SERVICES = State()
    DETAIL = State()
    CONTACT = State()
