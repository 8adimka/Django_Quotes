# Django Quotes

## Содержание

1. [Описание проекта](#описание-проекта)
2. [Используемые технологии](#используемые-технологии)
3. [Структура проекта](#структура-проекта)
4. [Работа с проектом](#работа-с-проектом)
   - 4.1 [Настройка Docker и окружения](#настройка-docker-и-окружения)
   - 4.2 [Переменные окружения](#переменные-окружения)
   - 4.3 [Управление миграциями](#управление-миграциями)
   - 4.4 [Запуск проекта](#запуск-проекта)
5. [Этапы запуска](#этапы-запуска)
6. [Полезные материалы](#полезные-материалы)

## Описание проекта

Django Quotes — это веб-приложение для управления цитатами с системой оценок и взвешенным случайным выбором.

Пользователи могут добавлять, оценивать цитаты лайками и дизлайками. Система автоматически учитывает вес оценок при подсчёте и выборе случайных цитат. Популярные цитаты появляются чаще.

Проект включает:

- Добавление цитат с указанием источника (фильм, книга, другое)
- Систему оценок с лайками и дизлайками
- Топ популярных цитат
- Дашборд с аналитикой и графиками
- Ограничения: не более 3 цитат на источник
- Защиту от дубликатов (регистронезависимая проверка)

## Используемые технологии

- **Python 3.13**
- **Django 5.2.6** — веб-фреймворк для создания приложения
- **PostgreSQL 16** — реляционная база данных
- **Docker & Docker Compose** — контейнеризация приложения и базы данных
- **psycopg2-binary** — PostgreSQL адаптер для Python
- **Bootstrap 5** — UI фреймворк
- **Chart.js** — графики и диаграммы

## Структура проекта

```
task_django_quotes/
├── scripts/
│   └── entrypoint.sh      # Скрипт запуска и миграций
├── quotes/                # Основное приложение Django
│   ├── models.py          # Модели данных
│   ├── views.py           # Представления
│   ├── forms.py           # Формы
│   ├── services.py        # Бизнес-логика
│   ├── urls.py            # URL маршруты
│   ├── static/            # Статические файлы
│   ├── templates/         # HTML шаблоны
│   └── migrations/        # Миграции базы данных
└── config/                # Настройки проекта
    ├── settings.py        # Основные настройки
    ├── urls.py            # Глобальные URL маршруты
    └── wsgi.py            # WSGI конфигурация
├── manage.py              # Входная точка Django
├── requirements.txt       # Список зависимостей
├── docker-compose.yml     # Конфигурация Docker
├── Dockerfile             # Сборка образа
└── .env.example           # Пример переменных окружения
```

**Описание директорий:**

- `scripts/` — скрипт entrypoint, который ждёт готовность базы и выполняет миграции
- `quotes/` — приложение для работы с цитатами (модели, представления, формы)
- `config/` — глобальные настройки проекта, включая базу данных и секретные ключи

## Работа с проектом

### Настройка Docker и окружения

В проекте используется Docker и docker-compose, поэтому нет необходимости создавать виртуальное окружение вручную.
Достаточно выполнить:

```bash
docker-compose build
docker-compose up

или

docker-compose up --build
```

### Переменные окружения

Создайте файл `.env` в корне проекта со следующими переменными:

```env
DJANGO_DEBUG=False
DJANGO_SECRET_KEY=django-insecure-change-me-in-production
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000
DATABASE_URL=postgres://quotes:quotes@db:5432/quotes
TIME_ZONE=Europe/Madrid
WEIGHT_LIKE_STEP=0.2
WEIGHT_DISLIKE_STEP=0.1
MIN_EFFECTIVE_WEIGHT=0.05
```

`DATABASE_URL` указывает на контейнер PostgreSQL, создаваемый через Docker Compose.

## Этапы запуска

1. **Клонируем репозиторий:**

   ```bash
   git clone https://github.com/8adimka/Django_Quotes.git
   cd Django_Quotes
   ```

2. **Создаём `.env` файл с переменными окружения:**

   ```bash
   cp .env.example .env
   ```

3. **Собираем Docker-образы:**

   ```bash
   docker-compose build
   ```

4. **Запускаем проект:**

   ```bash
   docker-compose up
   ```

  Скрипт `entrypoint.sh` автоматически ждёт доступности базы, применяет миграции и запускает сервер.

После первого запуска миграции выполняются автоматически, сервер готов к работе.

**Приложение будет доступно по адресу:** <http://localhost:8000>

### Управление миграциями (если потребуется)

Миграции выполняются автоматически при запуске через `entrypoint.sh`.

Чтобы создать новую миграцию вручную:

```bash
docker-compose exec web python manage.py makemigrations
```

Чтобы применить миграции к базе данных:

```bash
docker-compose exec web python manage.py migrate
```

## Production развертывание

### Для production использования рекомендую

1. **Измените переменные окружения:**

   ```bash
   DJANGO_DEBUG=False
   DJANGO_SECRET_KEY=your-strong-secret-key-here
   DJANGO_ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
   CSRF_TRUSTED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
   ```

2. **Используйте внешний веб-сервер (nginx, Apache)**
3. **Настройте SSL сертификаты**
4. **Регулярно делайте бэкапы базы данных**
5. **И переделайте нормально, а не на скорую руку**

## 🛠 Разработка

### Локальная разработка без Docker

```bash
# Создать виртуальное окружение
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows

# Установить зависимости
pip install -r requirements.txt

# Настроить переменные окружения для SQLite
export DATABASE_URL=sqlite:///db.sqlite3

# Выполнить миграции
python manage.py migrate

# Запустить сервер разработки
python manage.py runserver
```

## 📄 Лицензия

License - используйте свободно для личных проектов =]

## 🤝 Автор

Vadim Medintsev - [m8adimka@gmail.com](mailto:m8adimka@gmail.com)

## Полезные материалы

- [Документация Django](https://docs.djangoproject.com/)
- [Docker Docs](https://docs.docker.com/)
- [PostgreSQL Docs](https://www.postgresql.org/docs/)
- [psycopg2 Docs](https://www.psycopg.org/docs/)

---

*Создано с помощью Django и большой любовью к хорошим цитатам! 💬*
