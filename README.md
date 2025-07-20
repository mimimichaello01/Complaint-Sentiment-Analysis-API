
# Complaint Sentiment Analysis API

API для приёма жалоб клиентов с анализом тональности текста и проверкой на нецензурную лексику с помощью внешних сервисов. Кроме того, реализована определение геолокации пользователя по IP-адресу. Приложение построено на FastAPI с использованием SQLite, Docker и Alembic.

## Ключевые особенности

- **Анализ тональности** текста жалоб через Sentiment Analysis API
- **Фильтрация нецензурной лексики** с помощью Profanity Filter API
- **Геолокация** по IP-адресу клиента
- **Категоризация жалоб** (Технические, Платежи, Другое)
- **Асинхронная обработка** технических жалоб через Celery + RabbitMQ
- **Централизованное логирование** в ELK через Kafka

## Основные компоненты

  - Все жалобы сохраняются в SQLite
  - Жалобы с категорией "Технические" отправляются в очередь Celery
  - Для технических жалоб автоматически генерируется и отправляется email уведомление

## Логирование

  - Все события приложения логируются в Kafka
  - Логи агрегируются в ELK (Elasticsearch + Logstash + Kibana)
  - Доступен полнотекстовый поиск и анализ логов


## Структура проекта:
```
.
├── alembic.ini
├── docker-compose
│   ├── app.yaml
│   ├── logging.yaml
│   ├── logstash
│   │   └── logstash.conf
│   ├── messaging.yaml
│   └── volumes.yaml
├── Dockerfile
├── Makefile
├── poetry.lock
├── pyproject.toml
├── README.md
├── src
│   ├── alembic
│   │   ├── env.py
│   │   ├── __pycache__
│   │   ├── README
│   │   ├── script.py.mako
│   │   └── versions
│   ├── alembic.ini
│   ├── application
│   │   ├── builders
│   │   ├── dto
│   │   ├── enrichers
│   │   ├── exceptions
│   │   ├── __init__.py
│   │   ├── interfaces
│   │   ├── schemas
│   │   ├── service
│   │   └── validators
│   ├── data
│   │   └── test.db
│   ├── exceptions
│   │   ├── exception_handlers.py
│   │   └── __init__.py
│   ├── infra
│   │   ├── celery
│   │   ├── db
│   │   ├── exceptions
│   │   ├── http_clients
│   │   ├── __init__.py
│   │   ├── mail
│   │   ├── mappers
│   │   ├── models
│   │   └── repositories
│   ├── logger
│   │   ├── __init__.py
│   │   ├── kafka_handler.py
│   │   └── logger.py
│   ├── logs
│   │   └── app.log
│   ├── main.py
│   ├── presentation
│   │   ├── api
│   │   └── __init__.py
│   ├── settings
│   │   ├── config.py
│   │   └── __init__.py
│   └── utils
│       ├── case_converter.py
│       └── __init__.py
```

## Установка и запуск

### Требования

  - Docker и Docker Compose
  - Python 3.12
  - Poetry

### Установка

```bash
git clone <repo-url>
cd <repo-folder>
poetry install
```

### Запуск

```bash
make up  # Запускает все сервисы через docker-compose
```

##### После запуска будут доступны:

  - FastAPI приложение: http://localhost:8000
  - Kibana (для просмотра логов): http://localhost:5601
  - RabbitMQ management: http://localhost:15672

## API Endpoints

### Добавить жалобу

##### Запрос:

```json
{
  "text": "SMS code is not received"
}
```

##### Ответ:

```json
{
  "id": "62ad65d7-4721-4ccf-ab5a-911249db870a",
  "text": "SMS code is not received",
  "status": "Open",
  "sentiment": "Neutral",
  "category": "Technical",
  "ip": "172.20.0.1",
  "country": "Russia",
  "region": "Krasnodar Krai",
  "city": "Krasnodar",
  "created_at": "2025-07-13T16:05:26"
}
```

### Пояснения к полям ответа:

  - id — UUID жалобы, уникальный идентификатор
  - text — оригинальный текст жалобы
  - status — статус обработки (Open/Closed)
  - sentiment — тональность текста (Positive/Negative/Neutral/Unknown)
  - category — категория жалобы (Technical/Payment/Other)
  - ip — IP-адрес клиента
  - country/region/city — геолокационные данные
  - created_at — дата и время создания

## Мониторинг и логирование

Все логи приложения отправляются в Kafka и агрегируются в ELK. Для просмотра логов:

  1. Откройте Kibana: http://localhost:5601
  2. Создайте index pattern fastapi-logs*
  3. Используйте Discover для поиска и анализа логов

## Дополнительные команды

```bash
make logs      # Просмотр логов приложения
make down      # Остановка всех сервисов
```
