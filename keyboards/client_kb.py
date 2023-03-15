from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin_markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=4).add(
    KeyboardButton("/get_all 📒"),
    KeyboardButton("/today_reg ⏳"),
    KeyboardButton("/have_test 👌"),
    KeyboardButton("/get_all_test_done 😎 "),
    KeyboardButton("/results ✅"),
    KeyboardButton("/info_admin ℹ️"),
    KeyboardButton("/reg 📝"),
)
city_markup = ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=True, row_width=3
).add(
    KeyboardButton("Бишкек"),
    KeyboardButton("Ысык-Кол"),
    KeyboardButton("Жалал-Абад"),
    KeyboardButton("Чуй"),
    KeyboardButton("Нарын"),
    KeyboardButton("Талас"),
    KeyboardButton("Баткен"),
    KeyboardButton("Ош"),
)

level_markup = ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=True, row_width=3
).add(
    KeyboardButton("Advanced"),
    KeyboardButton("Upper-intermediate"),
    KeyboardButton("Intermediate"),
)

test_markup = ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=True, row_width=3
).add(KeyboardButton("TOEFL"), KeyboardButton("Duolingo"))
submit_markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
    KeyboardButton("ДА"), KeyboardButton("НЕТ")
)
cancel_markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
    KeyboardButton("CANCEL")
)
