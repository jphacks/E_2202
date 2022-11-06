backend-ci:
	docker-compose exec server pytest . -v --doctest-modules
	docker-compose exec server mypy --strict .
	docker-compose exec server python -m flake8 --max-line-length 120
