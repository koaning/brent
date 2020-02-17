import pandas as pd
import pytest

from brent.common import make_fake_df
from brent.graph import DAG
from brent.query import Query


@pytest.fixture
def dag():
    return (DAG.from_observations(make_fake_df(7))
            .add_edge("e", "a")
            .add_edge("e", "d")
            .add_edge("a", "d")
            .add_edge("b", "d")
            .add_edge("a", "b")
            .add_edge("a", "c")
            .add_edge("b", "c")
            .add_edge("c", "f")
            .add_edge("g", "f"))


@pytest.fixture
def simple_dag():
    df = pd.DataFrame({
        "a": [1, 1, 1, 1, 0, 0, 0, 0],
        "b": [0, 1, 0, 1, 1, 1, 1, 0],
        "c": [0, 0, 1, 0, 0, 1, 0, 1],
        "count": [1, 1, 1, 1, 1, 1, 1, 1],
    })
    return DAG(df).add_edge("a", "b").add_edge("a", "c").add_edge("c", "b")


def test_basic_query_creation_1(dag):
    query = Query(dag).do(a=1).given(b=0)
    assert query.do_dict['a'] == 1
    assert query.given_dict['b'] == 0


def test_basic_query_creation_2(dag):
    query = Query(dag).do(a=0).given(b=1)
    assert query.do_dict['a'] == 0
    assert query.given_dict['b'] == 1


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


def test_inference_dag_copies_correct_parents_1(dag):
    q = Query(dag)
    for node in dag.nodes:
        assert q.inference_dag().parents(node) == dag.parents(node)


def test_inference_dag_copies_correct_parents_2(simple_dag):
    q = Query(simple_dag)
    for node in simple_dag.nodes:
        assert q.inference_dag().parents(node) == simple_dag.parents(node)


def test_expected_output_query1(simple_dag):
    output = Query(simple_dag).given(a=0).infer()
    assert output["b"][0] == pytest.approx(0.25, abs=0.001)
    assert output["b"][1] == pytest.approx(0.75, abs=0.001)


def test_expected_output_query2(simple_dag):
    output = Query(simple_dag).given(a=1).infer()
    assert output["b"][0] == pytest.approx(0.50, abs=0.001)
    assert output["b"][1] == pytest.approx(0.50, abs=0.001)


def test_expected_output_query3(simple_dag):
    output = Query(simple_dag).do(b=1).infer()
    assert output["b"][1] == pytest.approx(1.0, abs=0.001)
    assert output["a"][0] == pytest.approx(0.5, abs=0.001)
    assert output["a"][1] == pytest.approx(0.5, abs=0.001)


@pytest.mark.parametrize("n", [100, 1000, 10000])
def test_query_sample_1(simple_dag, n):
    q1 = Query(simple_dag).given(a=1)
    assert q1.sample(n)["a"].sum() == n
    q0 = Query(simple_dag).given(a=0)
    assert q0.sample(n)["a"].sum() == 0
