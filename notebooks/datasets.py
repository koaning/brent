import numpy as np
import pandas as pd

def parse_suicide():
    return (pd.read_csv("../data/who_suicide_statistics.csv")
      .dropna()
      .assign(rate=lambda d: d.suicides_no/d.population,
              suicide=lambda d: np.where(d.rate >= np.quantile(d.rate, 0.5), "high", "low"))
      [["sex", "suicide", "age", "country"]])

def parse_milk():
    def func(row):
        if row > 200:
            return 'high'
        elif row > 100:
            return 'medium' 
        return 'low'
    df_milk = pd.read_csv("../data/milk.csv")
    df_milk.columns = ["rank", "country", "milk"]
    return df_milk[["country", "milk"]].assign(milk=lambda d: [func(_) for _ in d.milk])

def parse_alcohol():
    def func(row):
        if row > 10:
            return 'high'
        elif row > 5:
            return 'medium' 
        return 'low'
    df_beer = pd.read_csv("../data/drinking.csv")
    df_beer = df_beer.rename(str.lower, axis=1)[["country", "total"]]
    return df_beer.assign(alcohol=lambda d: [func(_) for _ in d['total']])[["country", "alcohol"]]


def parse_nobel():
    df_nobel = (pd.read_csv("../data/nobel-prizes.csv")
                .rename(str.lower, axis=1)
                .groupby("death country")
                .apply(len)
                .reset_index())
    df_nobel.columns = ["country", "nobel"]
    return df_nobel.assign(nobel=lambda d: ["high" if _ > 8 else "low" for _ in d.nobel])