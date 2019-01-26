import pandas as pd
import networkx as nx
from graphviz import Digraph
from dagger.common import normalise


class DAG:
    def __init__(self, dataframe: pd.DataFrame):
        self._df = dataframe
        self.graph = nx.DiGraph()
        for node in self._df.columns:
            self.graph.add_node(node)

    @property
    def origin_nodes(self):
        return tuple(x for x in self.graph.nodes() if self.graph.in_degree(x) == 0)

    @property
    def marginal_table(self):
        nodes = list(self.graph.nodes)
        marginal = self.calc_node_table(nodes.pop())
        for node in nodes:
            marginal = self.merge_probs(marginal, self.calc_node_table(node))
        return marginal

    @property
    def nodes(self):
        return list(self.graph.nodes)

    @property
    def edges(self):
        return list(self.graph.edges)

    def copy(self):
        new_dag = DAG(self._df)
        new_dag.graph = self.graph
        return new_dag

    def leaf_nodes(self, graph: nx.DiGraph = None):
        if not graph:
            graph = self.graph

        def predicate(node):
            type_a = (graph.in_degree(node) == 0) & (graph.out_degree(node) == 1)
            type_b = (graph.in_degree(node) == 1) & (graph.out_degree(node) == 0)
            return type_a | type_b

        return [x for x in graph.nodes() if predicate(x)]

    def no_parent_nodes(self, graph: nx.DiGraph = None):
        if not graph:
            graph = self.graph
        return [x for x in graph.nodes() if graph.in_degree(x) == 0]

    def calc_node_table(self, name):
        """
        Calculates probability table for a given node.

        Suppose we have graph A -> B -> C. Then `calc_node_table("b")`
        call will calculate P(C | B).
        :param name: Name of a node in the graph
        :return: Pandas dataframe with associated probabilities.
        """
        parents = self.parents(name)
        return (self._df
                .assign(count=1)
                .groupby(list(parents) + [name])
                .count()['count']
                .reset_index()
                .assign(prob=lambda d: d['count']/d['count'].sum())
                .drop("count", axis=1))

    def merge_probs(self, this_df, that_df):
        """
        Merges two probability dataframes while checking
        if nodes are connected in the graph.
        :param this_df: a probability dataframe
        :param that_df: a probability dataframe
        :return: a probability dataframe
        """
        common_cols = list(set(this_df.columns)
                           .intersection(set(that_df.columns))
                           .difference({"prob"}))
        if len(common_cols) == 0:
            columns = set(that_df.columns).difference({"prob"})
            loose_tables = []
            for c in columns:
                for value in self.calc_node_table(c)[c].values:
                    loose_tables.append(this_df.assign(**{c: value}))
            join_able = pd.concat(loose_tables)
            return self.merge_probs(join_able, that_df)
        return (this_df
                .set_index(common_cols)
                .join(that_df.set_index(common_cols), lsuffix="1", rsuffix="2")
                .assign(prob=lambda x: normalise(x.prob1 * x.prob2))
                .drop("prob1", axis=1)
                .drop("prob2", axis=1)
                .reset_index())

    def add_edge(self, source, sink):
        """
        Adds an edge to the graph.
        :param source: Name of a node in the graph
        :param sink: Name of a node in the graph
        :return: updated DAG object
        """
        if source not in self._df.columns:
            raise ValueError(f"cause {source} not in dataframe")
        if sink not in self._df.columns:
            raise ValueError(f"effect {sink} not in dataframe")
        self.graph.add_edge(source, sink)
        return self

    def children(self, node):
        """
        Return the children of a node.
        :param node: Name of a node
        :return: set of nodenames
        """
        return set(self.graph.successors(node))

    def parents(self, node):
        """
        Return the parents of a node.
        :param node: Name of a node
        :return: set of nodenames
        """
        return set(self.graph.predecessors(node))

    def connections(self, node):
        """
        Return all nodes connected to another.
        :param node: Name of a node
        :return: set of nodenames
        """
        return set(list(self.children(node)) + list(self.parents(node)))

    def independences(self):
        # https://www.slideshare.net/duytungpham18/lecture-1-graphical-models
        pass

    def plot(self):
        """A pretty plotting function."""
        d = Digraph()
        for n in self.graph.nodes:
            d.node(n)
        for n1, n2 in self.graph.edges:
            d.edge(n1, n2)
        return d

    def nx_plot(self, **kwargs):
        """A customizable plotting function."""
        nx.draw(self.graph, node_size=500, with_labels=True, node_color="white", **kwargs)
