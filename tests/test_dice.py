import pytest
from brent.games import Dice


def test_addition_1():
    d = Dice.from_string("11223")
    assert (d + 1).exp == pytest.approx((1 + d).exp, abs=0.001)
    assert (d + 1).var == pytest.approx((1 + d).var, abs=0.001)


def test_addition_2():
    d = Dice.from_string("11223")
    assert (d + 2 * d).exp == pytest.approx((3 * d).exp, abs=0.001)


def test_addition_3():
    d1 = Dice.from_string("11223")
    d2 = Dice.from_string("11223")
    assert (d1 + d2).exp == pytest.approx((d1 * 2).exp, abs=0.001)
