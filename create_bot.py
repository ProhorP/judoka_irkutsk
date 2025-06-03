import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from decouple import config
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from asyncpg_lite import DatabaseManager
from decouple import config

scheduler = AsyncIOScheduler(timezone='Asia/Irkutsk')
admins = [158563881]

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

bot = Bot(token=config('TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

questions = {
    1: {'qst': 'Как записаться на первую тренировку?', 'answer': 'Пройдите регистрацию(нажмите кнопку меню и выберите "Регистрация"), это автоматически запишет вас на первую тренировку. Приходите в подходящую вам группу(расписание смотрите в этом же приложении)'},
    2: {'qst': 'Сколько стоит первая тренировка?', 'answer': 'Бесплатно.'},
    3: {'qst': 'Что с собой взять на первую тренировку?', 'answer': 'Тапочки, футболка, спортивные штаны, ванные принадлежности.'},
    4: {'qst': 'Где взять кимоно?', 'answer': 'Рекомендации по подбору кимоно даст тренер.'},
    5: {'qst': 'Какие группы есть?', 'answer': 'Детская(до 12 лет), взрослая(до 18) и группа здоровья(старше 18).'},
    6: {'qst': 'Расписание группы здоровья?', 'answer': 'Вт Чт 19:00 - 20:30'},
    7: {'qst': 'Номера тренеров', 'answer': 'Карико В.А 89148876075\nАвраменко Л.С 89148734931\nЧувствин Р.В 89836994976\nТайдаков Е.С 89526270135'},
}

all_media_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'all_media')

pg_manager = DatabaseManager(db_url=config('PG_LINK'), deletion_password=config('ROOT_PASS'))
