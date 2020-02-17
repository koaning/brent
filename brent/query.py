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
    def __init__(self, dag: DAG, given=None, do=None):
        """
        A Query object describes a query that will be run on a DAG object.

        Inputs:

        - **dag**: DAG object that contains all edges.
        - **given**: Dictionary of key-value pairs of given items.
        - **do**: Dictionary of key-value pairs of do operated items.

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
        self.given_dict = given
        self.do_dict = do

    def inference_dag(self):
        """
        This is a DAG created from the original but has been altered
        to accomodate `do-calculus`.
        """
        infer_dag = self.dag.copy()
        logging.debug(f"constructing copy of original DAG nodes: {infer_dag.nodes}")
        for node in self.do_dict.keys():
            for parent in infer_dag.parents(node):
                infer_dag.remove_edge(parent, node)
                logging.debug(f"edge {parent} -> {node} ignored because of do operator")
        logging.debug(f"original DAG copied")
        return infer_dag

    def _check_query_input(self, **kwargs):
        for key, value in kwargs.items():
            logging.debug(f"checking key {key}={value}")
            if key not in self.dag.nodes:
                raise ValueError(f"node {key} does not exist in original dag")
            if value not in self.dag.values_for_node(key):
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
        return Query(dag=self.dag, given={**self.given_dict, **kwargs}, do=self.do_dict)

    def do(self, **kwargs):
        """
        Add items to the query that are enforced via `do` operation.

        ## Inputs

        - **kwargs**: key-value pairs of do items.
        """
        self._check_query_input(**kwargs)
        return Query(dag=self.dag, given=self.given_dict, do={**self.do_dict, **kwargs})

    def plot(self, emphesize_do=True, **kwargs):
        """
        A pretty plotting function. Given nodes have double circles.
        Nodes with `do` operations on them will have in-going arcs grayed.
        """
        givens = self.given_dict.keys()
        dos = self.do_dict.keys()
        d = Digraph(**kwargs)
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


class SupposeQuery:
    """
    A `SupposeQuery` can be used to ask the question "suppose we saw this"
    what would have happened if we did or saw something else?
    """
    def __init__(self, dag, when=None, suppose_do=None, suppose_given=None):
        """
        ## Inputs:

        - **dag**: the `DAG` object to base the query on
        - **when**: the observations we saw "before"
        - **suppose_do**: the things we might enforce "in hindsight"
        - **suppose_given**: the things we might witness "in hindsight"
        """
        self.dag = dag
        self.orig_query = when
        if not suppose_do:
            suppose_do = dict()
        if not suppose_given:
            suppose_given = dict()
        self.suppose_do_dict = suppose_do
        self.suppose_given_dict = suppose_given

    def _check_query_input(self, **kwargs):
        for key, value in kwargs.items():
            logging.debug(f"checking key {key}={value}")
            if key not in self.dag.nodes:
                raise ValueError(f"node '{key}' does not exist in original dag")
            if value not in self.dag.values_for_node(key):
                raise ValueError(f"value {value} does not occur for node {key}")
            if key in {**self.suppose_do_dict, **self.suppose_given_dict}.keys():
                raise ValueError(f"{key} is already used in this query")

    def inference_dag(self):
        """
        This is a DAG created from the original but has been altered
        to accomodate `do-calculus`.
        """
        infer_dag = self.dag.copy()
        logging.debug(f"constructing copy of original DAG nodes: {infer_dag.nodes}")
        for node in self.suppose_do_dict.keys():
            for parent in infer_dag.parents(node):
                infer_dag.remove_edge(parent, node)
                logging.debug(f"edge {parent} -> {node} ignored because of do operator")
        logging.debug(f"original DAG copied")
        return infer_dag

    def when(self, query):
        """
        With `when` you can specify what was observed.

        ## Inputs

        - **query**: query of what was observed before.
        """
        if self.orig_query is not None:
            raise ValueError("SupposeQuery already has a `.when` value assigned.")
        return SupposeQuery(dag=self.dag, when=query, suppose_do=self.suppose_do_dict,
                            suppose_given=self.suppose_given_dict)

    def suppose_do(self, **kwargs):
        """
        With `suppose_do` you can specify the "what if" part after seeing
        the facts seen before in the `when` statement. Note that these "what if"
        scenarios are enforced, not given.

        ## Inputs

        - **kwargs**: key-value pairs of given items.
        """
        self._check_query_input(**kwargs)
        return SupposeQuery(dag=self.dag, when=self.orig_query, suppose_do={**self.suppose_do_dict, **kwargs},
                            suppose_given=self.suppose_given_dict)

    def suppose_given(self, **kwargs):
        """
        With `suppose_do` you can specify the "what if" part after seeing
        the facts seen before in the `when` statement. Note that these "what if"
        scenarios are given, not enforced.

        ## Inputs

        - **kwargs**: key-value pairs of given items.
        """
        self._check_query_input(**kwargs)
        return SupposeQuery(dag=self.dag, when=self.orig_query, suppose_do=self.suppose_do_dict,
                            suppose_given={**self.suppose_given_dict, **kwargs})

    def infer(self, give_table=False):
        """
        Run the inference on the graph given the current query.

        ## Inputs

        - **give_table**: Instead of calculating marginal probabilities and
        returning a dictionary, return a pandas table instead. Defaults to `False`.
        """
        if self.orig_query is None:
            raise ValueError("SupposeQuery needs a `when` parameter defined.")
        dag_copy = self.dag.copy().cache()
        orig_query_table = self.orig_query.infer(give_table=True)
        names_to_omit = list(self.orig_query.given_dict.keys()) + list(self.orig_query.do_dict.keys())
        names_to_join = [n for n in self.orig_query.dag.nodes if n not in names_to_omit]

        for node in names_to_join:
            associated_table = dag_copy.prob_tables[node]
            colnames = list(associated_table.columns)
            res = (orig_query_table[colnames]
                   .groupby([_ for _ in colnames if _ != "prob"])
                   .sum()["prob"]
                   .reset_index())
            dag_copy.prob_tables[node] = res

        new_query = Query(dag=dag_copy, given=self.suppose_given_dict, do=self.suppose_do_dict)

        return new_query.infer(give_table=give_table)
