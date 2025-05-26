
from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from create_bot import admins
from keyboards.all_kb import main_kb, admin_kb
from aiogram.filters.state import State, StatesGroup
from aiogram.types import CallbackQuery
import asyncio
from aiogram.utils.chat_action import ChatActionSender
from create_bot import bot
from aiogram.types import ReplyKeyboardRemove
from keyboards.inline_kbs import get_inline_gender_kb, check_data, get_inline_notify_kb
from db.db import get_user_data

admin_router = Router()


@admin_router.message((F.text.contains('Админ панель')) & (F.from_user.id.in_(admins)))
async def start_profile(message: Message, state: FSMContext):
    await message.answer('Admin panel activate', reply_markup=admin_kb())


@admin_router.message(F.text == 'На главную')
async def send_back_home(message: Message):
    await message.answer('Главная страница', reply_markup=main_kb(message.from_user.id))

      
class Notify(StatesGroup):
    registration = State()
    photo = State()
    caption = State()
    check_state = State()


@admin_router.message(F.text.contains('Сделать рассылку'))
async def start_profile(message: Message, state: FSMContext):
    await message.answer('Вы действительно хотите написать пост?: ', reply_markup=get_inline_notify_kb())
    await state.set_state(Notify.registration)


@admin_router.callback_query(F.data, Notify.registration)
async def start_notify(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup(reply_markup=None)
    await state.clear()
    if call.data == 'yes':
        await call.message.answer('Приложите фото поста', reply_markup=ReplyKeyboardRemove())
        await state.set_state(Notify.photo)


@admin_router.message(F.photo, Notify.photo)
async def start_notify(message: Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    await state.update_data(photo=photo_id)
    await message.answer('Напишите описание поста: ')
    await state.set_state(Notify.caption)


@admin_router.message(F.document.mime_type.startswith('image/'), Notify.photo)
async def start_notify(message: Message, state: FSMContext):
    photo_id = message.document.file_id
    await state.update_data(photo=photo_id)
    await message.answer('Напишите описание поста: ')
    await state.set_state(Notify.caption)


@admin_router.message(F.document, Notify.photo)
async def start_notify(message: Message, state: FSMContext):
    await message.answer('Пожалуйста, отправьте фото!')
    await state.set_state(Notify.photo)


@admin_router.message(F.text, Notify.caption)
async def start_notify(message: Message, state: FSMContext):
    await state.update_data(caption=message.text)
    data = await state.get_data()
    await message.answer_photo(photo=data.get('photo'), caption=data.get("caption"), reply_markup=check_data())
    await state.set_state(Notify.check_state)


# отправляем пост
@admin_router.callback_query(F.data == 'correct', Notify.check_state)
async def start_notify(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup(reply_markup=None)
    data = await state.get_data()
    users = await get_user_data()
    for user in users:
        try:
            await bot.send_photo(chat_id=user.get("user_id"), photo=data.get('photo'), caption=data.get('caption'))
        except:
            None

    await call.message.answer('Пост отправлен', reply_markup=admin_kb())
    await state.clear()


# запускаем написание поста заново 
@admin_router.callback_query(F.data == 'incorrect', Notify.check_state)
async def start_notify(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup(reply_markup=None)
    await call.answer('Запускаем сценарий с начала')
    await call.message.answer('Вы действительно хотите написать пост?: ', reply_markup=get_inline_notify_kb())
    await state.set_state(Notify.registration)