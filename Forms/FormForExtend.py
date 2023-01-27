from aiogram.dispatcher.filters.state import State, StatesGroup


class FormForExtend(StatesGroup):
    library_card_number = State()
