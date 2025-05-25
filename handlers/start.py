from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from keyboards.all_kb import main_kb
from keyboards.inline_kbs import inline_contact_kb, get_inline_gender_kb, create_qst_inline_kb
from aiogram.filters import CommandStart, Command, CommandObject
from create_bot import questions

from utils.utils import get_random_person
from aiogram.types import CallbackQuery
import asyncio
from aiogram.utils.chat_action import ChatActionSender
from create_bot import questions, bot
from .anketa import Form
from aiogram.fsm.context import FSMContext
from db.db import get_user_data
from handlers.anketa import start_router

@start_router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        user_info = await get_user_data(user_id=message.from_user.id)

    if user_info:
        await message.answer('Привет. Я вижу, что ты зарегистрирован, а значит тебе можно '
                             'посмотреть, как выглядит твой профиль.', reply_markup=main_kb(message.from_user.id))
    else:
        await message.answer('Привет. Для начала выбери свой пол:', reply_markup=get_inline_gender_kb())
        await state.set_state(Form.gender)

@start_router.message(F.text == 'Связаться с нами')
async def cmd_start_3(message: Message):
    await message.answer('С нами можно связаться одним из следующих способов',
                         reply_markup=inline_contact_kb())

@start_router.callback_query(F.data == 'get_phone')
async def send_phone(call: CallbackQuery):
    await call.message.answer('+7‒914‒873‒49‒31\n'
                              '+7‒952‒627‒01‒35\n'
                              '+7 (3952) 99‒20‒09')

# await bot.send_message(chat_id=301711111, text='Hello Nelli!')

@start_router.message(F.text == 'На главную')
async def send_back_home(message: Message):
    await message.answer(eply_markup=main_kb(message.from_user.id))

@start_router.message(Command('faq'))
async def cmd_start_2(message: Message):
    await message.answer('Сообщение с инлайн клавиатурой с вопросами', reply_markup=create_qst_inline_kb(questions))

@start_router.callback_query(F.data.startswith('qst_'))
async def cmd_start1(call: CallbackQuery):
    await call.answer()
    qst_id = int(call.data.replace('qst_', ''))
    qst_data = questions[qst_id]
    msg_text = f'Ответ на вопрос {qst_data.get("qst")}\n\n' \
               f'<b>{qst_data.get("answer")}</b>\n\n' \
               f'Выбери другой вопрос:'
    async with ChatActionSender(bot=bot, chat_id=call.from_user.id, action="typing"):
        await asyncio.sleep(2)
        await call.message.answer(msg_text, reply_markup=create_qst_inline_kb(questions))

@start_router.message(Command(commands=["settings", "about"]))
async def univers_cmd_handler(message: Message, command: CommandObject):
    command_args: str = command.args
    command_name = 'settings' if 'settings' in message.text else 'about'
    response = f'Была вызвана команда /{command_name}'
    if command_args:
        response += f' с меткой <b>{command_args}</b>'
    else:
        response += ' без метки'
    await message.answer(response)

@start_router.message(F.text.contains('Профиль'))
async def start_profile(message: Message, state: FSMContext):
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        user_info = await get_user_data(user_id=message.from_user.id)
        profile_message = (
            f"<b>👤 Профиль пользователя:</b>\n"
            f"<b>🆔 ID:</b> {user_info['user_id']}\n"
            f"<b>💼 Логин:</b> @{user_info['user_login']}\n"
            f"<b>📛 Полное имя:</b> {user_info['full_name']}\n"
            f"<b>🧑‍🦰 Пол:</b> {user_info['gender']}\n"
            f"<b>🎂 Возраст:</b> {user_info['age']}\n"
            f"<b>📅 Дата регистрации:</b> {user_info['date_reg']}\n"
            f"<b>📝 О себе:</b> {user_info['about']}\n"
        )

        await message.answer_photo(photo=user_info.get('photo'), caption=profile_message)