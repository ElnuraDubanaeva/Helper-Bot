from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from database.bot_db import insert_sql
from keyboards.client_kb import (
    city_markup,
    level_markup,
    test_markup,
    submit_markup,
    cancel_markup,
)


class FSMAdmin(StatesGroup):
    student_fullname = State()
    student_number = State()
    student_city = State()
    student_level = State()
    student_test = State()
    student_age = State()
    student_username = State()
    submit = State()


async def fsm_start(message: types.Message):
    await FSMAdmin.student_fullname.set()
    await message.answer("Фамилия Имя Отчество : ", reply_markup=cancel_markup)


async def load_fullname(message: types.Message, state: FSMContext):
    if (
        str(message.text).replace(" ", "").isalpha()
        and str(message.text).count(" ") == 2
    ):
        async with state.proxy() as data:
            data["student_fullname"] = message.text.title()
        await FSMAdmin.next()
        await message.answer("Укажите свой WhatsApp номер", reply_markup=cancel_markup)
    else:
        await message.answer(
            "Введите ваше Фамилия Имя Отчество", reply_markup=cancel_markup
        )


async def load_number(message: types.Message, state: FSMContext):
    if (
        int(message.text)
        and len(str(message.text)) == 10
        and str(message.text).startswith("0")
    ):
        async with state.proxy() as data:
            data["student_number"] = f"+996{message.text}"
        await FSMAdmin.next()
        await message.answer(
            "Выберите город где вы сейчас находитесь", reply_markup=city_markup
        )
    else:
        await message.answer(
            "Введите номер: например 0777123456", reply_markup=cancel_markup
        )


async def load_city(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["student_city"] = message.text
    await FSMAdmin.next()
    await message.answer(
        "Укажите ваш уровень английского языка", reply_markup=level_markup
    )


async def load_level(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["student_level"] = message.text
    await FSMAdmin.next()
    await message.answer("Какой тест собираетесь сдавать?", reply_markup=test_markup)


async def load_test(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["student_test"] = message.text
    await FSMAdmin.next()
    await message.answer("Сколько вам лет?", reply_markup=cancel_markup)


async def load_age(message: types.Message, state: FSMContext):
    if str(message.text).isnumeric() and 15 < int(message.text) < 60:
        async with state.proxy() as data:
            data["student_age"] = int(message.text)
        await FSMAdmin.next()
        await message.answer("Скажи привет😊 ", reply_markup=cancel_markup)
    else:
        await message.answer("Введите ваш возраст", reply_markup=cancel_markup)


async def load_username(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["student_username"] = f"@{message.from_user.username}"
    await message.answer(
        f'\nФИО: {data["student_fullname"]}'
        f'\nНомер: {data["student_number"]} '
        f'\nУровень: {data["student_level"]}'
        f'\nГород: {data["student_city"]}'
        f'\nТест: {data["student_test"]}'
        f'\nВозраст: {data["student_age"]}'
        f'\nUsername: {data["student_username"]}'
    )
    await FSMAdmin.next()
    await message.answer("Все данные правильны?", reply_markup=submit_markup)


async def submit(message: types.Message, state: FSMContext):
    if message.text == "ДА":
        await insert_sql(state)
        await state.finish()
        await message.answer(
            "Регистрация успешно завершена"
            "\n<i><b>С вами Шарафидин свяжется в течений двух дней.</b></i>"
            "\n<b> Хорошего дня!</b>🤗 ",
            parse_mode="HTML",
        )
    elif message.text == ["НЕТ", "CANCEL"]:
        await message.answer(
            "Отмена! Чтобы заново пройти регистрацию нажмите на команду /reg"
        )
        await state.finish()
    else:
        await message.answer("ДА или НЕТ?!")


async def cancel_reg(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await message.answer("You CANCELED registration. To start again touch to /reg")
        await state.finish()


def register_handlers_fsm_student(dp: Dispatcher):
    dp.register_message_handler(cancel_reg, state="*", commands=["CANCEL"])
    dp.register_message_handler(
        cancel_reg, Text(equals=["CANCEL", "Отмена"], ignore_case=True), state=["*"]
    )
    dp.register_message_handler(fsm_start, commands=["reg"])
    dp.register_message_handler(load_fullname, state=FSMAdmin.student_fullname)
    dp.register_message_handler(load_number, state=FSMAdmin.student_number)
    dp.register_message_handler(load_city, state=FSMAdmin.student_city)
    dp.register_message_handler(load_level, state=FSMAdmin.student_level)
    dp.register_message_handler(load_test, state=FSMAdmin.student_test)
    dp.register_message_handler(load_age, state=FSMAdmin.student_age)
    dp.register_message_handler(load_username, state=FSMAdmin.student_username)
    dp.register_message_handler(submit, state=FSMAdmin.submit)
