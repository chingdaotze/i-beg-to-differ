from .fixture_ib2d_file import ib2d_file
from .fixture_logger import logger
from .fixture_parquet_files import parquet_files


def test_compare_rule_numeric_tolerance(
    ib2d_file,
    logger,
    parquet_files,
) -> None:

    with ib2d_file:
        compare_set = ib2d_file.compare_sets['CompareSet0']
        compare = compare_set['Compare1']

        assert parquet_files['values_comparison'].equals(
            other=compare.values_comparison,
        )

        assert parquet_files['source_only_records'].equals(
            other=compare.source_only_records,
        )

        assert parquet_files['target_only_records'].equals(
            other=compare.target_only_records,
        )
