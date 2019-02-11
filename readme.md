# dagger

## internals

Suppose we have a graph like below. 

![](images/dag1.png)

Calculating the marginal probability is defined via; 

```math
p(A, B, C, D, E, F, G) = p(A|E) p(B|A) p(C|A,B) p(D|A,B,E) p(E) p(F|C,G) p(G)
```

## inference plots 

![](images/dag2.svg)


## planned usage 

```python
from dagger import Graph, Query
dag = Graph(data=df)

dag.add_edge("smoking", "tar")
dag.add_edge("tar", "cancer")
dag.add_edge("smoking", "cancer")
```

## project structure 

```
│
├── data/               <- The original, immutable data dump. 
├── notebooks/          <- Jupyter notebooks. Naming convention is a short `-` delimited 
│                          description, a number (for ordering), and the creator's initials,
│                          e.g. `initial-data-exploration-01-hg`.
├── tests/              <- Unit tests.
├── dagger/             <- Python module with source code of this project.
├── Makefile            <- Makefile with commands like `make environment`
└── README.md           <- The top-level README for developers using this project.
```

## installation 

Install `dagger` in the virtual environment via:

```bash
$ pip install --editable .
```

You can generate documentation locally by running: 

```bash
$ pdoc --html --overwrite --template-dir doc/pdoc_template --http 0.0.0.0:12345 dagger
```