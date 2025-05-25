from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, KeyboardButtonPollType
from create_bot import admins
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import BotCommand, BotCommandScopeDefault
from create_bot import bot

async def set_commands():
    commands = [BotCommand(command='start', description='Старт'),
                BotCommand(command='faq', description='Частые вопросы'),
                ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())

def main_kb(user_telegram_id: int):
    kb_list = [
        KeyboardButton(text="Запись на первую тренировку"),
         KeyboardButton(text="👤 Профиль"),
         KeyboardButton(text="Связаться с нами")
    ]
    if user_telegram_id in admins:
        kb_list.append([KeyboardButton(text="⚙️ Админ панель")])
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню:"
    )
    return keyboard

def admin_kb():
    kb_list = [
        KeyboardButton(text="Сделать рассылку"),
         KeyboardButton(text="Редактировать FAQ"),
         KeyboardButton(text="На главную")
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню:"
    )
    return keyboard
