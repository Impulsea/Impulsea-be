run:
	cd src && uvicorn main:app --reload

docker-build:
	docker build -t impulsea .

docker-run:
	docker run -p 8000:8000 impulsea

ruff:
	ruff check src/

isort:
	isort src/
