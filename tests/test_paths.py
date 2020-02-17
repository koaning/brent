import pandas as pd
import pytest

from brent.graph import DAG


@pytest.fixture
def basic_dag():
    df = pd.DataFrame({
        "a": [1, 1, 1, 1, 0, 0, 0, 0],
        "b": [0, 1, 0, 1, 1, 1, 1, 0],
        "c": [0, 0, 1, 0, 0, 1, 0, 1],
        "d": [1, 1, 0, 1, 0, 0, 0, 0],
        "e": [1, 1, 1, 1, 0, 0, 0, 0],
        "count": [1, 1, 1, 1, 1, 1, 1, 1],
    })
    return DAG(df)


def test_find_undirected_paths_1(basic_dag):
    dag = (basic_dag
           .add_edge("a", "b")
           .add_edge("b", "c")
           .add_edge("c", "d")
           .add_edge("d", "e"))
    assert len(dag.undirected_paths("a", "e")) == 1
    assert len(dag.undirected_paths("e", "a")) == 1


def test_find_undirected_paths_2(basic_dag):
    dag = (basic_dag
           .add_edge("a", "b")
           .add_edge("b", "c")
           .add_edge("c", "d")
           .add_edge("d", "e")
           .add_edge("a", "e")
           .add_edge("b", "e"))
    assert len(dag.undirected_paths("a", "e")) == 3
    assert len(dag.undirected_paths("e", "a")) == 3


def test_find_undirected_paths_3(basic_dag):
    dag = (basic_dag
           .add_edge("a", "b")
           .add_edge("b", "c")
           .add_edge("c", "d"))
    assert len(dag.undirected_paths("a", "e")) == 0
    assert len(dag.undirected_paths("e", "a")) == 0
    assert len(dag.undirected_paths("d", "a")) == 1


def test_path_direction_1(basic_dag):
    dag = (basic_dag
           .add_edge("a", "b")
           .add_edge("b", "c"))
    assert dag.edge_direction("a", "b") == "->"
    assert dag.edge_direction("b", "a") == "<-"


def test_path_direction_2(basic_dag):
    dag = (basic_dag
           .add_edge("a", "b")
           .add_edge("b", "c"))
    with pytest.raises(ValueError):
        assert dag.edge_direction("a", "e")
    with pytest.raises(ValueError):
        assert dag.edge_direction("a", "c")
