from faker import Faker
from sqlalchemy import Column, BigInteger, String, Double

from fake_data_generator.database.core import Base, IGenerator


class Location(Base, IGenerator):
    id = Column(BigInteger, autoincrement=True, primary_key=True, nullable=False)
    country = Column(String(100), nullable=False)
    city = Column(String(100), nullable=False)
    region = Column(String(100), nullable=True)
    street_address = Column(String(100), nullable=False)
    latitude = Column(Double, nullable=False)
    longitude = Column(Double, nullable=False)

    @classmethod
    def generate(cls, fake: Faker, **kwargs) -> Base:
        return cls(
            country=kwargs.get("country") or fake.country(),
            city=kwargs.get("city") or fake.city(),
            region=kwargs.get("region") or fake.region(),
            street_address=kwargs.get("street_address") or fake.street_address(),
            latitude=kwargs.get("latitude") or fake.longitude(),
            longitude=kwargs.get("longitude") or fake.longitude()
        )
