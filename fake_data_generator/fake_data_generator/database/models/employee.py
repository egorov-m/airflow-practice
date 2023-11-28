from faker import Faker
from sqlalchemy import Column, Uuid, String, ForeignKey, Double
from uuid_extensions import uuid7

from fake_data_generator.database.core import Base, IGenerator


class Employee(Base, IGenerator):
    id = Column(Uuid, default=uuid7, primary_key=True, nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    second_name = Column(String(100), nullable=True)
    position_id = Column(ForeignKey("position.id"), nullable=False)
    department_id = Column(ForeignKey("department.id"), nullable=False)
    salary = Column(Double, nullable=False)

    @classmethod
    def generate(cls, fake: Faker, **kwargs) -> Base:
        return cls(
            first_name=kwargs.get("first_name") or fake.first_name(),
            last_name=kwargs.get("last_name") or fake.last_name(),
            position_id=kwargs["position_id"],
            department_id=kwargs["department_id"],
            salary=kwargs.get("salary") or fake.random_int(min=15000, max=400000)
        )
