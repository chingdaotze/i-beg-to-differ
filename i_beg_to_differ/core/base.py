from abc import ABC
from pathlib import Path


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
