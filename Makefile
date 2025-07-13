.PHONY: up down logs makemigrations migrate

up:
	docker-compose up --build -d

down:
	docker-compose down

logs:
	docker-compose logs -f

# Очистить ненужные контейнеры, тома, образы (опционально)
clean:
	docker-compose down -v --rmi all --remove-orphans


makemigrations:
	alembic revision --autogenerate -m "$(m)"

migrate:
	alembic upgrade head
