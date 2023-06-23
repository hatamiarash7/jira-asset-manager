clean:
	rm -rf dist

install:
	poetry install

lock:
	poetry lock

build: clean
	poetry build

test:
	python3 -m pytest tests/