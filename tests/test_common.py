from brent.common import window


def test_window():
    result = list(window([1, 2, 3, 4], n=2))
    assert result == [(1, 2), (2, 3), (3, 4)]
