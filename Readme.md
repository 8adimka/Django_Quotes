# Django Quotes

## Содержание

1. [Описание проекта](#описание-проекта)  
2. [Используемые технологии](#используемые-технологии)  
3. [Структура проекта](#структура-проекта)  
4. [Работа с проектом](#работа-с-проектом)  
   4.1 [Настройка Docker и окружения](#настройка-docker-и-окружения)  
   4.2 [Переменные окружения](#переменные-окружения)  
   4.3 [Управление миграциями](#управление-миграциями)  
   4.4 [Запуск проекта](#запуск-проекта)  
5. [Этапы запуска](#этапы-запуска)  
6. [Полезные материалы](#полезные-материалы)  

---

## Описание проекта

**Django Quotes** — это веб-приложение для управления цитатами.  
Пользователи могут добавлять, изменять и оценивать цитаты. Система позволяет вести рейтинг цитат и автоматически учитывать вес оценок при подсчёте.  

Проект разработан с акцентом на чистую архитектуру и удобство масштабирования.  

---

## Используемые технологии

- **Python 3.13**  
- **Django** — веб-фреймворк для создания приложения  
- **PostgreSQL** — реляционная база данных  
- **Docker & Docker Compose** — контейнеризация приложения и базы данных  
- **psycopg2** — PostgreSQL адаптер для Python  
- **Uvicorn/Gunicorn** — ASGI/WSGI сервер (по необходимости)  

---

## Структура проекта

```
/app
├─ manage.py              # Входная точка Django
├─ requirements.txt       # Список зависимостей
├─ docker-compose.yml     # Конфигурация Docker
├─ Dockerfile             # Сборка образа
├─ scripts/
│   └─ entrypoint.sh      # Скрипт запуска и миграций
├─ quotes/                # Основное приложение Django
│   ├─ models.py
│   ├─ views.py
│   ├─ serializers.py
│   ├─ urls.py
│   └─ ...
└─ config/                # Настройки проекта
    ├─ settings.py
    └─ ...
```

**Описание директорий:**

- `scripts/` — скрипт entrypoint, который ждёт готовность базы и выполняет миграции.  
- `quotes/` — приложение для работы с цитатами (модели, представления, API).  
- `config/` — глобальные настройки проекта, включая базу данных и секретные ключи.  

---

## Работа с проектом

### Настройка Docker и окружения

В проекте используется Docker и docker-compose, поэтому нет необходимости создавать виртуальное окружение вручную.  
Достаточно выполнить:

```bash
docker-compose build
docker-compose up
```

### Переменные окружения

Создайте файл `.env` в корне проекта со следующими переменными:

```env
DJANGO_DEBUG=True
DJANGO_SECRET_KEY=please-change-me
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.0
CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000
DATABASE_URL=postgres://quotes:quotes@db:5432/quotes
TIME_ZONE=Europe/Madrid
WEIGHT_LIKE_STEP=0.2
WEIGHT_DISLIKE_STEP=0.1
MIN_EFFECTIVE_WEIGHT=0.05
```

`DATABASE_URL` указывает на контейнер PostgreSQL, создаваемый через Docker Compose.

---

### Управление миграциями

Миграции выполняются автоматически при запуске через `entrypoint.sh`.

Чтобы создать новую миграцию вручную:

```bash
docker-compose run web python manage.py makemigrations
```

Чтобы применить миграции к базе данных:

```bash
docker-compose run web python manage.py migrate
```

---

### Запуск проекта

После сборки и запуска контейнеров:

```bash
docker-compose build
docker-compose up
```

Скрипт `entrypoint.sh` автоматически ждёт доступности базы, применяет миграции и запускает сервер.  
Приложение будет доступно по адресу: [http://localhost:8000](http://localhost:8000)

---

## Этапы запуска

1. Клонируем репозиторий:  

```bash
git clone https://github.com/8adimka/Django_Quotes.git
cd Django_Quotes
```

2. Создаём `.env` файл с переменными окружения.  
3. Собираем Docker-образы:  

```bash
docker-compose build
```

4. Запускаем проект:  

```bash
docker-compose up
```

После первого запуска миграции выполняются автоматически, сервер готов к работе.  

---

## Полезные материалы

- [Документация Django](https://docs.djangoproject.com/)  
- [Docker Docs](https://docs.docker.com/)  
- [PostgreSQL Docs](https://www.postgresql.org/docs/)  
- [psycopg2 Docs](https://www.psycopg.org/docs/)
