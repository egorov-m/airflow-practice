from asyncio import iscoroutinefunction
from functools import wraps
from sys import argv


def launch_with_command(command):
    def decorator(func):
        @wraps(func)
        async def wrapped_f(*args, **kwargs):
            if len(argv) > 1 and argv[1] == command:
                if iscoroutinefunction(func):
                    return await func(*args, **kwargs)
                else:
                    return func(*args, **kwargs)

        return wrapped_f

    return decorator
