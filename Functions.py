from Database import ( Accounts, USER_STATUS, get_session, Config, Admins,
                      Backup_messages, Banned_Accounts, Banned_Numbers)
from sqlalchemy import sql, select, insert, update, delete 
from sqlalchemy.exc import IntegrityError, SQLAlchemyError 
import os
from pyrogram import Client 
from pyrogram.types import Message 
from fabric import Connection, task 
import asyncio 
from concurrent.futures import ThreadPoolExecutor
import shutil
import requests 
import time 
import string
from config import OWNER_ID
import json 
from Database import TrackingCode 
import random
from textwrap import dedent 
import logging
from pyrogram.enums import ChatType
from pyrogram.types import Message, Chat, User
import json

def serialize_message(message: Message) -> dict:
    return {
        "message_id": message.id,
        "chat_id": message.chat.id,
        "text": message.text,
        "date": message.date.isoformat() if message.date else None,
        # Add other fields as needed
    }



admin_id = 1463788237

class Account_handler(): 
    @staticmethod
    async def add_account(creator_id: int, api_id: int, api_hash: str, phone_number: str, session_name: str, directory: str, server_ip: str, server_user_name: str, server_pass: str, left_time: int) -> bool:
        async with get_session() as session:  # Ensure get_session() returns an async context manager for the session
            try:
                account = await session.execute(
                    select(Accounts).where(Accounts.phone_number == phone_number)
                )
                account = account.scalars().first()
                print(account)

                if account:
                    print("Account already exists")
                else:
                    await session.execute(
                        insert(Accounts).values(
                            creator_id=creator_id,
                            api_id=api_id,
                            api_hash=api_hash,
                            phone_number=phone_number,
                            session_name=session_name,
                            directory=directory,
                            server_ip=server_ip,
                            server_user_name=server_user_name,
                            server_pass=server_pass,
                            left_time=left_time
                        )
                    )
                    await session.commit()
                    print("Account added successfully")
                    return True

            except IntegrityError as e:
                await session.rollback()
                print("Integrity error occurred:", str(e))
                return None

            except SQLAlchemyError as e:
                await session.rollback()
                print("An error occurred:", str(e))
                return None

            except Exception as e:
                print(f"Error in add_account: {e}")
                return None

    @staticmethod
    async def delete_account(phone_number: str) -> bool:
        async with get_session() as session:
            try:
                account = await session.execute(
                    sql.select(Accounts).where(Accounts.phone_number==phone_number)
                ) 
                account = account.scalars().first() 

                if account:
                    session_file = f"{account.session_name}.session"
                    session_journal_file = f"{account.session_name}.session-journal"
                    zip_file = f"{phone_number}.zip"
                    bot_directory = f"new_bot_{phone_number}"
                    
                    items_to_remove = [session_file, session_journal_file, zip_file, bot_directory]
                    
                    for i in items_to_remove: 
                        if os.path.exists(i): 
                            if os.path.isfile(i):
                                os.remove(i) 
                                
                            elif os.path.isdir(i): 
                                shutil.rmtree(i) 
                                print("directory deleted")
                        else:
                            logging.info(f"{i} does not exist")
                            
                    # Delete the account if it exists
                    await session.delete(account)
                    await session.commit()
                    # system("clear")
                    print("Account deleted successfully")
                    return True
                else:
                    # system("clear")
                    print("Account not found")
                    return False

            except SQLAlchemyError as e:
                # Rollback the session in case of SQLAlchemy errors
                await session.rollback()
                # Print the exception details
                print("An error occurred:", str(e))
                return False 
            except Exception as e: 
                logging.error(f"error in deleting account: {e}")

    @staticmethod
    async def update_account(phone_number: str, **kwargs) -> bool:
        async with get_session() as session:
            try:
                account = await session.execute(
                    sql.select(Accounts).where(Accounts.phone_number == phone_number)
                )
                account = account.scalars().first()

                if not account:
                    print("Account does not exist")
                    return False

                for key, value in kwargs.items():
                    setattr(account, key, value)

                await session.commit()
                print("Account updated successfully")
                return True

            except SQLAlchemyError as e:
                await session.rollback()
                print("An error occurred:", str(e))
                return False
            except Exception as e:
                print(f"Error in update_account: {e}")
                return False

    @staticmethod
    async def check_account(phone_number: str) -> bool:
        async with get_session() as session:
            try:
                user = await session.execute(
                    select(Accounts).where(Accounts.phone_number==phone_number)
                )
                user = user.scalars().first() 
                if user:
                    return True
                else:
                    return False

            except IntegrityError as e:
                await session.rollback()
                print("Integrity error occurred in check_account:", str(e))

            except SQLAlchemyError as e:
                await session.rollback()
                print("An error occurred in check_account:", str(e))

            finally:
                await session.close()

    @staticmethod
    async def get_one_account(phone_number: str) -> str:
        async with get_session() as session: 
            try: 
                account = await session.execute(
                    select(Accounts).where(Accounts.phone_number==phone_number)
                )
                account = account.scalars().first() 
                
                return account 
            except Exception as e: 
                print(f"error happened in get_one_account: {e}")
            

    @staticmethod
    async def get_accounts():
        async with get_session() as session:
            try:
                accounts = await session.execute(
                    select(Accounts)
                )
                accounts = accounts.scalars().all()
                return accounts

            except Exception as e:
                print(f"Error happened in get_accounts: {e}")
            
