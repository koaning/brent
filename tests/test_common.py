import pytest

from brent.common import window, normalise, check_node_blocking


def test_window():
    result = list(window([1, 2, 3, 4], n=2))
    assert result == [(1, 2), (2, 3), (3, 4)]


def test_normalise():
    assert normalise([1, 1]).sum() == pytest.approx(1, abs=0.0001)
    assert normalise([1, 1, 4]).sum() == pytest.approx(1, abs=0.0001)


def test_check_node_blocking_chain():
    assert not check_node_blocking(arrow_before='->', name='a', arrow_after='->')
    assert check_node_blocking(arrow_before='->', name='given_a', arrow_after='->')
    assert not check_node_blocking(arrow_before='<-', name='a', arrow_after='<-')
    assert check_node_blocking(arrow_before='<-', name='given_a', arrow_after='<-')


def test_check_node_blocking_split():
    assert not check_node_blocking(arrow_before='<-', name='a', arrow_after='->')
    assert check_node_blocking(arrow_before='<-', name='given_a', arrow_after='->')


def test_check_node_blocking_collider():
    assert check_node_blocking(arrow_before='->', name='a', arrow_after='<-')
    assert not check_node_blocking(arrow_before='->', name='given_a', arrow_after='<-')
