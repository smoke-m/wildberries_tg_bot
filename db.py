"""Модуль создания БД."""

from datetime import datetime

from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, declared_attr, sessionmaker

from constants import settings


class PreBase:
    """Базовый класс."""

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=PreBase)

engine = create_async_engine(settings.database_url)

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)


class RequestsInfo(Base):
    """Модель объекта."""

    user_id = Column(
        Integer,
    )
    article = Column(
        Integer,
    )
    create_date = Column(DateTime, default=datetime.utcnow)
