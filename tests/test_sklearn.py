import pytest

from brent.sklearn import BrentClassifier
from brent.graph import DAG
from brent.common import make_fake_df


@pytest.fixture
def dag_with_two_values():
    return (DAG(make_fake_df(nodes=4))
            .add_edge("a", "d")
            .add_edge("b", "d")
            .add_edge("a", "b")
            .add_edge("b", "c"))


@pytest.fixture
def dag_with_four_values():
    return (DAG(make_fake_df(nodes=4, rows=2000, values=4))
            .add_edge("a", "d")
            .add_edge("b", "d")
            .add_edge("a", "b")
            .add_edge("b", "c"))


def test_bad_column_raises_error(dag_with_two_values):
    with pytest.raises(ValueError):
        BrentClassifier(dag=dag_with_two_values, to_predict="q")


def test_can_make_prediction_1(dag_with_two_values):
    df = make_fake_df(4, rows=50)
    mod = BrentClassifier(dag=dag_with_two_values, to_predict="c")
    assert mod.fit(df, df['c']).predict_proba(df[:4]).shape == (4, 2)
    assert mod.fit(df, df['c']).predict_proba(df[:15]).shape == (15, 2)


def test_can_make_prediction_2(dag_with_four_values):
    df = make_fake_df(nodes=4, rows=2000, values=4)
    mod = BrentClassifier(dag=dag_with_four_values, to_predict="c")
    assert mod.fit(df, df['c']).predict_proba(df[:4]).shape == (4, 4)
    assert mod.fit(df, df['c']).predict_proba(df[:15]).shape == (15, 4)
