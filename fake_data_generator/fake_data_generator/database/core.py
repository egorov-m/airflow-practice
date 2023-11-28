from abc import abstractmethod
from re import split

from faker import Faker
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, declared_attr

from fake_data_generator.config import settings

engine: AsyncEngine = create_async_engine(url=settings.get_db_url(),
                                          pool_pre_ping=True,
                                          pool_size=settings.DB_POOL_SIZE,
                                          max_overflow=settings.DB_MAX_OVERFLOW)

get_session: sessionmaker = sessionmaker(engine, class_=AsyncSession)


def resolve_table_name(name):
    """Resolves table names to their mapped names."""
    names = split("(?=[A-Z])", name)
    return "_".join([x.lower() for x in names if x])


class CustomBase:
    @declared_attr
    def __tablename__(self):
        return resolve_table_name(self.__name__)


Base = declarative_base(cls=CustomBase)


class IGenerator:
    @classmethod
    @abstractmethod
    def generate(cls, fake: Faker, **kwargs) -> Base:
        pass
