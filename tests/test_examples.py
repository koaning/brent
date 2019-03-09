import pytest
from brent.examples import *


def test_risk_dag_error():
    with pytest.raises(ValueError):
        generate_risk_dag(attackers=2, defenders=2, battle_size=3)
