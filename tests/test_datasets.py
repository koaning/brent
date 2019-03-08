import pandas as pd
from brent.datasets import *


def test_datasets_load():
    for d in [alarm_dataset, asian_cancer_dataset, blue_baby_dataset, simple_study_dataset]:
        assert isinstance(d(), pd.DataFrame)
