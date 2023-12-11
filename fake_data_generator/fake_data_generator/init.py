import logging
from random import choice
from uuid import UUID

from faker import Faker

from fake_data_generator.database.models.company import Company
from fake_data_generator.database.models.company_branch import CompanyBranch
from fake_data_generator.database.models.department import Department
from fake_data_generator.database.models.employee import Employee
from fake_data_generator.database.models.location import Location
from fake_data_generator.database.models.personnel_records import PersonnelRecords
from fake_data_generator.database.models.position import Position
from fake_data_generator.database.repositories.base import BaseRepository
from fake_data_generator.database.utils import db_metadata_create_all, utcnow


fdg_logger = logging.getLogger("init_logger")


async def init_metadata_db(*args):
    fdg_logger.info("Start init db.")
    await db_metadata_create_all()
    fdg_logger.info("Done metadata create all.")


async def init_company_branches_and_departments(
        fake: Faker,
        repo: BaseRepository,
        company_id: UUID,
        count_company_branches: int = 30,
        count_departments: int = 15
) -> list[Department]:
    fdg_logger.info("Start init company branches and departments.")
    departments = []
    chefs = []
    for _ in range(count_company_branches):
        city = fake.city()
        location: Location = await repo.add_base(Location.generate(fake, city=city))
        company_branch: CompanyBranch = await repo.add_base(
            CompanyBranch.generate(
                fake,
                name=f"{fake.company_suffix()} {city}",
                company_id=company_id,
                location_id=location.id
            ),
        )
        for __ in range(count_departments):
            department_name = fake.catch_phrase()
            position: Position = await repo.add_base(Position.generate(fake, name=f"Chief {department_name}"))
            department: Department = await repo.add_base(
                Department.generate(
                    fake,
                    name=department_name,
                    company_branch_id=company_branch.id
                )
            )
            departments.append(department)
            chief: Employee = await repo.add_base(
                Employee.generate(
                    fake,
                    position_id=position.id,
                    department_id=department.id,
                    salary=fake.random_int(min=100000, max=400000)
                )
            )
            chefs.append(chief)
            department.chief_id = chief.id
            await repo.update_base(department)
    await init_personnel_records(fake, repo, chefs)

    return departments


async def init_positions(
        fake: Faker,
        repo: BaseRepository,
        count_positions: int = 5
) -> list[Position]:
    fdg_logger.info("Start init positions.")
    positions = []
    for _ in range(count_positions):
        position: Position = await repo.create_base(
            Position,
            name=fake.catch_phrase(),
            description=fake.text(max_nb_chars=400)
        )
        positions.append(position)

    return positions


async def init_employees(
        fake: Faker,
        repo: BaseRepository,
        positions: list[Position],
        departments: list[Department],
        count_employees: int = 5000
) -> list[Employee]:
    fdg_logger.info("Start init employees.")
    employees = []
    for _ in range(count_employees):
        employee: Employee = await repo.add_base(
            Employee.generate(
                fake,
                position_id=choice(positions).id,
                department_id=choice(departments).id
            )
        )
        employees.append(employee)

    return employees


async def init_personnel_records(
        fake: Faker,
        repo: BaseRepository,
        employees: list[Employee]
) -> list[PersonnelRecords]:
    fdg_logger.info("Start init personnel records.")
    personnel_records_list = []
    for employee in employees:
        department = await repo.get_base_by_id(Department, employee.department_id)
        personnel_records = await repo.add_base(
            PersonnelRecords.generate(
                fake,
                employee_id=employee.id,
                department_id=employee.department_id,
                company_branch_id=department.company_branch_id,
                date=utcnow(),
                salary=employee.salary
            )
        )
        personnel_records_list.append(personnel_records)

    return personnel_records_list


async def init_base_data_db(fake: Faker, repo: BaseRepository) -> list[PersonnelRecords]:
    fdg_logger.info("Start init data db.")
    company: Company = await repo.add_base(Company.generate(fake))
    departments = await init_company_branches_and_departments(fake, repo, company.id)
    positions = await init_positions(fake, repo)
    employees = await init_employees(fake, repo, positions, departments)
    personnel_records_list = await init_personnel_records(fake, repo, employees)
    fdg_logger.info("Done init base data db.")
    await repo.session.commit()
    await repo.session.close()
    return personnel_records_list
