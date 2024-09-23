from pytest import fixture

from i_beg_to_differ.core import (
    IB2DFile,
    open_ib2d_file,
)


@fixture
def ib2d_file(
    request,
) -> IB2DFile:
    test_name = request.node.name

    with open_ib2d_file(
        path=f'test_artifacts/{test_name}/{test_name}.ib2d',
    ) as ib2d_file:

        yield ib2d_file
