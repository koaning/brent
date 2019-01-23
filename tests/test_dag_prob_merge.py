from pytest import fixture, approx
import pandas as pd

from dagger.common import normalise
from dagger.graph import DAG


@fixture
def basic_dag():
    df = pd.DataFrame({"a": [1, 1, 1, 1, 0, 0, 0, 0],
                       "b": [0, 1, 0, 1, 1, 1, 1, 0],
                       "c": [0, 0, 1, 0, 0, 1, 0, 1],
                       "d": [1, 1, 0, 1, 0, 0, 0, 0],
                       "e": [1, 1, 1, 1, 0, 0, 0, 0]})
    return DAG(df).add_edge("a", "b").add_edge("a", "c").add_edge("c", "b")


def test_marginal_table(basic_dag):
    marginal = (basic_dag.calc_node_table("a")
                .pipe(basic_dag.merge_probs, that_df=basic_dag.calc_node_table("b"))
                .pipe(basic_dag.merge_probs, that_df=basic_dag.calc_node_table("c"))
                .pipe(basic_dag.merge_probs, that_df=basic_dag.calc_node_table("d"))
                .pipe(basic_dag.merge_probs, that_df=basic_dag.calc_node_table("e")))
    assert marginal.equals(basic_dag.marginal_table)


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
