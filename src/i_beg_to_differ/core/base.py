"""
Contains definition of the Base class.
"""

from multiprocessing import (
    Lock,
    Pool as MultiprocessingPool,
    Manager,
)
from multiprocessing.managers import SyncManager
from multiprocessing.pool import Pool
from typing import (
    ClassVar,
    Self,
    NoReturn,
)
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

    __manager: ClassVar[SyncManager] = None

    @abstractmethod
    def __str__(
        self,
    ) -> str:
        """
        String value used for hashing and equality tests,
        among other things.

        :return: String representation of this object.
        """

    def __repr__(
        self,
    ) -> str:

        return str(
            self,
        )

    def __format__(
        self,
        format_spec: str,
    ) -> str:

        return format(
            str(
                self,
            ),
            format_spec,
        )

    def __hash__(
        self,
    ) -> int:

        return hash(
            type(
                self,
            ).__name__
            + ': '
            + str(
                self,
            ),
        )

    def __eq__(
        self,
        other: Self,
    ) -> bool:
        # pylint: disable=unidiomatic-typecheck
        # Use unidiomatic type check for exact type (ignoring inheritance)
        if type(self) == type(other) and hash(self) == hash(other):
            return True

        return False

    def __ne__(
        self,
        other: Self,
    ) -> bool:

        if self == other:
            return False

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
        """

        lock.acquire()
        self.logger.info(
            msg=msg,
        )
        lock.release()

    def log_warning(
        self,
        msg: str,
    ) -> None:
        """
        Logs a warning to the log file. Multiprocess-safe.

        :param msg: Warning to log.
        """

        lock.acquire()
        self.logger.warning(
            msg=msg,
        )
        lock.release()

    def log_exception(
        self,
        exc: Exception,
    ) -> NoReturn:
        """
        Logs an exception and raises it. Multiprocess-safe.

        :param exc: Exception to raise.
        """

        lock.acquire()
        self.logger.exception(
            msg='Encountered exception. Traceback below:\n\n',
        )
        lock.release()

        raise exc

    @property
    def pool(
        self,
    ) -> Pool:
        """
        Global multiprocessing pool.
        """

        # FIXME: This is actually a class property, but Python 3.13+ deprecates class properties.

        if Base.__pool is None:
            Base.__pool = MultiprocessingPool(
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
    ) -> SyncManager:
        """
        Global multiprocessing manager.
        """

        # FIXME: This is actually a class property, but Python 3.13+ deprecates class properties.

        if Base.__manager is None:
            Base.__manager = Manager()

        return Base.__manager
