#!/usr/bin/env sh
set -e

echo "Starting FastAPI entrypoint..."

# Skip DB wait for Cloud Run (Cloud SQL proxy handles connection)
if [ "$K_SERVICE" ]; then
  echo "Running on Cloud Run, skipping DB wait..."
  alembic upgrade head
  exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT} --proxy-headers
fi

# Wait for Postgres
for i in $(seq 1 30); do
  if pg_isready -h "$POSTGRES_HOST" -p "${DB_PORT:-5432}" -U "${DB_USER}" -d "${DB_NAME}"; then
    echo "Postgres is ready!"
    break
  fi
  echo "Waiting for Postgres... ($i/30)"
  sleep 2
done

# Run migrations
alembic upgrade head || { echo "Migration failed!"; exit 1; }

# Start FastAPI
exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT} --proxy-headers

