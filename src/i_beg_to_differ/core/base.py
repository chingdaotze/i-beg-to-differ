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
from multiprocessing import (
    Lock,
    Pool,
)
from psutil import cpu_count


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
            msg=f"Function - {f.__name__}, Runtime - {runtime:.2f} seconds.",
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
                msg="Encountered exception. Traceback below:",
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

    __pool: Pool = None

    logger: Logger
    """
    Module-level logger.
    """

    _module_name: str

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
        module_name: str,
    ):

        self._module_name = type(
            self,
        ).__module__

        self.logger = getLogger(
            name=module_name,
        )

    @property
    def pool(
        self,
    ) -> Pool:
        """
        Global multiprocessing pool.
        """

        if self.__pool is None:

            self.__pool = Pool(
                processes=max(
                    cpu_count(
                        logical=False,
                    )
                    - 1,
                    1,
                ),
            )

        return self.__pool
