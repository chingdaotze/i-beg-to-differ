from pytest import (
    fixture,
    hookimpl,
)
from pathlib import Path
from logging import FileHandler

from i_beg_to_differ.core import setup_logger


@hookimpl
def pytest_runtest_setup(
    item,
) -> None:
    test_name = item.name
    item.config.cache.set(
        key='TEST_NAME',
        value=test_name,
    )

    test_artifacts_dir = Path(__file__).parent / 'test_artifacts' / test_name
    item.config.cache.set(
        key='TEST_ARTIFACTS_DIR',
        value=str(
            test_artifacts_dir,
        ),
    )

    benchmarks_dir = test_artifacts_dir / 'benchmarks'
    item.config.cache.set(
        key='BENCHMARKS_DIR',
        value=str(
            benchmarks_dir,
        ),
    )

    log_file_path = test_artifacts_dir / f'{test_name}.log'

    setup_logger(
        file_handler=FileHandler(
            filename=log_file_path,
            mode='w',
        ),
    )


@fixture
def test_name(
    cache,
) -> str:

    return cache.get(
        key='TEST_NAME',
        default=None,
    )


@fixture
def artifacts_dir(
    cache,
) -> Path:

    return Path(
        cache.get(
            key='TEST_ARTIFACTS_DIR',
            default=None,
        ),
    )


@fixture
def benchmarks_dir(
    cache,
) -> Path:

    return Path(
        cache.get(
            key='BENCHMARKS_DIR',
            default=None,
        ),
    )
