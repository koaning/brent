import itertools as it
from functools import reduce

import pandas as pd


def simple_study_dataset():
    """
    Creates a simple dataset that simulates the probability of passing
    a course given if the test for the course was hard and weather or
    not a student studied. This is a simulated dataset.
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
    pd.DataFrame(tween, columns=["study", "hard", "grade"])


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
    pass
