from aiogram.dispatcher.filters.state import StatesGroup, State


class AdminState(StatesGroup):
    MAIN_MENU = State()


class DiscountState(StatesGroup):
    PROMOTIONS_MENU = State()
    PROMOTIONS_LIST_MENU = State()
    PROMOTIONS_DETAIL_MENU = State()


class SendMessageState(StatesGroup):
    INPUT_MESSAGE_STATE = State()
    CHECKING_MESSAGE_STATE = State()