class User : 
    
    @staticmethod
    async def add_user(user_id, step, user_name):
        try:
            async with get_session() as session:

                # Check if the user exists in the database
                user = await session.execute(
                    select(USER_STATUS).where(USER_STATUS.user_id == user_id)
                )
                user = user.scalars().first()
                if user:
                    # If the user exists, update the step
                    user.step = step
                    print(f"User exists with user_id = {user_id}")
                    status = "exist"
                else:
                    # If the user doesn't exist, create a new user
                    await session.execute(
                        insert(USER_STATUS).values(
                            user_id = user_id, 
                            step = step, 
                            user_name = user_name
                        )
                    ) 
                    print(f"New user created with ID {user_id}")
                    status = "not_exist"

                # Commit the changes to persist the updates in the database
                await session.commit()

                return status

        except SQLAlchemyError as e:
            print(f"SQLAlchemy error occurred in add_user: {e}")
            return "error"

    @staticmethod
    async def update_del_message(user_id: int, message: Message):
        async with get_session() as session:
            try:
                # Fetch the user
                user = await session.execute(
                    select(USER_STATUS).where(USER_STATUS.user_id == user_id)
                )
                user = user.scalars().first()
                if user:
                    # Serialize the message object
                    serialized_message = serialize_message(message)
                    if user.del_messages is None :
                        user.del_messages = [serialized_message]
                    elif not user.del_messages:
                        user.del_messages = [serialized_message]
                    else:
                        # Check for duplicate message
                        if any(msg["message_id"] == message.id for msg in user.del_messages):
                            return 
                        else: 
                            user.del_messages.append(serialized_message)

                    await session.commit()
                    return True
                else:
                    print(f"User with user_id = {user_id} not found")
                    return False

            except SQLAlchemyError as e:
                print(f"SQLAlchemy error occurred in update_del_message: {e}")
                logging.error(f"SQLAlchemy error occurred in update_del_message: {e}")
                await session.rollback()
                return False

    @staticmethod
    async def get_del_messages(user_id: int):
        async with get_session() as session:
            try:
                # Fetch the user
                user = await session.execute(
                    select(USER_STATUS).where(USER_STATUS.user_id == user_id)
                )
                user = user.scalars().first()
                if user:
                    return user.del_messages
                else:
                    print(f"User with user_id = {user_id} not found")
                    return None

            except SQLAlchemyError as e:
                print(f"SQLAlchemy error occurred in get_del_messages: {e}")
                logging.error(f"SQLAlchemy error occurred in get_del_messages: {e}")
                return None

    @staticmethod
    async def revoke_del_message(user_id: int, message_id):
        async with get_session() as session:
            try:
                result = await session.execute(
                    select(USER_STATUS).where(USER_STATUS.user_id == user_id)
                )
                result = result.scalars().first()
                if result and result.del_messages is not None:
                    result.del_messages = [
                        msg for msg in result.del_messages if msg["message_id"] != message_id
                    ]
                    await session.commit()

            except Exception as e:
                logging.error(f"Error in revoking del_messages: {e}")
                await session.rollback()
                
    @staticmethod
    async def delete_message(c, del_messages, user_id):
        if isinstance(del_messages, list):
            print(type(del_messages))  # Should print <class 'list'>
            # Iterate through the list of messages
            for msg in del_messages:
                # Ensure each item is a dictionary and has the required keys
                if isinstance(msg, dict) and "chat_id" in msg and "message_id" in msg:
                    try:
                        # Delete the message
                        await c.delete_messages(msg["chat_id"], msg["message_id"])
                        print(f"Deleted message {msg['message_id']} from chat {msg['chat_id']}")
                        await User.revoke_del_message(user_id, msg["message_id"])
                        return True
                    except Exception as e:
                        print(f"Error deleting message {msg['message_id']} from chat {msg['chat_id']}: {e}")
                        result = False 
                else:
                    print(f"Invalid message format: {msg}")
                    result = False 
        else:
            print(f"Invalid del_messages format: {del_messages}")
            result = False 
            
        return result 

    # @staticmethod
    # async def get_message_ids_and_chat_ids(user_id: int):
    #     messages = await User.get_del_messages(user_id)
    #     if messages:
    #         return [(msg["message_id"], messages["chat_id"]) for msg in messages]
    #     return []
                



    @staticmethod
    async def update_step(user_id: int, step: str)->bool:
        try: 
            async with get_session() as session:
                result = await session.execute(
                        update(USER_STATUS)
                        .where(USER_STATUS.user_id == user_id)
                        .values(step=step)
                    )

                if result.rowcount > 0:
                    await session.commit()  # Commit the transaction
                    print(f"Step updated for user {user_id}")
                    return True
                else:
                    print(f"No user found with id {user_id}")
                    return False

        except SQLAlchemyError as e:
            print(f"SQLAlchemy error occurred in update_step: {e}")


    @staticmethod
    async def get_step(user_id):
        try:
            async with get_session() as session: 
                user = await session.execute(
                    select(USER_STATUS).where(USER_STATUS.user_id == user_id)
                )
                user = user.scalars().first() 

                if user:
                    # If the user exists, retrieve the step
                    step = user.step
                    print(f"Step for user {user_id} is {step}")
                    return step

        except SQLAlchemyError as e:
            print(f"SQLAlchemy error occurred in get_step: {e}")
            
    @staticmethod
    async def get_users(): 
        async with get_session() as session: 
            try: 
                users = await session.execute(
                    select(USER_STATUS)
                )
                users = users.scalars().all() 
                
                return users 
            
            except Exception as e: 
                print(f"error happened in get_users is : {e}")
        
            
            
