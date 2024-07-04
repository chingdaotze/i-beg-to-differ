from pathlib import Path
from logging import FileHandler
from multiprocessing import freeze_support

from i_beg_to_differ.core import (
    setup_logger,
    open_ib2d_file,
)


def main() -> None:
    # Setup logger
    log_file_path = (Path(__file__).parent.parent
        / 'tests'
        / 'test_artifacts'
        / 'ib2d_test.log'
    )

    setup_logger(
        file_handler=FileHandler(
            filename=log_file_path,
            mode='w',
        ),
    )

    with open_ib2d_file(
        path='../tests/test_artifacts/test_core/test.ib2d',
    ) as ib2d_file:

        compare_set = ib2d_file.compare_sets['CompareSet0']
        compare = compare_set['Compare1']

        compare.load()

        pass


if __name__ == '__main__':
    freeze_support()
    main()
