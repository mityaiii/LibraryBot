from Bot import Buttons

from aiogram import types


def get_buttons_for_start() -> types.InlineKeyboardMarkup:
    buttons = Buttons.create_buttons_for_start()

    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*buttons)

    return markup


def get_markup_with_cancel() -> types.InlineKeyboardMarkup:
    buttons = Buttons.add_cancel()

    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(*buttons)

    return markup

