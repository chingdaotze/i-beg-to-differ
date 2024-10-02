from .fixture_ib2d_file import ib2d_file
from .fixture_logger import logger
from .fixture_parquet_files import parquet_files


def test_compare_rule_equals(
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

        assert parquet_files['schema_comparison'].equals(
            other=compare.data_source_pair.schema_comparison
        )

        assert parquet_files['source_duplicate_records'].equals(
            other=compare.source_duplicate_primary_key_records,
        )

        assert parquet_files['target_duplicate_records'].equals(
            other=compare.target_duplicate_primary_key_records,
        )
