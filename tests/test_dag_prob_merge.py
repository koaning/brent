import pandas as pd
import pytest
from pytest import fixture, approx

from brent.common import normalise
from brent.graph import DAG


@fixture
def basic_dag():
    df = pd.DataFrame({
        "a": [1, 1, 1, 1, 0, 0, 0, 0],
        "b": [0, 1, 0, 1, 1, 1, 1, 0],
        "c": [0, 0, 1, 0, 0, 1, 0, 1],
        "d": [1, 1, 0, 1, 0, 0, 0, 0],
        "e": [1, 1, 1, 1, 0, 0, 0, 0],
        "count": [1, 1, 1, 1, 1, 1, 1, 1],
    })
    return DAG(df).add_edge("a", "b").add_edge("a", "c").add_edge("c", "b")


def test_marginal_table(basic_dag):
    colnames = ["a", "b", "c", "d", "e"]
    marginal = (basic_dag.calc_node_table("a")
                .pipe(basic_dag.merge_probs, that_df=basic_dag.calc_node_table("b"))
                .pipe(basic_dag.merge_probs, that_df=basic_dag.calc_node_table("c"))
                .pipe(basic_dag.merge_probs, that_df=basic_dag.calc_node_table("d"))
                .pipe(basic_dag.merge_probs, that_df=basic_dag.calc_node_table("e")))
    a = marginal.sort_values(colnames).reset_index()[colnames + ["prob"]]
    b = basic_dag.marginal_table.sort_values(colnames).reset_index()[colnames + ["prob"]]

    pd.testing.assert_frame_equal(a, b)


def test_marginal_table_values(basic_dag):
    tbl = basic_dag.marginal_table
    dict_a = tbl.groupby("a").sum()["prob"].to_dict()
    assert dict_a == {0: approx(0.5, abs=0.001), 1: approx(0.5, abs=0.001)}
    dict_b = tbl.groupby("b").sum()["prob"].to_dict()
    assert dict_b == {0: approx(0.375, abs=0.001), 1: approx(0.625, abs=0.001)}


def test_calc_node_table(basic_dag):
    assert set(basic_dag.calc_node_table("a").columns) == {"a", "prob"}
    assert set(basic_dag.calc_node_table("b").columns) == {"a", "b", "c", "prob"}
    assert set(basic_dag.calc_node_table("c").columns) == {"a", "c", "prob"}
    assert set(basic_dag.calc_node_table("d").columns) == {"d", "prob"}
    assert set(basic_dag.calc_node_table("e").columns) == {"e", "prob"}


def test_merge_probs_simple(basic_dag):
    res1 = (basic_dag.marginal_table
        .groupby(['d'])['prob'].mean()
        .reset_index()
        .assign(prob=lambda d: normalise(d.prob))
        .to_dict("list")["prob"])
    assert res1[0] == approx(.625, abs=0.01)
    assert res1[1] == approx(.375, abs=0.01)

    res2 = (basic_dag.marginal_table
        .groupby(['e'])['prob'].mean()
        .reset_index()
        .assign(prob=lambda d: normalise(d.prob))
        .to_dict("list")["prob"])
    assert res2[0] == approx(.5, abs=0.01)
    assert res2[1] == approx(.5, abs=0.01)

    res3 = (basic_dag.marginal_table
        .groupby(['a'])['prob'].mean()
        .reset_index()
        .assign(prob=lambda d: normalise(d.prob))
        .to_dict("list")["prob"])
    assert res3[0] == approx(.5, abs=0.01)
    assert res3[1] == approx(.5, abs=0.01)


def test_node_table_throws_value_error(basic_dag):
    with pytest.raises(ValueError):
        basic_dag.calc_node_table("z")


def test_after_bake_calc_node_still_works(basic_dag):
    basic_dag.cache().calc_node_table("a")
