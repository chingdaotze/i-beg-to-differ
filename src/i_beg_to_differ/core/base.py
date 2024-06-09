from typing import (
    Callable,
    Any,
    ClassVar,
)
from time import time
from abc import ABC
from logging import (
    getLogger,
    Logger,
)
from multiprocessing import Lock


def log_runtime(
    f: Callable,
) -> Callable:
    """
    Decorator that logs runtime to a log file.

    :param f: Arbitrary instance method from ``Base`` class.
    :return:
    """

    def wrapper(
        self,
        *args,
        **kwargs,
    ) -> Any:

        start_time = time()

        result = f(
            self,
            *args,
            **kwargs,
        )

        end_time = time()
        runtime = end_time - start_time

        self.lock.acquire()
        self.logger.info(
            msg=f'Function - {f.__name__}, Runtime - {runtime:.2f} seconds.',
        )
        self.lock.release()

        return result

    return wrapper


def log_exception(
    f: Callable,
) -> Callable:
    """
    Decorator that logs exceptions to a log file.

    :param f: Arbitrary instance method from ``Base`` class.
    :return:
    """

    def wrapper(
        self,
        *args,
        **kwargs,
    ) -> Any:

        try:

            result = f(
                self,
                *args,
                **kwargs,
            )

            return result

        except Exception as e:

            self.lock.acquire()
            self.logger.exception(
                msg='Encountered exception. Traceback below:',
            )
            self.lock.release()

            raise e

    return wrapper


class Base(
    ABC,
):
    """
    Base class for object model.
    """

    lock: ClassVar[Lock] = Lock()
    """
    Global multiprocessing lock.
    """

    logger: Logger
    """
    Module-level logger.
    """

    def __repr__(
        self,
    ) -> str:

        return str(
            self,
        )

    def __init__(
        self,
        module_name: str,
    ):

        self.logger = getLogger(
            name=module_name,
        )
