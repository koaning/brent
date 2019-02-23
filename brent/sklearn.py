"""
The `brent.sklearn` module contains objects that be used in `sklearn` pipelines.
In particulate it offers a classifier as well as an imputer.
"""

from brent.graph import DAG
from sklearn.base import BaseEstimator, ClassifierMixin, TransformerMixin


class BrentClassifier(BaseEstimator, ClassifierMixin):
    def __init__(self, dag: DAG):
        """
        Construct an estimator based on a DAG.
        :param dag:
        """
        self.dag = dag
        pass

    def fit(self, X, y):
        pass

    def predict(self, X, y):
        pass

    def predict_proba(self, X, y):
        pass


class BrentImputer(BaseEstimator, TransformerMixin):
    def __init__(self, dag: DAG):
        self.dag = dag
