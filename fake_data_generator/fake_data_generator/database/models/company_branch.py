from faker import Faker
from sqlalchemy import Column, BigInteger, String, DateTime, ForeignKey

from fake_data_generator.database.core import Base, IGenerator
from fake_data_generator.database.utils import utcnow


class CompanyBranch(Base, IGenerator):
    id = Column(BigInteger, autoincrement=True, primary_key=True, nullable=False)
    name = Column(String(100), nullable=False)
    foundation_date = Column(DateTime(timezone=True), nullable=False, default=utcnow())
    company_id = Column(ForeignKey("company.id"), nullable=False)
    location_id = Column(ForeignKey("location.id"), nullable=False)

    @classmethod
    def generate(cls, fake: Faker, **kwargs) -> Base:
        return cls(
            name=fake.company_suffix() + f" {kwargs.get('location')}" if kwargs.get('location') is not None else "",
            foundation_date=kwargs.get("foundation_date") or fake.date_time(),
            company_id=kwargs["company_id"],
            location_id=kwargs['location_id']
        )
