import Config
from Bot import Markup
from Bot.EnvironmentVariables import my_bot, my_database
from Bot import EnvironmentVariables
from AdditionalFunctions import Delay, Time
from Forms.FormForExtend import FormForExtend
from Mail import Mail

from aiogram import types, executor
from aiogram.dispatcher import FSMContext


@my_bot.dp.message_handler(state='*', commands=['cancel'])
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    await send_main_menu(message.from_user)
    if current_state is None:
        return

    await state.finish()
    await message.reply("Действие было отменено")


@my_bot.dp.callback_query_handler(my_bot.cb.filter(id=['cancel']), state='*')
async def send(call: types.CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()
    await call.message.reply("Действие было отменено")
    await Delay.make_button_normal(call)


async def send_main_menu(user_info):
    markup = Markup.get_buttons_for_start()
    _ = await my_bot.bot.send_photo(user_info.id, types.InputFile("./src/imgs/photoForMainPage.jpg"),
                                    caption=f'Добро пожаловать, {user_info.first_name}, в офицальный телеграмм-канал библиотеки города Таганрог',
                                    parse_mode="HTML",
                                    reply_markup=markup)
    try:
        msg_id_for_delete: int = my_database.get_msg_id_from_bd(user_info.id)[0]
        await my_bot.bot.delete_message(user_info.id, msg_id_for_delete)
    except Exception as _ex:
        print(_ex)

    my_database.add_in_table(user_info.id, _["message_id"])


@my_bot.dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    await send_main_menu(message.from_user)
    await my_bot.bot.delete_message(message.from_user.id, message.message_id)


@my_bot.dp.message_handler(state=[FormForExtend.library_card_number])
async def handler_library_card_number(message: types.Message, state: FSMContext):
    try:
        library_card_number = message.text

        await send_main_menu(message.from_user)

        if Mail.send_message_for_extend(library_card_number):
            date = Time.calc_time(quantity_of_weeks=2, days=1)
            await my_bot.bot.send_message(chat_id=message.from_user.id,
                                          text=f"{message.from_user.first_name} ({library_card_number}), вы продлили свои книги до {date}")
        else:
            await my_bot.bot.send_message(chat_id=message.from_user.id,
                                          text="Упс... что-то пошло не так. Попробуйте позже")

        await state.finish()

    except Exception as _ex:
        await message.reply(text="Вы указали неправильный номер билета")


@my_bot.dp.callback_query_handler(lambda cb: cb.game_short_name == "taganrog_library_game")
async def res(call: types.CallbackQuery):
    print(call)


@my_bot.dp.callback_query_handler(my_bot.cb.filter(id=["extend_book"]))
async def extend_book(call: types.CallbackQuery, state: FSMContext):
    user_info = call.from_user
    markup_with_cancel = Markup.get_markup_with_cancel()

    await my_bot.bot.send_message(chat_id=user_info.id,
                                  text="Введите номер читательского билета",
                                  reply_markup=markup_with_cancel)

    await state.set_state(FormForExtend.library_card_number)

    await Delay.make_button_normal(call)


@my_bot.dp.callback_query_handler(my_bot.cb.filter(id=["pushkin_card"]))
async def show_library_history(call: types.CallbackQuery):
    user_info = call.from_user
    await send_main_menu(user_info)
    await my_bot.bot.send_message(chat_id=user_info.id,
                                  text="Оплатить экскурсию вы можете по данной ссылке\nhttps://rnd.kassir.ru/frame/organizer/view/41139?key=b9c95356-77a1-9c01-9e67-e34eea7606d5&WIDGET_2754445811=eo6gr0n55vq0l4entpoeq47q66")

    await Delay.make_button_normal(call)


@my_bot.dp.callback_query_handler(my_bot.cb.filter(id=["events"]))
async def show_library_history(call: types.CallbackQuery):
    user_info = call.from_user
    await send_main_menu(user_info)
    await my_bot.bot.send_message(chat_id=user_info.id, text="Мероприятия")

    await Delay.make_button_normal(call)


@my_bot.dp.callback_query_handler(my_bot.cb.filter(id=["excursion"]))
async def show_library_history(call: types.CallbackQuery):
    user_info = call.from_user
    await send_main_menu(user_info)
    Delay.short_delay()
    await my_bot.bot.send_message(chat_id=user_info.id,
                                  text=f"""
Центральная городская публичная библиотека имени А. П. Чехова предлагает отправиться в увлекательное путешествие-экскурсию по старейшей библиотеке на юге России,заглянуть в самое сердце библиотеки - книгохранилище, пройтись по знаменитой винтовой лестнице, узнать интересные факты из истории библиотеки, познакомиться с архитектурной особенностью «шехтелевского» здания, с уникальными, ценными и редкими изданиями. А также посетить музейную экспозицию «Открытая коллекция» в отделе «Центр краеведческой информации». На выставке воспроизведена атмосфера быта старого Таганрога: старинные предметы домашнего обихода, мебель, посуда второй половины XIX – начала XX века… Мы ждем Вас!

Справки по телефону: {Config.phone_number_for_excursion}.""")

    await Delay.make_button_normal(call)


@my_bot.dp.callback_query_handler(my_bot.cb.filter(id=["litres"]))
async def send_litres_url(call: types.CallbackQuery):
    user_info = call.from_user
    await send_main_menu(user_info)

    await my_bot.bot.send_message(chat_id=user_info.id, text="Читайте и слушайте книги в Litres")

    await Delay.make_button_normal(call)


@my_bot.dp.callback_query_handler(my_bot.cb.filter(id=["digital_catalogue"]))
async def send_litres_url(call: types.CallbackQuery):
    user_info = call.from_user
    await send_main_menu(user_info)
    await my_bot.bot.send_message(chat_id=user_info.id, text="Не получается получить доступ от сервера")

    await Delay.make_button_normal(call)


@my_bot.dp.callback_query_handler(my_bot.cb.filter(id=["bundled_together"]))
async def bundled_together(call: types.CallbackQuery):
    user_info = call.from_user
    await send_main_menu(user_info)
    await my_bot.bot.send_message(chat_id=user_info.id,
                                  text="http://cbs-tag.ru/index.php/component/content/article?id=1453")

    await Delay.make_button_normal(call)


@my_bot.dp.callback_query_handler(my_bot.cb.filter(id=["game"]))
async def play_game(call: types.CallbackQuery):
    # field = game.get_field()
    # await my_bot.bot.send_message(call.from_user.id, text=field)
    await my_bot.bot.send_game(call.from_user.id, game_short_name="taganrog_library_game")


def main() -> None:
    executor.start_polling(my_bot.dp)


if __name__ == "__main__":
    main()
