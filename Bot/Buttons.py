import typing

from Bot.EnvironmentVariables import *

from aiogram import types


def create_buttons_for_start() -> typing.List[types.InlineKeyboardButton]:
    excursion = types.InlineKeyboardButton(text="Записаться на эксурсию",
                                           callback_data=my_bot.cb.new(id="excursion", msg_text=""))

    extend_book = types.InlineKeyboardButton(text="Продлить книгу",
                                             callback_data=my_bot.cb.new(id="extend_book", msg_text=""))

    events = types.InlineKeyboardButton(text="Афиша мероприятий",
                                        callback_data=my_bot.cb.new(id="events", msg_text=""),
                                        url="https://vk.com/bibl_chehova?w=app6819359_-89514391")

    litres = types.InlineKeyboardButton(text="Литрес",
                                        callback_data=my_bot.cb.new(id="litres", msg_text=""),
                                        url="http://taglib.ru/news/Biblioteki_Taganroga_predlagaut_novii_format_chteniya.html")

    pushkin_card = types.InlineKeyboardButton(text="Пушкинская карта",
                                              callback_data=my_bot.cb.new(id="puskin_card", msg_text=""),
                                              url="https://rnd.kassir.ru/frame/organizer/view/41139?key=b9c95356-77a1-9c01-9e67-e34eea7606d5&WIDGET_2754445811=eo6gr0n55vq0l4entpoeq47q66")

    searching_book = types.InlineKeyboardButton(text="Электронный каталог",
                                                callback_data=my_bot.cb.new(id="digital_catalogue", msg_text="cancel"),
                                                url="http://80.68.5.27/cgiopac/opacg/opac.exe")

    bundled_together = types.InlineKeyboardButton(text="Комплектуемся вместе",
                                                  callback_data=my_bot.cb.new(id="bundled_together", msg_text=""),
                                                  url="http://cbs-tag.ru/index.php/component/content/article?id=1453")

    return [excursion, extend_book, pushkin_card, events, litres, searching_book, bundled_together]


def add_cancel() -> typing.List[types.InlineKeyboardButton]:
    cancel = types.InlineKeyboardButton(text="Отменить операцию",
                                        callback_data=my_bot.cb.new(id="cancel", msg_text=""))

    return [cancel]
