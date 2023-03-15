from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeChat, BotCommandScopeDefault


async def set_default_commands(bot: Bot, chat_id: int):
    return await bot.set_my_commands(
        commands=[
            BotCommand("/admin", "To get access to admin commands"),
            BotCommand("/today_reg", "To get today registered students"),
            BotCommand("/get_all", "To get all registered students "),
            BotCommand("/have_test", "To get students with whom you arranged test"),
            BotCommand(
                "/get_all_test_done",
                "To get all students with whom you already had test",
            ),
            BotCommand("/results", "To get students results"),
            BotCommand(
                "/info_admin", "To get more detailed information about admins commands"
            ),
            BotCommand("/reg", "To register students by yourself e.g past students"),
            BotCommand("/info", "To get information about test"),
        ],
        scope=BotCommandScopeChat(chat_id),
    )


async def set_not_admins_commands(bot: Bot, chat_id: int):
    return await bot.set_my_commands(
        commands=[
            BotCommand("/start", "Чтобы начать или же перезапустить бот"),
            BotCommand("/info", "Чтобы получить информацию"),
            BotCommand("/reg", "Чтобы пройти регистрацию"),
            BotCommand(
                "/results",
                "Чтобы получить результаты других студентов(личной информаций не будет)",
            ),
        ],
        scope=BotCommandScopeChat(chat_id),
    )
