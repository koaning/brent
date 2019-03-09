import re
import logging
from typing import Tuple, List, Iterator

import pandas as pd

from brent.common import join_independent, join_dependent

logger = logging.getLogger(__name__)


PARSER_PATTERNS = {
    'network': r'network (?P<networktype>\w+) {',
    'variable': r"(variable (?P<varname>\w+) {\s+type (?P<vartype>\w+) \[ \d+ \] \{ (?P<states>[^}]*)\}\;)",
    'uncond_probability': r"probability \( (?P<varname>\w+) \) \{\s+table (?P<probtable>[^;]*)",
    'cond_probability': r"probability \( (?P<varname>\w+) \| (?P<conditionals>[^)]*) \) {\s (?P<probs>[^\}]*)",
    'prob_table': r"^(\s+)? \((?P<keys>.*?)\) (?P<probabilities>[^;]*);",
}


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
