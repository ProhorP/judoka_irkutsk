import os
from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
from handlers.start import start_router
from aiogram.filters import Command
from aiogram.types import Message
from create_bot import all_media_dir

@start_router.message(Command('send_audio'))
async def cmd_start(message: Message, state: FSMContext):
    audio_file = FSInputFile(path=os.path.join(all_media_dir, 'ireland rington.mp3'))
    await message.answer_audio(audio=audio_file)

@start_router.message(F.text == 'audio')
async def cmd_start(message: Message, state: FSMContext):
    audio_file = FSInputFile(path=os.path.join(all_media_dir, 'ireland rington.mp3'))
    await message.answer_audio(audio=audio_file)