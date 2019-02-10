from numpy import round

from dagger.graph import DAG
from dagger.common import normalise

from graphviz import Digraph


class Query:
    def __init__(self, dag: DAG, given=None, do=None):
        self.dag = dag
        if not given:
            given = dict()
        if not do:
            do = dict()
        self.given_dict = given
        self.do_dict = do

    def _check_query_input(self, **kwargs):
        for key, value in kwargs.items():
            if key not in self.dag.nodes:
                raise ValueError(f"node {key} does not exist in original dag")
            if value not in self.dag._df[key].values:
                raise ValueError(f"value {value} does not occur for node {key}")
            if key in {**self.given_dict, **self.do_dict}.keys():
                raise ValueError(f"{key} is already used in this query")

    def given(self, **kwargs):
        self._check_query_input(**kwargs)
        return Query(dag=self.dag, given={**self.given_dict, **kwargs}, do=self.do_dict)

    def do(self, **kwargs):
        self._check_query_input(**kwargs)
        return Query(dag=self.dag, given=self.given_dict, do={**self.do_dict, **kwargs})

    def plot(self):
        """A pretty plotting function."""
        givens = self.given_dict.keys()
        dos = self.do_dict.keys()
        d = Digraph()
        d.attr(rankdir='LR')
        d.attr('node', shape='circle')
        for n in self.dag.graph.nodes:
            if (n in givens) or (n in dos):
                d.node(n, shape='doublecircle')
            else:
                d.node(n)
        for n1, n2 in self.dag.graph.edges:
            if n2 in dos:
                d.edge(n1, n2, color="lightgray", style="dashed")
            else:
                d.edge(n1, n2)
        return d

    def infer(self, give_table=False):
        infer_dag = DAG(self.dag._df)
        for n1, n2 in self.dag.edges:
            if n2 not in self.do_dict.keys():
                self.dag.add_edge(n1, n2)
        marginal_table = infer_dag.marginal_table
        for k, v in {**self.do_dict, **self.given_dict}.items():
            marginal_table = marginal_table[marginal_table[k] == v]
        tbl = marginal_table.assign(prob=lambda d: normalise(d.prob))
        if give_table:
            return tbl
        output = {}
        for c in tbl.columns:
            if c != "prob":
                output[c] = tbl.groupby(c)['prob'].sum().to_dict()
        return output
