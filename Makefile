flake:
	flake8 dagger
	flake8 tests

install:
	pip install -e .

develop:
	python setup.py develop

test:
	pytest

clean:
	rm -rf .pytest_cache
	rm -rf dagger.egg-info