from pyrogram import filters
from pyrogram.types import Message
from Functions import Admin_handler, ConfigHandler, Ban_Handler, Account_handler 
from config import OWNER_ID

class MyFilters:
    @staticmethod
    async def admin_filter_fn(_, __, message: Message):
        admin_id = message.from_user.id
        admin = await Admin_handler.get_one_admin(admin_id)
        
        if admin_id == OWNER_ID:
            return True
        elif admin and admin.status == "on":
            return True
        else:
            return False
        
    @staticmethod 
    async def bot_on(_, __, meesage: Message):
        config = await ConfigHandler.load_config()
        if config["status"] == "on": 
            return True 
        else: 
            return False 
        
    @staticmethod
    async def not_ban(_, __, message: Message):
        user_id = message.from_user.id
        status = await Ban_Handler.is_banned(user_id)
        if status == True: 
            await message.reply("😓شما بن شدی عزیز دلم")
            return False 
        else: 
            return True
        
    @staticmethod 
    async def self_users(_, __, m: Message): 
        user_id = m.from_user.id 
        users = await Account_handler.get_accounts()
        user_ids = set(acc.creator_id for acc in users)
        if user_id == OWNER_ID: 
            return True 
        elif user_id in user_ids:
            return True 
        else: 
            return False  
        
        
                
    
        
# Create the filter
admins_filter = filters.create(MyFilters.admin_filter_fn)
status_filter = filters.create(MyFilters.bot_on)
not_banned_filter = filters.create(MyFilters.not_ban)
users_filter = filters.create(MyFilters.self_users) 



