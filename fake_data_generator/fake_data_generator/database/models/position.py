from faker import Faker
from sqlalchemy import Column, Uuid, String
from uuid_extensions import uuid7

from fake_data_generator.database.core import Base, IGenerator


class Position(Base, IGenerator):
    id = Column(Uuid, default=uuid7, primary_key=True, nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(String(400), nullable=False)

    @classmethod
    def generate(cls, fake: Faker, **kwargs) -> Base:
        return cls(
            name=kwargs.get("name") or fake.catch_phrase(),
            description=kwargs.get("description") or fake.text(max_nb_chars=400)
        )
