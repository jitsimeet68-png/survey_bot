FROM python:3.11-slim

WORKDIR /app

# системные зависимости для psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev curl && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# для flask autoreload полезно иметь watchdog
RUN pip install --no-cache-dir watchdog

COPY . /app

ENV FLASK_APP=app.py
EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000", "--reload"]