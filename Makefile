flake:
	flake8 dagger
	flake8 tests

install:
	pip install -e .

develop:
	python setup.py develop
	pip install -r requirements-dev.txt

test:
	pytest --nbval-lax

clean:
	rm -rf .pytest_cache
	rm -rf dagger.egg-info

check: test flake