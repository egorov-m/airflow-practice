from datetime import datetime, timezone
from enum import IntEnum
from functools import wraps

from fake_data_generator.database.core import engine, Base


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class CommitMode(IntEnum):
    """
    Commit modes for the managed db methods
    """

    NONE = 0
    FLUSH = 1
    COMMIT = 2
    ROLLBACK = 3


def menage_db_commit_method(auto_commit: CommitMode = CommitMode.FLUSH):
    def decorator(f):
        @wraps(f)
        async def wrapped_f(self, *args, **kwargs):
            result = await f(self, *args, **kwargs)
            match auto_commit:
                case CommitMode.FLUSH:
                    await self.session.flush()
                case CommitMode.COMMIT:
                    await self.session.commit()
                case CommitMode.ROLLBACK:
                    await self.session.rollback()

            return result

        return wrapped_f

    return decorator


async def db_metadata_create_all():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
