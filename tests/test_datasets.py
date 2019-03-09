import pytest
from brent.datasets import *


def test_datasets_load():
    for d in [alarm_dataset, asian_cancer_dataset, blue_baby_dataset, simple_study_dataset]:
        assert isinstance(d(), pd.DataFrame)


def test_risk_dataset_error():
    with pytest.raises(ValueError):
        generate_risk_dataset(attackers=2, defenders=2, battle_size=3)
