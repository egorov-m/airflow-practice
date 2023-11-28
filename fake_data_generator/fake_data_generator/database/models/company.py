from faker import Faker
from sqlalchemy import Column, Uuid, String, DateTime
from uuid_extensions import uuid7

from fake_data_generator.database.core import Base, IGenerator
from fake_data_generator.database.utils import utcnow


class Company(Base, IGenerator):
    id = Column(Uuid, default=uuid7, primary_key=True, nullable=False)
    name = Column(String(100), nullable=False)
    foundation_date = Column(DateTime(timezone=True), nullable=False, default=utcnow())

    @classmethod
    def generate(cls, fake: Faker, **kwargs) -> Base:
        return cls(
            name=kwargs.get("name") or fake.company(),
            foundation_date=kwargs.get("foundation_date") or fake.date_time()
        )
