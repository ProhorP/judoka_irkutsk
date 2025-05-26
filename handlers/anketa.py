import os
from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.filters.state import State, StatesGroup
from aiogram.types import Message
from keyboards.all_kb import main_kb
from aiogram.utils.chat_action import ChatActionSender
from create_bot import bot
import asyncio
import re
from keyboards.inline_kbs import get_inline_gender_kb, check_data, get_inline_reg_kb
from aiogram.types import CallbackQuery
from aiogram.types import ReplyKeyboardRemove
from db.db import insert_user

def extract_number(text):
    match = re.search(r'\b(\d+)\b', text)
    if match:
        return int(match.group(1))
    else:
        return None
      
class Form(StatesGroup):
    registration = State()
    gender = State()
    age = State()
    full_name = State()
    about = State()
    check_state = State()

start_router = Router()

@start_router.callback_query(F.data, Form.registration)
async def start_questionnaire_process(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.edit_reply_markup(reply_markup=None)
    if call.data == 'yes':
        await state.update_data(user_id=call.from_user.id)
        await state.update_data(user_login=call.from_user.username)
        await call.message.answer('Для начала выбери свой пол: ', reply_markup=get_inline_gender_kb())
        await state.set_state(Form.gender)
    else:
        await call.message.answer('Без регистрации можно узнать только часто задаваемые вопросы.', reply_markup=ReplyKeyboardRemove())


@start_router.callback_query((F.data.contains('Мужчина')) | (F.data.contains('Женщина')), Form.gender)
async def start_questionnaire_process(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup(reply_markup=None)
    await state.update_data(gender=call.data)
    await call.message.answer('Супер! А теперь напиши сколько тебе полных лет: ', reply_markup=ReplyKeyboardRemove())
    await state.set_state(Form.age)


@start_router.callback_query(F.data, Form.gender)
async def start_questionnaire_process(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer(f'Вы ввели: {call.data}', reply_markup=get_inline_gender_kb())
    await call.message.answer('Пожалуйста, выбери вариант из тех что в клавиатуре: ', reply_markup=get_inline_gender_kb())
    await state.set_state(Form.gender)


@start_router.message(F.text, Form.age)
async def start_questionnaire_process(message: Message, state: FSMContext):
    check_age = extract_number(message.text)
    if not check_age or not (1 <= int(message.text) <= 100):
        await message.reply("Пожалуйста, введите корректный возраст (число от 1 до 100).")
        return
    await state.update_data(age=check_age)
    await message.answer('Теперь укажите свое полное имя:')
    await state.set_state(Form.full_name)


@start_router.message(F.text, Form.full_name)
async def start_questionnaire_process(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await message.answer('А теперь расскажите пару слов о себе: ')
    await state.set_state(Form.about)


@start_router.message(F.text, Form.about)
async def start_questionnaire_process(message: Message, state: FSMContext):
    await state.update_data(about=message.text)
    data = await state.get_data()

    caption = f'Пожалуйста, проверьте все ли верно: \n\n' \
              f'<b>Полное имя</b>: {data.get("full_name")}\n' \
              f'<b>Пол</b>: {data.get("gender")}\n' \
              f'<b>Возраст</b>: {data.get("age")} лет\n' \
              f'<b>О себе</b>: {data.get("about")}'

    await message.answer(caption, reply_markup=check_data())
    await state.set_state(Form.check_state)


# сохраняем данные
@start_router.callback_query(F.data == 'correct', Form.check_state)
async def start_questionnaire_process(call: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    await insert_user(user_data)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer('Благодарю за регистрацию. Ваши данные успешно сохранены!',
                              reply_markup=main_kb(call.from_user.id))
    await state.clear()


# запускаем анкету сначала
@start_router.callback_query(F.data == 'incorrect', Form.check_state)
async def start_questionnaire_process(call: CallbackQuery, state: FSMContext):
    await call.answer('Запускаем сценарий с начала')
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer('Привет. Для начала пройди регистрацию:', reply_markup=get_inline_reg_kb())
    await state.set_state(Form.registration)