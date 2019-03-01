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

## planned usage 

```python
from brent import DAG, Query
dag = Graph(data=df)

dag.add_edge("smoking", "tar")
dag.add_edge("tar", "cancer")
dag.add_edge("smoking", "cancer")
```

## installation 

Install `brent` in the virtual environment via:

```bash
$ pip install --editable .
```

You can generate documentation locally by running: 

```bash
$ pdoc --html --overwrite --template-dir doc-settings --http 0.0.0.0:12345 brent
```