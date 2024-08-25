from i_beg_to_differ.core import open_ib2d_file


def test_core() -> None:
    with open_ib2d_file(
        path='test_artifacts/test_core/test.ib2d',
    ) as ib2d_file:

        compare_set = ib2d_file.compare_sets['CompareSet0']
        compare = compare_set['Compare1']

        schema_comparison = compare.data_sources.schema_comparison

        pass
