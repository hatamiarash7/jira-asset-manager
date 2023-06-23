install:
	poetry install

lock:
	poetry lock

build:
	poetry build

test:
	python3 -m pytest tests/