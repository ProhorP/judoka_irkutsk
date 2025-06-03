from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from create_bot import admins
from aiogram.types import BotCommand, BotCommandScopeDefault
from create_bot import bot

async def set_commands():
    commands = [
                BotCommand(command='start', description='Частые вопросы'),
                BotCommand(command='reg', description='Регистрация'),
                ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())
