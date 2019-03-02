[![Build Status](https://travis-ci.com/koaning/brent.svg?branch=master)](https://travis-ci.com/koaning/brent) [![Build status](https://ci.appveyor.com/api/projects/status/aancx73nveo29esu?svg=true)](https://ci.appveyor.com/project/koaning/brent)


![](images/logo.png)
> They're good DAGs brent. 

## What it is

Brent is a small, but fun, python library that makes it easy to explore causal graphical modelling and do-calculus
on systems with discrete variables. Brent is a tool that can help out when you can write a system like below, but 
want to write complex queries on it.  

![](images/dag1.png) 

## Documentation

## Plotting 

One of the main features is pretty pictures! 

![](images/dag2.svg)

## Quickstart 

First we need to have a dataset and create a graph from it. 
The code below demonstrates how to do this.  

```python
from brent import DAG
from brent.common import make_fake_df

dag = (DAG(dataframe=make_fake_df(7))
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

![](images/complex-graph.png)

Not only do we get pretty plots, but we also can build
an expressive query on top of it. 

```python
from brent import Query
q = Query(dag).given(d=1).do(a=0, c=1)
q.plot()
```

![](images/complex-query.png)

If you're more interested in doing the inference, that's simple 
too. 

```python
# we can also see updated probabilities
q.infer()
q.infer(give_table=True)
```

## Developing Locally 

After cloning you may install `brent` in the virtual 
environment via:

```bash
$ pip install --editable .
```

You can generate documentation locally by running: 

```bash
$ pdoc --html --overwrite --template-dir doc-settings --http 0.0.0.0:12345 brent
```
