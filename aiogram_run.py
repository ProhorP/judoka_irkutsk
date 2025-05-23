import asyncio
from create_bot import bot, dp, scheduler
from handlers.start import start_router
from keyboards.all_kb import set_commands
import handlers.media
import handlers.anketa
import db.db
# from work_time.time_func import send_time_msg

async def main():
    await db.db.create_table_users()
    # scheduler.add_job(send_time_msg, 'interval', seconds=10)
    # scheduler.start()
    dp.include_router(start_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    await set_commands()

if __name__ == "__main__":
    asyncio.run(main())