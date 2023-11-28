import logging
from random import randint, choice

from faker import Faker

from fake_data_generator.database.models.department import Department
from fake_data_generator.database.models.employee import Employee
from fake_data_generator.database.models.personnel_records import PersonnelRecords
from fake_data_generator.database.models.position import Position
from fake_data_generator.database.repositories.base import BaseRepository
from fake_data_generator.database.utils import utcnow

fdg_logger = logging.getLogger("modify_logger")


async def random_modification(fake: Faker, repo: BaseRepository):
    fdg_logger.info("Start random modification.")
    employees: list[Employee] = await repo.get_all_base(Employee)
    positions: list[Position] = await repo.get_all_base(Position)
    departments: list[Department] = await repo.get_all_base(Department)
    for _ in range(randint(0, len(employees) // 4)):
        employee = choice(employees)
        employee.position_id = choice(positions).id
        if choice([True, False]):
            employee.salary = randint(15000, 400000)
        if choice([True, False]):
            employee.department_id = choice(departments).id

        await repo.update_base(employee)
        department = await repo.get_base_by_id(Department, employee.department_id)
        await repo.add_base(
            PersonnelRecords.generate(
                fake,
                employee_id=employee.id,
                department_id=employee.department_id,
                company_branch_id=department.company_branch_id,
                date=utcnow(),
                salary=employee.salary
            )
        )
