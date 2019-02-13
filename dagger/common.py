"""
The `dagger.common` module contains common functions that can be
used while working with dataframes and dagger graphs. They are also
used internally by the library.
"""

import numpy as np
import pandas as pd


def make_fake_df(nodes=6, rows=100, values=2, seed=42):
    """
    Creates a fake and random dataframe that can be used for demos.

    ## Inputs:

    - **nodes**: the number of nodes/variables to be generated
    - **rows**: the number of rows of fake data to generate
    - **values**: the different values that the variables can take
    - **seed**: the seed value for the random numbers to be generated

    ## Example

    ```
    from dagger.common import make_fake_df
    # let's start with a new dataset
    df = make_fake_df(nodes=4, rows=1000, values=4, seed=41)
    ```
    """
    letters = 'abcdefghijklmnopqrstuvwxyz'
    np.random.seed(seed)
    if nodes > 26:
        raise ValueError('only allow 26 letters in the alfabet')
    return pd.DataFrame({k: np.random.randint(0, values, rows) for k in letters[:nodes]})


def normalise(x):
    """
    Simply normalises a numpy-like array or pandas-series.

    ## Inputs
    - **x**: a numpy array of pandas series

    ## Example

    ```
    import numpy as np
    from dagger.common import normalise
    normalise(np.array([1,2,3,4]))
    ```
    """
    return x / x.sum()


def quantize_column(column, parts=4):
    """
    Turns a continous dataset into a discrete one by splitting
    it into quantiles.

    ## Inputs
    - **column**: a numpy array of pandas series
    - **parts**: the number of parts to split the data into

    ## Example

    ```
    import numpy as np
    from dagger.common import quantize_column
    quantize_column(np.array([1,2,3,4]), parts=2)
    ```
    """
    return pd.cut(column, parts, labels=range(1, parts+1))
