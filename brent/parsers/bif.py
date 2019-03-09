import re
import logging
from typing import Tuple, List, Iterator

import pandas as pd

logger = logging.getLogger(__name__)


PARSER_PATTERNS = {
    'network': r'network (?P<networktype>\w+) {',
    'variable': r"(variable (?P<varname>\w+) {\s+type (?P<vartype>\w+) \[ \d+ \] \{ (?P<states>[^}]*)\}\;)",
    'uncond_probability': r"probability \( (?P<varname>\w+) \) \{\s+table (?P<probtable>[^;]*)",
    'cond_probability': r"probability \( (?P<varname>\w+) \| (?P<conditionals>[^)]*) \) {\s (?P<probs>[^\}]*)",
    'prob_table': r"^(\s+)? \((?P<keys>.*?)\) (?P<probabilities>[^;]*);",
}


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


def parse_network_type(bif: str) -> str:
    """Returns the network type of a bif string"""
    return re.match(PARSER_PATTERNS['network'], bif).group('networktype')


def parse_variables(bif: str) -> Iterator[Tuple[str, List[str]]]:
    """Returns a generator of `(varname, states)` tuples from a bif string"""
    for var in re.finditer(PARSER_PATTERNS['variable'], bif):
        varname = var.group('varname')
        vartype = var.group('vartype')
        states = var.group('states').strip().split(', ')

        logger.info(f'Found variable: {varname} with states {states}')
        if vartype != 'discrete':
            raise ValueError('Brent only supports discrete variables')

        yield varname, states


def parse_unconditional_probabilities(bif: str) -> Iterator[Tuple[str, List[float]]]:
    """Parses unconditional probabilities from a bif string"""
    for prob in re.finditer(PARSER_PATTERNS['uncond_probability'], bif):
        varname = prob.group('varname')
        probs = [float(p) for p in prob.group('probtable').split(', ')]

        logger.info(f'Found base probability for variable {varname}: {probs}')
        if 1 - sum(probs) > 0.01:
            logger.warning(f'Variable {varname} has probabilities not summing to 1 (sums to {sum(probs)})')

        yield varname, probs


def parse_conditional_probabilities(bif: str):
    """parses conditional probabilities from a bif string"""
    for cond_prob in re.finditer(PARSER_PATTERNS['cond_probability'], bif):
        varname, prob_table = cond_prob.group('varname'), cond_prob.group('probs')
        conditionals = cond_prob.group('conditionals').split(', ')
        logger.info(f'Found conditional probability: {varname} | {conditionals}')

        probabilities_lst = []

        for line_no, prob_entry in enumerate(re.finditer(PARSER_PATTERNS['prob_table'], prob_table, re.MULTILINE)):
            keys = prob_entry.group('keys').split(', ')
            probabilities = [float(p) for p in prob_entry.group('probabilities').split(', ')]
            if 1 - sum(probabilities) > 0.01:
                logger.warning(f'Variable {varname} | {conditionals} has probabilities not summing to 1 '
                               f'in line {line_no + 1} (sums to {sum(probabilities)})')

            logger.info(f'\t{keys} - {probabilities}')
            probabilities_lst.append((keys + probabilities))

        yield varname, conditionals, probabilities_lst


def bif(bif: str) -> Tuple[pd.DataFrame, List[Tuple[str, str]]]:
    """
    Parses a Bayesian Interchange Format (bif) string into a probability table and a set of links
    """
    probability_table = pd.DataFrame({'key': [1], 'prob': [1]})

    if parse_network_type(bif) != 'unknown':
        logger.warning("BIF Parser does not take into account known networks")

    variable_states = dict(parse_variables(bif))
    edges = []

    for varname, probs in parse_unconditional_probabilities(bif):
        var_df = pd.DataFrame({varname: variable_states[varname], 'prob': probs})
        probability_table = join_independent(probability_table, var_df)

    for varname, conditionals, probabilities in parse_conditional_probabilities(bif):
        cond_df = (pd.DataFrame(probabilities, columns=conditionals + variable_states[varname])
                   .melt(id_vars=conditionals, var_name=varname, value_name='prob')
                   .set_index(conditionals)
                   )
        probability_table = join_dependent(probability_table, cond_df)
        edges += [(conditional, varname) for conditional in conditionals]

    return probability_table, edges
