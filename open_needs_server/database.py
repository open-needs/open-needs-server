from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from open_needs_server.config import settings

import logging


class ONSBase(object):
    def to_dict(self):
        """Returns the current Model bas dict. Without any sqlalchemy specific data"""
        data = dict(self.__dict__)
        data.pop('_sa_instance_state', None)
        return data


SQLALCHEMY_DATABASE_URL = settings.database.sql_string

log = logging.getLogger(__name__)
log.debug(f'SQL string: {SQLALCHEMY_DATABASE_URL}')

engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
# engine = create_async_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base(cls=ONSBase)


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

