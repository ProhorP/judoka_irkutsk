
from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

admin_router = Router()

@admin_router.message(F.text.contains('Админ панель'))
async def start_profile(message: Message, state: FSMContext):
    await message.answer('Admin panel activate')