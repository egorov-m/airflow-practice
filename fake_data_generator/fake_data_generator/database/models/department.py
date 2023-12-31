from faker import Faker
from sqlalchemy import Column, BigInteger, String, ForeignKey

from fake_data_generator.database.core import Base, IGenerator


class Department(Base, IGenerator):
    id = Column(BigInteger, autoincrement=True, primary_key=True, nullable=False)
    name = Column(String(100), nullable=False)
    company_branch_id = Column(ForeignKey("company_branch.id"), nullable=False)
    chief_id = Column(ForeignKey("employee.id"), nullable=True)

    @classmethod
    def generate(cls, fake: Faker, **kwargs) -> Base:
        return cls(
            name=kwargs.get("department_name") or fake.catch_phrase(),
            company_branch_id=kwargs["company_branch_id"],
            chief_id=kwargs.get("chief_id")
        )
