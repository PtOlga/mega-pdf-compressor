FROM python:3.11-slim

WORKDIR /app

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Копируем requirements.txt из backend
COPY backend/requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копируем app.py из backend
COPY backend/app.py .

# Копируем frontend
COPY frontend /app/frontend

EXPOSE 8000
CMD gunicorn --bind 0.0.0.0:${PORT:-8000} app:app

