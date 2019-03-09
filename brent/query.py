"""
The `brent.query` module contains the `Query` object. This is the
main object that you'll use to describe complex queries against
casual graphs.
"""

import logging

import numpy as np
from graphviz import Digraph

from brent.graph import DAG
from brent.common import normalise


class Query:
    def __init__(self, dag: DAG, given=None, do=None, counterfact=None):
        """
        A Query object describes a query that will be run on a DAG object.

        Inputs:

        - **dag**: DAG object that contains all edges.
        - **given**: Dictionary of key-value pairs of given items.
        - **do**: Dictionary of key-value pairs of do operated items.
        - **counterfact**: Dictionary of key-value pairs of counterfact operated items.

        Example:

        ```
        from brent import DAG, Query
        from brent.common import make_fake_df
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
        if not counterfact:
            counterfact = dict()
        self.given_dict = given
        self.do_dict = do
        self.counterfact = counterfact

    def inference_dag(self):
        """
        This is a DAG created from the original but has been altered
        to accomodate `do-calculus`.
        """
        infer_dag = DAG(self.dag.df.copy())
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
            if value not in self.dag.df[key].values:
                raise ValueError(f"value {value} does not occur for node {key}")
            if key in {**self.given_dict, **self.do_dict}.keys():
                raise ValueError(f"{key} is already used in this query")

    def given(self, **kwargs):
        """
        Add items to the query that are `given`.

        ## Inputs

        - **kwargs**: key-value pairs of given items.
        """
        self._check_query_input(**kwargs)
        return Query(dag=self.dag, given={**self.given_dict, **kwargs}, do=self.do_dict, counterfact=self.counterfact)

    def do(self, **kwargs):
        """
        Add items to the query that are enforced via `do` operation.

        ## Inputs

        - **kwargs**: key-value pairs of do items.
        """
        self._check_query_input(**kwargs)
        return Query(dag=self.dag, given=self.given_dict, do={**self.do_dict, **kwargs}, counterfact=self.counterfact)

    def counterfact(self, **kwargs):
        """
        Add items to the query that are observed but will be counterfacted.

        ## Inputs

        - **kwargs**: key-value pairs of observations to be counterfacted.
        """
        self._check_query_input(**kwargs)
        return Query(dag=self.dag, given=self.given_dict, do=self.do_dict, counterfact={**self.counterfact, **kwargs})

    def plot(self, emphesize_do=True):
        """
        A pretty plotting function. Given nodes have double circles.
        Nodes with `do` operations on them will have in-going arcs grayed.
        """
        givens = self.given_dict.keys()
        dos = self.do_dict.keys()
        d = Digraph()
        d.attr(rankdir='LR')
        d.attr('node', shape='circle')
        for idx, n in enumerate(self.dag.graph.nodes):
            if (n in givens) or (n in dos):
                d.node(n, shape='doublecircle')
            if n in dos:
                if emphesize_do:
                    d.node(" " * idx, shape="none")
                    d.edge(" " * idx, n)
            else:
                d.node(n)
        for n1, n2 in self.dag.graph.edges:
            if ((n1 in dos) or (n1 in givens)) and ((n2 in dos) or (n2 in givens)):
                d.edge(n1, n2, color="lightgray")
            elif n2 in dos:
                d.edge(n1, n2, color="lightgray", style="dashed")
            else:
                d.edge(n1, n2)
        return d

    def infer_counterfact(self):
        """
        If counterfact is in the query we will need to return.

        The counterfacted variable is first assumed to be "given". We apply inference
        on the entire graph as a first step. This gives us probabilities for all values.
        This is the new graph definition.


        """
        pass

    def infer(self, give_table=False):
        """
        Run the inference on the graph given the current query.

        ## Inputs

        - **give_table**: Instead of calculating marginal probabilities and
        returning a dictionary, return a pandas table instead. Defaults to `False`.
        """
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

    def sample(self, n_samples=1):
        """
        Sample data from the current query.

        ## Inputs

        - **n_samples**: the number of samples to get

        ## Output

        `pandas.DataFrame` with new samples

        ## Example

        Example:

        ```
        from brent import DAG, Query
        from brent.common import make_fake_df
        # let's start with a new dataset
        df = make_fake_df(4)
        dag = DAG(df).add_edge("a", "b").add_edge("b", "c").add_edge("c","d")
        # we can build a query dynamically
        q1 = Query().given(a=1).do(d=1)
        q1.sample(100)
        ```
        """
        table = self.infer(give_table=True)
        idx = np.random.choice(table.index, p=table.prob, replace=True, size=n_samples)
        return table.loc[idx].reset_index(drop=True).drop(columns=['prob'])
