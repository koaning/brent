"""
The `brent.sklearn` module contains objects that be used in scikit-learn pipelines.
In particulate it offers a classifier as well as an imputer.
"""

from brent.graph import DAG
from brent.query import Query

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, ClassifierMixin


class BrentClassifier(BaseEstimator, ClassifierMixin):
    """
    A classifier that allows you to define your own model via a DAG.
    """
    def __init__(self, dag: DAG, to_predict: str):
        """
        Construct an estimator based on a DAG. You need to specify the DAG as well as
        the column name that requires prediction.

        ## Inputs

        - **dag**: `brent.DAG` object that describes the dag
        - **to_predict**: the column to predict

        ## Output

        A classifier that can be used in scikit-learn pipelines.
        """
        if to_predict not in dag.df.columns:
            raise ValueError(f"column {to_predict} not found in DAG {dag}")
        self.dag = dag
        self.to_predict = to_predict
        self.query = None
        self.k = self.dag.df[to_predict].nunique()

    def fit(self, X: pd.DataFrame, y):
        for node in self.dag.nodes:
            if node not in X.columns:
                raise ValueError(f"column {node} not in dataframe but in DAG")
        return self

    def predict(self, X, y):
        return np.argmax(self.predict_proba(X, y), axis=1)

    def predict_proba(self, X, y):
        predictions = np.zeros(y.shape)
        for idx, row in X.iterrows():
            query = Query(dag=self.dag, given=row.to_dict())
            predictions[idx] = query.infer()[self.to_predict]
        return predictions
