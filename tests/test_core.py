from i_beg_to_differ.core import open_ib2d_file


def test_core() -> None:
    with open_ib2d_file(
        path='./test_data/test_data.ib2d',
    ) as ib2d_file:

        pass