help:
	@echo "setup     - create virtualenv and install the requirements"
	@echo "test      - run all tests"
	@echo "lint      - run python lint"
	@echo "clean   	 - clean python cache files"

setup:
	rm -rf venv/ || True
	python3 -m venv venv
	venv/bin/pip install -U pip

clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

test:
	venv/bin/python3 -m pytest -svvv warehouse_service/tests/

lint:
	venv/bin/flake8 --max-line-length=119 --exclude=venv/ .