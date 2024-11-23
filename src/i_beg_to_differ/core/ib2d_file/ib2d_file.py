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

from ..base import (
    Base,
    log_exception,
)
from ..wildcards_sets import WildcardSets
from ..compare_sets import CompareSets
from ..data_sources import DataSources


class IB2DFile(
    Base,
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

    data_sources: DataSources
    """
    Data sources object.
    """

    working_dir_path: Path
    """
    Working directory path.
    """

    path: Path | None
    """
    Path to the ``*.ib2d`` file.
    """

    def __init__(
        self,
        working_dir_path: str | Path | None = None,
        wildcard_sets: WildcardSets | None = None,
        compare_sets: CompareSets | None = None,
        data_sources: DataSources | None = None,
        path: Path | None = None,
    ):

        Base.__init__(
            self=self,
        )

        self.working_dir_path = self.get_working_dir_path(
            working_dir_path=working_dir_path,
        )

        # Wildcard sets
        if wildcard_sets is None:
            wildcard_sets = WildcardSets()

        self.wildcard_sets = wildcard_sets

        # Compare sets
        if compare_sets is None:
            compare_sets = CompareSets()

        self.compare_sets = compare_sets

        # Data sources
        if data_sources is None:
            data_sources = DataSources()

        self.data_sources = data_sources

        self.path = path

    def __str__(
        self,
    ) -> str:

        return f'*.ib2d file [{self.path}]'

    def __enter__(
        self,
    ) -> Self:

        return self

    def __exit__(
        self,
        exc_type,
        exc_val,
        exc_tb,
    ) -> None:

        rmtree(
            self.working_dir_path,
        )

    @staticmethod
    def get_working_dir_path(
        working_dir_path: str | Path | None = None,
    ) -> Path:
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

            working_dir_path /= f'ib2d_{uuid4()!s}'

            working_dir_path.mkdir()

        elif isinstance(working_dir_path, str):
            working_dir_path = Path(
                working_dir_path,
            )

        return working_dir_path

    @staticmethod
    def load_zip_file(
        path: Path,
    ) -> ZipFile:

        with open(file=path, mode='rb') as input_file:
            ib2d_file_bytes = BytesIO(
                initial_bytes=input_file.read(),
            )

            ib2d_file = ZipFile(
                file=ib2d_file_bytes,
                mode='r',
            )

        return ib2d_file

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
                    f'Unable to locate *.ib2d file: "{path!s}"!',
                )

            working_dir_path = IB2DFile.get_working_dir_path(
                working_dir_path=working_dir_path,
            )

            # Load *.ib2d file to memory
            ib2d_file = cls.load_zip_file(
                path=path,
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

            # Add system paths to wildcard set
            wildcard_sets.update_system_wildcard(
                key='ib2d_file_path',
                value=str(
                    path.absolute(),
                ),
            )

            wildcard_sets.update_system_wildcard(
                key='ib2d_file_dir_path',
                value=str(
                    path.parent.absolute(),
                ),
            )

            # Create data sources
            data_sources_file = ib2d_file.open(
                name='data_sources.json',
            )

            data_sources_data = load(
                fp=data_sources_file,
            )

            data_sources = DataSources.deserialize(
                instance_data=data_sources_data,
                working_dir_path=working_dir_path,
                ib2d_file=ib2d_file,
                wildcard_sets=wildcard_sets,
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

            compare_sets.set_data_sources(
                data_sources=data_sources,
            )

            # Create instance
            ib2d_file = IB2DFile(
                working_dir_path=working_dir_path,
                wildcard_sets=wildcard_sets,
                compare_sets=compare_sets,
                data_sources=data_sources,
                path=path,
            )

            yield ib2d_file

        except Exception as e:
            raise e

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

        self.log_info(
            msg=f'Saving *.ib2d file to location: "{str(path.absolute())}" ...',
        )

        # Create *.ib2d file in memory
        ib2d_file_buffer = BytesIO()

        ib2d_file = ZipFile(
            file=ib2d_file_buffer,
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
                indent=2,
            ),
        )

        # Serialize data sources
        data_source_data = self.data_sources.serialize(
            ib2d_file=ib2d_file,
        )

        ib2d_file.writestr(
            zinfo_or_arcname='data_sources.json',
            data=dumps(
                obj=data_source_data,
                indent=2,
            ),
        )

        # Serialize wildcard sets
        wildcard_sets_data = self.wildcard_sets.serialize(
            ib2d_file=ib2d_file,
        )

        ib2d_file.writestr(
            zinfo_or_arcname='wildcard_sets.json',
            data=dumps(
                obj=wildcard_sets_data,
                indent=2,
            ),
        )

        ib2d_file.close()

        # Write *.ib2d file to disk
        with open(file=path, mode='wb') as output_file:
            output_file.write(
                ib2d_file_buffer.getvalue(),
            )

        self.log_info(
            msg=f'Save complete: "{str(path.absolute())}"',
        )

        self.path = path

        # Add paths to wildcard set
        self.wildcard_sets.update_system_wildcard(
            key='ib2d_file_path',
            value=str(
                self.path.absolute(),
            ),
        )

        self.wildcard_sets.update_system_wildcard(
            key='ib2d_file_dir_path',
            value=str(
                self.path.parent.absolute(),
            ),
        )
