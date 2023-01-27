import datetime

_names_of_month = {1: "января",
                  2: "февраля",
                  3: "марта",
                  4: "апреля",
                  5: "мая",
                  6: "июня",
                  7: "июля",
                  8: "августа",
                  9: "сентября",
                  10: "октябряя",
                  11: "ноября",
                  12: "декабря"}


def calc_time(quantity_of_weeks, days) -> str:
    date = datetime.datetime.now() + datetime.timedelta(weeks=quantity_of_weeks, days=days)

    return f'{date.day} {_names_of_month[date.month]} {date.year}'
