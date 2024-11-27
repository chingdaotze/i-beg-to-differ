from pathlib import Path
from logging import FileHandler
from multiprocessing import freeze_support

from i_beg_to_differ.core import (
    setup_logger,
    open_ib2d_file,
)


TEST_NAME = 'test_compare_rule_equals'
OUTPUT_PATH = r'C:\Users\chingdaotze\Desktop\test\test.xlsx'


def main() -> None:
    # Setup logger
    log_file_path = (
        Path(__file__).parent.parent / 'tests' / 'test_artifacts' / 'ib2d_test.log'
    )

    setup_logger(
        file_handler=FileHandler(
            filename=log_file_path,
            mode='w',
        ),
    )

    with open_ib2d_file(
        path=f'../tests/test_artifacts/{TEST_NAME}/{TEST_NAME}.ib2d',
    ) as ib2d_file:

        compare_set = ib2d_file.compare_sets['CompareSet0']
        compare = compare_set['Compare1']
        compare.to_excel(
            path=OUTPUT_PATH,
        )


if __name__ == '__main__':
    freeze_support()
    main()
