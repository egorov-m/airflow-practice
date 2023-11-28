from asyncio import run
from time import sleep
from typing import Callable

from faker import Faker

from fake_data_generator.cli import launch_with_command
from fake_data_generator.database.deps import get_db
from fake_data_generator.database.repositories.base import BaseRepository
from fake_data_generator.fdg_logging import setup_logging
from fake_data_generator.init import init_metadata_db, init_base_data_db
from fake_data_generator.modify import random_modification


async def start(*funcs: list):
    session = await get_db()
    repo = BaseRepository(session)
    fake = Faker("ru_RU")
    try:
        funcs: list[Callable[[Faker, BaseRepository], any]]
        for f in funcs:
            await f(fake, repo)
        await session.commit()
    except KeyboardInterrupt:
        await session.rollback()
    finally:
        await session.close()


@launch_with_command("init")
async def init():
    await start(init_metadata_db, init_base_data_db)


@launch_with_command("startup")
async def startup():
    while True:
        await start(random_modification)
        sleep(60)


if __name__ == "__main__":
    setup_logging()
    run(init())
    run(startup())
