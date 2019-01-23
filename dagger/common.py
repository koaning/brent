import numpy as np
import pandas as pd


def make_fake_df(nodes=6):
    letters = 'abcdefghijklmnopqrstuvwxyz'
    if nodes > 26:
        raise ValueError('only allow 26 letters in the alfabet')
    return pd.DataFrame({k: np.random.randint(0, 2, 100) for k in letters[:nodes]})


def normalise(x):
    return x / x.sum()
