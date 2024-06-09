from pathlib import Path
from zipfile import ZipFile
from io import BytesIO
from shutil import rmtree
from json import (
    load,
    dumps,
)
from os import getenv
from contextlib import contextmanager
from uuid import uuid4
from typing import Self

from .ib2d_file_base import IB2DFileBase
from ..base import log_exception
from ..wildcards_sets import WildcardSets
from ..compare_sets import CompareSets


class IB2DFile(
    IB2DFileBase,
):
    """
    ``*.ib2d`` file object.
    """

    wildcard_sets: WildcardSets
    """
    Wildcard sets object.
    """

    compare_sets: CompareSets
    """
    Comparison sets object.
    """

    path: Path | None
    """
    Path to the ``*.ib2d`` file.
    """

    def __init__(
        self,
        working_dir_path: Path,
        wildcard_sets: WildcardSets,
        compare_sets: CompareSets,
        path: Path | None = None,
    ):

        IB2DFileBase.__init__(
            self=self,
            module_name=__name__,
            working_dir_path=working_dir_path,
        )

        self.wildcard_sets = wildcard_sets
        self.compare_sets = compare_sets
        self.path = path

    def __str__(
        self,
    ) -> str:

        return f'Path: {self.path}'

    @log_exception
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
    @log_exception
    def open(
        cls,
        path: str | Path,
        working_dir_path: str | Path | None = None,
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

            # Create wildcard sets
            wildcard_sets_file = ib2d_file.open(
                name='wildcard_sets.json',
            )

            wildcard_sets_data = load(
                fp=wildcard_sets_file,
            )

            wildcard_sets = WildcardSets.deserialize(
                instance_data=wildcard_sets_data,
                working_dir_path=working_dir_path,
                ib2d_file=ib2d_file,
            )

            # Add paths to wildcard set
            wildcard_sets.update_global_wildcard(
                key='ib2d_file_path',
                value=str(
                    path.absolute(),
                ),
            )

            wildcard_sets.update_global_wildcard(
                key='ib2d_file_dir_path',
                value=str(
                    path.parent.absolute(),
                ),
            )

            # Create compare sets
            compare_set_file = ib2d_file.open(
                name='compare_sets.json',
            )

            compare_set_data = load(
                fp=compare_set_file,
            )

            compare_sets = CompareSets.deserialize(
                instance_data=compare_set_data,
                working_dir_path=working_dir_path,
                ib2d_file=ib2d_file,
                wildcard_sets=wildcard_sets,
            )

            # Create instance
            ib2d_file = IB2DFile(
                working_dir_path=working_dir_path,
                wildcard_sets=wildcard_sets,
                compare_sets=compare_sets,
                path=path,
            )

            yield ib2d_file

        finally:

            pass

    @log_exception
    def save(
        self,
        path: str | Path,
    ) -> None:
        """
        Writes a ``*.ib2d`` file to disk.

        :param path: ``*.ib2d`` file path.
        :return:
        """

        if isinstance(path, str):
            path = Path(
                path,
            )

        # Create *.ib2d file in memory
        ib2d_file_bytes = BytesIO()

        ib2d_file = ZipFile(
            file=ib2d_file_bytes,
            mode='w',
        )

        # Serialize compare set
        compare_set_data = self.compare_sets.serialize(
            ib2d_file=ib2d_file,
        )

        # Flush buffer in *.ib2d file
        ib2d_file.writestr(
            zinfo_or_arcname='compare_sets.json',
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

        self.path = path

        # Add paths to wildcard set
        self.wildcard_sets.update_global_wildcard(
            key='ib2d_file_path',
            value=str(
                self.path.absolute(),
            ),
        )

        self.wildcard_sets.update_global_wildcard(
            key='ib2d_file_dir_path',
            value=str(
                self.path.parent.absolute(),
            ),
        )
