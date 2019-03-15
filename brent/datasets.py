"""
The `brent.datasets` module contains functions that will generate
datasets. Typically these datasets are meant for educational purposes.

Don't forget to see the docstring for a reference to the origin of the
dataset.
"""

import itertools as it
from functools import reduce

import pandas as pd
import numpy as np


def simple_study_dataset():
    """
    Creates a simple dataset that simulates the probability of passing
    a course given if the test for the course was hard and weather or
    not a student studied. This is a fake dataset.
    """
    grade = ["good", "pass", "fail"]
    study = ["lots", "little", "no"]
    hard = ["yes", "no"]
    probs = [0.6, 0.3, 0.1,
             0.9, 0.09, 0.01,
             0.3, 0.3, 0.4,
             0.6, 0.2, 0.2,
             0.1, 0.3, 0.6,
             0.1, 0.5, 0.4]
    zipprod = zip(it.product(study, hard, grade), probs)
    tween = reduce(lambda a, b: a + b, [[c] * int(p * 100) for c, p in zipprod])
    return pd.DataFrame(tween, columns=["study", "hard", "grade"])


def simple_sickness():
    """
    Inspiration of the data: https://www.cdc.gov/flu/about/qa/coldflu.htm.
           cold  flu  none astma
    sneeze sure   na  sure   bit
    cough   bit  yep  sure   yep
    weak   sure  yep    na   bit
    nose    yep sure  sure   bit
    chills   na  yep    na   bit
    tired  sure  yes  sure   yep
    """
    raise NotImplementedError("not yet implemented")


def asian_cancer_dataset():
    """
    This function reads in the asian cancer dataset. It is a dataset
    that has orignally also been featured in the `bnlearn` package. It
    is simulated data but has been used historically in benchmarks.

    The original description to the dataset can be found here:
    http://www.bnlearn.com/bnrepository/discrete-small.html#cancer

    ## Reference

    S. Lauritzen, D. Spiegelhalter. Local Computation with Probabilities on
    Graphical Structures and their Application to Expert Systems (with discussion).
    Journal of the Royal Statistical Society: Series B (Statistical Methodology),
    50(2):157-224, 1988.
    """
    return pd.read_csv("http://www.ccd.pitt.edu/wiki/images/ASIA10k.csv")


def alarm_dataset():
    """
    This function reads in the alarm dataset which has historically been
    used to describe alarms for monitoring stations for anesthesia.
    It is a dataset that has orignally also been featured in the `bnlearn` package.
    It is simulated data but has been used historically in benchmarks.

    The original description to the dataset can be found here:
    http://www.bnlearn.com/bnrepository/discrete-medium.html#alarm

    ## Reference:
    I. A. Beinlich, H. J. Suermondt, R. M. Chavez, and G. F. Cooper.
    The ALARM Monitoring System: A Case Study with Two Probabilistic Inference
    Techniques for Belief Networks. In Proceedings of the 2nd European Conference
    on Artificial Intelligence in Medicine, pages 247-256. Springer-Verlag, 1989.
    """
    return pd.read_csv("http://www.ccd.pitt.edu/wiki/images/ALARM10k.csv")


def blue_baby_dataset():
    """
    This function reads in the blue baby dataset. It involves a
    network for diagnosing congenital heart disease in a new born "blue baby".
    It is a dataset that has orignally also been featured in the `bnlearn` package.
    It is simulated data but has been used historically in benchmarks.

    The original description to the dataset can be found here:
    http://www.bnlearn.com/bnrepository/discrete-medium.html#child

    ## Reference
    D. J. Spiegelhalter, R. G. Coewll (1992). Learning in probabilistic expert systems.
    In Bayesian Statistics 4 (J. M. Bernardo, J. 0. Berger, A. P. Dawid and A. F. M.
    Smith, eds.) 447-466. Clarendon Press, Oxford.
    """
    return pd.read_csv("http://www.ccd.pitt.edu/wiki/images/CHILD10k.csv")


def earthquake_dataset():
    raise NotImplementedError("not yet implemented")


def generate_risk_dataset(attackers=3, defenders=2, battle_size=2):
    """
    This dataset generalises a scenario in the RISK board game. In this game
    typically three armies attack and two defend. The highest scoring attacker
    (based on a dice roll) is matched with the highest scoring defender, the second
    highest attacker goes with the second highest defender and so on. The defending
    party has the advantage so the attacker needs to roll higher than the defender
    in order to win. The `losses` column in the dataframe corresponds to the losses
    that the attacker incurs after the battle.

    This dataset is used in the corresponding `brent.examples.generate_risk_dag`.

    ## Input

    - **num_attackers**: The number of dice rolled by the attacker (default: 3)
    - **num_defenders**: The number of dice rolled by the defender (default: 2)
    - **num_attackers**: The number of armies that take part in the battle (default: 2)

    ## Output

    A dataframe with dice rolls, scores for participating armies and the loss outcome.
    """
    if min(attackers, defenders) < battle_size:
        raise ValueError(
            f"We demand min(num_attackers={attackers}, num_defenders={defenders}) >= battle_size={battle_size}.")
    attack_names = [f"a{i}" for i in range(1, attackers + 1)]
    defend_names = [f"d{i}" for i in range(1, defenders + 1)]
    combinations = it.product(*[range(1, 6+1) for i in range(attackers + defenders)])
    df = pd.DataFrame(combinations, columns=attack_names + defend_names)
    for side in ['a', 'd']:
        for b in range(1, battle_size + 1):
            names = attack_names if side == 'a' else defend_names
            df[f'best_{side}{b}'] = np.sort(df[names].values)[:, -b]

    best_attackers = df[[c for c in df.columns if 'best' in c and 'a' in c]].values
    best_defenders = df[[c for c in df.columns if 'best' in c and 'd' in c]].values

    df['losses'] = (best_attackers > best_defenders).sum(axis=1)
    return df
