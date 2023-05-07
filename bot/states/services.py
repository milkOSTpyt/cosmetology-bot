from aiogram.dispatcher.filters.state import StatesGroup, State


class ServicesState(StatesGroup):
    SERVICES = State()
    DETAIL = State()
    CONTACT = State()
    PROMOTIONS = State()
