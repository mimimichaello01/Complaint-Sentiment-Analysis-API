
# Complaint Sentiment Analysis API

API для приёма жалоб клиентов с анализом тональности текста и проверкой на нецензурную лексику с помощью внешних сервисов. Кроме того, реализована определение геолокации пользователя по IP-адресу. Приложение построено на FastAPI с использованием SQLite, Docker и Alembic.

## Описание

- Принимает POST-запросы с текстом жалобы (например, {"text": "SMS code is not received"}).

- Проверяет текст на нецензурную лексику с помощью Profanity Filter API.

- Получает IP клиента из запроса и определяет геолокацию через IP API.

- Отправляет текст жалобы на Sentiment Analysis API (APILayer).

- Сохраняет жалобу в SQLite с полями:

    - id — UUID жалобы.
    - text — текст жалобы.
    - status — статус (по умолчанию "Open").
    - timestamp — время создания.
    - sentiment — тональность (Positive, Negative, Neutral, Unknown).
    - category — категория жалобы (по умолчанию "Other").
    - ip, country, region, city — данные геолокации клиента.

- Обрабатывает ошибки:

    - Если внешний API Sentiment Analysis недоступен — сохраняет sentiment: "Unknown".
    - Если геолокация не найдена — сохраняет IP, остальные поля null.
    - При обнаружении мата в тексте — возвращает ошибку с 400.

## Структура проекта:
```
.
├── alembic.ini
├── docker-compose.yaml
├── Dockerfile
├── Makefile
├── poetry.lock
├── pyproject.toml
└── src
    ├── alembic              # миграции базы данных
    ├── application          # бизнес-логика, DTO, сервисы
    ├── data                 # файл базы данных SQLite
    ├── exceptions           # обработка ошибок
    ├── infra                # доступ к БД, HTTP клиенты, модели
    ├── logger               # логирование
    ├── logs                 # файлы логов
    ├── main.py              # точка входа FastAPI приложения
    ├── presentation         # API-роуты
    ├── settings             # конфигурации
    └── utils                # утилиты
```

## Установка:
```bash
git clone <repo-url>
cd <repo-folder>

poetry install
```

```bash
### Если база еще не создана, выполните миграции:

cd src
alembic revision --autogenerate -m "create table"
alembic upgrade head
```
## Запуск:
```bash
make up # запускает docker-compose с настройками приложения
```
## API

### Добавить жалобу

Тело запроса:
```json
{
  "text": "SMS code is not received"
}
```
Ответ:
```json
{
  "id": "62ad65d7-4721-4ccf-ab5a-911249db870a",
  "text": "IP check",
  "status": "Open",
  "sentiment": "Neutral",
  "category": "Other",
  "ip": "172.20.0.1",
  "country": "Russia",
  "region": "Krasnodar Krai",
  "city": "Krasnodar",
  "created_at": "2025-07-13T16:05:26"
}
```

## Пояснения к полям ответа:
- **id** — UUID жалобы, уникальный идентификатор.
- **text** — текст жалобы, как пришёл от клиента.
- **status** — статус жалобы (Open/Closed).
- **sentiment** — тональность текста (Positive/Negative/Neutral/Unknown).
- **category** — категория жалобы (Technical/Payment/Other).
- **ip** — IP-адрес клиента, полученный из запроса.
- **country, region, city** — геолокация по IP (через IP API).
- **created_at** — timestamp создания записи.
