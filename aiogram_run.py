import asyncio
from create_bot import bot, dp
from handlers.start import start_router
from keyboards.all_kb import set_commands
import handlers.anketa
import db.db

async def main():
    await db.db.create_table_users()
    dp.include_router(start_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    await set_commands()

if __name__ == "__main__":
    asyncio.run(main())