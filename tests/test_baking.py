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
        "count": [1, 1, 1, 1, 1, 1, 1, 1]
    })
    return DAG(df).add_edge("a", "b").add_edge("a", "c").add_edge("c", "b")


def test_after_bake_calc_node_still_works(basic_dag):
    basic_dag.cache().calc_node_table("a")


def test_after_bake_no_graph_changes_allowed(basic_dag):
    with pytest.raises(RuntimeError):
        basic_dag.cache().add_edge("d", "e")
