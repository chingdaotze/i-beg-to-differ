from typing import (
    Callable,
    Any,
    ClassVar,
)
from time import time
from abc import ABC
from pathlib import Path
from logging import (
    getLogger,
    Logger,
)
from multiprocessing import Lock


def log_base_instance_method(
    log_runtime: bool = False,
) -> Callable:
    """
    Logs exceptions using the logger and re-raises the exception. Can also log runtimes.

    :param log_runtime: Boolean switch to log runtime.
    :return:
    """

    def decorator(
        f: Callable,
    ) -> Callable:

        def wrapper(
            self,
            *args,
            **kwargs,
        ) -> Any:

            try:
                start_time = time()

                result = f(
                    self,
                    *args,
                    **kwargs,
                )

                end_time = time()
                runtime = end_time - start_time

                if log_runtime:
                    self.lock.acquire()
                    self.logger.info(
                        msg=f'Function - {f.__name__}, Runtime - {runtime:.2f} seconds.',
                    )
                    self.lock.release()

                return result

            except Exception as e:

                self.logger.exception(
                    msg='Exception',
                )

                raise e

        return wrapper

    return decorator


class Base(
    ABC,
):
    """
    Base class for object model.
    """

    working_dir_path: Path
    """
    Working directory path.
    """

    lock: ClassVar[Lock] = Lock()
    """
    Global multiprocessing lock.
    """

    logger: ClassVar[Logger] = getLogger(
        name=__name__,
    )
    """
    Module-level logger.
    """

    @log_base_instance_method()
    def __init__(
        self,
        working_dir_path: Path,
    ):
        """
        Checks if working directory exists.

        :param working_dir_path: Working directory path.
        """

        self.working_dir_path = working_dir_path

        if not self.working_dir_path.exists():

            raise FileNotFoundError(
                f'Unable to locate working directory: "{str(self.working_dir_path)}"!',
            )
