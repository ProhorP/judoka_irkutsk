from aiogram import F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from keyboards.inline_kbs import create_qst_inline_kb, get_inline_reg_kb
from aiogram.filters import CommandStart, Command
from create_bot import questions
from aiogram.types import CallbackQuery
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

    if user_info == None:
        await message.answer('Привет. Запишись на первую тренировку:', reply_markup=get_inline_reg_kb())
        await state.set_state(Form.registration)
    else:
        await message.answer('Привет. Ты зарегистрирован, что тебе нужно?')


@start_router.message(Command('faq'))
async def cmd_start_2(message: Message):
    await message.answer('Какой вопрос вас интересует?', reply_markup=create_qst_inline_kb(questions))


@start_router.callback_query(F.data.startswith('qst_'))
async def cmd_start1(call: CallbackQuery):
    await call.answer()
    qst_id = int(call.data.replace('qst_', ''))
    qst_data = questions[qst_id]
    msg_text = f'Ответ на вопрос "{qst_data.get("qst")}"\n\n' \
               f'<b>{qst_data.get("answer")}</b>\n\n' 
    await call.message.answer(msg_text)
