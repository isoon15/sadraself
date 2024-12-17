from pyrogram import Client
import logging
from pyrogram.methods.utilities.idle import idle  
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from Database import get_session, Accounts 
from sqlalchemy import select 
from datetime import datetime, timedelta
from Functions import Ban_Handler 
from config import API_HASH, API_ID, BOT_TOKEN 
import asyncio 
import os , sys
SCRIPT_DIR = str(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(-1,(SCRIPT_DIR))


logging.basicConfig(
    filename="bot.log",
    level=logging.INFO,
    format="Nuoqte | %(asctime)s -> %(message)s",
    datefmt="%Y/%m/%d , %H:%M:%S"
)


plugins = dict(root="plugins")

self_maker = Client("self_maker", 
                    api_id=API_ID, 
                    api_hash=API_HASH, 
                    bot_token=BOT_TOKEN,
                    plugins=plugins)

scheduler = AsyncIOScheduler()

async def update_left_time():
    async with get_session() as session:
        result = await session.execute(select(Accounts))
        accounts = result.scalars().all()
        if not accounts: 
            return 
        for account in accounts:
            if account.left_time > 0:
                account.left_time -= 1
                session.add(account)
        await session.commit()
    logging.info("Left time updated for all accounts")

# Schedule the update job to run daily
scheduler.add_job(update_left_time, 'interval', days=1, start_date=datetime.now() + timedelta(seconds=1))

async def main():
    await Ban_Handler.load_banned_users() 
    print('Ban_Handler.load_banned_users() ')
    await self_maker.start() 
    print('await self_maker.start()')
    scheduler.start()
    print('scheduler.start()')
    await idle()
    print('await idle()')
    await self_maker.stop() 
    print('await self_maker.stop() ')
    

loop = asyncio.get_event_loop()
loop.run_until_complete(main())