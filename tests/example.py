import logging
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pylab as plt

from dagger.graph import DAG
from dagger.query import Query
from dagger.common import make_fake_df, normalise

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(filename)s:%(funcName)s:%(lineno)d] %(levelname)s - %(message)s',
)

df = pd.DataFrame({"a": [1, 1, 1, 1, 0, 0, 0, 0],
                   "b": [0, 1, 0, 1, 1, 1, 1, 0],
                   "c": [0, 0, 1, 0, 0, 1, 0, 1]})
dag = DAG(df).add_edge("a", "b").add_edge("a", "c").add_edge("c", "b")
logging.debug(f"parents of c: {dag.parents('c')}")
for node in dag.nodes:
    logging.debug(f"confirming parents({node}) = {dag.parents(node)}")
print(Query(dag).infer())
# print(Query(dag).given(a=1).infer())