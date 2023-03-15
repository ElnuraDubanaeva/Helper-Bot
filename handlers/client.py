from aiogram import types, Dispatcher

from config import admin
from handlers.commands import set_not_admins_commands


async def start_handler(message: types.Message):
    if message.from_user.id not in admin:
        await message.answer(
            f"Здравствуйте {message.from_user.first_name}👋! Добро пожаловать в наш бот!"
            f"\n<b>Я бот помощник Шарафидина.</b> 🤖😎"
            f"\n Чтобы получить информацию насчет сдачи тестов нажмите на команду <b>/info</b>",
            parse_mode="HTML",
        )
        await set_not_admins_commands(message.bot, message.from_user.id)

    else:
        await message.answer(
            "Welcome <b>ADMIN</b> to start the bot touch to <b>/admin</b>",
            parse_mode="HTML",
        )


async def info_handler(message: types.Message):
    await message.answer(
        f"\n1) <i><b>Как</b></i> будет проходить тест?"
        f"\n2) <i><b>Где</b></i> будет проходить тест?"
        f"\n3) <i><b>Сколько</b></i> уже работаете?"
        f"\n4) Какие <i><b>требование</b></i> от студента?"
        f"\n5) <i><b>Сколько студентам</b></i> сдали тест?"
        f"\n6) Какие <i><b>тесты</b></i> вы сдаете?"
        f"\n7) Вы <i><b>сами</b></i> сдавали тест?"
        f"\n8) Какие <i><b>баллы</b></i> были у студентов?"
        f"\n9) Сколько <i><b>стоит</b></i> ваша услуга?"
        f"\n10) еше какой то вопрос крч "
        f"\n Если вы согласны на условие нажмите на <i><b>/reg </b></i>чтобы "
        f"<b><i>пройти регистрацию</i></b> "
        f"и в течение двух дней "
        f"Шарафидин лично с вами свяжется чтобы обсудить детали прохождение теста😊",
        parse_mode="HTML",
    )


def register_message_handler_client(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands=["start"])
    dp.register_message_handler(info_handler, commands=["info"])
