from fake_data_generator.database.core import get_session


async def get_db():
    return get_session()
