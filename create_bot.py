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

# from db_handler.db_class import PostgresHandler

# pg_db = PostgresHandler(config('PG_LINK'))
scheduler = AsyncIOScheduler(timezone='Asia/Irkutsk')
admins = [158563881,296572025]

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

bot = Bot(token=config('TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

questions = {
    1: {'qst': 'ФИО тренера?', 'answer': 'Хренов Семен Олегович - мастер спорта по дзюдо'},
    2: {'qst': 'Как записаться на первую тренировку?', 'answer': 'После прохождения регистрации выберите "Запись на первую тренировку".'},
    3: {'qst': 'Сколько стоит первая тренировка?', 'answer': 'Бесплатно.'},
    4: {'qst': 'Расписание старшей группы', 'answer': 'Вторник Четверг 20:00 - 21:00'},
    5: {'qst': 'Что с собой взять на первую тренировку?', 'answer': 'Тапочки, спортивная одежда, ванные принадлежности.'},
    6: {'qst': 'Где взять кимоно?', 'answer': 'Рекомендации по подбору кимоно даст тренер.'},
    7: {'qst': 'Где находится клуб??', 'answer': 'После регистрации нажмите "Связаться с нами" - там будет вся информация'},
}

all_media_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'all_media')

pg_manager = DatabaseManager(db_url=config('PG_LINK'), deletion_password=config('ROOT_PASS'))