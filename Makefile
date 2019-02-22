flake:
	flake8 brent
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
	rm -rf html
	rm -rf docs
	rm -rf dist
	rm -rf build
	rm -rf .ipynb_checkpoints

check: test flake