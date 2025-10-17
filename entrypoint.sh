#!/usr/bin/env sh
set -e

echo "Starting FastAPI entrypoint..."

# Check if running on Cloud Run
if [ "$K_SERVICE" ]; then
  echo "Running on Cloud Run..."
  
  # Run migrations (with timeout protection)
  echo "Running migrations..."
  timeout 60 alembic upgrade head || { 
    echo "Migration failed or timed out!"; 
    exit 1; 
  }
  
  echo "Starting uvicorn..."
  exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080} --proxy-headers
fi

# Local development path
if [ "$CLOUD_SQL_CONNECTION_NAME" ]; then
  POSTGRES_HOST="/cloudsql/$CLOUD_SQL_CONNECTION_NAME"
else
  POSTGRES_HOST="${DB_HOST:-db}"
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
exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080} --proxy-headers