import os
from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
# from handlers.start import start_router
from aiogram.filters import Command
from aiogram.filters.state import State, StatesGroup
from aiogram.types import Message
from create_bot import all_media_dir
from keyboards.all_kb import main_kb
from aiogram.utils.chat_action import ChatActionSender
from create_bot import bot
import asyncio
import re
# from handlers.start import start_router as questionnaire_router
from keyboards.all_kb import gender_kb
from keyboards.inline_kbs import get_login_tg, check_data
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
    gender = State()
    age = State()
    full_name = State()
    user_login = State()
    photo = State()
    about = State()
    check_state = State()
    caption = None

# questionnaire_router = Router()
start_router = Router()


@start_router.message(Command('start_questionnaire'))
async def start_questionnaire_process(message: Message, state: FSMContext):
    await state.clear()
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await asyncio.sleep(2)
        await message.answer('Привет. Для начала выбери свой пол: ', reply_markup=gender_kb())
    await state.set_state(Form.gender)


@start_router.message((F.text.lower().contains('мужчина')) | (F.text.lower().contains('женщина')), Form.gender)
async def start_questionnaire_process(message: Message, state: FSMContext):
    await state.update_data(gender=message.text, user_id=message.from_user.id)
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await asyncio.sleep(2)
        await message.answer('Супер! А теперь напиши сколько тебе полных лет: ', reply_markup=ReplyKeyboardRemove())
    await state.set_state(Form.age)


@start_router.message(F.text, Form.gender)
async def start_questionnaire_process(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await asyncio.sleep(2)
        await message.answer('Пожалуйста, выбери вариант из тех что в клавиатуре: ', reply_markup=gender_kb())
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
    text = 'Теперь укажите ваш логин, который будет использоваться в боте'

    if message.from_user.username:
        text += ' или нажмите на кнопку ниже и в этом случае вашим логином будет логин из вашего телеграмм: '
        await message.answer(text, reply_markup=get_login_tg())
    else:
        text += ' : '
        await message.answer(text)

    await state.set_state(Form.user_login)

# вариант когда мы берем логин из профиля телеграмм
@start_router.callback_query(F.data, Form.user_login)
async def start_questionnaire_process(call: CallbackQuery, state: FSMContext):
    await call.answer('Беру логин с телеграмм профиля')
    await call.message.edit_reply_markup(reply_markup=None)
    await state.update_data(user_login=call.from_user.username)
    await call.message.answer('А теперь отправьте фото, которое будет использоваться в вашем профиле: ')
    await state.set_state(Form.photo)


# вариант когда мы берем логин из введенного пользователем
@start_router.message(F.text, Form.user_login)
async def start_questionnaire_process(message: Message, state: FSMContext):
    await state.update_data(user_login=message.from_user.username)
    await message.answer('А теперь отправьте фото, которое будет использоваться в вашем профиле: ')
    await state.set_state(Form.photo)


@start_router.message(F.photo, Form.photo)
async def start_questionnaire_process(message: Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    await state.update_data(photo=photo_id)
    await message.answer('А теперь расскажите пару слов о себе: ')
    await state.set_state(Form.about)


@start_router.message(F.document.mime_type.startswith('image/'), Form.photo)
async def start_questionnaire_process(message: Message, state: FSMContext):
    photo_id = message.document.file_id
    await state.update_data(photo=photo_id)
    await message.answer('А теперь расскажите пару слов о себе: ')
    await state.set_state(Form.about)


@start_router.message(F.document, Form.photo)
async def start_questionnaire_process(message: Message, state: FSMContext):
    await message.answer('Пожалуйста, отправьте фото!')
    await state.set_state(Form.photo)


@start_router.message(F.text, Form.about)
async def start_questionnaire_process(message: Message, state: FSMContext):
    await state.update_data(about=message.text)

    data = await state.get_data()

    caption = f'Пожалуйста, проверьте все ли верно: \n\n' \
              f'<b>Полное имя</b>: {data.get("full_name")}\n' \
              f'<b>Пол</b>: {data.get("gender")}\n' \
              f'<b>Возраст</b>: {data.get("age")} лет\n' \
              f'<b>Логин в боте</b>: {data.get("user_login")}\n' \
              f'<b>О себе</b>: {data.get("about")}'

    await state.update_data(caption=caption)

    await message.answer_photo(photo=data.get('photo'), caption=caption, reply_markup=check_data())
    await state.set_state(Form.check_state)

# сохраняем данные
@start_router.callback_query(F.data == 'correct', Form.check_state)
async def start_questionnaire_process(call: CallbackQuery, state: FSMContext):
    await call.answer('Данные сохранены')
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
    await call.message.answer('Привет. Для начала выбери свой пол: ', reply_markup=gender_kb())
    await state.set_state(Form.gender)