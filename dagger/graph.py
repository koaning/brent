import itertools as it

import pandas as pd
import networkx as nx
from graphviz import Digraph


def _calc_prior_discrete(dataf, name):
    return (dataf
            .assign(n=1)
            .groupby(name)
            .count()['n']
            .reset_index()
            .assign(p=lambda d: d.n/d.n.sum())
            .drop(columns=["n"])
            .set_index(name)
            .to_dict()["p"])


def _nodes_to_handle(dag, nodes_done=set()):
    if len(nodes_done) == 0:
        return dag.origin_nodes
    graph = dag.graph.copy()
    for node in nodes_done:
        graph.remove_node(node)
    return tuple(x for x in graph.nodes() if graph.in_degree(x) == 0)


def _group_probs(dataf, parents):
    sum_per_group = dataf.groupby(parents).sum()['n'].reset_index()
    return (dataf
            .merge(sum_per_group, on=parents)
            .assign(p=lambda d: d.n_x/d.n_y)
            .drop(columns=["n_x", "n_y"]))


class DAG:
    def __init__(self, dataframe: pd.DataFrame):
        self._is_baked = False
        self._df = dataframe
        self._priors = {n: _calc_prior_discrete(self._df, n) for n in self._df.columns}
        self.graph = nx.DiGraph()
        for node in self._df.columns:
            self.graph.add_node(node)

    @property
    def origin_nodes(self):
        return tuple(x for x in self.graph.nodes() if self.graph.in_degree(x) == 0)

    def add_edge(self, cause, effect):
        if cause not in self._df.columns:
            raise ValueError(f"cause {cause} not in dataframe")
        if effect not in self._df.columns:
            raise ValueError(f"effect {effect} not in dataframe")
        self.graph.add_edge(cause, effect)
        return self

    def children(self, node):
        return set(self.graph.successors(node))

    def parents(self, node):
        return set(self.graph.predecessors(node))

    def prob_paths(self, node_a, node_b):
        pass

    def independences(self):
        for node in self.graph.nodes():
            children = [c for c in self.children(node) if len(self.parents(c) - {node}) == 0]
            for n1, n2 in it.combinations(children, 2):
                print(f"({n1} __||__ {n2}) | {node}")

    def bake(self):
        self._is_baked = True
        return self

    def plot(self):
        d = Digraph()
        for n1, n2 in self.graph.edges:
            d.edge(n1, n2)
        return d

    def nx_plot(self, **kwargs):
        nx.draw(self.graph, node_size=500, with_labels=True, node_color="white", **kwargs)
