COMPOSE = docker-compose \
	-f docker-compose/volumes.yaml \
	-f docker-compose/messaging.yaml \
	-f docker-compose/app.yaml \
	-f docker-compose/logging.yaml \

.PHONY: up down logs clean

up:
	$(COMPOSE) up --build -d

down:
	$(COMPOSE) down

logs:
	$(COMPOSE) logs -f

clean:
	$(COMPOSE) down -v --rmi all --remove-orphans

makemigrations:
	alembic revision --autogenerate -m "$(m)"

migrate:
	alembic upgrade head
