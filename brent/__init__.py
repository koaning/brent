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

Note that the plot demonstrates which edges are affected with the `do`
operation by making the lines dashed and gray. Nodes that have information
injected in them have double circles and edges that don't contribute to
the inference are grayed out. In this case, because `d` is given and because `a`
is enforced with a `do()` operation the arc between `a -> d` does not participate
in the inference much.

Inference is still done in the same way as before. Note that you can
get marginal probabilities in json format but you can also
get pass `give_table=True` if you prefer to get a full probability
table. This will give a pandas dataframe.

```python
# we can also see updated probabilities
q.infer()
q.infer(give_table=True)
```

## CounterFactual Inference

Let's dicuss a theoretical example that might help to explain how
counterfactuals work. The example is not based on a "real dataset"
but we might assume that we actually had a dataset that contains
information about test scores in a school.

The dataset contains three columns:

- **study**: an indicator if the student in question studied a little, lots or not at all
- **hard**: an indicator if the test in question was hard
- **grade**: an indicator if the result of the test was good, a pass or a fail

We will use this dataset with `brent` to ask some interesting queries.

```
from brent import Query, DAG, SupposeQuery
from brent.datasets import simple_study_dataset

simple_study_dataset().sample(5)
```

## Do-Calculus
"""

from .query import Query, SupposeQuery
from .graph import DAG
