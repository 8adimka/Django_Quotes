# Django Quotes

Веб-приложение для управления цитатами с системой оценок и взвешенным случайным выбором.

## Функциональность

- **Добавление цитат** с указанием источника (фильм, книга, другое)
- **Система оценок** - лайки и дизлайки
- **Взвешенный случайный выбор** - популярные цитаты появляются чаще
- **Топ цитат** - список самых популярных
- **Дашборд с аналитикой** - статистика по источникам и графики
- **Ограничения** - не более 3 цитат на источник
- **Защита от дубликатов** - регистронезависимая проверка

## 🛠 Технологии

- **Django 5.2.6** - веб-фреймворк
- **PostgreSQL 16** - база данных  
- **Docker & Docker Compose** - контейнеризация
- **Bootstrap 5** - UI фреймворк
- **Chart.js** - графики и диаграммы

## 📦 Быстрый запуск

### Предварительные требования

- Docker
- Docker Compose

### Запуск

```bash
# Клонировать репозиторий
git clone <repository-url>
cd task_django_quotes

# Скопировать переменные окружения
cp .env.example .env

# Запустить приложение
docker-compose up --build
```

Приложение будет доступно по адресу: **<http://localhost:8000>**

## 📁 Структура проекта

```
task_django_quotes/
├── config/                # Django настройки
│   ├── settings.py       # Основные настройки
│   ├── urls.py           # URL маршруты
│   └── wsgi.py           # WSGI конфигурация
├── quotes/               # Основное приложение
│   ├── models.py         # Модели данных
│   ├── views.py          # Представления
│   ├── forms.py          # Формы
│   ├── services.py       # Бизнес-логика
│   ├── urls.py           # URL маршруты приложения
│   ├── static/           # Статические файлы
│   ├── templates/        # HTML шаблоны
│   └── migrations/       # Миграции базы данных
├── scripts/
│   └── entrypoint.sh     # Скрипт запуска контейнера
├── docker-compose.yml    # Docker Compose конфигурация
├── Dockerfile            # Docker образ
├── requirements.txt      # Python зависимости
└── .env.example          # Пример переменных окружения
```

## Основные страницы

- **/** - Главная страница со случайной цитатой
- **/add/** - Добавление новой цитаты
- **/top/** - Топ популярных цитат
- **/dashboard/** - Аналитика и графики
- **/admin/** - Панель администратора Django

## ⚙️ Переменные окружения

| Переменная | Описание | По умолчанию |
|-----------|----------|--------------|
| `DJANGO_DEBUG` | Режим отладки | `False` |
| `DJANGO_SECRET_KEY` | Секретный ключ Django | `django-insecure-change-me-in-production` |
| `DJANGO_ALLOWED_HOSTS` | Разрешенные хосты | `localhost,127.0.0.1,0.0.0.0` |
| `DATABASE_URL` | URL подключения к PostgreSQL | `postgres://quotes:quotes@db:5432/quotes` |
| `TIME_ZONE` | Часовой пояс | `Europe/Madrid` |
| `WEIGHT_LIKE_STEP` | Увеличение веса за лайк | `0.2` |
| `WEIGHT_DISLIKE_STEP` | Уменьшение веса за дизлайк | `0.1` |
| `MIN_EFFECTIVE_WEIGHT` | Минимальный вес цитаты | `0.05` |

## 🔧 Команды управления

### Основные команды

```bash
# Запуск
docker-compose up

# Запуск в фоне
docker-compose up -d

# Пересборка и запуск
docker-compose up --build

# Остановка
docker-compose down

# Просмотр логов
docker-compose logs -f
```

### Управление данными

```bash
# Выполнение миграций
docker-compose exec web python manage.py migrate

# Создание суперпользователя
docker-compose exec web python manage.py createsuperuser

# Сбор статических файлов
docker-compose exec web python manage.py collectstatic

# Загрузка тестовых данных (если есть fixtures)
docker-compose exec web python manage.py loaddata fixtures/quotes.json
```

### Работа с базой данных

```bash
# Подключение к PostgreSQL
docker-compose exec db psql -U quotes -d quotes

# Бэкап базы данных
docker-compose exec db pg_dump -U quotes quotes > backup.sql

# Восстановление из бэкапа
docker-compose exec -T db psql -U quotes quotes < backup.sql

# Полная очистка данных (включая volumes)
docker-compose down -v
```

## 📊 Система весов

Приложение использует взвешенную систему для случайного выбора цитат:

- **Базовый вес**: 1.0 для каждой цитаты
- **Лайк**: +0.2 к весу (настраивается)
- **Дизлайк**: -0.1 к весу (настраивается)
- **Минимальный вес**: 0.05 (цитата всегда имеет шанс появиться)

Формула: `Эффективный вес = max(Базовый вес + Лайки × 0.2 - Дизлайки × 0.1, 0.05)`

## Модели данных

### Source (Источник)

- `title` - название источника
- `type` - тип (фильм, книга, другое)
- `created_at` - дата создания

### Quote (Цитата)

- `source` - связь с источником
- `text` - текст цитаты
- `normalized_text` - нормализованный текст (для проверки дубликатов)
- `base_weight` - базовый вес (по умолчанию 1.0)
- `likes` - количество лайков
- `dislikes` - количество дизлайков
- `views` - количество просмотров
- `created_at` - дата создания

## 🔒 Ограничения и валидация

- **Максимум 3 цитаты на источник** - валидация на уровне модели
- **Уникальность цитат** - регистронезависимая проверка
- **Обязательные поля** - название источника и текст цитаты

## Использование

1. **Добавьте цитаты** через форму или админку Django
2. **Оценивайте цитаты** лайками и дизлайками
3. **Просматривайте случайные цитаты** на главной странице
4. **Изучайте статистику** на дашборде
5. **Смотрите топ цитат** по популярности

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

---

*Создано с помощью Django и большой любовью к хорошим цитатам! 💬*
