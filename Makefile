.PHONY: docs

flake:
	flake8 brent
	flake8 tests

install:
	pip install -e ".[dev]"

develop:
	python setup.py develop

test:
	pytest

clean:
	rm -rf .pytest_cache
	rm -rf brent.egg-info
	rm -rf html
	rm -rf dist
	rm -rf build
	rm -rf .ipynb_checkpoints

check: test flake

docs: docfiles
	pdoc --html --overwrite --template-dir doc-settings --http 0.0.0.0:12345 brent

docfiles:
	pdoc --html --overwrite --template-dir doc-settings brent
	rm -r docs
	mkdir docs
	mv html/brent/* docs
	rm -r html

pypi:
	rm -rf dist
	python setup.py sdist
	python setup.py bdist_wheel --universal
	twine upload dist/*
