from . import settings


def printd(*objects, sep: str = ' ', end: str = '\n'):
    if settings.DEBUG:
        print(*objects, sep = sep, end = end)
