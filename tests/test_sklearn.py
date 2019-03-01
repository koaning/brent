import pytest

from brent.sklearn import BrentClassifier
from brent.graph import DAG
from brent.common import make_fake_df


@pytest.fixture
def dag():
    return (DAG(make_fake_df(4))
            .add_edge("a", "d")
            .add_edge("b", "d")
            .add_edge("a", "b")
            .add_edge("b", "c"))


def test_bad_column_raises_error(dag):
    with pytest.raises(ValueError):
        clf = BrentClassifier(dag=dag, to_predict="q")


def test_can_make_prediction(dag):
    df = make_fake_df(4, rows=50)
    mod = BrentClassifier(dag=dag, to_predict="c")
    mod.fit(df, df['c']).predict(df[1:5])
    mod.fit(df, df['c']).predict_proba(df[1:5])