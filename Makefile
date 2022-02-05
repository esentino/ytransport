all: isort black flake8 test mypy
	echo "Done"
test:
	TORTOISE_TEST_DB=postgres://postgres:coderslab@127.0.0.1:5432/test_{} pytest -vvv -l --log-level=DEBUG
flake8:
	flake8 .
black:
	black .
isort:
	isort .
mypy:
	mypy .
