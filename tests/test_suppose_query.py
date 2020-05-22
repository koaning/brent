import pandas as pd
import pytest

from brent import DAG, Query, SupposeQuery
from brent.datasets import simple_study_dataset

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


def test_empty_when_equals_query(simple_dag):
    q = Query(dag=simple_dag)
    s1 = SupposeQuery(dag=simple_dag).when(q)
    s2 = SupposeQuery(dag=simple_dag).when(q).suppose_given(a=1)
    assert s1.infer()['b'] == s2.infer()['b']


def test_student_example():
    dag = (DAG(dataframe=simple_study_dataset())
           .add_edge("study", "grade")
           .add_edge("hard", "grade"))
    q = Query(dag).given(study="lots", grade="pass")
    sp = SupposeQuery(dag).when(q).suppose_given(study="little")
    assert q.infer()['hard']['yes'] == pytest.approx(sp.infer()['hard']['yes'], abs=0.001)
    assert q.infer()['hard']['no'] == pytest.approx(sp.infer()['hard']['no'], abs=0.001)
