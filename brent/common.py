"""
The `brent.common` module contains common functions that can be
used while working with dataframes and brent graphs. They are also
used internally by the library.
"""
import logging
from itertools import islice

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
    from brent.common import make_fake_df
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
    from brent.common import normalise
    normalise(np.array([1,2,3,4]))
    ```
    """
    if isinstance(x, list):
        x = np.array(x)
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
    from brent.common import quantize_column
    quantize_column(np.array([1,2,3,4]), parts=2)
    ```
    """
    return pd.cut(column, parts, labels=range(1, parts+1))


def window(seq, n=2):
    """
    Calculates a moving window over an iterable.

    ## Inputs
    - **seq**: an iterable sequence
    - **n**: the size of the window, typically this is equal to 2

    ## Example

    ```
    from brent.common import window

    list(window([1,2,3,4), n=2))
    ```
    """
    it = iter(seq)
    result = tuple(islice(it, n))
    if len(result) == n:
        yield result
    for elem in it:
        result = result[1:] + (elem,)
        yield result


def check_node_blocking(arrow_before, arrow_after, name):
    """
    Checks if a node is a blocking node. As a side effects logs can be
    written if you listen to `logging.debug`.

    ## Inputs
    - **arrow_before**: the direction of the arrow before the node
    - **arrow_after**: the direction of the arrow after the node
    - **name**: name of the node in question, if the string "given" is
                in it we will assume that it is given.

    ## Output
    Return `True`/`False`.

    ## Example

    ```
    from brent.common import check_node_blocking

    check_node_blocking("->", "->", "given_a") # True
    check_node_blocking("->", "->", "a") # False
    ```
    """
    given = "given" in name
    if (arrow_before == '<-') and (arrow_after == '->'):
        blocking = True if given else False
        logging.debug(f"checking: ... {arrow_before} {name} {arrow_after} ... type: `split` blocking: {blocking}")
    elif (arrow_before == '->') and (arrow_after == '<-'):
        blocking = False if given else True
        logging.debug(f"checking: ... {arrow_before} {name} {arrow_after} ... type: `collider` blocking: {blocking}")
    elif arrow_before == arrow_after:
        blocking = True if given else False
        logging.debug(f"checking: ... {arrow_before} {name} {arrow_after} ... type: `chain` blocking: {blocking}")
    else:
        raise ValueError(f"check arrow_before/arrow_after now:{arrow_before}, {arrow_after}")
    return blocking


def is_path_blocked(path_list):
    """
    Given a list of nodes and arcs, this function checks if the path is
    probabilistically blocked. We check if the path is blocked between
    the first and last element.

    ## Inputs
    - **path_list**: iterable of node_names (which might have the `given_` prefix
                     to indicate that it is given) which are alternated by arrows
                     ("->" or "<-") indicating the direction of the arcs on the path

    ## Output

    Return `True`/`False`.

    ## Example

    ```
    from brent.common import is_path_blocked

    check_node_blocking(["a", "->", "b", "->", "c") # False
    check_node_blocking(["a", "->", "given_b", "->", "c") # True
    ```
    """
    for idx, name in enumerate(path_list):
        if idx in [0, len(path_list) - 1]:
            pass
        elif name in ['<-', '->']:
            pass
        else:
            arrow_before = path_list[idx - 1]
            arrow_after = path_list[idx + 1]
            blocking = check_node_blocking(arrow_before, arrow_after, name)
            if blocking:
                logging.info("found blocking node, can skip path")
                return True
    return False


def join_independent(this_df: pd.DataFrame, that_df: pd.DataFrame) -> pd.DataFrame:
    """
    Merges two probability dataframes assuming independent nodes

    ## Example:

    ```
    >>> this_df = pd.DataFrame({'A': ['true', 'false'], 'prob': [0.5, 0.5]})
    >>> that_df = pd.DataFrame({'B': ['true', 'false'], 'prob': [0.5, 0.5]})
    >>> join_independent(this_df, that_df) # doctest: +NORMALIZE_WHITESPACE
           A      B  prob
    0   true   true  0.25
    1   true  false  0.25
    2  false   true  0.25
    3  false  false  0.25
    ```
    """
    if 'prob' not in this_df.columns:
        raise ValueError('this_df should contain a `prob` column containing probabilities')
    if 'prob' not in that_df.columns:
        raise ValueError('that_df should contain a `prob` column containing probabilities')

    return (this_df.assign(key=1)
            .merge(that_df.assign(key=1), on='key')
            .drop('key', 1)
            .assign(prob=lambda d: d.prob_x * d.prob_y)
            .drop(columns=['prob_x', 'prob_y'])
            )


def join_dependent(this_df: pd.DataFrame, that_df: pd.DataFrame) -> pd.DataFrame:
    """
    Merges two probability dataframes assuming dependencies between nodes by using that_df's indexes as conditionals.

    If `this_df` denotes `p(A)` in table form and `that_df` denotes `p(B|A)` in table form
    then the output of this function will denote `p(A, B)`.

    `that_df` should have two columns `B` and `prob` and its index should be set to `A`'s values.

    ## Example:

    ```
    >>> this_df = pd.DataFrame({'A': ['true', 'false'], 'prob': [0.5, 0.5]})
    >>> that_df = pd.DataFrame({
    ... 'A': ['true', 'false', 'true', 'false'],
    ... 'B': ['true', 'true', 'false', 'false'],
    ... 'prob': [0.3, 0.7, 0.8, 0.2]}).set_index('A')
    >>> join_dependent(this_df, that_df) # doctest: +NORMALIZE_WHITESPACE
           A      B  prob
    0   true   true  0.15
    0   true  false  0.40
    1  false   true  0.35
    1  false  false  0.10
    ```
    """
    if 'prob' not in this_df.columns:
        raise ValueError('this_df should contain a `prob` column containing probabilities')
    if 'prob' not in that_df.columns:
        raise ValueError('that_df should contain a `prob` column containing probabilities')

    missing_names = [name for name in that_df.index.names if name not in this_df.columns]
    if len(missing_names) > 0:
        raise ValueError('missing_names are set as indexes to `that_df` but are not present in `this_df`')

    if len(that_df.columns) > 2:
        raise ValueError('`that_df` has more than two columns, perhaps you forgot to set the variables that '
                         'are to be conditioned on as the index of the dataframe')

    return (this_df
            .merge(that_df, left_on=that_df.index.names, right_index=True)
            .assign(prob=lambda d: d.prob_x * d.prob_y)
            .drop(columns=['prob_x', 'prob_y'])
            .reset_index(drop=True)
            )
