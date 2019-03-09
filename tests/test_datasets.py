import pytest
from brent.datasets import *


@pytest.mark.parametrize("dataset", [alarm_dataset, asian_cancer_dataset, blue_baby_dataset, simple_study_dataset])
def test_datasets_load(dataset):
    assert isinstance(dataset(), pd.DataFrame)
