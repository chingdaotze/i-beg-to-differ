from pathlib import Path
from zipfile import ZipFile
from io import BytesIO
from shutil import rmtree
from json import (
    load,
    dumps,
)
from os import (
    PathLike,
    getenv,
)
from contextlib import contextmanager
from uuid import uuid4
from typing import Self

from ..base import Base
from ..compare_set import CompareSet


class IB2DFile(
    Base,
):
    """
    ``*.ib2d`` file object.
    """

    compare_set: CompareSet
    """
    Comparison set object.
    """

    def __init__(
        self,
        working_dir_path: Path,
        compare_set: CompareSet,
    ):

        Base.__init__(
            self=self,
            working_dir_path=working_dir_path,
        )

        self.compare_set = compare_set

    def __del__(
        self,
    ) -> None:
        """
        Cleans up the working directory.

        :return:
        """

        rmtree(
            self.working_dir_path,
        )

    @classmethod
    @contextmanager
    def open(
        cls,
        path: str | PathLike,
        working_dir_path: str | PathLike | None = None,
    ) -> Self:
        """
        Reads a ``*.ib2d`` file from disk and creates an instance. Also initializes the working directory.

        :param path: ``*.ib2d`` file path.
        :param working_dir_path: Working directory path.
        :return:
        """

        try:
            # Parse path
            if isinstance(path, str):
                path = Path(
                    path,
                )

            if not path.exists():
                raise FileNotFoundError(
                    f'Unable to locate *.ib2d file: "{str(path)}"!',
                )

            # Get working directory
            if working_dir_path is None:
                working_dir_path = getenv(
                    key='TEMP',
                )

                if working_dir_path is None:
                    raise KeyError(
                        'Unable to create default working directory: working_dir_path not specified '
                        'and could not locate "TEMP" environment variable.'
                    )

                working_dir_path = Path(
                    working_dir_path,
                )

                working_dir_path /= f'ib2d_{str(uuid4())}'

                working_dir_path.mkdir()

            else:
                working_dir_path = Path(
                    working_dir_path,
                )

            # Load *.ib2d file to memory
            with open(file=path, mode='rb') as input_file:

                ib2d_file_bytes = BytesIO(
                    initial_bytes=input_file.read(),
                )

                ib2d_file = ZipFile(
                    file=ib2d_file_bytes,
                    mode='r',
                )

            # Create compare set
            compare_set_file = ib2d_file.open(
                name='compare_set.json',
            )

            compare_set_data = load(
                fp=compare_set_file,
            )

            compare_set = CompareSet.deserialize(
                instance_data=compare_set_data,
                working_dir_path=working_dir_path,
                ib2d_file=ib2d_file,
            )

            # Create instance
            ib2d_file = IB2DFile(
                working_dir_path=working_dir_path,
                compare_set=compare_set,
            )

            yield ib2d_file

        finally:

            pass

    def save(
        self,
        path: str | PathLike,
    ) -> None:
        """
        Writes a ``*.ib2d`` file to disk.

        :param path: ``*.ib2d`` file path.
        :return:
        """

        # Create *.ib2d file in memory
        ib2d_file_bytes = BytesIO()

        ib2d_file = ZipFile(
            file=ib2d_file_bytes,
            mode='w',
        )

        # Serialize compare set
        compare_set_data = self.compare_set.serialize(
            ib2d_file=ib2d_file,
        )

        # Flush buffer in *.ib2d file
        ib2d_file.writestr(
            zinfo_or_arcname='compare_set.json',
            data=dumps(
                obj=compare_set_data,
                indent=4,
            ),
        )

        ib2d_file.close()

        # Write *.ib2d file to disk
        with open(file=path, mode='wb') as output_file:
            output_file.write(
                ib2d_file_bytes.getvalue(),
            )
