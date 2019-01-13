import pandas as pd

from dagger.graph import DAG, _nodes_to_handle


def test_origin_nodes_1():
    df = pd.DataFrame({"a": [1, 0, 1, 0, 1], "b": [1, 1, 1, 0, 0], "c": [0, 0, 1, 0, 1]})
    dag = DAG(df).add_edge("a", "b").add_edge("b", "c").add_edge("a", "c")
    assert dag.origin_nodes == ("a",)


def test_origin_nodes_2():
    df = pd.DataFrame({"a": [1, 0, 1, 0, 1], "b": [1, 1, 1, 0, 0], "c": [0, 0, 1, 0, 1]})
    dag = DAG(df).add_edge("a", "b").add_edge("c", "b")
    assert dag.origin_nodes == ("a", "c")


def test_nodes_to_handle1():
    df = pd.DataFrame({"a": [1, 0, 1, 0, 1], "b": [1, 1, 1, 0, 0], "c": [0, 0, 1, 0, 1]})
    dag = DAG(df).add_edge("a", "b").add_edge("b", "c").add_edge("a", "c")
    assert _nodes_to_handle(dag, nodes_done=[]) == ("a",)
    assert _nodes_to_handle(dag, nodes_done=["a"]) == ("b",)
    assert _nodes_to_handle(dag, nodes_done=["a", "b"]) == ("c",)


def test_nodes_to_handle2():
    df = pd.DataFrame({"a": [1, 0, 1, 0, 1], "b": [1, 1, 1, 0, 0], "c": [0, 0, 1, 0, 1]})
    dag = DAG(df).add_edge("a", "b").add_edge("c", "b")
    assert _nodes_to_handle(dag, nodes_done=[]) == ("a", "c",)
    # make sure we get all root nodes before moving a layer deeper
    assert _nodes_to_handle(dag, nodes_done=["a"]) == ("c",)
    assert _nodes_to_handle(dag, nodes_done=["c"]) == ("a",)
    assert _nodes_to_handle(dag, nodes_done=["a", "c"]) == ("b",)