class Code_handler: 
    @staticmethod
    async def generate_tracking_code(length=6):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
    
    @staticmethod
    async def create_tracking_code(user_id: int):
        async with get_session() as session:
            # Check if the user has already made a request within the last day
            yesterday = time.time() - 86400
            existing_user = await session.execute(
                select(TrackingCode).filter(
                    TrackingCode.user_id == user_id
            )) 
            existing_user = existing_user.scalars().first() 
            
            if existing_user:
                existing_code = await session.execute(
                    select(TrackingCode).filter(
                        TrackingCode.user_id == user_id,
                        TrackingCode.timestamp > yesterday
                    )
                )
                if existing_code.scalars().first():
                    return None

            tracking_code = await Code_handler.generate_tracking_code()
            confirmation_code = await  Code_handler.generate_tracking_code()
            timestamp = int(time.time())

            new_code = TrackingCode(
                user_id=user_id,
                tracking_code=tracking_code,
                confirmation_code=confirmation_code,
                timestamp=timestamp
            )
            session.add(new_code)
            await session.commit()
            return tracking_code, confirmation_code
        
        
    @staticmethod 
    async def is_code_valid(user_id, confirmation_code: str, validity_period=86400):
        async with get_session() as session:
            record = await session.execute(
                select(TrackingCode).filter(
                    TrackingCode.user_id == user_id, 
                    TrackingCode.confirmation_code == confirmation_code
                )
            )
            tracking_record = record.scalars().first()
            if tracking_record:
                if time.time() - tracking_record.timestamp <= validity_period:
                    return True
                else: 
                    return None 
        return False
    
    @staticmethod 
    async def get_info(c: Client, user_id): 
        async with get_session() as session:
            try: 
                record = await session.execute(
                    select(TrackingCode).where(TrackingCode.user_id == user_id)
                )
                
                record = record.scalars().first() 
                yesterday = time.time() - 86400 
                if record and record.timestamp < yesterday: 
                    await session.execute(
                        delete(TrackingCode).where(
                            TrackingCode.user_id == user_id 
                        )
                    )
                    await session.commit()  
                    
                return record 
            
            except Exception as e: 
                error_text = f"""
                در قسمت گرفتن اطلاعات کد رهگیری از دیتابیس خطایی رخ داد.
                {e}
                """
                await c.send_message(admin_id, text=error_text)
                return  

