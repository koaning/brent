"""
The `sklearn` module contains objects that be used in scikit-learn pipelines.
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

        - **dag**: DAG object that describes the dag
        - **to_predict**: the column to predict

        ## Output

        A classifier that can be used in scikit-learn pipelines.
        """
        if to_predict not in dag.df.columns:
            raise ValueError(f"column {to_predict} not found in DAG {dag}")
        self.dag = dag
        self.to_predict = to_predict
        self.to_use = [_ for _ in self.dag.df.columns if _ != self.to_predict]
        self.query = None
        self.k = self.dag.df[to_predict].nunique()

    def _check_dataframe(self, X):
        for node in self.dag.nodes:
            if node not in X.columns:
                raise ValueError(f"column {node} not in dataframe but in DAG")

    def fit(self, X: pd.DataFrame, y):
        """
        Make the estimator "train". This is a bit verbose since the DAG object
        is already pretrained. We mainly check if the supplied dataframe given in `X`
        is consistent with the graph.

        ## Inputs

        - **X**: a dataframe to be used
        - **y**: ignored but required by the api

        ## Output

        A "trained" classifier that can be used in scikit-learn pipelines.
        """
        self._check_dataframe(X)
        return self

    def predict(self, X):
        """
        Predict the class.

        ## Inputs

        - **X**: a dataframe to be used

        ## Output

        A numpy array containing the predicted classes.
        """
        return np.argmax(self.predict_proba(X), axis=1)

    def predict_proba(self, X):
        """
        Predict the probabilities for all classes

        ## Inputs

        - **X**: a dataframe to be used

        ## Output

        A numpy array (num_rows, num_classes) containing the predicted classes.
        """
        self._check_dataframe(X)
        predictions = np.zeros((X.shape[0], self.k))
        for idx, row in X[self.to_use].reset_index(drop=True).iterrows():
            query = Query(dag=self.dag, given=row.to_dict())
            table = query.infer(give_table=True).sort_values(self.to_predict)[[self.to_predict, 'prob']]
            for i, r in table.iterrows():
                k = r[self.to_predict]
                predictions[idx, int(k)] = r['prob']
        return predictions
