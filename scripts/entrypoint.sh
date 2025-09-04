#!/bin/bash
set -e

# Ждем доступность Postgres
echo "Waiting for database..."
python - <<'PY'
import os, time, psycopg2
from urllib.parse import urlparse

url = os.environ.get("DATABASE_URL")
if not url:
    raise SystemExit("DATABASE_URL not set")

u = urlparse(url)
for _ in range(30):
    try:
        psycopg2.connect(
            dbname=u.path.lstrip('/'),
            user=u.username,
            password=u.password,
            host=u.hostname,
            port=u.port or 5432,
        ).close()
        break
    except Exception:
        time.sleep(1)
else:
    raise SystemExit("Postgres not available")
PY

echo "Applying migrations..."
python manage.py migrate --noinput

exec "$@"