class ConfigHandler:
    
    @staticmethod
    async def load_config():
        config = {}
        async with get_session() as session:
            try:
                config_entries = await session.execute(select(Config))
                config_entries = config_entries.scalars().all()
                for entry in config_entries:
                    config[entry.key] = entry.value
            except Exception as e:
                print(f"Error loading config: {e}")
        return config

            

    @staticmethod
    async def save_config(config):
        async with get_session() as session:
            try:
                for key, value in config.items():
                    entry = await session.execute(select(Config).filter_by(key=key))
                    entry = entry.scalars().first()
                    if entry:
                        entry.value = value
                    else:
                        await session.execute(
                            insert(Config).values(key=key, value=value)
                        )
                await session.commit()
            except Exception as e:
                await session.rollback()
                print(f"Error saving config: {e}")
            finally:
                await session.close()
                print("session closed in save_cionfig")

            
        
    @staticmethod
    async def update_status(key: str, value: str):
        async with get_session() as session:
            try: 
                print(f"in update status and key is {key} value is {value}")
                result = await session.execute(select(Config).filter_by(key=key)) 
                config = result.scalar_one_or_none()
                print(config)
                if config != None:
                    config.value = value
                    await session.commit() 
                else:
                    await session.execute(
                        insert(Config).values(key=key, value=value)
                    )
                    await session.commit()
                return True 
            except Exception as e: 
                return e 
            
class Admin_handler:
    @staticmethod
    async def check_admin(admin_id): 
        async with get_session() as session: 
            try: 
                existence = await session.execute(
                    select(Admins).where(Admins.admin_id==admin_id)
                )
                existence = existence.scalars().first() 
                if existence != None: 
                    return True 
                
                elif admin_id == OWNER_ID: 
                    return True 
                
                else: 
                    return False 
            except Exception as e: 
                print(f"error in check admin is: {e}")
                
    @staticmethod            
    async def add_admin(admin_id: int, admin_user_name: str, status: str):
        async with get_session() as session:
            try: 
                new_admin = await session.execute(
                    insert(Admins).values(admin_id=admin_id, admin_user_name=admin_user_name, status=status)
                )
                await session.commit()
                return True 
            except Exception as e: 
                print(f"error in add_admin is: {e}")
                return False 

    @staticmethod
    async def delete_admins():
        async with get_session() as session:
            try:
                await session.execute(
                    delete(Admins)
                )
                await session.commit()
                return True
            except Exception as e:
                print(f"error in delete_admins is {e}") 
                return False 
            
    @staticmethod
    async def get_admins():
        async with get_session() as session:
            result = await session.execute(
                select(Admins)
            )
            admins = result.scalars().all()
            print(admins)
            return admins
    
    @staticmethod
    async def update_status_admin(admin_id: int, new_status: str):
        async with get_session() as session:
            try:
                admin = await session.execute(
                    update(Admins).
                    where(Admins.admin_id==admin_id).
                    values(status=new_status)
                )
                await session.commit() 
                return True 
            except Exception as e:
                print(f"error in update_status_admin is: {e}")
                return False
            
    @staticmethod  
    async def get_one_admin(admin_id): 
        async with get_session() as session:
            try:

                admin = await session.execute(
                    select(Admins).where(Admins.admin_id == admin_id)
                )
                admin = admin.scalars().first() 
                return admin 
            except Exception as e:
                print(f"error in get_one_admin is {e}")
                return None
            
    @staticmethod
    async def delete_one_admin(admin_id):
        async with get_session() as session: 
            try: 
                result = await session.execute(
                    delete(Admins).where(Admins.admin_id == admin_id)
                ) 
                await session.commit() 
                return True 
            except Exception as e: 
                print(f"error in delete_one_admin is: {e}")
                
                
