import logging
import pandas as pd

from brent.graph import DAG
from brent.query import Query

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
