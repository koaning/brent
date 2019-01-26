import pytest

from dagger.graph import DAG
from dagger.query import Query
from dagger.common import make_fake_df


@pytest.fixture
def dag():
    return (DAG(make_fake_df(7))
            .add_edge("e", "a")
            .add_edge("e", "d")
            .add_edge("a", "d")
            .add_edge("b", "d")
            .add_edge("a", "b")
            .add_edge("a", "c")
            .add_edge("b", "c")
            .add_edge("c", "f")
            .add_edge("g", "f"))


def test_basic_query_creation(dag):
    query = Query(dag).do(a=1).given(b=0)
    assert query.do_dict['a'] == 1
    assert query.given_dict['b'] == 0


def test_throwing_of_errors_1(dag):
    with pytest.raises(ValueError):
        Query(dag).given(b=2)


def test_throwing_of_errors_2(dag):
    with pytest.raises(ValueError):
        Query(dag).do(q=1)


def test_throwing_of_errors_3(dag):
    with pytest.raises(ValueError):
        Query(dag).do(a=1).given(a=0)


def test_throwing_of_errors_4(dag):
    with pytest.raises(ValueError):
        Query(dag).given(a=0).do(a=1)
