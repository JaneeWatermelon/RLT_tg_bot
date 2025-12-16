# Telegram-бот для аналитики видео по запросам на естественном языке

## Описание

Telegram-бот принимает текстовые запросы на русском языке и возвращает **одно числовое значение**, рассчитанное на основе статистики видео и почасовых снапшотов.

## Запуск проекта (Docker):
Перед этим необходимо создать и добавить в корневую директорию файл dev.env (вид файла можно посмотреть ниже в следующем разделе)

```
docker-compose --env-file dev.env -f docker-compose.example.yml up -d --build
```

После успешного запуска контейнеров необходимо дождаться загрузки данных из JSON файла и запуска бота.
Статус можно посмотреть командой:
```
docker logs rlt-backend
```
Должен содержать "Data loaded successfully!" и "Starting bot..."

## Файл dev.env имеет вид:
```
DEBUG=True
BOT_API_KEY=bot_api_key
AI_PROVIDER=google
AI_API_KEY=ai_api_key

DB_HOST=db
DB_PORT=5432
DB_NAME=rlt_bot_db
DB_USER=postgres
DB_PASSWORD=db_password

ASSETS_ROOT=assets
SQL_ROOT=scripts/sql
```

---

## Стек технологий

- **Python 3.13**
- **PostgreSQL**
- **aiogram**
- **LLM**:
  - OpenAI (по умолчанию)
  - Ollama (локально, в режиме DEBUG)

---

## Архитектура
- core/
    - bot.py # Telegram-бот (aiogram)
    - database.py # Работа с PostgreSQL (psycopg2)
    - llm.py # Преобразование текста -> SQL
    - vars.py # Константы
- scripts/
    - load_json.py # Загрузка JSON-данных в БД
    - entrypoint.sh # Действия для запуска бота
    - sql/
        - videos.sql
        - video_snapshots.sql
- assets/
    - prompt_new.txt # Prompt с описанием схемы данных (там их несколько штук, итоговый prompt_new.txt)
- docker-compose.yml
- Dockerfile
- dev.env
- requirements.txt
- README.md

---

## Принцип обработки запросов

1. Пользователь отправляет текстовый запрос боту
2. LLM преобразует текст **только в SQL**
3. Произодится дополнительная обработка - удаление лишних сиволов
3. SQL выполняется в PostgreSQL
4. Бот возвращает **одно число**

---

## Prompt и работа с LLM

Описание системного промпта - схемы данных и правил генерации SQL хранится в файле:
- assets/prompt_new.txt

