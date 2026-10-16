import argparse
import logging
import time
from collections.abc import Callable
from functools import wraps

logger = logging.getLogger(__name__)
Command = Callable[[argparse.Namespace], int]


def timed(func: Command) -> Command:
    @wraps(func)
    def wrapper(args: argparse.Namespace) -> int:
        start = time.perf_counter()
        try:
            result = func(args)
        finally:
            elapsed = time.perf_counter() - start
            logger.debug("Функция %s заняла %.3f с", func.__name__, elapsed)
        return result

    return wrapper
