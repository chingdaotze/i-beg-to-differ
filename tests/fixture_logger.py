from pytest import fixture
from pathlib import Path
from logging import FileHandler

from i_beg_to_differ.core import setup_logger


@fixture
def logger(
    request,
) -> None:
    test_name = request.node.name

    log_file_path = (
        Path(__file__).parent / 'test_artifacts' / test_name / f'{test_name}.log'
    )

    setup_logger(
        file_handler=FileHandler(
            filename=log_file_path,
            mode='w',
        ),
    )
