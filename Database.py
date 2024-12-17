import logging
from sqlalchemy.ext.asyncio import AsyncAttrs, create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import sqltypes
import asyncio
from contextlib import asynccontextmanager


# Define your models
class Model(AsyncAttrs, DeclarativeBase):
    __table_args__ = {"mysql_engine": "InnoDB"}

    def __repr__(self) -> str:
        return "{}({})".format(
            self.__class__.__qualname__,
            ", ".join(f"{k}={getattr(self, k, None)}" for k in self.__table__.columns.keys()),
        )

class Accounts(Model):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(sqltypes.Integer, primary_key=True, autoincrement=True)
    creator_id: Mapped[int] = mapped_column(sqltypes.BigInteger, nullable=False)
    api_id: Mapped[int] = mapped_column(sqltypes.BigInteger, nullable=False)
    api_hash: Mapped[str] = mapped_column(sqltypes.Text, nullable=False)
    phone_number: Mapped[str] = mapped_column(sqltypes.Text, nullable=False, unique=True)
    session_name: Mapped[str] = mapped_column(sqltypes.Text, nullable=False)
    directory: Mapped[str] = mapped_column(sqltypes.Text, nullable=False)
    server_ip: Mapped[str] = mapped_column(sqltypes.Text, nullable=False) 
    server_user_name: Mapped[str] = mapped_column(sqltypes.Text, nullable=False) 
    server_pass: Mapped[str] = mapped_column(sqltypes.Text, nullable=False) 
    # I choosed the left time based on remainig days 
    left_time: Mapped[int] = mapped_column(sqltypes.BigInteger, nullable=False) 
    
     
    
class USER_STATUS(Model):
    __tablename__ = "user_status"

    user_id: Mapped[int] = mapped_column(sqltypes.Integer, primary_key=True, autoincrement=True)
    step: Mapped[int] = mapped_column(sqltypes.Text, nullable=False)
    user_name: Mapped[str] = mapped_column(sqltypes.VARCHAR(32), nullable=False)
    del_messages: Mapped[str] = mapped_column(sqltypes.JSON, nullable=True)
    
    
class Main_self(Model): 
    __tablename__ = "main_self"
    id: Mapped[int] = mapped_column(sqltypes.Integer, primary_key=True, autoincrement=True)
    api_id: Mapped[int] = mapped_column(sqltypes.Integer, nullable=False)
    api_hash: Mapped[str] = mapped_column(sqltypes.Text, nullable=False)
    phone_number: Mapped[str] = mapped_column(sqltypes.Text, nullable=False, unique=True)
    session_name: Mapped[str] = mapped_column(sqltypes.Text, nullable=False)

class Admins(Model):
    __tablename__ = "admins"

    id: Mapped[int] = mapped_column(sqltypes.Integer, primary_key=True, autoincrement=True)
    admin_id: Mapped[int] = mapped_column(sqltypes.BigInteger, nullable=False)
    admin_user_name: Mapped[str] = mapped_column(sqltypes.Text, nullable=False)
    status: Mapped[str] = mapped_column(sqltypes.Text, nullable=False, default="on")
    
class TrackingCode(Model):
    __tablename__ = "tracking_codes"

    id: Mapped[int] = mapped_column(sqltypes.Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(sqltypes.BigInteger, nullable=False)
    tracking_code: Mapped[str] = mapped_column(sqltypes.VARCHAR(32), nullable=False, unique=True)
    confirmation_code: Mapped[str] = mapped_column(sqltypes.VARCHAR(32), nullable=False)
    timestamp: Mapped[int] = mapped_column(sqltypes.Integer, nullable=False)

class Config(Model):
    __tablename__ = "config"
    id: Mapped[int] = mapped_column(sqltypes.Integer, primary_key=True, autoincrement=True)
    key = mapped_column(sqltypes.Text, nullable=False)
    value = mapped_column(sqltypes.Text, nullable=False)
    
class Backup_messages(Model):
    __tablename__ = "backup_messages"
    id: Mapped[int] = mapped_column(sqltypes.Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(sqltypes.BigInteger, nullable=False)
    message_id: Mapped[int] = mapped_column(sqltypes.BigInteger, nullable=False)
    chat_id: Mapped[int] = mapped_column(sqltypes.BigInteger, nullable=False) 
    message_text: Mapped[str] = mapped_column(sqltypes.Text, nullable=True) 
    
    
class Banned_Accounts(Model):
    __tablename__ = "banned_accounts" 
    id: Mapped[int] = mapped_column(sqltypes.Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(sqltypes.BigInteger, nullable=False)
    
class Banned_Numbers(Model):
    __tablename__ = "banned_numbers"
    id: Mapped[int] = mapped_column(sqltypes.Integer, primary_key=True, autoincrement=True)
    phone_number: Mapped[str] = mapped_column(sqltypes.Text, nullable=False) 
    
    
    
    

# Setup the database engine and session
DATABASE_URL = "sqlite+aiosqlite:///self_maker_data.db"  # Adjust to your actual database URL
_engine = create_async_engine(DATABASE_URL)
db = async_sessionmaker(_engine, expire_on_commit=False)

async def initialize_database():
    async with _engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)
        logger.debug("Database initialized with updated schema")

async def dispose_database():
    await _engine.dispose()

# Create a global lock
db_lock = asyncio.Lock()

# Context manager to handle session with a lock
@asynccontextmanager
async def get_session():
    async with db_lock:
        async with db.begin() as session:
            try:
                yield session
            except Exception as e:
                logging.error(f"Session error: {e}")
                await session.rollback()
                raise
            finally:
                await session.close()
                logging.debug("Database session closed")

# Run the code below to apply the changes 
# async def main(): 
#     await initialize_database()
    
# asyncio.run(main())
