"""
The `dagger.query` module contains the `Query` object. This is the
main object that you'll use to describe complex queries against
casual graphs.
"""

import logging

from dagger.graph import DAG
from dagger.common import normalise

from graphviz import Digraph


class Query:
    def __init__(self, dag: DAG, given=None, do=None):
        """
        A `dagger.Query` object describes a query that will be run
        on a `dagger.DAG` object.

        Inputs:

        - **dag**: DAG object that contains all edges.
        - **given**: Dictionary of key-value pairs of given items.
        - **do**: Dictionary of key-value pairs of do operated items.

        Example:

        ```
        from dagger import DAG, Query
        from dagger.common import make_fake_df
        # let's start with a new dataset
        df = make_fake_df(4)
        dag = DAG(df).add_edge("a", "b").add_edge("b", "c").add_edge("c","d")
        # we can build a query dynamically
        q1 = Query().given(a=1).do(d=1)
        # alternatively we can build one from start
        q2 = Query(given={'a':1}, do={'d':1})
        ```
        """
        self.dag = dag
        if not given:
            given = dict()
        if not do:
            do = dict()
        self.given_dict = given
        self.do_dict = do

    def inference_dag(self):
        """
        This is a DAG created from the original but has been altered
        to accomodate `do-calculus`.
        """
        infer_dag = DAG(self.dag._df.copy())
        logging.debug(f"constructing copy of original DAG nodes: {infer_dag.nodes}")
        for n1, n2 in self.dag.edges:
            if n2 not in self.do_dict.keys():
                infer_dag.add_edge(n1, n2)
            else:
                logging.debug(f"edge {n1} -> {n2} ignored because of do operator")
        logging.debug(f"original DAG copied")
        return infer_dag

    def _check_query_input(self, **kwargs):
        for key, value in kwargs.items():
            logging.debug(f"checking key {key}={value}")
            if key not in self.dag.nodes:
                raise ValueError(f"node {key} does not exist in original dag")
            if value not in self.dag._df[key].values:
                raise ValueError(f"value {value} does not occur for node {key}")
            if key in {**self.given_dict, **self.do_dict}.keys():
                raise ValueError(f"{key} is already used in this query")

    def given(self, **kwargs):
        """
        Add items to the query that are `given`.
        :param kwargs: key-value pairs of given items.
        :return:
        """
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
        for idx, n in enumerate(self.dag.graph.nodes):
            if (n in givens) or (n in dos):
                d.node(n, shape='doublecircle')
            if n in dos:
                d.node(" " * idx, shape="none")
                d.edge(" " * idx, n)
            else:
                d.node(n)
        for n1, n2 in self.dag.graph.edges:
            if n2 in dos:
                d.edge(n1, n2, color="lightgray", style="dashed")
            else:
                d.edge(n1, n2)
        return d

    def infer(self, give_table=False):
        logging.debug(f"about to make an inference")
        infer_dag = self.inference_dag()
        for node in infer_dag.nodes:
            logging.debug(f"confirming parents({node}) = {infer_dag.parents(node)}")
        marginal_table = infer_dag.marginal_table
        for k, v in {**self.do_dict, **self.given_dict}.items():
            logging.debug(f"processing {k}={v}")
            marginal_table = marginal_table.loc[lambda d: d[k] == v]
        tbl = marginal_table.assign(prob=lambda d: normalise(d.prob))
        if give_table:
            return tbl
        output = {}
        for c in tbl.columns:
            if c != "prob":
                output[c] = tbl.groupby(c)['prob'].sum().to_dict()
        return output
