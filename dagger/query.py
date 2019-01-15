import networkx as nx

from dagger.graph import DAG


class DAG:
    def __init__(self, dag: DAG):
        self.dag = dag

    def given(self, plot=False, **kwargs):
        if plot:
            self.plot_given(**kwargs)
        pass

    def do(self, plot=False, **kwargs):
        if plot:
            self.plot_do(**kwargs)
        pass

    def plot_given(self, **kwargs):
        # https://networkx.github.io/documentation/stable/auto_examples/drawing/plot_weighted_graph.html#sphx-glr-auto-examples-drawing-plot-weighted-graph-py
        G = nx.Graph()

        givens = kwargs.keys()
        for source, sink in self.dag.graph.edges:
            weight = 0.9 if ((source in givens) | (sink in givens)) else 0.1
            G.add_edge(source, sink, weight=weight)

        pos = nx.spring_layout(self.dag.graph)

        # nodes
        nx.draw_networkx_nodes(self.dag.graph, pos, node_size=700)

        # edges
        nx.draw_networkx_edges(G, pos, edgelist=elarge,
                               width=6)
        nx.draw_networkx_edges(G, pos, edgelist=esmall,
                               width=6, alpha=0.5, edge_color='b', style='dashed')

        # labels
        nx.draw_networkx_labels(G, pos, font_size=20, font_family='sans-serif')

    def plot_do(self):
        pass
        # https://networkx.github.io/documentation/stable/auto_examples/drawing/plot_weighted_graph.html#sphx-glr-auto-examples-drawing-plot-weighted-graph-py
        # pos = nx.spring_layout(G)  # positions for all nodes
        #
        # # nodes
        # nx.draw_networkx_nodes(G, pos, node_size=700)
        #
        # # edges
        # nx.draw_networkx_edges(G, pos, edgelist=elarge,
        #                        width=6)
        # nx.draw_networkx_edges(G, pos, edgelist=esmall,
        #                        width=6, alpha=0.5, edge_color='b', style='dashed')
        #
        # # labels
        # nx.draw_networkx_labels(G, pos, font_size=20, font_family='sans-serif')

