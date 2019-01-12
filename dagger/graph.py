import pandas as pd
import networkx as nx


class DAG:
    def __init__(self, dataframe: pd.DataFrame):
        self._is_baked = False
        self._df = dataframe
        self.graph = nx.DiGraph()
        for node in self._df.columns:
            self.graph.add_node(node)

    def add_edge(self, cause, effect):
        if cause not in self._df.columns:
            raise ValueError(f"cause {cause} not in dataframe")
        if effect not in self._df.columns:
            raise ValueError(f"effect {effect} not in dataframe")
        self.graph.add_edge(cause, effect)
        return self

    def bake(self):
        self._is_baked = True
        return self

    def plot(self):
        nx.draw(self.graph, node_size=500, with_labels=True, node_color="white")

    def nx_plot(self, **kwargs):
        nx.draw(self.graph, **kwargs)
