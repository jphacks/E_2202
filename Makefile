backend-ci:
	docker-compose exec server python -m flake8 --max-line-length 120
	docker-compose exec server python -m pytest
	docker-compose exec server mypy --strict .
	docker-compose exec server python main.py
