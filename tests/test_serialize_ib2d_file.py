from pathlib import Path

from .fixture_ib2d_file import ib2d_file
from .fixture_logger import logger


def test_serialize_ib2d_file(
    ib2d_file,
    logger,
    tmpdir,
) -> None:
    # Serialize
    module_name = __name__.split('.')[-1]

    ib2d_save_path = Path(
        tmpdir / f'{module_name}.ib2d',
    )

    ib2d_file.save(
        path=ib2d_save_path,
    )

    # TODO: Compare
    pass