class Server_Handler: 
    
    @staticmethod
    async def setup_and_run(server_ip, server_user_name, server_password, venv_name, local_path, phone_number):
        try:
            with Connection(
                host=server_ip,
                user=server_user_name,
                connect_kwargs={"password": server_password},
            ) as conn:
                # Create virtual environment
                conn.run(f"python3 -m venv {venv_name}", hide=False)
                print("Virtual environment created.")
                
                # Activate virtual environment
                venv_activate = f"source {venv_name}/bin/activate"
                
                # Zip the local directory
                result = os.system(f"zip -r {phone_number}.zip {local_path}")
                print(result)
                zip_file = f"{phone_number}.zip"
                file_name = local_path.split("/")[-1]
                print("Local directory zipped.")
                
                # Upload the zip file to bashupload.com
                with open(zip_file, 'rb') as f:
                    response = requests.post('https://bashupload.com', files={'file': f})
                download_url = response.text.splitlines()[5].replace("wget ", "")
                print(f"File uploaded. Download URL: \n{download_url}")
                zipped_file_name = download_url.split("/")[-1]
                
                # Combine commands into one call
                commands = f"""
                    wget {download_url} &&
                    unzip {zipped_file_name} &&
                    rm -rf {zipped_file_name} &&
                    tmux new-session -d -s main &&
                    tmux send-keys -t main '{venv_activate}' C-m&&
                    tmux send-keys -t main 'cd {local_path}' C-m && 
                    tmux send-keys -t main 'pip3 install -r requirements.txt' C-m && 
                    tmux send-keys -t main 'python3 main.py' C-m 
                """
                conn.run(commands, hide=False)
                print("All commands executed successfully.")

                # Check if the processes are running
                check_process = conn.run("tmux ls", hide=False)
                print(check_process.stdout)

                return True
        except Exception as e:
            logging.error(f"An error occurred in setup and run: {e}")
            return e

    @staticmethod
    def fetch_logs(server_ip, server_user_name, server_password, log_file_path):
        try:
            with Connection(
                host=server_ip,
                user=server_user_name,
                connect_kwargs={"password": server_password},
            ) as conn:
                result = conn.run(f"cat {log_file_path}", hide=True)
                return result.stdout
        except Exception as e:
            logging.error(f"An error occurred while fetching logs: {e}")
            return str(e)

        
    @staticmethod
    async def deploy_to_server(ac_info: dict):
        SERVER_IP = ac_info["server_ip"]
        USERNAME = ac_info["server_username"]
        PASSWORD = ac_info["server_password"]
        PHONE_NUMBER = ac_info["phone_number"]
        VENV_NAME = "myenv"
        TMUX_SESSION = "mytmuxsession"
        LOCAL_PATH = f"./new_bot_{ac_info['phone_number']}" 

        result = await Server_Handler.setup_and_run(
                                     server_ip=SERVER_IP, 
                                     phone_number=PHONE_NUMBER, 
                                     local_path=LOCAL_PATH, 
                                     server_password=PASSWORD, 
                                     server_user_name=USERNAME, 
                                     venv_name=VENV_NAME)
        return result 
    
    
    @staticmethod 
    # Function to run the bot after getting server info
    async def run_bot(ac_info: dict):
        try:
            current_dir = os.getcwd()
            src_dir = os.path.join(current_dir, "self_bot")
            dest_dir = os.path.join(current_dir, f"new_bot_{ac_info['phone_number']}")
            session_dir = os.path.join(current_dir, f"{ac_info['phone_number']}.session")

            shutil.copytree(src_dir, dest_dir)
            print("new self bot folder created!") 
            shutil.move(session_dir, dest_dir)

            config_py_path = os.path.join(dest_dir, "config.py")
            with open(config_py_path, "r") as file:
                filedata = file.read()

            filedata = filedata.replace("API_ID =", f"API_ID = {ac_info['api_id']}")
            filedata = filedata.replace("API_HASH =", f"""API_HASH = "{ac_info['api_hash']}" """)
            filedata = filedata.replace("SESSION_NAME =", f"""SESSION_NAME = "{ac_info['phone_number']}" """)

            with open(config_py_path, "w") as file:
                file.write(filedata)

            # Deploy the new bot to the server using Fabric
            deploy = await Server_Handler.deploy_to_server(ac_info)
            if deploy == True:  
                print("Bot has been successfully deployed to the server.")
                return True 
            else: 
                print(f"خطا!!\n{deploy}")
                return False 

        except Exception as e:
            print(f"خطا در بخش run_bot {e}")
            return e  
        
    @staticmethod
    def remove_privious_server(server_ip, server_user_name, server_password, 
                               tmux):
        try: 
            with Connection(
                host=server_ip, 
                user=server_user_name, 
                connect_kwargs={"password": server_password}
            ) as conn: 
                conn.run(f"tmux kill-session -t {tmux}") 
                print("session killed in the privious server. deploying on new one ......")
                
                return True 
        except Exception as e: 
            print(f"error happened in renewing server: {e} ")
            return e 
        
    @staticmethod 
    async def renewing_server(info: dict, phone_number: str):
        server_ip = info["server_ip"] 
        server_name = info["server_username"] 
        server_password = info["server_password"] 
        
        account = await Account_handler.get_one_account(phone_number) 
        current_ip = account.server_ip 
        current_user_name = account.server_user_name
        current_password = account.server_pass
        session_name = account.session_name 
        TMUX_SESSION = f"mytmuxsession"
        VENV_NAME = "myenv"
        LOCAL_PATH = f"./new_bot_{phone_number}"
                
        remove_result = Server_Handler.remove_privious_server(
                                              server_ip=current_ip, 
                                              server_user_name=current_user_name, 
                                              server_password=current_password, 
                                              tmux=TMUX_SESSION)
        adding_result = Server_Handler.setup_and_run(
                                     local_path=LOCAL_PATH, 
                                     phone_number=phone_number, 
                                     server_ip=server_ip, 
                                     server_password=server_password, 
                                     server_user_name=server_name, 
                                     tmux=TMUX_SESSION, 
                                     venv_name=VENV_NAME, 
                                     )
        return remove_result, adding_result 
        
    @staticmethod 
    async def terminate_account(phone_number: str):
        account = await Account_handler.get_one_account(phone_number)
        
        def terminate():
            TMUX_SESSION = f"main"
            with Connection(
                host=account.server_ip,
                user=account.server_user_name,
                connect_kwargs={"password": account.server_pass}
            ) as conn: 
                try: 
                    session = conn.run(f"tmux has-session -t {TMUX_SESSION}", warn=True)
                    if session.failed:
                        print(f"tmux session {TMUX_SESSION} does not exist.")
                        return None 
                    
                    conn.run(f"tmux kill-session -t {TMUX_SESSION}")
                    print("session killed in the previous server.")
                    
                    return True
            
                except Exception as e:
                    return e
        
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as pool:
            result = await loop.run_in_executor(pool, terminate)
        return result
        
            
