from .fixture_ib2d_file import ib2d_file
from .fixture_logger import logger


def test_compare_rule_equals(
    ib2d_file,
    logger,
) -> None:
    with ib2d_file:

        compare_set = ib2d_file.compare_sets['CompareSet0']
        compare = compare_set['Compare1']

        values_comparison = compare.values_comparison

        pass
