from .fixture_ib2d_file import ib2d_file
from .fixture_logger import logger


def test_report_excel(
    ib2d_file,
    logger,
    tmp_path,
) -> None:
    with ib2d_file:

        compare_set = ib2d_file.compare_sets['CompareSet0']
        compare = compare_set['Compare1']

        report_path = tmp_path / 'report.xlsx'

        compare.to_excel(
            path=report_path,
        )
