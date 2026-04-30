FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY core/ ./core/
COPY slack_bot/ ./slack_bot/

# Context DB lives here when CONTEXT_DB_PATH=/data/context.db is set.
# Mount a named volume at /data in production to persist across restarts.
RUN mkdir -p /data && \
    groupadd -r appuser && \
    useradd -r -g appuser -d /app -s /sbin/nologin appuser && \
    chown -R appuser:appuser /app /data

USER appuser

ENV PORT=3000
EXPOSE 3000

# Single worker — ThreadContext is in-process (or SQLite via CONTEXT_DB_PATH).
# Raise --workers only after migrating to a shared-storage backend.
CMD ["gunicorn", \
     "--bind", "0.0.0.0:3000", \
     "--workers", "1", \
     "--threads", "4", \
     "--timeout", "60", \
     "--graceful-timeout", "30", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "slack_bot.wsgi:flask_app"]
