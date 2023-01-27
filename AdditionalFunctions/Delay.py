import time
from aiogram import types


def short_delay():
    time.sleep(0.2)


async def make_button_normal(call):
    short_delay()
    await call.answer()