class Backup_Handler:
    @staticmethod 
    async def add_message(user_id: int, message_id: int, chat_id: int, message_text: str): 
        async with get_session() as session: 
            try:
                account = await session.execute(
                    select(Backup_messages).where(Backup_messages.user_id == user_id) 
                )
                
                account = account.scalars().first() 
                
                if account: 
                    return False 
                else:
                    await session.execute(
                        insert(Backup_messages).values(
                            user_id=user_id, 
                            message_id=message_id, 
                            chat_id=chat_id, 
                            message_text=message_text
                        )
                    )
                    await session.commit()
                    return True
            
            except Exception as e: 
                logging.error(f"error in adding backup_message \n {e}")
                return e 
    
    @staticmethod 
    async def get_message(user_id: int):
        async with get_session() as session: 
            try: 
                account = await session.execute(
                    select(Backup_messages).where(Backup_messages.user_id==user_id)
                )
                
                account = account.scalars().first() 
                
                if account: 
                    return account 
                else: 
                    return None 
                
            except Exception as e: 
                logging.error(f"error in getting backup_message \n {e}")
                return e 
                
        
    @staticmethod 
    async def delete_request(user_id):
        async with get_session() as session: 
            try:
                await session.execute(
                    delete(Backup_messages).where(Backup_messages.user_id == user_id)
                )
                await session.commit() 
                return True 
                
            except Exception as e: 
                logging.error(f"error in removing backup request \n {e}")
                return e 
            
