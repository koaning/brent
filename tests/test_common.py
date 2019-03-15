import pandas as pd
import pytest

from brent.common import window, normalise, check_node_blocking, join_independent, join_dependent


@pytest.fixture
def prob_a():
    return pd.DataFrame({'A': ['true', 'false'], 'prob': [0.5, 0.5]})


@pytest.fixture
def prob_b():
    return pd.DataFrame({'B': ['true', 'false'], 'prob': [0.5, 0.5]})


@pytest.fixture
def cond_prob_b():
    return pd.DataFrame({
        'A': ['true', 'false', 'true', 'false'],
        'B': ['true', 'true', 'false', 'false'],
        'prob': [0.3, 0.7, 0.8, 0.2]}).set_index('A')


def test_window():
    result = list(window([1, 2, 3, 4], n=2))
    assert result == [(1, 2), (2, 3), (3, 4)]


def test_normalise():
    assert normalise([1, 1]).sum() == pytest.approx(1, abs=0.0001)
    assert normalise([1, 1, 4]).sum() == pytest.approx(1, abs=0.0001)


def test_check_node_blocking_chain():
    assert not check_node_blocking(arrow_before='->', name='a', arrow_after='->')
    assert check_node_blocking(arrow_before='->', name='given_a', arrow_after='->')
    assert not check_node_blocking(arrow_before='<-', name='a', arrow_after='<-')
    assert check_node_blocking(arrow_before='<-', name='given_a', arrow_after='<-')


def test_check_node_blocking_split():
    assert not check_node_blocking(arrow_before='<-', name='a', arrow_after='->')
    assert check_node_blocking(arrow_before='<-', name='given_a', arrow_after='->')


def test_check_node_blocking_collider():
    assert check_node_blocking(arrow_before='->', name='a', arrow_after='<-')
    assert not check_node_blocking(arrow_before='->', name='given_a', arrow_after='<-')


def test_join_independent(prob_a, prob_b):
    target = pd.DataFrame({
        'A': ['true', 'true', 'false', 'false'],
        'B': ['true', 'false', 'true', 'false'],
        'prob': [0.25, 0.25, 0.25, 0.25]
    })
    pd.testing.assert_frame_equal(join_independent(prob_a, prob_b), target)


def test_join_independent_input_checks(prob_a, prob_b):
    with pytest.raises(ValueError):
        join_independent(prob_a.drop(columns=['prob']), prob_b)

    with pytest.raises(ValueError):
        join_independent(prob_a, prob_b.drop(columns=['prob']))


def test_join_dependent(prob_a, cond_prob_b):
    target = pd.DataFrame({
        'A': ['true', 'true', 'false', 'false'],
        'B': ['true', 'false', 'true', 'false'],
        'prob': [0.15, 0.4, 0.35, 0.1]
    })
    pd.testing.assert_frame_equal(join_dependent(prob_a, cond_prob_b), target)


def test_join_dependent_input_checks(prob_a, cond_prob_b):
    with pytest.raises(ValueError):
        join_dependent(prob_a.drop(columns=['prob']), cond_prob_b)

    with pytest.raises(ValueError):
        join_dependent(prob_a, cond_prob_b.drop(columns=['prob']))

    with pytest.raises(ValueError):
        join_dependent(prob_a.drop(columns=['A']), cond_prob_b)

    with pytest.raises(ValueError):
        join_dependent(prob_a, cond_prob_b.reset_index())
