from multiprocessing import (
    Lock,
    Pool,
    Manager,
)
from typing import (
    Callable,
    Any,
    ClassVar,
    Self,
)
from time import time
from abc import (
    ABC,
    abstractmethod,
)
from logging import (
    getLogger,
    Logger,
)
from psutil import cpu_count


lock = Lock()
"""
Global multiprocessing lock.
"""


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

        lock.acquire()
        self.logger.info(
            msg=f'Function - {f.__name__}, Runtime - {runtime:.2f} seconds.',
        )
        lock.release()

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

            lock.acquire()
            self.logger.exception(
                msg='Encountered exception. Traceback below:\n\n',
            )
            lock.release()

            raise e

    return wrapper


class Base(
    ABC,
):
    """
    Base class for object model.
    """

    logger: Logger
    """
    Module-level logger.
    """

    __pool: ClassVar[Pool] = None

    __manager: ClassVar[Manager] = None

    @abstractmethod
    def __str__(
        self,
    ) -> str:
        """
        Method that returns a string representation of this object.
        This string value is used for hashing and equality tests.
        """

    def __repr__(
        self,
    ) -> str:

        return str(
            self,
        )

    def __format__(
        self,
        format_spec,
    ) -> str:

        return str(
            self,
        )

    def __hash__(
        self,
    ) -> int:

        return hash(
            str(
                self,
            ),
        )

    def __eq__(
        self,
        other: Self,
    ) -> bool:

        if hash(self) == hash(other):
            return True

        else:
            return False

    def __ne__(
        self,
        other: Self,
    ) -> bool:

        if self == other:
            return False

        else:
            return True

    def __init__(
        self,
    ):
        self.logger = getLogger(
            name=type(
                self,
            ).__module__,
        )

    def log_info(
        self,
        msg: str,
    ) -> None:
        """
        Logs a message to the log file. Multiprocess-safe.

        :param msg: Message to log.
        :return:
        """

        lock.acquire()
        self.logger.info(
            msg=msg,
        )
        lock.release()

    @property
    def pool(
        self,
    ) -> Pool:
        """
        Global multiprocessing pool.

        :return:
        """

        # FIXME: This is actually a class property, but Python 3.13+ deprecates class properties.

        if Base.__pool is None:
            Base.__pool = Pool(
                processes=max(
                    cpu_count(
                        logical=False,
                    )
                    - 1,
                    1,
                ),
            )

        return Base.__pool

    @property
    def manager(
        self,
    ) -> Manager:
        """
        Global multiprocessing manager.

        :return:
        """

        # FIXME: This is actually a class property, but Python 3.13+ deprecates class properties.

        if Base.__manager is None:
            Base.__manager = Manager()

        return Base.__manager
