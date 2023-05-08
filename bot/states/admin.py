from aiogram.dispatcher.filters.state import StatesGroup, State


class AdminState(StatesGroup):
    MAIN_MENU = State()
    PROMOTIONS = State()
