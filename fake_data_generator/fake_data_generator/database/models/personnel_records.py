from faker import Faker
from sqlalchemy import Column, Uuid, ForeignKey, DateTime, Double
from uuid_extensions import uuid7

from fake_data_generator.database.core import Base, IGenerator
from fake_data_generator.database.utils import utcnow


class PersonnelRecords(Base, IGenerator):
    id = Column(Uuid, default=uuid7, primary_key=True, nullable=False)
    employee_id = Column(ForeignKey("employee.id"), nullable=False)
    department_id = Column(ForeignKey("department.id"), nullable=False)
    company_branch_id = Column(ForeignKey("company_branch.id"), nullable=False)
    date = Column(DateTime(timezone=True), nullable=False, default=utcnow())
    salary = Column(Double, nullable=False)

    @classmethod
    def generate(cls, fake: Faker, **kwargs) -> Base:
        return cls(
            employee_id=kwargs["employee_id"],
            department_id=kwargs["department_id"],
            company_branch_id=kwargs["company_branch_id"],
            date=kwargs.get("date") or fake.date_time(),
            salary=kwargs.get("salary") or fake.random_int(min=15000, max=400000)
        )
