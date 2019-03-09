import pandas as pd
import pytest

from brent import DAG
from brent import Query, SupposeQuery


@pytest.fixture
def simple_dag():
    df = pd.DataFrame({"a": [1, 1, 1, 1, 0, 0, 0, 0],
                       "b": [0, 1, 0, 1, 1, 1, 1, 0],
                       "c": [0, 0, 1, 0, 0, 1, 0, 1]})
    return DAG(df).add_edge("a", "b").add_edge("a", "c").add_edge("c", "b")


def test_value_error_with_when_twice(simple_dag):
    q = Query(dag=simple_dag).given(b=1)
    with pytest.raises(ValueError):
        SupposeQuery(dag=simple_dag).when(q).when(q)


def test_value_error_double_keys(simple_dag):
    q = Query(dag=simple_dag).given(b=1)
    with pytest.raises(ValueError):
        SupposeQuery(dag=simple_dag).when(q).suppose_do(a=1).suppose_given(a=0)


def test_value_error_wrong_value(simple_dag):
    q = Query(dag=simple_dag).given(b=1)
    with pytest.raises(ValueError):
        SupposeQuery(dag=simple_dag).when(q).suppose_do(a=1000)


def test_value_error_wrong_key(simple_dag):
    q = Query(dag=simple_dag).given(b=1)
    with pytest.raises(ValueError):
        SupposeQuery(dag=simple_dag).when(q).suppose_do(foobar=1)


def test_value_error_inference_no_when(simple_dag):
    with pytest.raises(ValueError):
        SupposeQuery(dag=simple_dag).infer()


# def test_empty_when_equals_query(simple_dag):
#     # TODO: this is a test that needs to be adressed!
#     q1 = Query(dag=simple_dag)
#     q2 = Query(dag=simple_dag).given(b=1)
#     s = SupposeQuery(dag=simple_dag).when(q1).suppose_given(b=1)
#     assert q2.infer() == s.infer()
