import networkx as nx

from dagger.graph import DAG


class DAG:
    def __init__(self, dag: DAG, ):
        self.dag = dag
        self.given = {}
        self.do = {}

    def given(self, plot=False, **kwargs):


    def do(self, plot=False, **kwargs):
        if plot:
            self.plot_do(**kwargs)
        pass
