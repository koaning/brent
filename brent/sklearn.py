"""
The `brent.sklearn` module contains objects that be used in scikit-learn pipelines.
In particulate it offers a classifier as well as an imputer.
"""

from brent.graph import DAG
from sklearn.base import BaseEstimator, ClassifierMixin, TransformerMixin


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

    def check_predict_name(self,):
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
