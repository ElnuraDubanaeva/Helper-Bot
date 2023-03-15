from aiogram import Bot
from aiogram.utils import executor
import logging
from config import dp, bot
from database.bot_db import create_sql
from handlers import fsm_students, client, admin


async def on_startup(_):
    create_sql()


fsm_students.register_handlers_fsm_student(dp)
client.register_message_handler_client(dp)
admin.register_admin_handler(dp)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
