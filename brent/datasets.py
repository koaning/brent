"""
The `brent.datasets` module contains functions that will generate
datasets. Typically these datasets are meant for educational purposes.

Don't forget to see the docstring for a reference to the origin of the
dataset.
"""

import itertools as it
from functools import reduce

import pandas as pd


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