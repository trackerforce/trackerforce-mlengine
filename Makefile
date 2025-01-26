.PHONY: build run test cover

install:
	pip install -r requirements.txt

run:
	python src/app.py