class Ban_Handler:  
    # In-memory cache to store banned user IDs
    banned_users_cache = set()

    @staticmethod
    async def load_banned_users():
        """Load banned users from the database into the cache."""
        async with get_session() as session:
            try:
                result = await session.execute(select(Banned_Accounts.user_id))
                Ban_Handler.banned_users_cache = {row[0] for row in result.fetchall()}
                logging.info("Banned users loaded into cache")
            except Exception as e:
                logging.error(f"Error loading banned users: {e}")

    @staticmethod
    async def ban_account(user_id):
        """Ban a user by adding them to the database and updating the cache."""
        if user_id in Ban_Handler.banned_users_cache:
            return None  # User is already banned

        async with get_session() as session:
            try:
                target = await session.execute(
                    select(Banned_Accounts).where(Banned_Accounts.user_id == user_id)
                )
                target = target.scalars().first()

                if not target:
                    await session.execute(
                        insert(Banned_Accounts).values(user_id=user_id)
                    )
                    await session.commit()
                    Ban_Handler.banned_users_cache.add(user_id)  # Update the cache
                    return True
                else:
                    return None

            except Exception as e:
                logging.error(f"Error in ban_account: {e}")
                return e

    @staticmethod
    async def un_ban_account(user_id):
        """Unban a user by removing them from the database and updating the cache."""
        if user_id not in Ban_Handler.banned_users_cache:
            return None  # User is not banned

        async with get_session() as session:
            try:
                await session.execute(
                    delete(Banned_Accounts).where(Banned_Accounts.user_id == user_id)
                )
                await session.commit()
                Ban_Handler.banned_users_cache.discard(user_id)  # Update the cache
                return True

            except Exception as e:
                logging.error(f"Error in un_ban_account: {e}")
                return e

    @staticmethod
    async def get_banned_accounts():
        """Return the list of banned user IDs from the cache."""
        return list(Ban_Handler.banned_users_cache)

    @staticmethod
    async def is_banned(user_id) -> bool :
        """Check if a user is banned using the cache."""
        return user_id in Ban_Handler.banned_users_cache
            
    @staticmethod 
    async def ban_number(phone_number): 
        async with get_session() as session: 
            try: 
                target = await session.execute(
                    select(Banned_Numbers).where(Banned_Numbers.phone_number == phone_number)
                )
                
                target = target.scalars().first() 
                
                if not target:
                    await session.execute(
                        insert(Banned_Numbers).values(
                            phone_number=phone_number
                        )
                    )
                    
                    await session.commit() 
                    return True 
                else: 
                    return None 
            except Exception as e: 
                logging.error(f"error in ban_number: {e}")
                return e 
            
    
    @staticmethod         
    async def un_ban_number(phone_number): 
        async with get_session() as session: 
            try: 
                target = await session.execute(
                    select(Banned_Numbers).where(Banned_Numbers.phone_number == phone_number)
                ) 
                
                target = target.scalars().first() 
                
                if not target: 
                    return None 
                
                else: 
                    await session.execute(
                        delete(Banned_Numbers).where(Banned_Numbers.phone_number == phone_number)
                    )
                    
                    await session.commit()
                    return True  
                
            except Exception as e: 
                logging.error(f"error in un ban number: {e}") 
                return e  
            
            
            
    @staticmethod 
    async def get_banned_numbers():
        async with get_session() as session: 
            try: 
                banned_numbers = await session.execute(
                    select(Banned_Numbers)
                )
                
                banned_numbers = banned_numbers.scalars().all() 
                
                return banned_numbers 
            except Exception as e: 
                logging.error(f"error in get_Banned_Numbers: {e}")
                return e 
        
        
        
                
            