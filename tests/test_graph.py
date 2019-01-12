import pandas as pd
import networkx as nx

from dagger.graph import DAG, _calc_prior_discrete, _nodes_to_handle


def test_origin_nodes_1():
    df = pd.DataFrame({"a": [1, 0, 1, 0, 1], "b": [1, 1, 1, 0, 0], "c": [0, 0, 1, 0, 1]})
    dag = DAG(df).add_edge("a", "b").add_edge("b", "c").add_edge("a", "c")
    assert dag.origin_nodes == ("a",)


def test_origin_nodes_2():
    df = pd.DataFrame({"a": [1, 0, 1, 0, 1], "b": [1, 1, 1, 0, 0], "c": [0, 0, 1, 0, 1]})
    dag = DAG(df).add_edge("a", "b").add_edge("c", "b")
    assert dag.origin_nodes == ("a", "c")


# def test_calc_prior_discrete():
#     df = pd.DataFrame({"a": [1, 0, 1, 0, 1], "b": [1, 1, 1, 0, 0], "c": [0, 0, 0, 0, 1]})
#     p_dict = _calc_prior_discrete(df, "a")["p"]
#     assert p_dict[0] == 0.4
#     assert p_dict[1] == 0.6
#     p_dict = _calc_prior_discrete(df, "c").to_dict()["p"]
#     assert p_dict[0] == 0.8
#     assert p_dict[1] == 0.2


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
    assert _nodes_to_handle(dag, nodes_done=["a"]) == ("c",)
    assert _nodes_to_handle(dag, nodes_done=["c"]) == ("a",)
    assert _nodes_to_handle(dag, nodes_done=["a", "c"]) == ("b",)
