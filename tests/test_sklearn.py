import pytest

from brent.sklearn import BrentClassifier
from brent.graph import DAG
from brent.common import make_fake_df


@pytest.fixture
def dag():
    return (DAG(make_fake_df(7))
            .add_edge("e", "a")
            .add_edge("e", "d")
            .add_edge("a", "d")
            .add_edge("b", "d")
            .add_edge("a", "b")
            .add_edge("a", "c")
            .add_edge("b", "c")
            .add_edge("c", "f")
            .add_edge("g", "f"))


def test_bad_column_raises_error(dag):
    with pytest.raises(ValueError):
        clf = BrentClassifier(dag=dag, to_predict="q")
