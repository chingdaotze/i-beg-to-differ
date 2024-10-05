from pytest import fixture
from pathlib import Path

from i_beg_to_differ.core import (
    IB2DFile,
    open_ib2d_file,
)


@fixture
def ib2d_file(
    artifacts_dir: Path,
    test_name: str,
) -> IB2DFile:

    path = artifacts_dir / f'{test_name}.ib2d'

    with open_ib2d_file(
        path=path,
    ) as ib2d_file:

        yield ib2d_file
