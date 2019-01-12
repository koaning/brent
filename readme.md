# dagger

## planned usage 

```
from dagger import Graph, Query
dag = Graph(data=df)

dag.add_edge(cause="smoking", effect="tar")
dag.add_edge(cause="tar", effect="cancer")
dag.add_edge(cause="smoking", effect="cancer")

dag.add_edge(causes=[...], effect="cancer")

Query(dag=dag).do().given().counterfact()
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
