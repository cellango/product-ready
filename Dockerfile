FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY core/ ./core/
COPY slack_bot/ ./slack_bot/

ENV PORT=3000
EXPOSE 3000

# Single worker — ThreadContext lives in-process.
# If you add Redis-backed context, you can raise --workers.
CMD ["gunicorn", \
     "--bind", "0.0.0.0:3000", \
     "--workers", "1", \
     "--threads", "4", \
     "--timeout", "60", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "slack_bot.wsgi:flask_app"]
