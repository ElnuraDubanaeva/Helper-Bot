import re

from aiogram import types, Dispatcher, Bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import admin, bot
from database.bot_db import (
    all_sql,
    today_students,
    students_test,
    get_all_test_done,
    get_results_bd,
    delete_sql,
    get_data_to_test_done,
    insert_test_done,
    update_test,
    get_fullname,
)
from handlers.commands import set_default_commands
from keyboards.client_kb import admin_markup

global student_name_td, student_name


class Info:
    def __init__(self, student):
        self.student = student

    def get_info(self):
        student_info = (
            f"\nID {self.student[0]}"
            f"\nФИО: {self.student[2]}"
            f"\nНомер: {self.student[3]}"
            f"\nУровень: {self.student[5]}"
            f"\nГород: {self.student[4]}"
            f"\nТест: {self.student[6]}"
            f"\nВозраст: {self.student[7]}"
            f"\nUsername: {self.student[8]}"
            f"\nDate: {self.student[1]}"
            f"\nTEST_DATE: {self.student[9]}"
        )
        return student_info


async def admin_check(message: types.Message):
    if message.from_user.id not in admin:
        await message.answer("You are not admin")
    else:
        await set_default_commands(message.bot, message.from_user.id)
        await message.answer(
            "Welcome to <b>admin commands</b>👽"
            "To get more detail information about admins commands touch the command "
            "<b>/info_admin</b> ",
            reply_markup=admin_markup,
            parse_mode="HTML",
        )


async def today_reg(message: types.Message):
    if message.from_user.id in admin:
        t_students = await today_students()
        for t_student in t_students:
            info_1 = Info(t_student)
            await message.answer(
                f"{info_1.get_info()}",
                reply_markup=InlineKeyboardMarkup(row_width=3).add(
                    InlineKeyboardButton(
                        f"delete {t_student[2]} ❌",
                        callback_data=f"delete {t_student[0]} ",
                    ),
                    InlineKeyboardButton(
                        f"test ✅", callback_data=f"test {t_student[0]}"
                    ),
                ),
            )


async def get_student_id(call: types.CallbackQuery):
    global student_id, fullname
    student_id = call.data.replace("test ", "")
    fullname = await get_fullname(student_id)
    await call.answer(text="Send me e.g 'arrange YYYY-MM-DD '", show_alert=True)


async def test_arranged(message: types.Message):
    if message.from_user.id in admin:
        ta_students = await students_test()
        for ta_student in ta_students:
            global student_name_td
            student_name_td = ta_student[2]
            info_2 = Info(ta_student)
            await message.answer(
                f"\n{info_2.get_info()}",
                reply_markup=InlineKeyboardMarkup(row_width=3).add(
                    InlineKeyboardButton(
                        f"delete {ta_student[2]} ❌",
                        callback_data=f"delete {ta_student[0]} ",
                    ),
                    InlineKeyboardButton(
                        "DONE ✅", callback_data=f"DONE {ta_student[0]}"
                    ),
                ),
            )


async def test_done(call: types.CallbackQuery):
    await get_data_to_test_done(call.data.replace("DONE ", ""))
    await delete_sql(call.data.replace("DONE ", ""))
    await call.answer(
        text=f"Student {student_name_td} moved to other DB! "
        f"To get that student use command /get_all_test_done ",
        show_alert=True,
    )
    await bot.delete_message(call.from_user.id, call.message.message_id)


async def delete_data(message: types.Message):
    if message.from_user.id not in admin:
        await message.answer("Only admins can delete the data")
    else:
        students = await all_sql()
        for student in students:
            global student_name
            student_name = student[2]
            info_3 = Info(student)
            await message.answer(
                f"\n{info_3.get_info()}",
                reply_markup=InlineKeyboardMarkup(row_width=3).add(
                    InlineKeyboardButton(
                        f"delete {student[2]} ❌", callback_data=f"delete {student[0]} "
                    )
                ),
            )


async def complete_delete(call: types.CallbackQuery):
    await delete_sql(call.data.replace("delete ", ""))
    await call.answer(text=f"deleted! {student_name}", show_alert=True)
    await bot.delete_message(call.from_user.id, call.message.message_id)


async def get_test_done(message: types.Message):
    if message.from_user.id in admin:
        test_dones = await get_all_test_done()
        for test_done in test_dones:
            info_4 = Info(test_done)
            await message.answer(
                f"DONE ✅" f"\n{info_4.get_info()}",
                reply_markup=InlineKeyboardMarkup(row_width=3).add(
                    InlineKeyboardButton(
                        f"results {test_done[2]}",
                        callback_data=f"results {test_done[0]}",
                    )
                ),
            )


async def get_test_done_id(call: types.CallbackQuery):
    global test_done_id, test_done_fullname
    test_done_id = call.data.replace("results ", "")
    test_done_fullname = await get_fullname(test_done_id)
    await call.answer(text="send me 'results s-? l-? r-? w-? t-?'", show_alert=True)


