"""
Brent
-----

![](https://github.com/koaning/brent/blob/master/images/dag1.png?raw=true)

Brent is a playful tool to help understand bayesian graphical
modelling as well as do-calculus. It offers support for discrete
values and comes with great plotting tools. Under the hood is merely
uses [pandas](http://pandas.pydata.org/pandas-docs/stable/reference/index.html)
and [networkx](https://networkx.github.io/documentation/stable/index.html).

## Example 1

The basics of the tool can be demonstrated via the following codeblock.

```python
from brent import DAG, Query
from brent.common import make_fake_df

# let's start with a new dataset and visualise it's graph
df = make_fake_df(4)
dag = DAG(df).add_edge("a", "b").add_edge("b", "c").add_edge("c","d")
dag.plot()
```

![](https://github.com/koaning/brent/blob/master/images/simple-graph.png?raw=true)

Such a graph is nice and we can get properties from it, these can be
found in the documentation page. The main usecase for it though is
to use

```python
# we can build a query dynamically
q = Query(dag).given(a=1).do(d=1)
q.plot()
```

![](https://github.com/koaning/brent/blob/master/images/simple-query.png?raw=true)

The nodes that are given have double circles around them while the
nodes that are affected by a `do()`-operation have greyed out arcs
going in. This is because these are usually removed for inference.

If you're interested in inferring probabilities, you can get the
updated probabilities by calling the inference method on the object.

```python
# we can also see updated probabilities
q.infer()
```

## Example 2

We'll still be using fake data for this example, but we're going to
create a more complex graph.

```
from brent import DAG, Query
from brent.common import make_fake_df

dag = (DAG(make_fake_df(7))
       .add_edge("e", "a")
       .add_edge("e", "d")
       .add_edge("a", "d")
       .add_edge("b", "d")
       .add_edge("a", "b")
       .add_edge("a", "c")
       .add_edge("b", "c")
       .add_edge("c", "f")
       .add_edge("g", "f"))

dag.plot()
```

![](https://github.com/koaning/brent/blob/master/images/complex-graph.png?raw=true)

This graph will be more involved when we create a query on it.

```
q = Query(dag).given(d=1).do(a=0, c=1)
q.plot()
```

But we can still make a pretty plot appear.

![](https://github.com/koaning/brent/blob/master/images/complex-query.png?raw=true)

Inference is still done in the same way. Note that you can
get marginal probabilities in json format but you can also
get pass `give_table=True` if you prefer to get a full probability
table. This will give a pandas dataframe.

```python
# we can also see updated probabilities
q.infer()
q.infer(give_table=True)
```

"""

from .query import Query
from .graph import DAG
