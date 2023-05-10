from aiogram.dispatcher.filters.state import StatesGroup, State


class AdminState(StatesGroup):
    MAIN_MENU = State()
    PROMOTIONS_MENU = State()
    PROMOTIONS_LIST_MENU = State()
    PROMOTIONS_DETAIL_MENU = State()
