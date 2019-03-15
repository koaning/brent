import pandas as pd
import pytest

from brent import parsers
from brent.parsers.bif import parse_network_type, parse_variables, \
    parse_unconditional_probabilities, parse_conditional_probabilities


@pytest.fixture
def test_bif():
    return """network unknown {
}
variable A {
  type discrete [ 2 ] { yes, no };
}
variable B {
  type discrete [ 2 ] { yes, no };
}
variable C {
  type discrete [ 2 ] { yes, no };
}
variable D {
  type discrete [ 2 ] { yes, no };
}
probability ( A ) {
  table 0.01, 0.99;
}
probability ( C | B ) {
  (yes) 0.05, 0.95;
  (no) 0.01, 0.99;
}
probability ( B ) {
  table 0.5, 0.5;
}
probability ( D | B, A ) {
  (yes, yes) 1.0, 0.0;
  (no, yes) 1.0, 0.0;
  (yes, no) 1.0, 0.0;
  (no, no) 0.0, 1.0;
}
"""


def test_parse(test_bif):
    probability_df, links = parsers.bif(test_bif)

    target = pd.DataFrame({
        'A': ['yes', 'yes', 'yes', 'yes', 'no', 'no', 'no', 'no', 'yes', 'yes', 'yes', 'yes', 'no', 'no', 'no', 'no'],
        'B': ['yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no'],
        'C': ['yes', 'yes', 'no', 'no', 'yes', 'yes', 'no', 'no', 'yes', 'yes', 'no', 'no', 'yes', 'yes', 'no', 'no'],
        'D': ['yes', 'no', 'yes', 'no', 'yes', 'no', 'yes', 'no', 'yes', 'no', 'yes', 'no', 'yes', 'no', 'yes', 'no'],
        'prob': [0.00025, 0.0, 0.00475, 0.0, 0.02475, 0.0, 0.47025, 0.0, 5e-05, 0.0, 0.00495, 0.0, 0.0, 0.00495, 0.0,
                 0.49005]
    })

    pd.testing.assert_frame_equal(probability_df, target)
    target_links = [
        ('A', 'D'),
        ('B', 'D'),
        ('B', 'C'),
    ]
    assert sorted(links) == sorted(target_links)


def test_parse_network_type(test_bif):
    assert parse_network_type(test_bif) == 'unknown'


def test_parse_variables(test_bif):
    target = [
        ('A', ['yes', 'no']),
        ('B', ['yes', 'no']),
        ('C', ['yes', 'no']),
        ('D', ['yes', 'no']),
    ]
    assert list(parse_variables(test_bif)) == target


def test_parse_unconditional_variables(test_bif):
    target = [
        ('A', [0.01, 0.99]),
        ('B', [0.5, 0.5]),
    ]
    assert list(parse_unconditional_probabilities(test_bif)) == target


def test_parse_conditional_variables(test_bif):
    target = [
        ('C', ['B'], [
            ['yes', 0.05, 0.95],
            ['no', 0.01, 0.99]
        ]),
        ('D', ['B', 'A'], [
            ['yes', 'yes', 1.0, 0.0],
            ['no', 'yes', 1.0, 0.0],
            ['yes', 'no', 1.0, 0.0],
            ['no', 'no', 0.0, 1.0]
        ]),
    ]
    assert list(parse_conditional_probabilities(test_bif)) == target