async def get_results(message: types.Message):
    if message.from_user.id in admin:
        results = await get_results_bd()
        for result in results:
            await message.answer(
                f"\nName: <i>{result[2]}</i>"
                f"\nTest: <i>{result[6]}</i>"
                f"\nDateTest: <i>{result[9]}</i>"
                f"\n<i><b>speaking:</b></i> <b>{result[10]}</b>"
                f"\n<i><b>listening:</b></i> <b>{result[11]}</b>"
                f"\n<i><b>writing:</b></i> <b>{result[12]}</b>"
                f"\n<i><b>reading:</b></i> <b>{result[13]}</b>"
                f"\n<i><b>TOTAL:</b></i> <b><b>{result[14]}</b></b>",
                parse_mode="HTML",
            )
    else:
        results = await get_results_bd()
        for result in results:
            await message.answer(
                f"\nName: <i>{list(str(result[2]).split())[1]}</i>"
                f"\nTest: <i>{result[6]}</i>"
                f"\nDateTest: <i>{result[9]}</i>"
                f"\n<i><b>speaking:</b></i> <b>{result[10]}</b>"
                f"\n<i><b>listening:</b></i> <b>{result[11]}</b>"
                f"\n<i><b>writing:</b></i> <b>{result[12]}</b>"
                f"\n<i><b>reading:</b></i> <b>{result[13]}</b>"
                f"\n<i><b>TOTAL:</b></i> <b><b>{result[14]}</b></b>",
                parse_mode="HTML",
            )


async def arrange_test_and_insert_results(message: types.Message):
    if message.from_user.id in admin and message.text.startswith("arrange "):
        if message.text.replace("arrange ", "").replace("-", "").isdigit():
            test_day = message.text.replace("arrange ", "")
            await update_test(test_day, student_id)
            await message.answer(f"Test with student {fullname[0]} arranged.")
        else:
            await message.answer(
                "You can write only date e.g <b>arrange 2023-01-12</b>",
                parse_mode="HTML",
            )
    elif message.from_user.id in admin and message.text.startswith("results"):
        speaking = re.findall(r"(?:s-\d+)", message.text)[0]
        listening = re.findall(r"(?:l-\d+)", message.text)[0]
        writing = re.findall(r"(?:w-\d+)", message.text)[0]
        reading = re.findall(r"(?:r-\d+)", message.text)[0]
        total = re.findall(r"(?:t-\d+)", message.text)[0]
        await insert_test_done(
            f"{str(speaking).replace('s-', '')}",
            f"{str(listening).replace('l-', '')}",
            f"{str(writing).replace('w-', '')}",
            f"{str(reading).replace('r-', '')}",
            f"{str(total).replace('t-', '')}",
            test_done_id,
        )
        await message.answer("Results successfully inserted to the data base")

    else:
        await message.answer("You are not admin")


async def info_handler(message: types.Message):
    if message.from_user.id in admin:
        await message.answer(
            f"\n<b>/get_all - </b> To get all registered students."
            f"\n<b>/today_reg - </b> To get all students who registered today"
            f"\n<b>/admin - </b> To get access to all admin commands"
            f"\n<b>/have_test - </b> To get students with whom you will have test"
            f"\n<b>/get_all_test_done - </b> To get students with whom you had test . "
            f"\n<b>/results - </b> To get all students results"
            f"\n<b>/info - </b> To get info "
            f"\n<i>If you want to add new student to database touch /reg and register</i>"
            f"\n<i>To <b>arrange test:</b></i>"
            f"\n1) /today_reg"
            f"\n2) Touch the inline button <b>test</b>"
            f"\n3) Send me message <i><b> arrange YYYY-MM-DD</b></i> YYYY-MM-DD test date"
            f"\n<i>If you finished test with student:</i>"
            f"\n1) Select /have_test"
            f"\n2) Touch done"
            f"\n<i><b>To add results</b></i>"
            f"\n1) Select /get_all_test_done"
            f"\n2) Touch results"
            f"\n3) send me <i><b>results s-? l-? w-? r-? t-?</b></i>"
            f"\ns-speaking, l-listening, r-reading, w-writing, t-total ?-score",
            parse_mode="HTML",
        )


def register_admin_handler(dp: Dispatcher):
    dp.register_message_handler(delete_data, commands=["get_all"])
    dp.register_message_handler(today_reg, commands=["today_reg"])
    dp.register_message_handler(admin_check, commands=["admin"])
    dp.register_message_handler(test_arranged, commands=["have_test"])
    dp.register_message_handler(get_test_done, commands=["get_all_test_done"])
    dp.register_message_handler(get_results, commands=["results"]),
    dp.register_message_handler(info_handler, commands=["info_admin"])
    dp.register_callback_query_handler(
        complete_delete, lambda call: call.data and call.data.startswith("delete ")
    )
    dp.register_callback_query_handler(
        test_done, lambda call: call.data and call.data.startswith("DONE ")
    )
    dp.register_message_handler(arrange_test_and_insert_results)
    dp.register_callback_query_handler(
        get_test_done_id, lambda call: call.data and call.data.startswith("results ")
    )

    dp.register_callback_query_handler(
        get_student_id, lambda call: call.data and call.data.startswith("test ")
    )
