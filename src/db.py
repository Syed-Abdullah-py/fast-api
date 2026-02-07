from collections.abc import AsyncGenerator
import uuid
from datetime import datetime
import os

from dotenv import load_dotenv
from fastapi import Depends
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, create_engine
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from fastapi_users.db import (
    SQLAlchemyUserDatabase
)

from sqlalchemy.orm import DeclarativeBase, relationship
load_dotenv()


# Define the Base class, we cannot directly inherit from the DeclarativeBase class.
class Base(DeclarativeBase):
    pass


class User(SQLAlchemyBaseUserTableUUID, Base):
    posts = relationship("Post", back_populates="user")

# Declare the Schema of the Database
class Post(Base):
    __tablename__ = "posts"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    caption = Column(Text)
    url = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    file_name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="posts")



# Create 2 Engines (Synchronous and Asynchronous)
engine = create_async_engine(os.getenv("DATABASE_URL"))
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


# Async Function to create the database and the tables
async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Get an async session using this function
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)