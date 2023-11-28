from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fake_data_generator.database.core import Base
from fake_data_generator.database.utils import menage_db_commit_method, CommitMode


class BaseRepository:
    session: AsyncSession

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_base(self, model_class: type[Base]) -> list[Base]:
        return (await self.session.execute(select(model_class))).scalars().all()

    async def get_base_by_id(self, model_class: type[Base], base_id: UUID) -> Base:
        return await self.session.get(model_class, base_id)

    @menage_db_commit_method(CommitMode.FLUSH)
    async def create_base(self, model_class: type[Base], **kwargs) -> Base:
        new = model_class(**kwargs)
        self.session.add(new)

        return new

    @menage_db_commit_method(CommitMode.FLUSH)
    async def add_base(self, model: Base) -> Base:
        self.session.add(model)

        return model

    @menage_db_commit_method(CommitMode.FLUSH)
    async def update_base(self, obj: Base) -> Base:
        self.session.add(obj)

        return obj
