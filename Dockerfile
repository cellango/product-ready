FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY core/ ./core/
COPY slack_bot/ ./slack_bot/

ENV PORT=3000
EXPOSE 3000

CMD ["python", "-m", "slack_bot.app"]
