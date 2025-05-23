import os
from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
from handlers.start import start_router
from aiogram.filters import Command
from aiogram.types import Message
from create_bot import all_media_dir
from keyboards.all_kb import main_kb
from aiogram.utils.chat_action import ChatActionSender
from create_bot import questions, bot
import asyncio

# @start_router.message(Command('send_audio'))
# async def cmd_start(message: Message, state: FSMContext):
#     audio_file = FSInputFile(path=os.path.join(all_media_dir, 'ireland rington.mp3'))
#     await message.answer_audio(audio=audio_file)

# @start_router.message(Command('send_audio'))
# async def cmd_start(message: Message, state: FSMContext):
#     audio_file = FSInputFile(path=os.path.join(all_media_dir, 'ireland rington.mp3'))
#     msg_id = await message.answer_audio(audio=audio_file, reply_markup=main_kb(message.from_user.id),
#                                         caption='Моя <u>отформатированная</u> подпись к <b>файлу</b>')
#     print(msg_id.audio.file_id)

@start_router.message(Command('send_audio'))
async def cmd_start(message: Message, state: FSMContext):
    # audio_file = FSInputFile(path=os.path.join(all_media_dir, 'ireland rington.mp3'))
    audio_id = 'CQACAgIAAxkDAAIBwWgvQhcM1wL3wiqfkDfJ5twCn5E5AAJGeQACgEV4SWbjtTk1t0vCNgQ'
    msg_id = await message.answer_audio(audio=audio_id, reply_markup=main_kb(message.from_user.id),
                                        caption='Моя <u>отформатированная</u> подпись к <b>файлу</b>')

@start_router.message(Command('send_photo'))
async def cmd_start(message: Message, state: FSMContext):
    photo_file = FSInputFile(path=os.path.join(all_media_dir, 'photo.jpg'))
    async with ChatActionSender.upload_photo(bot=bot, chat_id=message.from_user.id):
        await asyncio.sleep(10)
        msg_id = await message.answer_photo(photo=photo_file, reply_markup=main_kb(message.from_user.id),
                                        caption='Моя <u>отформатированная</u> подпись к <b>фото</b>')
        print(msg_id.photo[-1].file_id)